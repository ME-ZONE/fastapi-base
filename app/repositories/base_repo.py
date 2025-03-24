from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import Select, and_, delete, exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, RelationshipProperty

from app.common.constants import AppStatus
from app.common.enums import ClassEnum
from app.core import AppException
from app.utils import logger_class_methods

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


@logger_class_methods(class_name=ClassEnum.REPOSITORY)
class BaseRepository(Generic[ModelType]):
    ## Variable ##
    _model: type[ModelType]

    ## Init ##
    def __init__(self, model: type[ModelType]) -> None:
        self._model = model

    ## External Function ##
    async def count_all(self, session: AsyncSession, *args, **kwargs) -> int:
        query = select(func.count()).select_from(self._model)

        if "filter_rpn" in kwargs:
            if kwargs["filter_rpn"]:
                condition = self._convert_filter_rpn_into_condition(kwargs["filter_rpn"])
                query = query.filter(condition)
            del kwargs["filter_rpn"]

        query = query.filter(*args).filter_by(**kwargs)
        result = await session.execute(query)
        return result.scalar_one()

    @staticmethod
    async def exists(session: AsyncSession, *args, **kwargs) -> bool:
        query = select(exists().where(*args).filter_by(**kwargs))
        result = await session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        session: AsyncSession,
        *args,
        include: list[InstrumentedAttribute] | None = None,
        exclude: list[InstrumentedAttribute] | None = None,
        **kwargs,
    ) -> list[ModelType]:
        query = await self._build_query(*args, include=include, exclude=exclude, **kwargs)
        result = await session.execute(query)

        if include or exclude:
            return [self._model(**dict(row._mapping)) for row in result.all()]
        else:
            return list(result.scalars().all())

    async def get_multi(
        self,
        session: AsyncSession,
        *args,
        include: list[InstrumentedAttribute] | None = None,
        exclude: list[InstrumentedAttribute] | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs,
    ) -> list[ModelType]:
        query = await self._build_query(*args, include=include, exclude=exclude, **kwargs)
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)

        if include or exclude:
            return [self._model(**dict(row._mapping)) for row in result.all()]
        else:
            return list(result.scalars().all())

    async def get(
        self,
        session: AsyncSession,
        *args,
        include: list[InstrumentedAttribute] | None = None,
        exclude: list[InstrumentedAttribute] | None = None,
        **kwargs,
    ) -> ModelType | None:
        """Lấy một bản ghi, trả về None nếu không tìm thấy."""
        return await self._get_query_result(session, *args, include=include, exclude=exclude, **kwargs)

    async def get_or_404(
        self,
        session: AsyncSession,
        *args,
        include: list[InstrumentedAttribute] | None = None,
        exclude: list[InstrumentedAttribute] | None = None,
        **kwargs,
    ) -> ModelType:
        obj = await self._get_query_result(session, *args, include=include, exclude=exclude, **kwargs)
        if not obj:
            raise AppException(app_status=AppStatus.BASE_REPO_404_MODEL_NOT_FOUND, model_name=self._model.__name__)
        return obj

    async def get_or_create(self, session: AsyncSession, *args, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        instance = await self.get(session, *args, **kwargs)
        if instance:
            raise AppException(
                app_status=AppStatus.BASE_REPO_400_MODEL_ALREADY_EXISTS_BAD_REQUEST,
                model_name=self._model.__name__.capitalize(),
            )

        instance = await self.create(session, obj_in)
        return instance

    async def create_bulk(self, session: AsyncSession, objs_in: list[CreateSchemaType]) -> list[ModelType]:
        db_objs = [self._model(**obj_in.model_dump()) for obj_in in objs_in]
        session.add_all(db_objs)
        await session.flush()
        return db_objs

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self._model(**obj_in.model_dump())
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def create_or_update(
        self,
        session: AsyncSession,
        *args,
        obj_in: CreateSchemaType | UpdateSchemaType | dict[str, Any],
        db_obj: ModelType | None = None,
        **kwargs,
    ) -> ModelType:
        db_obj = db_obj or await self.get(session, *args, **kwargs)

        if db_obj is None:
            return await self.create(session, obj_in=obj_in)
        else:
            return await self.update(session, obj_in=obj_in, db_obj=db_obj)

    async def update_bulk(
        self,
        session: AsyncSession,
        *args,
        objs_in: list[UpdateSchemaType],
        db_objs: list[ModelType] | None = None,
        **kwargs,
    ) -> ModelType | None:
        db_objs = db_objs or await self.get_all(session, *args, **kwargs)
        if len(objs_in) != len(db_objs):
            raise AppException(app_status=AppStatus.BASE_REPO_400_OBJECT_COUNT_MISMATCH_BAD_REQUEST)

        for i, db_obj in enumerate(db_objs):
            obj_data = db_obj.to_dict()
            update_data = objs_in[i].model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

        session.add_all(db_objs)
        await session.flush()
        ids = [db_obj.id for db_obj in db_objs]
        db_objs = await self.get_all(session, self._model.id.in_(ids))
        return db_objs

    async def update(
        self,
        session: AsyncSession,
        *args,
        obj_in: UpdateSchemaType | dict[str, Any],
        db_obj: ModelType | None = None,
        **kwargs,
    ) -> ModelType | None:
        db_obj = db_obj or await self.get(session, *args, **kwargs)
        if db_obj is not None:
            obj_data = db_obj.to_dict()
            update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.flush()
            await session.refresh(db_obj)
        return db_obj

    async def delete_bulk(self, session: AsyncSession, *args, db_objs: list[ModelType] | None = None, **kwargs) -> None:
        db_objs = db_objs or await self.get_all(session, *args, **kwargs)
        if not db_objs:
            return

        stmt = delete(self._model).where(self._model.id.in_([obj.id for obj in db_objs]))
        await session.execute(stmt)
        await session.flush()

    async def delete(self, session: AsyncSession, *args, db_obj: ModelType | None = None, **kwargs) -> ModelType:
        db_obj = db_obj or await self.get(session, *args, **kwargs)
        if db_obj is None:
            return None

        await session.delete(db_obj)
        await session.flush()
        return db_obj

    ## Internal Function ##
    async def _get_query_result(
        self,
        session: AsyncSession,
        *args,
        include: list[InstrumentedAttribute] | None = None,
        exclude: list[InstrumentedAttribute] | None = None,
        **kwargs,
    ) -> ModelType | None:
        query = await self._build_query(*args, include=include, exclude=exclude, **kwargs)
        result = await session.execute(query)

        if include or exclude:
            row = result.first()
            return self._model(**dict(row._mapping)) if row else None
        else:
            return result.scalars().first()

    async def _build_query(
        self,
        *args,
        include: list[InstrumentedAttribute] | None = None,
        exclude: list[InstrumentedAttribute] | None = None,
        **kwargs,
    ) -> Select:
        if include:
            query = select(*include)
        elif exclude:
            all_columns = [getattr(self._model, col) for col in self._model.__table__.columns]
            filtered_columns = [col for col in all_columns if col not in exclude]
            query = select(*filtered_columns)
        else:
            query = select(self._model)

        if "filter_rpn" in kwargs:
            if kwargs["filter_rpn"]:
                condition = self._convert_filter_rpn_into_condition(kwargs["filter_rpn"])
                query = query.filter(condition)
            del kwargs["filter_rpn"]

        query = query.filter(*args).filter_by(**kwargs)
        return query

    def _build_condition(self, key: Any, value: Any) -> Any:
        try:
            if "__" in key:
                relationship_key, attribute_key = key.split("__", 1)
                relationship_attr = getattr(self._model, relationship_key)

                if not (
                    isinstance(relationship_attr, InstrumentedAttribute)
                    and isinstance(relationship_attr.property, RelationshipProperty)
                ):
                    raise AppException(
                        app_status=AppStatus.BASE_REPO_400_RELATIONSHIP_BAD_REQUEST, relationship_name=relationship_key
                    )

                related_model = relationship_attr.prop.mapper.class_
                if not hasattr(related_model, attribute_key):
                    raise AppException(app_status=AppStatus.BASE_REPO_404_Field_NOT_FOUND, field_name=attribute_key)

                condition: Any = getattr(related_model, attribute_key) == value
                return (
                    relationship_attr.any(condition)
                    if relationship_attr.property.uselist
                    else relationship_attr.has(condition)
                )

            if hasattr(self._model, key):
                return getattr(self._model, key) == value

            raise AppException(app_status=AppStatus.BASE_REPO_404_Field_NOT_FOUND, field_name=key)
        except AttributeError:
            raise AppException(app_status=AppStatus.BASE_REPO_404_Field_NOT_FOUND, field_name=key) from None

    def _convert_filter_rpn_into_condition(self, rpn_list: Any) -> Any:
        stack: list[Any] = []
        for item in rpn_list:
            if item == "|":  # OR Operator
                right = stack.pop()
                left = stack.pop()
                result = or_(left, right)
            elif item == "&":  # AND Operator
                right = stack.pop()
                left = stack.pop()
                result = and_(left, right)
            else:  # Operand
                condition = dict(item)
                key = list(condition.keys())[0]
                value = condition[key]
                result = self._build_condition(key, value)
            stack.append(result)

        return stack.pop()
