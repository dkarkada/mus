import sys
import re
from datetime import date
from time import strptime

class Artist:
	def __init__(self, name):
		self.name = name
		self.songs = {}
	def getSongs(self):
		return self.songs
	def addSong(self, song, role):
		if (song.title not in self.songs):
			self.songs[song.title] = (song, role)
		else:
			err = "Artist already has song:"
			print("{} {}, {}".format(err, self.name, song.title))

class Song:
	def __init__(self, title, month, year, ind, pl):
		self.title = title
		self.artists = []
		self.month = month
		self.year = year
		self.index = ind
		self.playlist = pl
	def addArtist(self, artist):
		self.artists.append(artist)

def parseDate(date):
	info = re.split(" ", date)
	if len(info) == 1:
		return "", info[0]
	return info[0], info[1]

def parse(quiet, artists, playlists):
	file = open('data.txt', 'r')
	month = ""
	year = 0
	playlist = ""
	ind = 0
	for line in file:
		songdata = re.split(r"\t", line)
		if songdata[0].strip() != "":
			playlist = songdata[0].strip()
			month, year = "", 0
			if playlist not in playlists:
				playlists[playlist] = []
			else:
				err = "Playlist double specified:"
				print("{} {}".format(err, line))
			for info in songdata[1:]:
				if (info.strip() != ""):
					err = "Playlist should be specified in its own line:"
					print("{} {}".format(err, line))
		else:
			if songdata[1].strip() != "":
				month, year = parseDate(songdata[1].strip())
			if songdata[2].strip() != "":
				ind += 1
				title = songdata[2].strip()
				song = Song(title, month, year, ind, playlist)
				# expectFlag = False
				ppl = [info.strip()[1:] if info.strip()[0]=="\\" else info.strip()\
						for info in songdata[3:] if len(info.strip())>1 and info.strip()[0]!=":"]
				artistmeta = [info.strip()[1:] for info in songdata[3:] if len(info.strip())>0 and info.strip()[0]==":"]
				if (len(artistmeta)==0):
					artistmeta.append("o")
				elif (len(artistmeta)>1):
					err = "Multiple instances of artist metainfo:"
					print("{} {}".format(err, line))
				for i in range(len(ppl)):
					meta = artistmeta[0]
					if (i >= len(meta)):
						err = "Artist metainfo has insufficient length:"
						print("{} {}".format(err, line))
						role = 'o'
					else:
						role = meta[i]
					name = ppl[i]
					if (name.lower() not in artists):
						artist = Artist(name)
						artists[name.lower()] = artist
					else:
						artist = artists[name.lower()]
					song.addArtist(artist)
					artist.addSong(song, role)
				playlists[playlist].append(song)
			else:
				err = "No song title:"
				print("{} {}".format(err, line))

	# for artistname in artists:
	# 	print(artistname)
	# 	artist = artists[artistname]
	# 	print("---------")
	# 	for title in artist.songs:
	# 		song, role = artist.songs[title]
	# 		if (song.month != ""):
	# 			month = strptime(song.month, "%B").tm_mon
	# 		else:
	# 			month = ""
	# 		print(role, "\t", song.title)
	# 	print()
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