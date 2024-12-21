from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cruds import category as cruds
from app.database import get_db
from app.schemas import category as schemas

router = APIRouter()


@router.post("/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryRequest, db: Session = Depends(get_db)):
    try:
        db_category = cruds.create_category(db=db, category=category)
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        db_category = cruds.get_category(db=db, category_id=category_id)
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        db_categories = cruds.get_categories(db=db, skip=skip, limit=limit)
        return db_categories
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category: schemas.CategoryRequest, db: Session = Depends(get_db)):
    try:
        db_category = cruds.update_category(db=db, category_id=category_id, category=category)
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}", response_model=schemas.CategoryResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        db_category = cruds.delete_category(db=db, category_id=category_id)
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))