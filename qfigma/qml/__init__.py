import os
import json
from .. import jibberish
from . import qmlobjects

class FigmaQMLParser(object):
	"""docstring for FigmaQMLParser."""

	# types
	ITEM = 'Item'
	RECTANGLE = "Rectangle"
	LABEL = "Label"
	IMAGE = "Image"
	PATH = "Path"


	def __init__(self, figjson):
		super(FigmaQMLParser, self).__init__()
		self.nodes = self.clean(figjson)

	def qmltype(self, figmatype):
		types = {
			"FRAME": FigmaQMLParser.RECTANGLE,
			"RECTANGLE": FigmaQMLParser.RECTANGLE,
			"GROUP": FigmaQMLParser.RECTANGLE,
			"VECTOR": FigmaQMLParser.PATH,
			"BOOLEAN_OPERATION": FigmaQMLParser.PATH,
			"STAR": FigmaQMLParser.PATH,
			"LINE": FigmaQMLParser.PATH,
			"ELLIPSE": FigmaQMLParser.PATH,
			"REGULAR_POLYGON": FigmaQMLParser.PATH,
			"TEXT": FigmaQMLParser.LABEL,
			"COMPONENT": FigmaQMLParser.RECTANGLE
		}
		return types.get(figmatype, FigmaQMLParser.ITEM)

	def clean(self, fig):
		# cleans figma json into a more simplified format
		pages = fig["document"]["children"].copy()		# list of dictionary objects

		# digs parent for children
		###############
		def dig(node):
			node[".qfigma"] = dict(
				initial_type = node.get("type"),
				comments = []
			)																					# add special keys
			node["id"] = node.get("type", "qfigma").lower()+"_"+jibberish(node['id'])			# set unique id for object
			node["type"] = self.qmltype(node["type"])	 										# swap figma to qml type
			# dig for children here
			if node.get("children"):
				clone = node["children"].copy()
				node["children"] = []
				for child in clone:
					node["children"].append(dig(child))
			else:
				node["children"] = []
			return node

		# access pages to extract root nodes
		nodes = []
		for page in pages:
			for node in page["children"]:
				nodes.append(dig(node))
		return nodes

	def parse(self):
		# returns a list of class=>QmlDocument
		res = []
		for doc in self.nodes:
			res.append(QmlDocument(doc))
		return res


class QmlDocument(object):

	"""docstring for QmlDocument."""
	STYLES = {"DEFAULT": 0, "IMAGINE": 1, "FUSION": 2, "MATERIAL": 3, "UNIVERSAL": 4}

	def __init__(self, data, resfolder="res/"):
		super(QmlDocument, self).__init__()
		self.imports = {"QtQuick": 2.0, "QtQuick.Layouts": 1.3, "QtQuick.Controls": 2.9}
		self.resources = {}
		self.root = qmlobjects.QOBJECTS.get(data["type"], qmlobjects.Item)(data, parent=None, doc=self)
		self.style = QmlDocument.STYLES["DEFAULT"]

	def setstyle(self, style):
		if style == QmlDocument.DEFAULT:
			pass
		elif style == QmlDocument.IMAGINE:
			pass
		elif style == QmlDocument.FUSION:
			pass
		elif style == QmlDocument.MATERIAL:
			pass
		elif style == QmlDocument.UNIVERSAL:
			pass
		else:
			raise TypeError("Invalid Style type")

	def add_import(self, module, version):
		self.imports[module] = version

	def remove_module(self, module):
		del self.imports[module]

	def stringify(self):
		pass