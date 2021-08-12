import pytest
# import DBSkr
import os


@pytest.mark.asyncio
async def test_client():
    raise TypeError(os.environ.get('KEY'))
