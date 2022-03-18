#!/usr/bin/python

class Peers:
	def __init__(self):
		self.peers = {}
		self.dicern_accents = False

		self.fill_peers()

	def add(self, char, normal):
		self.peers[char] = normal


	def fill_normals(self, chars, normal):
		for c in chars:
			self.add(c.upper(), normal)
			self.add(c.lower(), normal)

	def fill_peers(self):
		if not self.dicern_accents:
			self.fill_normals("áàãâä", 'a')
			self.fill_normals("éèẽêë", 'e')
			self.fill_normals("íìĩîï", 'i')
			self.fill_normals("óòõôö", 'o')
			self.fill_normals("úùũûü", 'u')
			self.fill_normals("ýỳŷŷÿ", 'y')
			self.fill_normals("ç"    , 'c')
			self.fill_normals("ñ"    , 'n')

			for c in range(ord('a'), ord('z')+1):
				self.add(chr(c),chr(c).lower())

			for c in range(ord('A'), ord('Z')+1):
				self.add(chr(c),chr(c).lower())

			for c in range(0, 10):
				self.add(str(c),str(c).lower())

	def normal(self, c):
		return self.peers[c]

	def is_peer(self, c):
		return c in self.peers.keys()

	def is_matching(self, c1, c2):
		return self.normal(c1) == self.normal(c2)

	def normalize(self, text):
	
		text = text.lower().strip()

		result = ""
		for c in text:
			if self.is_peer(c):
				result+= self.normal(c)
			else:
				if c in " ,.":
					result+= " "

		# replace all spaces (including new lines, tabs, etc) by a single space
		# and removes double spaces too
		result = " ".join(result.split()) 
		
		return result





