from . import text
from uuid import uuid4
from json import dumps

FIGMA_TYPE_MAPPING = dict()


# Document
class QmlDocument:
	NODE_COUNT = 0

	def __init__(self, figma_document: dict, resource_folder="res"):
		self.resource_folder = resource_folder
		self.imports_ = {"QtQuick": 2.12}
		self.figma_document = figma_document
		self.node = FIGMA_TYPE_MAPPING.get(figma_document["type"], Item)(
			document=self,
			figma_data=figma_document,
			parent=None
		)

	def stringify(self):
		# imports
		result = ""
		for import_, version in self.imports.items():
			result += text(f"import {import_} {version}", tabs=0)
		result += text("", 0)
		result += self.node.stringify()
		return result

	@property
	def imports(self) -> dict:
		return self.imports_

	@imports.setter
	def imports(self, value: dict) -> None:
		self.imports_.update(value)

	def save(self, filename="_"):
		qml = self.stringify()
		with open(f"{filename}.qml", "w") as file:
			file.write(qml)


# base item
class Item:
	QML_TYPE = "Item"
	QML_REQUIREMENTS = {}

	def __init__(self, document: QmlDocument, figma_data: dict, parent=None):
		self.document = document			# the qml document that holds this tree
		self._parent: Item = parent			# the direct parent
		self.figma_data = figma_data		# the dictionary data from figma json file
		self.id = figma_data.get("id")

		# the position on the tree, starting from 0
		self.depth = 0 if parent is None else (parent.depth+1)
		self.qml_properties = {}			# a key, value pair of this object's property
		self.children = []
		self.is_layout = False				# is this qml item a layout

		# properties
		QmlDocument.NODE_COUNT += 1
		self.qml_properties["id"] = f"node_{QmlDocument.NODE_COUNT}"
		if self._parent is None:
			self.qml_properties["visible"] = True

		# initialize on created
		self.update_imports()
		self.update_properties()
		self.create_children()

	@property
	def is_ghost(self):
		"""ghost objects are objects who arent really parents of there children
		this is actually affected by figma node objects like GROUPS
		children of GROUP nodes are not positioned relative to itself."""
		return False

	@property
	def parent(self):
		# returns the parent of this item
		if not (self._parent is None):
			if self._parent.is_ghost:
				return self._parent.parent
		return self._parent

	def update_imports(self):
		# update imports
		self.document.imports = self.QML_REQUIREMENTS

	def update_properties(self):
		# properties
		self.prop_x()
		self.prop_y()
		self.prop_width()
		self.prop_height()
		self.prop_visible()
		self.prop_opacity()
		self.prop_rotation()
		self.prop_anchors()
		self.prop_anchor_margins()

	def create_children(self):
		# children
		children: list = self.figma_data.get("children", [])
		for child_data in children:
			item: Item = FIGMA_TYPE_MAPPING.get(child_data["type"], Item)(
				document=self.document,
				figma_data=child_data,
				parent=self
			)
			self.children.append(item)

	def __str__(self):
		return self.QML_TYPE

	def __repr__(self):
		return f"<{self.QML_TYPE} children={len(self.children)}>"

	def stringify(self, include_children=True) -> str:
		tab = self.depth if include_children else 0
		result = text(self.QML_TYPE + " {", tab, newline=True)

		tab += 1
		# property
		for prop, value in self.qml_properties.items():

			ignore_jsonify = (		# ignore json serialization for the value of this key
				prop == "id" or
				prop.split(".")[0] == "anchors" or
				(prop == "color" and value.split(".")[0] == "Qt") or
				(type(value) == str and (value or "").startswith("qsTr(")) or
				prop in ["font.weight", "wrapMode", "lineHeightMode"]
			)

			if not ignore_jsonify:
				value = dumps(value)

			result += text(
				f"{prop}: {value}",
				tab, newline=True
			)
		else:
			result += "\n"
			for child in self.children:
				child: Item
				result += child.stringify()
			else:
				tab -= 1

		return result + text("}\n", tab, newline=True)

	def prop_x(self):
		if not (self.parent is None):
			box: dict = self.figma_data.get("absoluteBoundingBox", {})
			parent_box: dict = self.parent.figma_data.get("absoluteBoundingBox", {})

			if box:
				x = int(box.get("x", 0) - parent_box.get("x", 0))
				if x != 0:
					self.qml_properties["x"] = x

	def prop_y(self):
		if not (self.parent is None):
			box: dict = self.figma_data.get("absoluteBoundingBox", {})
			parent_box: dict = self.parent.figma_data.get("absoluteBoundingBox", {})

			if box:
				y = int(box.get("y", 0) - parent_box.get("y", 0))
				if y:
					self.qml_properties["y"] = y

	def prop_width(self):
		width: float = self.figma_data.get(
			"absoluteBoundingBox", {}
		).get("width", 0.0)
		width: int = int(width)
		if width:
			self.qml_properties["width"] = width

	def prop_height(self):
		height: float = self.figma_data.get(
			"absoluteBoundingBox", {}
		).get("height", 0.0)
		height: int = int(height)
		if height:
			self.qml_properties["height"] = height

	def prop_visible(self):
		visible = self.figma_data.get("visible", True)
		if not visible:
			self.qml_properties["visible"] = visible

	def prop_opacity(self):
		opacity = self.figma_data.get("opacity")
		if not (opacity is None):
			self.qml_properties["opacity"] = opacity

	def prop_rotation(self):
		rotation = self.figma_data.get("rotation")
		if not (rotation is None):
			self.qml_properties["rotation"] = rotation

	def prop_anchors(self):
		layout_child = True if self.parent is None else self.parent.is_layout
		
		if layout_child:
			return
		
		constraints: dict = self.figma_data.get("constraints")
		if constraints:
			horizontal: str = constraints.get("horizontal", "LEFT")
			vertical: str	= constraints.get("vertical", "TOP")

			if horizontal == "CENTER" and vertical == "CENTER":
				self.qml_properties["anchors.centerIn"] = "parent"
				# remove the x, y coords cus it's no longer needed
				del self.qml_properties["x"]
				del self.qml_properties["y"]

			elif (vertical=="TOP_BOTTOM" or vertical=="SCALE") and (horizontal=="LEFT_RIGHT" or horizontal=="SCALE"):
				self.qml_properties["anchors.fill"] = "parent"
				# remove the x, y coords cus it's no longer needed
				del self.qml_properties["x"]
				del self.qml_properties["y"]

			else:
				if vertical=="TOP":
					pass
				elif vertical=="BOTTOM":
					self.qml_properties["anchors.bottom"] = "parent.bottom"

				elif vertical=="CENTER":
					self.qml_properties["anchors.verticalCenter"] = "parent.verticalCenter"

				elif vertical=="TOP_BOTTOM" or vertical=="SCALE":
					self.qml_properties["anchors.top"] = "parent.top"
					self.qml_properties["anchors.bottom"] = "parent.bottom"

				if horizontal=="LEFT":
					pass
				elif horizontal=="RIGHT":
					self.qml_properties["anchors.right"] = "parent.right"

				elif horizontal=="CENTER":
					self.qml_properties["anchors.horizontalCenter"] = "parent.horizontalCenter"

				elif horizontal=="LEFT_RIGHT" or horizontal=="SCALE":
					self.qml_properties["anchors.left"] = "parent.left"
					self.qml_properties["anchors.right"] = "parent.right"

	def prop_anchor_margins(self):
		layout_child = True if self.parent is None else self.parent.is_layout
		
		if layout_child:
			return

		me = self.qml_properties
		parent = self.parent.qml_properties

		top_offset = me.get("y", 0) - parent.get("y", 0)
		ver_offset = (me.get("y", 0) + (me.get("height", 0)/2)) - (parent.get("y", 0)+(parent.get("height", 0)/2))
		hor_offset = (me.get("x", 0) + (me.get("width", 0)/2)) - (parent.get("x", 0)+(parent.get("width", 0)/2))
		left_offset = me.get("x", 0) - parent.get("x", 0)
		right_offset = (parent.get("width", 0) - (me.get("x", 0) + me.get("width", 0)))
		bottom_offset = (parent.get("height", 0) - (me.get("y", 0) + me.get("height", 0)))

		top_offset		= int(top_offset)
		ver_offset 		= int(ver_offset)
		hor_offset 		= int(hor_offset)
		left_offset 	= int(left_offset)
		right_offset 	= int(right_offset)
		bottom_offset 	= int(bottom_offset)

		if top_offset==bottom_offset==left_offset==right_offset:
			offset = top_offset
			if offset and me.get("anchors.fill"):
				self.qml_properties["anchors.margins"] = top_offset
		else:
			if top_offset and (me.get("anchors.top") or me.get("anchors.fill")):
				self.qml_properties["anchors.topMargin"] = top_offset

			if ver_offset and (me.get("anchors.verticalCenter") or me.get("anchors.fill")):
				self.qml_properties["anchors.verticalCenterOffset"] = ver_offset

			if hor_offset and (me.get("anchors.horizontalCenter") or me.get("anchors.fill")):
				self.qml_properties["anchors.horizontalCenterOffset"] = hor_offset

			if left_offset and (me.get("anchors.left") or me.get("anchors.fill")):
				self.qml_properties["anchors.leftMargin"] = left_offset

			if right_offset and (me.get("anchors.right") or me.get("anchors.fill")):
				self.qml_properties["anchors.rightMargin"] = right_offset

			if bottom_offset and (me.get("anchors.bottom") or me.get("anchors.fill")):
				self.qml_properties["anchors.bottomMargin"] = bottom_offset


