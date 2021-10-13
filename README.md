# trsb-finder
find_trsb.py:
Searches for potential TRS-B locations in an alignment, given a TRS-L sequence and a conservation threshold.
Specifically, finds all occurences of subsequences with a hamming distance of 0 or 1 from the TRS-L. 
Then filters out all the potential sites which aren't conserved across more than (conservation threshold)% of the sequences in the alignment.

random_trsb.py:
Randomly generates an amount of TRS-B site locations given an alignment, TRS-B length and the amount of sites.
