from fuzzysearch import find_near_matches

#find_near_matches('PATTERN', '---PATERN---', max_l_dist=1)
#substring first
#[Match(start=3, end=9, dist=1, matched="PATERN")]

#to get start:
#kek = [Match(start=3, end=9, dist=1, matched="PATERN")]
#kek[0].start

class trsb_finder:
	def __init__(self, fasta_filename, query, conservation_threshold):
		self.fasta_filename = fasta_filename
		self.query = query
		self.conservation_threshold = conservation_threshold

		self.alignment_sequences = []
		self.alignment_sequences_no_gaps = []
		self.gap_record = []

		self.trsb_locations_no_gaps_exact = []
		self.trsb_locations_no_gaps_inexact = []
		self.trsb_locations_exact = []
		self.trsb_locations_inexact = []
		self.exact_sites_with_conservation = []
		self.inexact_sites_with_conservation = []

		self.rFasta()
		self.removeGaps()
		self.findSites()
		self.modifyPositionsWithGaps()
		self.calculateConservation()

	def rFasta(self):
		#reads fasta file and stores sequences in list
		n = self.fasta_filename
		a = open(n).read().split('>')[1:]
		a = [x.split('\n', 1) for x in a]
		for x in a:
			x[1] = x[1].replace('\n', '')

		self.alignment_sequences = [y[1].upper() for y in a]			

	def removeGaps(self):
		#removes all gaps, stores gapless sequences
		#also stores an array which records the positions of gap characters
		#for example: [(2,5), (10,14)] means 5 gap characters starting at position 2 and 14 gap characters at position 10

		#first iterate through all alignment sequences and store record of all gap characters
		for s in self.alignment_sequences:
			gaps = []			
			gap_counter = 0
			start_position = 0

			for i, c in enumerate(s):
				if c == '-' and gap_counter == 0:					
					gap_counter += 1
					start_position = i

				elif c == '-' and gap_counter > 0:					
					gap_counter += 1

				elif c != '-' and gap_counter > 0:
					gaps.append((start_position, gap_counter))
					gap_counter = 0	

			#need to add gaps at tail end of string
			if gap_counter != 0:
				gaps.append((start_position, gap_counter))

			self.gap_record.append(gaps)

		#now store alignment strings with all gap characters removed		
		for sequence in self.alignment_sequences:
			self.alignment_sequences_no_gaps.append(sequence.translate({45: None}))

	def findSites(self):
		for s in self.alignment_sequences_no_gaps:	
			#exact matches
			exact_matches = find_near_matches(self.query, s, max_l_dist=0)
			starting_locations = {m.start for m in exact_matches}

			self.trsb_locations_no_gaps_exact.append(starting_locations)

			#Now we do inexact matching
			inexact_matches = find_near_matches(self.query, s, max_l_dist=1)
			inexact_starting_locations = {m.start for m in inexact_matches}			

			self.trsb_locations_no_gaps_inexact.append(inexact_starting_locations - starting_locations)

	def modifyPositionsWithGaps(self):
		#Now we need to consider the removed gap characters, adjusting the location of the sites as neccesary
		exact = self.trsb_locations_no_gaps_exact
		inexact = self.trsb_locations_no_gaps_inexact


		for i, location_set in enumerate(exact):
			sorted_locations = list(sorted(location_set))
			updated_locations = set()			
			gaps = self.gap_record[i]
			j = 0
			max_j = len(gaps)-1
			gap_total = 0

			for pos in sorted_locations:	
				temp_pos = pos + gap_total			
				#while position of TRSB location after sequence of gaps
				while temp_pos >= gaps[j][0] and j <= max_j:
					gap_total += gaps[j][1]
					temp_pos += gaps[j][1]
					j += 1		

				updated_locations.add(pos + gap_total)

			self.trsb_locations_exact.append(updated_locations)
		
		for i, location_set in enumerate(inexact):
			sorted_locations = list(sorted(location_set))
			updated_locations = set()			
			gaps = self.gap_record[i]
			j = 0
			max_j = len(gaps)-1
			gap_total = 0

			for pos in sorted_locations:	
				temp_pos = pos + gap_total			
				#while position of TRSB location after sequence of gaps
				while temp_pos >= gaps[j][0] and j <= max_j:
					gap_total += gaps[j][1]
					temp_pos += gaps[j][1]
					j += 1		

				updated_locations.add(pos + gap_total)

			self.trsb_locations_inexact.append(updated_locations)
	

	def calculateConservation(self):
		#calculate in what percentage of sequences is a specific potential trsb site found
		sequence_count = len(self.alignment_sequences)
		exact = self.trsb_locations_exact
		inexact = self.trsb_locations_inexact	

		unique_exact_sites = set.union(*exact)
		unique_inexact_sites = set.union(*inexact)		

		for site in unique_exact_sites:
			count = 0
			for site_set in exact:
				if site in site_set:
					count += 1
			conservation_percentage = round(count*100/sequence_count, 2)
			if conservation_percentage >= self.conservation_threshold:
				self.exact_sites_with_conservation.append((site, conservation_percentage))

		for site in unique_inexact_sites:
			count = 0
			for site_set in inexact:
				if site in site_set:
					count += 1
			conservation_percentage = round(count*100/sequence_count, 2)
			if conservation_percentage >= self.conservation_threshold:
				self.inexact_sites_with_conservation.append((site, conservation_percentage))

		#sorting by conservation
		self.exact_sites_with_conservation = sorted(self.exact_sites_with_conservation, key= lambda x: x[1], reverse=True)
		self.inexact_sites_with_conservation = sorted(self.inexact_sites_with_conservation, key= lambda x: x[1], reverse=True)


			
if __name__ == '__main__':

	#-----------------------------------------------------------------
	#VARIABLES
	coronavirus_genera = "Embecovirus"
	aligmnent_path = "alignments/AAA_EmbecovirusAligned.fasta"
	TRSL_sequence = "ATCTAAAC"
	conservation = 75.0
	#-----------------------------------------------------------------


	#VROOM VROOM
	finder = trsb_finder(aligmnent_path, TRSL_sequence, conservation)

	#Getting results from search
	exact_matches = finder.exact_sites_with_conservation
	inexact_matches = finder.inexact_sites_with_conservation

	#all potential TRS-B sites in downstream order
	all_matches = sorted(exact_matches+inexact_matches, key= lambda x: x[0])

	print("EXACT MATCHES: ")
	print(sorted(exact_matches, key= lambda x: x[0]))
	print("INEXACT MATCHES (one levenshtein distance from TRS-L): ")
	print(sorted(inexact_matches, key= lambda x: x[0]))

	site_len = len(TRSL_sequence)
	seq_len = len(finder.alignment_sequences[0])
	matches_len = len(all_matches)

	#Output results to format which works with RDP
	with open(coronavirus_genera + ".txt", 'w', newline = '\r\n') as f:
		f.write("[siteset]\n")		
		j=0
		for i in range(1, seq_len+1):
			if j < matches_len and i >= all_matches[j][0]+1 and i < all_matches[j][0]+site_len:
				f.write(str(i) + "," + '1' + "\n")
			elif j < matches_len and i == all_matches[j][0]+site_len:
				f.write(str(i) + "," + '1' + "\n")				
				j+=1
			else:
				f.write(str(i) + "," + '0' + "\n")

	#Output locations to readable csv file
	with open(coronavirus_genera + "_trsbs.csv", 'w', newline = '\r\n') as f:
		f.write("TRSBBP" + '\n')
		for tup in all_matches:
			f.write(str(tup[0]) + '\n')


