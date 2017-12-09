class Tab:

	def __init__(self, myFile):
		self.tab = self.parsing(myFile)


	def parsingDSSP(self, myFile, chaine):
		myfile = open(myFile, "r")
		parsedFile = open("data.txt", "a")
		cList = ['p', 'q', 'n', 'd', 'l', 'e', 'b', 'f', 'o', 'c', 'k', 'r', 'a', 'm', 'h', 'j', 'g', 'i']
		dic = {"H" : "H", "G" : "H", "I" : "H", "E" : "E", "B" : "E", "T" : "C", "C" : "C", "S" : "C", " ": "C"}
		notAA = ["X", "B", "Z"]
		sequence = ""
		structure = ""
		reading = False
		parsedFile.write("> identifier|protein name|organism\n")
		for line in myfile:
			if line[0:3] == "  #":
				reading = True
			elif reading:
				if line[11] == chaine:
					AA = line[13]
					if AA in cList:
						AA = "C"
					if AA not in notAA:
						sequence += AA
						structure += dic[line[16]]
		parsedFile.write(sequence)
		parsedFile.write("\n")
		parsedFile.write(structure)
		parsedFile.write("\n")


	def parsing(self, myFile):
		myfile = open(myFile, "r")
		nbLine = 0
		for line in myfile:
			current = line.replace("\n", "").split(" ")
			ID = current[0][0:4]
			chaine = current[0][4]
			dsspFile = "dataset/dssp/" + ID + ".dssp"
			self.parsingDSSP(dsspFile, chaine)
			nbLine += 1


def main():
	myFile = "dataset/CATH_info.txt"
	Tab(myFile)


main()