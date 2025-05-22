class Affilation:
	name: str
	country: str
	city: str

	def __init__(self, json_dict: dict):
		self.name = json_dict.get('affilname', '')
		self.city = json_dict.get('affiliation-city', '')
		self.country = json_dict.get('affiliation-country', '')

class Article:
	title: str
	publication_name: str
	scopus_link: str
	creator: str
	'''first author on the document'''
	affiliations: list[Affilation]

	def __init__(self, json_dict: dict):
		if 'dc:title' not in json_dict:
			raise Exception(f'Invalid response: {json_dict}')
		self.title = json_dict['dc:title']
		self.publication_name = json_dict.get('prism:publicationName', '')
		self.scopus_link = ''
		links = json_dict['link']
		for link in links:
			if link['@ref'] == 'scopus':
				self.scopus_link = link['@href']
				break
		self.creator = json_dict.get('dc:creator', '')
		self.affiliations = []
		if 'affiliation' in json_dict:
			for affil in json_dict['affiliation']:
				affilation = Affilation(affil)
				self.affiliations.append(affilation)
