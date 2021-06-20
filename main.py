from DBSkr import koreanbots, topgg, uniquebots
import asyncio
import logging

event = asyncio.get_event_loop()

stream = logging.StreamHandler()
stream.setFormatter(logging.Formatter('[%(asctime)s | %(name)s | %(levelname)s]: %(message)s', "%Y-%m-%d %p %I:%M:%S"))

log = logging.getLogger()
log.addHandler(stream)


async def main():
    http1 = koreanbots.HttpClient(loop=event)
    #widget = http1.widget(widget_type=koreanbots.WidgetType.Server, bot_id=680694763036737536)

    #print(type(widget))
    #print(widget.url())

    #http2 = topgg.HttpClient(loop=event)
    #widget = http2.widget(widget_type=topgg.WidgetType.normal, bot_id=680694763036737536)

    #print(type(widget))
    #print(widget.url())

    #http3 = uniquebots.HttpClient(loop=event)
    #bot = await http3.bot(680694763036737536)

    #print(bot)
    #print(bot.owners)
    #print(bot.owners[0].bots)
    #print(bot.owners[0].bots[0].owners)

    bot = await http1.bot(680694763036737536)
    print(bot)
    print(bot.owners)
    print(bot.owners[0].bots)

    http1.requests.session.close()
    #await http2.requests.close()
    #await http3.requests.close()

event.run_until_complete(main())
