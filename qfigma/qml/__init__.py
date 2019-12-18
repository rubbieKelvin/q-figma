import os
import json
from .. import jibberish
from . import qmlobjects

class FigmaQMLParser(object):
	# types
	# the following types are used for simplification of json file
	# converting figmatypes to qml types
	# these are also the basic avalable qmltypes... for now
	ITEM = 'Item'
	RECTANGLE = "Rectangle"
	LABEL = "Label"
	IMAGE = "Image"
	PATH = "Path"


	def __init__(self, figma_data):
		super(FigmaQMLParser, self).__init__()
		self.nodes = self.clean(figma_data)

	def qmltype(self, figmatype):
		# figma types translated into qml types
		# `figmatype` is passed in as a str and the corresponding qmltype is returned
		# if the figma type is not reconized, it would return "FigmaQMLParser.ITEM" by default
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
		# returns a list of dictionaries:nodes,
		# nodes are extracted from every page as root elements
		# below:list of dictionary objects
		pages = fig["document"]["children"].copy()
		# digs parent for childrens 
		# the digging process add a few more keys eg: .qfigma
		# and also sets typing for node, alternating a few more keys
		# the digging process also checks for children's children attaching them to the "children" key
		# if node doesnt have any child, an empty list is assigned to the "children" key
		def dig(node):
			node[".qfigma"] = dict(initial_type=node["type"], comments=[], initial_id=node["id"])
			node["id"] = node.get("type", "qfigma").lower()+"_"+jibberish(node['id'])
			node["type"] = self.qmltype(node["type"])			
			if node.get("children"):
				clone = node["children"].copy()
				node["children"] = []
				for child in clone: node["children"].append(dig(child))
			else:
				node["children"] = []
			return node
		# access pages to extract root nodes
		# now loop through pages to seek root nodes
		nodes = []
		for page in pages:
			for node in page["children"]:
				nodes.append(dig(node))
		return nodes

	def parse(self):
		# returns a list of class=>QmlDocument
		# parsing makes an object out of the dictionary
		# this function returns a list of class=>QmlDocument, each document having special components
		# component 1: imports
		# component 2: root => children
		# component 3: resources (typically images:svg,png)
		# component 4: style
		res = []
		for doc in self.nodes:
			res.append(QmlDocument(doc))
		return res


class QmlDocument(object):
	DEFAULT = 0
	IMAGINE = 1
	FUSION = 2
	MATERIAL = 3
	UNIVERSAL = 4

	def __init__(self, data, resfolder="res/"):
		super(QmlDocument, self).__init__()
		self.imports = {"QtQuick": 2.0, "QtQuick.Layouts": 1.3, "QtQuick.Controls": 2.9}
		self.resources = {}
		self.root = qmlobjects.QOBJECTS.get(data["type"], qmlobjects.Item)(data, parent=None, doc=self)
		self.style = ""
		self.setstyle(QmlDocument.DEFAULT)

	def setstyle(self, style):
		# sets qml styling for application
		# see qt docs for more details
		self.style = style
		if style == QmlDocument.DEFAULT:
			pass
		elif style == QmlDocument.IMAGINE:
			pass
		elif style == QmlDocument.FUSION:
			pass
		elif style == QmlDocument.MATERIAL:
			self.add_import("QtQuick.Controls.Material", 2.0)
		elif style == QmlDocument.UNIVERSAL:
			pass
		else:
			self.style = QmlDocument.DEFAULT

	def add_import(self, module, version):
		# adds a qml module to the imports component
		# added module is stored in self.imports
		# any child-node can make imports call as $doc arguments are passed to them
		self.imports[module] = version

	def remove_import(self, module):
		# remove a module fom the imports component
		del self.imports[module]

	def stringify(self):
		# merges all resources and converts them to string
		# deal with imports first
		# the handle nodes
		# the function operates by asking the root node for strings, which in turn,
		# asks its children for strings
		# the whole thing is compiled and returned here
		res = ""
		for module in self.imports:
			version = self.imports[module]
			res += f"import {module} {version}\n"
		res += self.root.to_string()
		return res
