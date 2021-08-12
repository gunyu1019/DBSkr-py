import pytest
import os

import DBSkr


async def check_client(func, **kwargs):
    try:
        await func(**kwargs)
    except DBSkr.TooManyRequests:
        pass
    # except Exception as error:
    #     if len(error.args) != 0:
    #         return "{} {}".format(error.__class__.__name__, error.args)
    #     return "{}".format(error.__class__.__name__)
    # else:
    #     return


@pytest.mark.asyncio
async def test_client():
    exception = []
    client = DBSkr.HttpClient(
        koreanbots_token=os.environ.get('KOREAN_BOTS_TOKEN'),
        uniquebots_token=os.environ.get('UNIQUE_BOTS_TOKEN')
    )

    result = await check_client(client.bot, bot_id=680694763036737536)
    if result is not None:
        exception.append(result)
    result = await check_client(client.vote, bot_id=680694763036737536, user_id=340373909339635725)
    if result is not None:
        exception.append(result)
    result = await check_client(client.votes, bot_id=680694763036737536)
    if result is not None:
        exception.append(result)
    result = await check_client(client.users, user_id=340373909339635725)
    if result is not None:
        exception.append(result)

    assert len(exception) == 0
