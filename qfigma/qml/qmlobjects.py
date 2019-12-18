# rubbie kelvin
# Item is the simplest form of a qml object(if i'm not mistaken), so its our parent class for the rest of them
# NOTE: figma property for rotation hasnt been found, all objects needs it;

class Item(object):
	def __init__(self, data, parent=None, doc=None):
		super(Item, self).__init__()
		self.data = data
		self.type = "Item"
		self.config = data[".qfigma"]
		self.doc = doc
		self.parent = parent
		self.is_layout = False
		self.properties = {}
		self.tab = 0 if self.parent is None else self.parent.tab+1
		self.children = []
		# ...
		self.load_properties()
		self.read_children()

	def _load_standard_properties(self):
		# load standard properties for all nodes
		# this method should not be Overridden
		self.set("id", self.data.get("id"))
		self.set("x", self.coords[0])
		self.set("y", self.coords[1])
		self.set("width", self.size[0])
		self.set("height", self.size[1])
		# complicated properties
		self.set("opacity", None) if self.data.get("opacity", 0) == 0 else self.set("opacity", self.data.get("opacity", None))
		self.set("visible", None) if self.data.get("visible", True) else self.set("visible", "false")
		self.set("rotation", None) if self.data.get("rotation", 0) == 0 else None
		self.put_anchors()
		# exceptions for root
		if self.parent is None:
			self.set("x", None)
			self.set("y", None)
			self.set("visible", "true")
			self.set("id", "root")

	def load_properties(self):
		# this function loads all properties for the node.
		# this method should be Overridden, instead of $_load_standard_properties()
		# make sure to call super when overriding
		self._load_standard_properties()

	def newline(self, indent):
		# gives a qml style newline
		# indent gives the code a clean look
		# returns a string with new line and appropriate indentation
		return ("\n"+("\t"*indent))

	def put_anchors(self):
		# this function sets anchors for child nodes, when nessesary
		# anchors will not be given to root nodes, or children with laouts as parent
		# layouting would be giving to child=>parent:layouts instead of anchors
		layout = None if self.parent is None else self.parent.is_layout
		# parform layouting
		if layout is True:
			pass
		# performs anchoring
		elif layout is False:
			hor = self.data["constraints"]["vertical"]
			ver = self.data["constraints"]["horizontal"]

			top = self.get("y", 0)-self.parent.get("y", 0)
			bottom = (self.parent.get("y", 0)+self.get("height"))-(self.get("y", 0)+self.get("height"))
			left = self.get("x", 0)-self.parent.get("x", 0)
			right = (self.parent.get("x", 0)+self.get("width"))-(self.get("x", 0)+self.get("width"))
			h_offset = (self.get("x", 0)+(self.get("width")/2))-(self.parent.get("x", 0)+(self.parent.get("width")/2))
			v_offset = (self.get("y", 0)+(self.get("height")/2))-(self.parent.get("y", 0)+(self.parent.get("height")/2))

			if hor == "CENTER" and ver == "CENTER":
				self.set("anchors.centerIn", "parent")
			elif (hor == "LEFT_RIGHT" or hor == "SCALE") and (ver == "TOP_BOTTOM" or ver == "SCALE"):
				self.set("anchors.fill", "parent")
				self.set("anchors.topMargin", top if top > 0 else None)
				self.set("anchors.bottomMargin", bottom if bottom > 0 else None)
				self.set("anchors.leftMargin", left if left > 0 else None)
				self.set("anchors.rightMargin", right if right > 0 else None)
			else:
				if hor == "LEFT":
					pass
				elif hor == "RIGHT":
					self.set("anchors.right", "parent.right")
					self.set("anchors.rightMargin", right if right > 0 else None)
				elif hor == "CENTER":
					self.set("anchors.horizontalCenter", "parent.horizontalCenter")
					self.set("anchors.horizontalCenterOffset", h_offset)
				elif hor == "LEFT_RIGHT" or hor == "SCALE":
					self.set("anchors.right", "parent.right")
					self.set("anchors.rightMargin", right if right > 0 else None)
					self.set("anchors.horizontalCenter", "parent.horizontalCenter")
					self.set("anchors.horizontalCenterOffset", h_offset)

				if ver == "TOP":
					pass
				elif ver == "BOTTOM":
					self.set("anchors.bottom", "parent.bottom")
					self.set("anchors.bottomMargin", bottom if bottom > 0 else None)
				elif ver == "CENTER":
					self.set("anchors.verticalCenter", "parent.verticalCenter")
					self.set("anchors.verticalCenterOffset", v_offset)
				elif ver == "TOP_BOTTOM" or ver == "SCALE":
					self.set("anchors.bottom", "parent.bottom")
					self.set("anchors.bottomMargin", bottom if bottom > 0 else None)
					self.set("anchors.verticalCenter", "parent.verticalCenter")
					self.set("anchors.verticalCenterOffset", v_offset)

	@property
	def coords(self):
		# returns tuple (x, y)
		if self.parent is None:
			return 0, 0
		else:
			box = self.data.get("absoluteBoundingBox")
			if box: return box["x"]-self.parent.data.get("absoluteBoundingBox", {}).get("x", 0), box["y"]-self.parent.data.get("absoluteBoundingBox", {}).get("y", 0)
			else: return 0, 0

	@property
	def size(self):
		# returns tuple (width, height)
		box = self.data.get("absoluteBoundingBox")
		if box: return box["width"], box["height"]
		else: return 0, 0

	def add(self, child):
		# adds a child to node.
		# one line of code, but cost me a lot :|
		self.children.append(child)

	def get(self, key, default=None):
		# returns a property with the following key
		# if the value is None, it returns default
		res = self.properties.get(key, default)
		if res == None: return default
		else: return res

	def set(self, key, value):
		# sets a key:value to property
		self.properties[key] = value

	def read_children(self):
		# read children from node
		# making them python objects in the process
		for child in self.data["children"]:
			child_obj = QOBJECTS.get(child["type"], Item)(child, parent=self, doc=self.doc)
			self.add(child_obj)

	def to_string(self, include_children=True):
		# convert this specific object to a string
		# if not $include_children, string for only this node will be returned
		tab = self.tab if include_children else 0
		res = self.newline(indent=tab)+self.type+"{"
		# write properties
		tab += 1
		for props in self.properties:
			value = self.properties[props]
			if value is not None:
				res += self.newline(indent=tab) + props + ": " + str(value)
		# add children below...
		if include_children:
			res += "\n"
			for child in self.children:
				res += child.to_string()
		# add children above...
		tab -= 1
		res += (self.newline(indent=tab) + "}\n")
		return res

	def fill(self):
		# this method should be used for nodes with "fill" key
		# color: may be fiil or gradient or image
		if len(self.data.get("fills")) > 0:
			color = self.data.get("fills")[0]
			# SOLID
			if color["type"]=="SOLID":
				self.set("color", "Qt.rgba({r}, {g}, {b}, {a})".format(r=color["color"]["r"], g=color["color"]["g"], b=color["color"]["b"], a=color["color"]["a"]))
			# GRADIENT
			elif color["type"]=="GRADIENT_LINEAR":
				self.doc.add_import("QtQuick.Shapes", 1.11)
				pos = color.get("gradientHandlePositions")
				res = "LinearGradient {"+"{n}x1: {x1}{n}y1: {y1}{n}x2: {x2}{n}y2: {y2}".format(n=self.newline(self.tab+2), x1=pos[0]['x']*self.get("width"), y1=pos[0]["y"]*self.get("height"), x2=pos[1]["x"]*self.get("width"), y2=pos[1]["y"]*self.get("height"))
				for gradient in color["gradientStops"]:
					res += "{n}GradientStop ".format(n=self.newline(self.tab+2))+"{"+"position: {position}; color: Qt.rgba({r}, {g}, {b}, {a})".format(position=gradient["position"], r=gradient["color"]["r"], g=gradient["color"]["g"], b=gradient["color"]["b"], a=gradient["color"]["a"])+"}"
				res += (self.newline(self.tab+1)+"}")
				self.set("gradient", res)



