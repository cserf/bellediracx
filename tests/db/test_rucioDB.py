from __future__ import annotations

import random
import asyncio

import pytest

from bellediracx.db.rucio.db import RucioDB


def generate_random_path():
    prodid = random.random.randint(0, 100000)
    path = f"/belle/test/MC/{prodid}"
    return path



@pytest.fixture
async def rucio_db(tmp_path):
    rucio_db = RucioDB("sqlite+aiosqlite:///:memory:")
    async with rucio_db.engine_context():
        yield rucio_db


async def test_some_asyncio_code(rucio_db):
    async with rucio_db as rucio_db:

        result = await asyncio.gather(
            *(
                rucio_db.insert(
                    f"/belle/test/MC/{prodid}",
                    "ToStage",
                    prodid,
                    "ToStage",
                    3,
                )
                for prodid in range(100)
            )
        )

    #async with rucio_db as rucio_db:
    #    result = await rucio_db.search(["JobID"], [], [])
    #    assert result
