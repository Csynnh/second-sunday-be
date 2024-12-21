from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.category import CategoryRequest, CategoryResponse
from fastapi import HTTPException
from datetime import datetime

def create_category(db: Session, category: CategoryRequest):
    try:
        query_str = text(
            """
            INSERT INTO dbo.category (name, description, created_at, updated_at)
            OUTPUT inserted.id, inserted.name, inserted.description, inserted.created_at, inserted.updated_at
            VALUES (:name, :description, :created_at, :updated_at);
            """
        )

        db_category = db.execute(
            query_str,
            {
                "name": category.name.upper(),
                "description": category.description,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        ).fetchone()
        db.commit()
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_category(db: Session, category_id: int):
    try:
        query_str = text(
            """
            SELECT id, name, description, created_at, updated_at
            FROM dbo.category
            WHERE id = :category_id;
            """
        )

        db_category = db.execute(query_str, {"category_id": category_id}).fetchone()
        return db_category

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    try:
        query_str = text(
            """
            SELECT id, name, description, created_at, updated_at
            FROM dbo.category
            ORDER BY id DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        db_categories = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()
        return db_categories
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_category(db: Session, category_id: int, category: CategoryRequest):
    try:
        query_str = text(
            """
            UPDATE dbo.category
            SET name = :name,
            description = :descripton,
            updated_at = :updated_at
            WHERE id = :category_id
            RETURNING id, name, description, created_at, updated_at;
            """
        )

        db_category = db.execute(
            query_str,
            {
                "category_id": category_id,
                "name": category.name.upper(),
                "description": category.description,
                "updated_at": datetime.now(),
            },
        ).fetchone()
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_category(db: Session, category_id: int):
    try:
        query_str = text(
            """
            DELETE FROM dbo.category
            WHERE id = :category_id
            RETURNING id, name, description, created_at, updated_at;
            """
        )

        db_category = db.execute(query_str, {"category_id": category_id}).fetchone()
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
