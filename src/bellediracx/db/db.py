from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


from sqlalchemy import func, insert, select, update

from diracx.core.exceptions import InvalidQueryError
from diracx.core.utils import JobStatus

from diracx.db.utils import BaseDB
from .schema import StagingBaseLPNsPARAMS

class RucioDB(BaseDB):
    metadata = StagingBaseLPNsPARAMS.metadata

    async def _insertLPN(self, lpnData: dict[str, Any]):
        stmt = insert(StagingBaseLPNsPARAMS).values(lpnData)
        await self.conn.execute(stmt)

    async def insert(
        self,
        BaseLPN,
        STATUS,
        ProductionID,
        ProductionStatus,
        Priority,
    ):
         InitialUpdate = datetime.now(tz=timezone.utc)
         uuid = str(uuid4())
         attrs = dict()
         attrs['ID'] = uuid
         attrs["BaseLPN"] = BaseLPN
         attrs["STATUS"] = STATUS
         attrs["ProductionID"] = ProductionID
         attrs["ProductionStatus"] = ProductionStatus
         attrs["Priority"] = Priority
         attrs["InitialUpdate"] = InitialUpdate
         attrs["LastUpdate"] = InitialUpdate

         await self._insertLPN(attrs)

         return {
                "ID": uuid,
                "BaseLPN": BaseLPN,
                "STATUS": STATUS,
                "ProductionID": ProductionID,
                "ProductionStatus": ProductionStatus,
                "Priority": Priority,
                "InitialUpdate": InitialUpdate,
                "LastUpdate": InitialUpdate,
            }
