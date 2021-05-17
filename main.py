from DBSkr import koreanbots

http = koreanbots.https.HttpClient()
widget = http.widget(widget_type=koreanbots.WidgetType.Server, bot_id=680694763036737536)

print(type(widget))
print(widget.url())
