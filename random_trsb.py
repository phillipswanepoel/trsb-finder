import random

def rFasta(path):
	#reads fasta file and stores sequences in list
	n = path
	a = open(n).read().split('>')[1:]
	a = [x.split('\n', 1) for x in a]
	for x in a:
		x[1] = x[1].replace('\n', '')

	return [y[1] for y in a]

def rCSV(path):
	a = open(path).read().strip().split("\n")[1:]
	a = [int(y) for y in a]
	return a



if __name__ == '__main__':

	for i in range(1,21):
		#-----------------------------------------------------------------
		#VARIABLES	
		alignment_choose = random.randint(1, 6)	
		alignment_path = "alignments/" + str(alignment_choose) + ".fasta"
		trsb_path = "alignments/" + str(alignment_choose) + "_trsbs.csv"		
		trsb_length = 8
		#-----------------------------------------------------------------		
		
		alignment_sequences = rFasta(alignment_path)
		trsb_locations = rCSV(trsb_path)		
		seq_len = len(alignment_sequences[0])

		#amount of sites to translate sites with
		random_sites_start_position = random.sample(range(1, seq_len+1), 1)[0]	
		
		trsb_locations = [(x+random_sites_start_position)%seq_len for x in trsb_locations]
		print(alignment_choose)
		print(trsb_locations)
		print("")

		random_sites_start_positions = {x for x in trsb_locations}	

		
		#Output results to format which works with RDP
		with open("RDP/sitesets/" + str(i) + "_" + str(alignment_choose) + ".txt", 'w', newline = '\r\n') as f:
			f.write("[siteset]\n")	
			j=0
			for i in range(1, seq_len+1):	
				if i in random_sites_start_positions and j == 0:
					f.write(str(i) + "," + '1' + "\n")
					j += 1
				elif j < trsb_length and j > 0:
					f.write(str(i) + "," + '1' + "\n")
					j += 1
				else:
					f.write(str(i) + "," + '0' + "\n")
					j = 0
			
