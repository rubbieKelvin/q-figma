class Item(object):
	"""docstring for Item."""
	def __init__(self, data, parent=None, doc=None):
		super(Item, self).__init__()
		self.data = data
		self.type = data["type"]
		self.config = data[".qfigma"]
		self.doc = doc
		self.parent = parent
		self.properties = dict(
			id = data.get("id"),
			x = self.coords[0],
			y = self.coords[1]
		)
		self.children = []
		self.read_children()

	@property
	def coords(self):
		""" returns tuple (x, y)"""
		if self.parent is None:
			return 0, 0
		else:
			box = self.data.get("absoluteBoundingBox")
			if box:
				return box["x"]-self.parent.coords[0], box["y"]-self.parent.coords[1]
			else:
				return 0, 0

	@property
	def size(self):
		""" returns tuple (width, height)"""
		if self.parent is None:
			return 0, 0
		else:
			box = self.data.get("absoluteBoundingBox")
			if box:
				return box["width"], box["height"]
			else:
				return 0, 0

	def add(self, child):
		self.children.append(child)

	def get(self, key, default=None):
		return self.properties.get(key, default)

	def set(self, key, value):
		self.properties[key] = value

	def read_children(self):
		for child in self.data["children"]:
			child_obj = QOBJECTS.get(child["type"], Item)(child, parent=self, doc=self.doc)
			self.add(child_obj)

QOBJECTS = {
	"ITEM": Item
}
