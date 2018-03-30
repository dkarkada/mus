import sys
import re
from datetime import date

class Artist:
	def __init__(self, name):
		self.name = name
		self.songs = []
	def getSongs(self):
		return self.songs

class Song:
	def __init__(self, title, month, year, ind, pl):
		self.title = title
		self.artists = []
		self.date = date(year, month, 1)
		self.index = ind
		self.playlist = pl

def parse(quiet, artists, playlists):
	file = open('data.txt', 'r')
	for line in file:
		songdata = re.split(r"\t", line)
		
	file.close()	

def main():
	quiet = len(sys.argv)>0 and sys.argv[1].lower()=='true'
	if (not quiet):
		print("Starting mus...")
		print("Reading data...")
	artists = {}
	playlists = {}
	parse(quiet, artists, playlists)	
	done = False
	while (not done):
		try:
			inp = input(">> ")
		except KeyboardInterrupt:
			print()
			sys.exit();
		args = inp.split(" ")
		if (len(args) != 0):
			cmd = args[0]
			if (cmd in ('quit','exit')):
				done = True
			elif (cmd == 'ls'):
				print("AA")

if __name__ == "__main__":
	main()