class GhostItem(Item):

	@property
	def is_ghost(self):
		return True

	def stringify(self, include_children=True) -> str:
		tab = self.depth if include_children else 0
		result = text("// This is a Ghost-Group - do not uncomment {", tab, newline=True)

		tab += 1
		for child in self.children:
			child: Item
			result += child.stringify()
		else:
			tab -= 1

		return result + text("// }\n", tab, newline=True)

	def update_properties(self):
		pass


class Image(Item):
	QML_TYPE = "Image"

	def update_properties(self):
		pass

FIGMA_TYPE_MAPPING["GROUP"] = GhostItem


# rectangle
class Rectangle(Item):
	QML_TYPE = "Rectangle"

	def update_properties(self):
		super(Rectangle, self).update_properties()
		self.prop_color()
		self.prop_radius()

	def prop_color(self):
		fills: list = self.figma_data.get("fills")
		if fills:
			# this library only supports one fill per node
			# TODO: add support for multiple fills
			for fill in fills:
				if fill["type"] == "SOLID":
					self.qml_properties["color"] = "Qt.rgba({r}, {g}, {b}, {a})".format(
						**fill.get("color")
					)
				if fill["type"] == "IMAGE":
					# create a new child... Image qml type
					image: Image  = Image(document=self.document, figma_data=fill, parent=self)
					image.qml_properties["anchors.fill"] = "parent"
					image.qml_properties["source"] = ""
					
					self.children.append(image)

	def prop_radius(self):
		radius: float = self.figma_data.get("cornerRadius")
		if type(radius) == float or type(radius) == int:
			if int(radius) != 0:
				self.qml_properties["radius"] = radius


