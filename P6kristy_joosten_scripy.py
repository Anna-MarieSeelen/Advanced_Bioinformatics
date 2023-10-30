#!/usr/bin/env python3
"""
Author: Kristy Joosten student_number:1141864
Script to do something
usage: python3 <your_script> P6ref.fasta P6related.fasta <gap_penalty>
	input_file: class, file explenation
"""
# import statements
from sys import argv
import os.path
import subprocess

def extract_sequence(fasta_file):
	"""parses the fasta file to create a dict with header as keys and sequence as value.

	Key arguments:
		fasta_file -- _io.TextIOWrapper, fasta file that contains GPA1 
		protein
	Returns:
		fasta_dictionary -- dict, fasta header is key and aminoacid sequence is value.
	"""
	fasta_dictionary = {}
	for sequence in fasta_file:
		if sequence.startswith('>'):
			header = sequence.strip()[1:]
			fasta_dictionary[header] = ""
		else:
			fasta_dictionary[header] += sequence.strip()
	return fasta_dictionary

def find_length_of_sequence(fasta_dictionary):
	"""find the sequence length for each sequence.

	Key arguments:
		fasta_dictionary -- dict, fasta header is key and aminoacid sequence is value.
	Returns:
		sequence_length -- list, of sequence length in numbers.
	"""
	sequence_length = [len(sequence) for sequence in fasta_dictionary.values()]
	return sequence_length

def run_needle(reference, related):
	"""uses run needle to get pairwise alignmends.

	Key arguments:

		reference -- _io.TextIOWrapper, fasta file that contains GPA1 
		protein from Arabidopsis.
		related -- _io.TectIOWrapper, fasta file that contains GPA1 
		proteins from plant species related to arabidopsis.
	Returns:
		out_needle -- int, file containg pairwise alignmends.
	""" 
	out_needle = "out.needle"
	gap_penalty = argv[3]
	gap_extend = 0.5
	if os.path.exists(out_needle):
		return out_needle
	cmd = "needle -asequence %s -bsequence %s -gapopen %s -gapextend %s\
	 -outfile %s" %(reference, related, gap_penalty, gap_extend, out_needle)
	print(cmd)
	e = subprocess.check_call(cmd, shell=True)
	print('EXIT STATUS AND TYPE', e, type(e))
	return out_needle

def parse_out_needle(out_needle):
	"""get sequence and name from file

	Key arguments:
		out_needle -- _io.TextIOWrapper, needle file that contains aligned sequences.
	Returns:
		output_file -- list, with header and sequence.
	"""
	data = []
	alignment = {}
	for sequence in out_needle:
		if sequence.startswith('GP'):
			lines = sequence.split()
			for i in range(len(lines)):
				if i % 2 != 1:
					sequence = lines[i]
					data.append(sequence)
	return data

def hamming_distance():
	"""for each sequence compare lines """
	return None
def calculate_identity():
	return None

def main():
	"""Main function of this module"""
	reference = argv[1]
	related = argv[2]
	reference_dict = extract_sequence(open(reference))
	related_dict = extract_sequence(open(related))
	find_length_of_sequence(related_dict)
	print(run_needle(reference, related))
	out_needle = run_needle(reference, related)
	parse_out_needle(open(out_needle))

if __name__ == "__main__":
	main()