class Rectangle(Item):
	"""docstring for Rectangle."""
	def __init__(self, data, parent=None, doc=None):
		super(Rectangle, self).__init__(data, parent=parent, doc=doc)
		self.type = "Rectangle"

	def load_properties(self):
		super(Rectangle, self).load_properties()

		b_width = self.data.get("strokeWeight", 0)
		self.set("radius", None) if self.data.get("cornerRadius", 0) == 0 else self.set("radius", self.data.get("cornerRadius", None))
		self.set("border.width", None) if b_width <= 1 else b_width-1
		self.fill()

class Label(Item):
	"""docstring for Label."""
	def __init__(self, data, parent=None, doc=None):
		super(Label, self).__init__(data, parent=parent, doc=doc)
		self.type = "Label"

	def load_properties(self):
		super(Label, self).load_properties()

		self.set("text", "qsTr(\"{text}\")".format(text=self.data.get("characters", "")))
		self.set("font.family", "\"{font}\"".format(font=self.data["style"].get("fontFamily", "Roboto")))
		self.set("font.pixelSize", int(self.data["style"].get("fontSize", 12)))
		self.set("font.letterSpacing", self.data["style"].get("letterSpacing", 0.1))
		self.set("lineHeight", self.data["style"].get("lineHeightPx", 1))

		# setting fontalignment
		v = self.data["style"].get("textAlignVertical")
		h = self.data["style"].get("textAlignHorizontal")
		self.set("verticalAlignment", "Text.AlignTop" if v == "TOP" else "Text.AlignVCenter" if v == "CENTER" else "Text.AlignBottom")
		self.set("horizontalAlignment", "Text.AlignLeft" if h == "LEFT" else "Text.AlignHCenter" if h == "CENTER" else "Text.AlignRight")

		self.fill()


QOBJECTS = {
	"Item": Item,
	"Rectangle": Rectangle,
	"Label": Label
}
