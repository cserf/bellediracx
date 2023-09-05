from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


from sqlalchemy import func, insert, select, update

from diracx.core.exceptions import InvalidQueryError
from diracx.core.utils import JobStatus

from diracx.db.utils import BaseDB
from .schema import Production


class ProductionDB(BaseDB):
    metadata = Production.metadata

    async def insert(
        self,
        ProductionName,
        ProductionGroup,
        Description,
        Release,
        DBGlobalTag,
        Campaign,
        BeamEnergy,
    ):
        attrs = {
            "ProductionName": ProductionName,
            "ProductionGroup": ProductionGroup,
            "Description": Description,
            "Release": Release,
            "DBGlobalTag": DBGlobalTag,
            "Campaign": Campaign,
            "BeamEnergy": BeamEnergy,
            "CreationDate": datetime.now(tz=timezone.utc),
        }
        stmt = insert(Production).values(attrs)
        result = await self.conn.execute(stmt)
        return result.lastrowid

    async def search(
        self,
        prod_name,
    ):
        stmt = select(ProductionName=prod_name)
        # Execute the query
        return [dict(row._mapping) async for row in (await self.conn.stream(stmt))]
