import random

def rFasta(path):
	#reads fasta file and stores sequences in list
	n = path
	a = open(n).read().split('>')[1:]
	a = [x.split('\n', 1) for x in a]
	for x in a:
		x[1] = x[1].replace('\n', '')

	return [y[1] for y in a]

if __name__ == '__main__':

	for i in range(1,5):
		#-----------------------------------------------------------------
		#VARIABLES	
		alignment_choose = random.randint(1, 6)	
		alignment_path = "alignments/" + str(alignment_choose) + ".fasta"
		minimum_site_amount = 5
		maximum_site_amount = 10
		amount_of_random_trsb_sites = random.randint(minimum_site_amount, maximum_site_amount)	
		trsb_length = 8
		#-----------------------------------------------------------------
		

		alignment_sequences = rFasta(alignment_path)
		seq_len = len(alignment_sequences[0])

		random_sites_start_positions = set(random.sample(range(1, seq_len+1), amount_of_random_trsb_sites ))

		print(alignment_choose)
		print(seq_len)
		print(amount_of_random_trsb_sites)
		print(random_sites_start_positions)
		
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
			
