import pytest
# import DBSkr
import os


@pytest.mark.asyncio
async def test_client():
    raise TypeError(len(os.environ.get('KEY')))
