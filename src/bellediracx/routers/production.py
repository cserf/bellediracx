from __future__ import annotations

from pydantic import BaseModel, root_validator
from datetime import datetime, timezone
from typing import Annotated

from fastapi import (
    Depends,
    Header,
    HTTPException,
    Response,
    status,
)

from diracx.core.config import Config, ConfigSource
from diracx.routers.auth import UserInfo, has_properties, verify_dirac_token

from diracx.routers.fastapi_classes import DiracxRouter
from bellediracx.db.production.db import ProductionDB

LAST_MODIFIED_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

router = DiracxRouter()


class Production(BaseModel):
    ProductionName: str
    ProductionGroup: str
    Description: str
    Release: str
    DBGlobalTag: str
    Campaign: str
    BeamEnergy: str


@router.post("/")
async def add_production(
    production: Production,
    #    user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    production_db: Annotated[ProductionDB, Depends(ProductionDB.transaction)],
):
    production_id = await production_db.insert(
        ProductionName=production.ProductionName,
        ProductionGroup=production.ProductionGroup,
        Description=production.Description,
        Release=production.Release,
        DBGlobalTag=production.DBGlobalTag,
        Campaign=production.Campaign,
        BeamEnergy=production.BeamEnergy,
    )
    return production_id


@router.get("/{prod_name}")
async def get_production(
    prod_name: str,
    #    user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    production_db: Annotated[ProductionDB, Depends(ProductionDB.transaction)],
):
    return production_db.search(prod_name)
