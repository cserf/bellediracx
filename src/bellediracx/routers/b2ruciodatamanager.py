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

LAST_MODIFIED_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

router = DiracxRouter()

class LFNParams(BaseModel):
    lfns: list[str]

    @root_validator
    def validate_fields(cls, v):
        # TODO
        return v


@router.get("/{datablock}")
async def get_single_datablock(datablock: str):
    return f"This datablock {datablock}"

@router.post("/staging/status")
async def get_multiple_file_status(
    user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    body: LFNParams,
):
    lfns = body.lfns
    return f"This list of LFNs {lfns}"
