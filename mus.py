import sys

def main():
	quiet = len(sys.argv)>0 and sys.argv[1].lower()=='true'
	if (not quiet): print("Starting mus...")
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