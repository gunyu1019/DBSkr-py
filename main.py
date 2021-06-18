from DBSkr import koreanbots, topgg, uniquebots
import asyncio

event = asyncio.get_event_loop()

http1 = koreanbots.HttpClient()
widget = http1.widget(widget_type=koreanbots.WidgetType.Server, bot_id=680694763036737536)

print(type(widget))
print(widget.url())

http2 = topgg.HttpClient()
widget = http2.widget(widget_type=topgg.WidgetType.normal, bot_id=680694763036737536)

print(type(widget))
print(widget.url())

http3 = uniquebots.HttpClient()
bot = event.run_until_complete(http3.bot(680694763036737536))

print(bot)
print(bot.owners)
print(bot.owners[0].bots)
print(bot.owners[0].bots[0].owners)
