from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas import ProductRequest, ProductResponse
from fastapi import HTTPException


def get_product(db: Session, product_id: int):
    query_str = text(
        """
        SELECT p.*, pcs.id as product_id, pcs.inventory, s.name as size_name, s.id as size_id, c.name as color_name, c.id as color_id, pcs.images as images
    FROM dbo.PRODUCT AS p
    LEFT JOIN dbo.ProductColorSize AS pcs ON pcs.product_id = p.id
    LEFT JOIN [dbo].[Size] AS s ON s.id = pcs.size_id
    LEFT JOIN [dbo].[Color] AS c ON c.id = pcs.color_id
    WHERE p.id = :product_id
    ORDER BY p.id, pcs.color_id, pcs.size_id
    """
    )
    products = db.execute(query_str, {"product_id": product_id}).fetchall()

    if not products:
        return None

    result = {
        "id": products[0].id,
        "name": products[0].name,
        "description": products[0].description,
        "price": products[0].price,
        "colors": [],
    }
    for product in products:
        existing_color = next(
            (c for c in result["colors"] if c["id"] == product.color_id), None
        )
        if existing_color:
            existing_size = next(
                (s for s in existing_color["sizes"] if s["id"] == product.size_id), None
            )
            if existing_size:
                existing_size["inventory"] += product.inventory
            else:
                existing_color["sizes"].append(
                    {
                        "id": product.size_id,
                        "name": product.size_name,
                        "inventory": product.inventory,
                    }
                )
        else:
            result["colors"].append(
                {
                    "id": product.color_id,
                    "name": product.color_name,
                    "images": (
                        [product.images]
                        if isinstance(product.images, str)
                        else product.images
                    ),
                    "sizes": [
                        {
                            "id": product.size_id,
                            "name": product.size_name,
                            "inventory": product.inventory,
                        }
                    ],
                }
            )

    return result


def get_products(db: Session, skip: int = 0, limit: int = 10):
    query_str = text(
        """
        SELECT p.*, pcs.id as product_id, pcs.inventory, s.name as size_name, s.id as size_id, c.name as color_name, c.id as color_id, pcs.images as images
    FROM dbo.PRODUCT AS p
    LEFT JOIN dbo.ProductColorSize AS pcs ON pcs.product_id = p.id
    LEFT JOIN [dbo].[Size] AS s ON s.id = pcs.size_id
    LEFT JOIN [dbo].[Color] AS c ON c.id = pcs.color_id
    ORDER BY p.id, pcs.color_id, pcs.size_id
    OFFSET :skip ROWS
    FETCH NEXT :limit ROWS ONLY;
    """
    )
    products = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()

    # Transform the data into a format that matches your ProductOut model
    result = []
    for product in products:
        existing_product = next((p for p in result if p["id"] == product.id), None)
        if existing_product:
            existing_color = next(
                (c for c in existing_product["colors"] if c["id"] == product.color_id),
                None,
            )
            if existing_color:
                existing_size = next(
                    (s for s in existing_color["sizes"] if s["id"] == product.size_id),
                    None,
                )
                if existing_size:
                    existing_size["inventory"] += product.inventory
                else:
                    existing_color["sizes"].append(
                        {
                            "id": product.size_id,
                            "name": product.size_name,
                            "inventory": product.inventory,
                        }
                    )
            else:
                existing_product["colors"].append(
                    {
                        "id": product.color_id,
                        "name": product.color_name,
                        "images": (
                            [product.images]
                            if isinstance(product.images, str)
                            else product.images
                        ),
                        "sizes": [
                            {
                                "id": product.size_id,
                                "name": product.size_name,
                                "inventory": product.inventory,
                            }
                        ],
                    }
                )
        else:
            product_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "colors": [
                    {
                        "id": product.color_id,
                        "name": product.color_name,
                        "images": (
                            [product.images]
                            if isinstance(product.images, str)
                            else product.images
                        ),
                        "sizes": [
                            {
                                "id": product.size_id,
                                "name": product.size_name,
                                "inventory": product.inventory,
                            }
                        ],
                    }
                ],
            }
            result.append(product_data)

    return result


