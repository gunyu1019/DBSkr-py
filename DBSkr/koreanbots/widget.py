from ..assets import Assets


class Widget(Assets):
    def __init__(self, path: str, query: dict, session):
        self.path = path
        self.query = query

        self.BASE = "https://beta.koreanbots.dev/api"
        super().__init__(self, support_format=['svg'], session=session)
