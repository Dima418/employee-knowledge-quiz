"""Base class for all CRUD operations.

"""

from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for all CRUD operations.

    Args:
        Generic (Base): The model class.
    """

    def __init__(self, model: ModelType):
        """Initialize the CRUDBase class with privided model class.

        Args:
            model (ModelType): The model class.
        """
        self.model = model

    async def get(self, db: Session, id: Any) -> ModelType | None:
        """Get a single object by id.

        Args:
            db (Session): The database session.
            id (Any): The id of the object.

        Returns:
            (ModelType, optional): The object or None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Get multiple objects.

        Args:
            db (Session): The database session.
            skip (int, optional): The number of objects to skip. Defaults to 0.
            limit (int, optional): The number of objects to limit. Defaults to 100.

        Returns:
            (list[ModelType]): The list of objects.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db: Session, *, new_obj: CreateSchemaType) -> ModelType:
        """Create a new object.

        Args:
            db (Session): The database session.
            new_obj (CreateSchemaType): The object to create.

        Returns:
            (ModelType): The created object.
        """
        new_obj_data = jsonable_encoder(new_obj)
        db_obj = self.model(**new_obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(self, db: Session, *, old_obj: ModelType, new_obj: UpdateSchemaType | dict[str, Any]) -> ModelType:
        """Update an object.

        Args:
            db (Session): The database session.
            old_obj (ModelType): The existing object in database.
            new_obj (ModelType | dict[str, Any]): The new object`s values.

        Returns:
            (ModelType): The updated object.
        """
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
        """Delete an object.

        Args:
            db (Session): The database session.
            id (int): The id of the object.

        Returns:
            (ModelType): The deleted object.
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
