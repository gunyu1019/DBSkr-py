import pytest
# import DBSkr
import os


@pytest.mark.asyncio
async def test_client():
    print(os.getenv("KEY"))
    return os.getenv("KEY") is None
