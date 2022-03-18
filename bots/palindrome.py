#!/usr/bin/python

from peers import Peers
import re

#  Palindrome_data


#  Palindrome_Judeg
#  Palindromic_tweet
class Palindrome:
	def __init__(self, text, peers=None):
		self.text = text
		self.min_uniques = 3

		if peers is None: 
			self.peers = Peers()
		else:
			self.peers = peers

		self.straight = None

		self.id = self.get_id()
	

	def get_id(self):
		return self.peers.normalize(self.text)


	def prepared_text(self):
		result = self.text.replace("#", "")
		result = result.strip()
		return result


	def __eq__(self, other):
		return isinstance(other, Palindrome) and self.text == other.text


	def __str__(self):
		#  return self.text 
		return self.prepared_text() 

	def count_peers(self):
		count = 0

		for c in self.text:
			if self.peers.is_peer(c):
				count+=1

		return count

	def count_unique_peers(self):
		s = []

		for c in self.text:
			if not self.peers.is_peer(c):
				continue

			n = self.peers.normal(c)

			if not n in s:
				s.append(n)

		return len(s)


	def how_nice(self):
		nl = 0


		uniques = self.count_unique_peers()

		tokens_count = len(re.findall(r'\w+', self.text))

		chars_diversity = (uniques / len(self.text) / 2)

	

		if self.straight:
			nl+=800

		if self.count_peers() > 5:
			nl+=200

		if uniques >= self.min_uniques:
			nl+=200


		# 700

		if tokens_count > 9:
			nl+=600
		elif tokens_count == 9:
			nl+=500
		elif tokens_count == 8:
			nl+=400
		elif tokens_count == 7:
			nl+=400
		elif tokens_count == 6:
			nl+=300
		elif tokens_count == 5:
			nl+=300
		elif tokens_count == 4:  # 1400
			nl+=200
		elif tokens_count == 3:
			nl+=100


		#  if uniques <= 2:
			#  nl-=800


		#  if tokens_count < 3 and chars_diversity < 0.3 and uniques < 4:
		if chars_diversity < 0.3 and uniques < 4:
		#  if chars_diversity < 0.3:
			nl-= 815


		#  print(f"\nuniques={uniques} tokens_count={tokens_count} chars_diversity={chars_diversity} straight={self.straight}\n")

		return nl



# https://stackoverflow.com/questions/8031658/python-count-word-tokens-in-sentence

#
