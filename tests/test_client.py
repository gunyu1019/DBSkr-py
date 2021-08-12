import pytest
# import DBSkr
import os


@pytest.mark.asyncio
async def test_client():
    return os.getenv("korean_bots_token") is None