FIGMA_TYPE_MAPPING["FRAME"] = Rectangle
FIGMA_TYPE_MAPPING["ELLIPSE"] = Rectangle
FIGMA_TYPE_MAPPING["RECTANGLE"] = Rectangle
FIGMA_TYPE_MAPPING["COMPONENT"] = Rectangle


class Label(Item):
	QML_TYPE = "Label"
	QML_REQUIREMENTS = {
		"QtQuick.Controls": 2.12
	}

	def update_properties(self):
		super(Label, self).update_properties()
		self.prop_text()
		self.prop_font()
		self.prop_color()

	def prop_text(self):
		text = self.figma_data.get("characters", "")
		self.qml_properties["text"] = f'qsTr("{text}")'

	def prop_font(self):
		qml: dict = self.qml_properties
		style: dict = self.figma_data.get("style")
		if style:
			qml["font.family"] = style["fontFamily"]
			qml["font.weight"] = {
				100: "Font.ExtraLight",
				200: "Font.Thin",
				300: "Font.Light",
				400: "Font.Normal",
				500: "Font.Medium",
				600: "Font.DemiBold",
				700: "Font.Bold",
				800: "Font.ExtraBold",
				900: "Font.Black"
			}[style["fontWeight"]]
			qml["font.pixelSize"] = style["fontSize"]
			qml["lineHeight"] = style["lineHeightPx"]
			qml["font.letterSpacing"] = style["letterSpacing"]
			qml["wrapMode"] = {
				"NONE": "Text.NoWrap",
				"HEIGHT": "Text.Wrap",
				"WIDTH_AND_HEIGHT": "Text.Wrap"
			}[style["textAutoResize"]]
			qml["lineHeightMode"] = "Text.FixedHeight"

	def prop_color(self):
		fills: list = self.figma_data.get("fills")
		if fills:
			# TODO: add support for multiple fills
			fill: dict = fills[0]

			if fill["type"] == "SOLID":
				self.qml_properties["color"] = "Qt.rgba({r}, {g}, {b}, {a})".format(
					**fill.get("color")
				)


FIGMA_TYPE_MAPPING["TEXT"] = Label
