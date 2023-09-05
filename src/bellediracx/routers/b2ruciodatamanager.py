from __future__ import annotations

from pydantic import BaseModel, root_validator
from datetime import datetime, timezone
from typing import Annotated, Any, TypedDict

from fastapi import (
    Body,
    Depends,
    Header,
    HTTPException,
    Response,
    status,
)

from diracx.core.config import Config, ConfigSource
from diracx.routers.auth import UserInfo, has_properties, verify_dirac_token

from diracx.routers.fastapi_classes import DiracxRouter
from bellediracx.db.rucio.db import RucioDB

LAST_MODIFIED_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

router = DiracxRouter()

class LFNParams(BaseModel):
    lfns: list[str]

    @root_validator
    def validate_fields(cls, v):
        # TODO
        return v

class StagingBaseLPN(TypedDict):
    BaseLPN: str
    Status: str
    ProductionID: int
    ProductionStatus: str
    Priority: int

EXAMPLE_STAGINGBASELPN = {
 "BaseLPN": "test1",
 "Status": "ToStage",
 "ProductionID": 1,
 "ProductionStatus": "",
 "Priority": 3,
}

EXAMPLE_BASELPN = "test"

@router.get("/{datablock}")
async def get_single_datablock(
    datablock: str,
    user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    rucio_db: Annotated[RucioDB, Depends(RucioDB.transaction)],
):
    return f"This datablock {datablock}"

@router.get("/staging/searchBaseLPNs/{base_lpn:path}")
async def get_staging_base_lpn(
    user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    rucio_db: Annotated[RucioDB, Depends(RucioDB.transaction)],
    #base_lpn: Annotated[str, Body(examples=EXAMPLE_BASELPN)],
    base_lpn: str,

):
    return await rucio_db.search(base_lpn)

@router.post("/staging/stagingBaseLPN")
async def stage_base_lpn(
    #user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    rucio_db: Annotated[RucioDB, Depends(RucioDB.transaction)],
    body: Annotated[StagingBaseLPN, Body(examples=EXAMPLE_STAGINGBASELPN)]
    #body: StagingBaseLPN
):
    return await rucio_db.insert(body["BaseLPN"],body["Status"],body["ProductionID"],body["ProductionStatus"],body["Priority"])