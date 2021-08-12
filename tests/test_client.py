import pytest
# import DBSkr
import os


@pytest.mark.asyncio
async def test_client():
    print(os.environ.get('KEY'))
    return os.environ.get('KEY') is None
