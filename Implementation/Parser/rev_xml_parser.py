from xml.etree import ElementTree as ET
from collections import defaultdict as dd
import json

def get_reviews(in_filepath, out_filepath):
	tree = ET.parse("laptop.xml")
	prty = {'negative':[0,0,1], 'positive':[1,0,0], 'neutral':[0,1,0], 'conflict':[0,0,1]}
	root = tree.getroot()
	reviews = []
	for node in root:
		review = node.find('text').text
		aspects = node.find('aspectTerms')
		if aspects is not None:
			for aspect in aspects:
				attribs = aspect.attrib
				print attribs
				print attribs.keys()
				reviews.append({'review':review, 'aspect':attribs['term'], 'polarity':prty[attribs['polarity']], 'is_present':[0,1], 'to_from':[attribs['from'], attribs['to']]})

	with open(out_filepath+'/reviews.json', 'w') as file:
			file.write(json.dumps(reviews))

def main():
    get_reviews("laptop.xml", ".")

if __name__ == '__main__':
    main()