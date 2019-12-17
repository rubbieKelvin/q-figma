class Item(object):
	"""docstring for Item."""
	def __init__(self, data, parent=None):
		super(Item, self).__init__()
		self._figmatype = ""
		self.type = ""
		self.parent = parent
		self.properties = dict(
			id = data.get("id")
		)
		self.children = []

	def add(self, child):
		self.children.append(child)

	def get(self, key, default=None):
		return self.properties.get(key, default)

	def set(self, key, value):
		self.properties[key] = value
