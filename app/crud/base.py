from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    async def get(self, db: Session, id: Any) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db: Session, *, new_obj: CreateSchemaType) -> ModelType:
        new_obj_data = jsonable_encoder(new_obj)
        db_obj = self.model(**new_obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(self, db: Session, *, old_obj: ModelType, new_obj: UpdateSchemaType | dict[str, Any]) -> ModelType:
        old_obj_data = jsonable_encoder(old_obj)
        if isinstance(new_obj, dict):
            update_data = new_obj
        else:
            update_data = new_obj.dict(exclude_unset=True)
        for field in old_obj_data:
            if field in update_data:
                setattr(old_obj, field, update_data[field])
        db.add(old_obj)
        db.commit()
        db.refresh(old_obj)
        return old_obj

    async def delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj