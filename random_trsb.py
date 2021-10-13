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
	#-----------------------------------------------------------------
	#VARIABLES
	coronavirus_genera = "embecovirus"
	alignment_path = "alignments/AAA_EmbecovirusAligned.fasta"
	amount_of_random_trsb_sites = 10	
	trsb_length = 8
	#-----------------------------------------------------------------
	

	alignment_sequences = rFasta(alignment_path)
	seq_len = len(alignment_sequences[0])

	random_sites_start_positions = set(random.sample(range(1, seq_len+1), amount_of_random_trsb_sites ))

	print(seq_len)
	print(random_sites_start_positions)
	
	#Output results to format which works with RDP
	with open(coronavirus_genera + "_random" + ".txt", 'w', newline = '\r\n') as f:
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
			
