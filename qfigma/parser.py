from .types import QmlDocument


class FigmaParser:
    def __init__(self, figma: dict):
        self.figma = figma
        self.documents = dict()
        self.title = figma.get("name", "Unknown")
        self.icon_url = figma.get("thumbnailUrl")

    def parse(self):
        figma = self.figma
        canvases: list = figma.get("document", {}).get("children", [])
        for canvas in canvases:
            canvas: dict
            self.documents[canvas["name"]] = [
                QmlDocument(data) for data in canvas.get("children", [])
            ]