def create_product(db: Session, product: ProductRequest):
    # Step 1: Check if the product already exists by name using a raw query
    query_str = text(
        """
    SELECT id FROM dbo.PRODUCT WHERE name = :name
    """
    )
    result = db.execute(query_str, {"name": product.name})
    db_product = result.fetchone()

    if db_product:
        db_product_id = db_product[0]  # Access the result as a tuple, with 0 for 'id'
    else:
        query_str = text(
            """
        INSERT INTO dbo.PRODUCT (name, price, description)
        OUTPUT inserted.id
        VALUES (:name, :price, :description)
        """
        )
        result = db.execute(
            query_str,
            {
                "name": product.name,
                "price": product.price,
                "description": product.description,
            },
        )
        db_product_id = result.fetchone()[0]

    # Step 2: Insert colors if not already present
    color_ids = []
    for color in product.colors:
        query_str = text(
            """
        SELECT id, name FROM dbo.COLOR WHERE name = :color
        """
        )
        result = db.execute(query_str, {"color": color.name})
        db_color = result.fetchone()

        if not db_color:
            query_str = text(
                """
            INSERT INTO dbo.COLOR (name)
            OUTPUT inserted.id, inserted.name
            SELECT :color
            """
            )
            result = db.execute(query_str, {"color": color.name})
            db_color_id = result.fetchone()
        else:
            db_color_id = db_color

        images_str = (
            ",".join(color.images)
            if isinstance(color.images, list)
            else color.images
        )
        color_ids.append({
            "id": db_color_id.id,
            "name": db_color_id.name,
            "images": images_str.split(","),
            "sizes": [],
        })
        # Step 3: Insert sizes if not already present
        for size in color.sizes:
            query_str = text(
                """
            SELECT id, name FROM dbo.SIZE WHERE name = :size
            """
            )
            result = db.execute(query_str, {"size": size.name})
            db_size = result.fetchone()

            if not db_size:
                query_str = text(
                    """
                INSERT INTO dbo.SIZE (name)
                OUTPUT inserted.id, inserted.name
                SELECT :size
                """
                )
                result = db.execute(query_str, {"size": size.name})
                db_size_id = result.fetchone()
            else:
                db_size_id = db_size
            query_str = text(
                """
                SELECT id FROM dbo.PRODUCTCOLORSIZE WHERE product_id = :product_id AND color_id = :color_id AND size_id = :size_id
                """
            )
            result = db.execute(
                query_str,
                {
                    "product_id": db_product_id,
                    "color_id": db_color_id.id,
                    "size_id": db_size_id.id,
                },
            )
            db_product_color_size = result.fetchone()
            if db_product_color_size:
                raise HTTPException(
                    status_code=400, detail="Product already exists with the same color and size"
                )

            query_str = text(
                """
            INSERT INTO dbo.PRODUCTCOLORSIZE (product_id, color_id, size_id, inventory, images)
            VALUES (:product_id, :color_id, :size_id, :inventory, :images)
            """
            )
            db.execute(
                query_str,
                {
                    "product_id": db_product_id,
                    "color_id": db_color_id.id,
                    "size_id": db_size_id.id,
                    "inventory": size.inventory,
                    "images": images_str
                },
            )
            color_ids[-1]["sizes"].append({
                "id": db_size_id.id,
                "name": db_size_id.name,
                "inventory": size.inventory,
            })
    db.commit()

    # Return the product along with the necessary fields
    return ProductResponse(
        colors=color_ids,
        description=product.description,
        id=db_product_id,
        name=product.name,
        price=product.price,
    )

def update_product(db: Session, product_id: int, product: ProductRequest):
    # Step 1: Check if the product exists by id
    query_str = text(
        """
    SELECT id FROM dbo.PRODUCT WHERE id = :product_id
    """
    )
    result = db.execute(query_str, {"product_id": product_id})
    db_product = result.fetchone()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Step 2: Update the product details
    query_str = text(
        """
    UPDATE dbo.PRODUCT
    SET name = :name, price = :price, description = :description
    WHERE id = :product_id
    """
    )
    db.execute(
        query_str,
        {
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "product_id": product_id,
        },
    )

    # Step 3: Update the color and size details
    for color in product.colors:
        for size in color.sizes:
            query_str = text(
                """
            UPDATE dbo.PRODUCTCOLORSIZE
            SET inventory = :inventory
            WHERE product_id = :product_id AND color_id = :color_id AND size_id = :size_id
            """
            )
            db.execute(
                query_str,
                {
                    "inventory": size.inventory,
                    "product_id": product_id,
                    "color_id": color.id,
                    "size_id": size.id,
                },
            )
    db.commit()

    return ProductResponse(
        colors=product.colors,
        description=product.description,
        id=product_id,
        name=product.name,
        price=product.price,
    )

def delete_product(db: Session, product_id: int):
    # Step 1: Check if the product exists by id
    query_str = text(
        """
    SELECT id FROM dbo.PRODUCT WHERE id = :product_id
    """
    )
    result = db.execute(query_str, {"product_id": product_id})
    db_product = result.fetchone()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Step 2: Delete the product
    query_str = text(
        """
    DELETE FROM dbo.PRODUCT WHERE id = :product_id
    """
    )
    db.execute(query_str, {"product_id": product_id})
    db.commit()

    return {"message": "Product deleted successfully"}