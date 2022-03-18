#!/usr/bin/python

from palindrome import Palindrome
from peers import Peers

class Palindromer:

	def __init__(self):

		#  self.include_surrunding = True
		self.include_left_surrounding = False
		self.include_right_surrounding = True
		#  self.include_surrunding = False
		self.min_size           = 4
		self.peers              = Peers()

		self.max_surrounding		= 3
	

	#  Remember ...
	#  - center-l and center+r always ponts to the next chars, not the last matched peers
	#  - in text[center-l+1:center+r] the first index is included and the last not

	#  center-l+1     is the first index
	#  center+r       is the last  index
	#  text[center-l] is the the char before the first
	#  text[center+r] is the the char after  the last



	def find_palindrome(self, text, center, dc):

		l=0
		r=0
		count=0

		if (dc):
			l=0
			r=1
		else:
			l=1
			r=1

		text_len = len(text)

		while(True):

			if (center-l < 0) or (center+r == text_len):
				break


			cl = text[center-l]
			cr = text[center+r]
			#  print(f".{cl}.=.{cr}.")


			try_again = False

			if not self.peers.is_peer(cl):
				l+=1
				try_again = True

			if not self.peers.is_peer(cr):
				r+=1
				try_again = True

			if try_again:
				continue


			if not self.peers.is_matching(cl, cr):
				break

			l+=1
			r+=1
			count+=1

			r_last_matched = r
			l_last_matched = l

			next_left  = text[center-l]
			if center+r < text_len:
				next_right = text[center+r]
			else:
				next_right = None

		if count == 0:
			return ""


		r = r_last_matched
		l = l_last_matched


		leng = count * 2
		if not dc:
			leng = leng + 1

		#  when there is a non peer in the center, decrease length. For exemple in "abcd!dcba"
		if not dc and not self.peers.is_peer(text[center]):
			leng+=-1


		if leng < self.min_size:
			return ""


		starts_ok = (center-l+1 == 0)        or (not self.peers.is_peer(next_left))
		ends_ok   = (center+r   == text_len) or (not self.peers.is_peer(next_right))
		straight  = starts_ok and ends_ok


		if(self.include_right_surrounding):
			count = 0
			while (count <= self.max_surrounding) and (center+r < text_len) and (not self.peers.is_peer(text[center+r])):
				r+=1
				count+=1
		else:
			while (not self.peers.is_peer(text[center+r-1])):
				r-=1


		if(self.include_left_surrounding):
			count = 0
			while (count <= self.max_surrounding) and (center-l >=0) and (not self.peers.is_peer(text[center-l])):
				l+=1
				count+=1
		else:
			while (not self.peers.is_peer(text[center-l+1])):
				l-=1


        
		pal = text[center-l+1:center+r]
		pal = pal.strip()

		palindrome = Palindrome(pal, self.peers)
		palindrome.straight = straight

		return palindrome



	def longestPalindrome(self, text):
		pal = ""

		for i in range(0, len(text)):
			p1 = self.find_palindrome(text, i, True)
			p2 = self.find_palindrome(text, i, False)

			if len(p1) > len(pal):
				pal = p1
			if len(p2) > len(pal):
				pal = p2

		return pal


	def find_subpalindromes(self, text):
		pals = []
		
		for i in range(0, len(text)):
			p1 = self.find_palindrome(text, i, True)
			p2 = self.find_palindrome(text, i, False)


			if (p1 != ""):
				if not p1 in pals:
					pals.append(p1)
			if (p2 != ""):
				if not p2 in pals:
					pals.append(p2)


		return pals


