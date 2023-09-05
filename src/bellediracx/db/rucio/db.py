from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
#from uuid import uuid4


from sqlalchemy import func, insert, select, update

from diracx.core.exceptions import InvalidQueryError
from diracx.core.utils import JobStatus

from diracx.db.utils import BaseDB
from .schema import StagingBaseLPNs

class RucioDB(BaseDB):
    metadata = StagingBaseLPNs.metadata

    async def _insertLPN(self, lpnData: dict[str, Any]):
        print(lpnData)
        stmt = insert(StagingBaseLPNs).values(lpnData)
        return await self.conn.execute(stmt)

    async def insert(
        self,
        BaseLPN,
        Status,
        ProductionID,
        ProductionStatus,
        Priority,
    ):
        InitialUpdate = datetime.now(tz=timezone.utc)
        attrs = dict()
        #attrs['ID'] = uuid
        attrs["BaseLPN"] = BaseLPN
        attrs["Status"] = Status
        attrs["ProductionID"] = ProductionID
        attrs["ProductionStatus"] = ProductionStatus
        attrs["Priority"] = Priority
        attrs["InitialUpdate"] = InitialUpdate
        attrs["LastUpdate"] = InitialUpdate

        result = await self._insertLPN(attrs)

        return {
               "ID": result.lastrowid,
               "BaseLPN": BaseLPN,
               "Status": Status,
               "ProductionID": ProductionID,
               "ProductionStatus": ProductionStatus,
               "Priority": Priority,
               "InitialUpdate": InitialUpdate,
               "LastUpdate": InitialUpdate,
           }

    async def search(
        self,
        BaseLPN,
    ):
        # Find which columns to select
        columns = [x for x in StagingBaseLPNs.__table__.columns]
        stmt = select(*columns).where(StagingBaseLPNs.BaseLPN==BaseLPN)
        # Execute the query
        return [dict(row._mapping) async for row in (await self.conn.stream(stmt))]

