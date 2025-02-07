from fastapi import APIRouter, status, Response
from repository.attribute_repository import AttributeRepository
from product_catalouge.service.attributes_service import AttributeService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.attribute import (
    AttributeSchema, AttributeUpdateSchema)


router = APIRouter()


@router.get("/attributes/", tags=["attributes"], response_model=list[AttributeSchema])
async def get_all():
    attribute_service = AttributeService(AttributeRepository)
    attributes = await attribute_service.get_all()
    print(f"[ATTRIBUTEs]: {attributes}")
    return [attr.dict() for attr in attributes]


@router.get("/attributes/{id}", tags=["attributes"], response_model=AttributeSchema)
async def get_one(id:str):
    attribute_service = AttributeService(AttributeRepository)
    attribute = await attribute_service.get_one(id)
    print(f"[ATTRIBUTE]: {attribute.dict()}")
    return attribute.dict()


@router.post("/attributes/", tags=["attributes"], response_model=AttributeSchema)
async def create_attribute(payload:AttributeSchema):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        attribute, record = await uow.service.create(payload)
        uow.track(record)
        await uow.commit()
        return attribute.dict()


@router.patch("/attributes/{id}", tags=["attributes"], response_model=AttributeSchema)
async def update_attribute(id:str, payload:AttributeUpdateSchema):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        updated_attribute, updated_record = await uow.service.update_one(id, payload)
        print(f"[UPATED Attribute]: {updated_attribute}")
        uow.track(updated_record)
        await uow.commit()
        return updated_attribute.dict()


@router.delete("/attributes/{id}", tags=["attributes"], 
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(id:str):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        attribute = await uow.service.delete_one(id)
        print(f"[DELETED][DOCUMENT]: {attribute}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
