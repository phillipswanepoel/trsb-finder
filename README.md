# trsb-finder
find_trsb.py:
Searches for potential TRS-B locations in an alignment, given a TRS-L sequence and a conservation threshold.
Specifically, finds all occurences of subsequences with a Levenshtein distance of 0 or 1 from the TRS-L. 
Then filters out all the potential sites which aren't conserved across more than (conservation threshold)% of the sequences in the alignment.

random_trsb.py:
Generates a permuted version of a siteset file. So given some list of TRS-Bs at specific nucleotide positions for an alignment, this script generates an RDP siteset file where the positions were all translated such that the distance between them is preserved. Maximum translation length = length of genome. Wraps around ends.
