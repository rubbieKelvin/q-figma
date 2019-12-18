import json
import qfigma
import unittest
from qfigma import qml

# with open("tests/t2l1iO6hmcdwzGcGgyChvM.json") as file:
# 	jsonsource = json.load(file)

# printer = pprint.PrettyPrinter()
# parser = qml.FigmaQMLParser(jsonsource)

# documents = parser.parse()

# printer.pprint(documents)

class ConversionTest(unittest.TestCase):
	"""testing for figma/qml conversion
	"""

	def setUp(self):
		super(ConversionTest, self).setUp()
		self.token = "19675-8e5c271c-01ad-49aa-b8ec-5001db996702"	# this is rubbie's personal token
		self.file_id = "t2l1iO6hmcdwzGcGgyChvM"						# i already designed a litle figma file here for testing.
		self.fig_file = "garbage\\t2l1iO6hmcdwzGcGgyChvM.json"		# already called figma json file
		with open(self.fig_file) as file: self.parser = qml.FigmaQMLParser(json.load(file))	# parser object

	def test_fetch_figmafile(self):
		response = qfigma.requestfigmafile(self.token, self.file_id)
		self.assertIs(type(response), dict)

	def test_parser(self):
		pass