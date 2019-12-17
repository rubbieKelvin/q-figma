import json
import pprint
from qfigma import qml

with open("tests/t2l1iO6hmcdwzGcGgyChvM.json") as file:
	jsonsource = json.load(file)

printer = pprint.PrettyPrinter()
parser = qml.FigmaQMLParser(jsonsource)

documents = parser.parse()

printer.pprint(documents)
