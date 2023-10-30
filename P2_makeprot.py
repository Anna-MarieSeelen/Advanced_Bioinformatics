#!/usr/bin/env python3

"""
Author: Unknown & Anna-Marie Seelen
Studentnumber: 1008970
Description: This script generates protein sequences and returns an
output file. The scipt takes three command line arguments, 
argv[1]= desired amount of protein sequences, argv[2]= either 0
(ascending protein sequences) or 1 (descending protein sequences),
argv[3]= filename of outputfile.

Usage: python3 P2_makeprot.py
"""

#import statements
from sys import argv
from random import randrange, choice

#functions
def process_input():
    """Putting the given command line arguments into variables
    no input required
    return: num_seq: int, number of protein sequences to be generated.
            descending: int, 0 or 1, 0= sort protein sequences by 
            ascending lenght, 1= sort protein sequences by descending
            lenght.
            out_fn: str, text file to store generate protein sequences.
    """
    
    num_seqs = int(argv[1])
    if num_seqs < 1:
        raise ValueError("First argument should be larger than 0")
    
    descending = int(argv[2])
    if descending == 0 or descending == 1:
        sort_descending = bool(int(argv[2]))
    else:
        raise ValueError("Second argument should be 0 or 1")
    
    try: 
        out_fn = argv[3]
    except IndexError:
        out_fn = None

    return num_seqs, descending, out_fn

def generate_sequences(num_sequences, min_lenght=25, max_lenght=250):
    """ Generate given number of protein sequences of various lenghts.
    
    num_sequences: int or float, desired lenght of protein sequence
    min_lenght: int or float, minimum lenght a generated protein
    sequences will have, default=25
    max_lenght: int or float, maximum lenght a generated protein
    sequences will have default=250
    return: list of proteins of various lenghts starting with "M"
    
    Generate given number of protein sequences of lenghts between a 
    minimum and maximum lenght
    """
    proteins = []
    AA = "ACDEFGHIKLMNPQRSTVWY"
    for seq in range(num_sequences):
        prot_label = "prot{}".format(seq+1)
        prot_length = randrange(min_lenght,max_lenght+1)
        new_prot = "M"
        for pos in range(1,prot_length):
            new_prot += choice(AA)
        proteins.append((prot_label, new_prot))
    return proteins

def sort_seq(gen_sequences, d=False):
    """ Returns a sorted list of protein sequences based on lenght
    
    gen_sequences: list, generated protein sequences of various lenghts
    d: bool, False = sort protein sequences by ascending lenght,
    True= sort protein sequences by descending lenght
    return: list of protein sequences sorted by lenght
    """

    seqs_with_len = [(len(sequence),label,sequence) for \
     (label,sequence) in gen_sequences]
    seqs_with_len.sort(reverse=d)
    sorted_list = [(label, sequence) for (leng, label, sequence) \
    in seqs_with_len]
    return sorted_list

def write_fasta(sorted_seq, out_file=None):
    """ Writes list to an output text file in fasta format
    
    sorted_seq: list, sorted protein sequences of various lenghts
    out_file: string, name of the output file
    return: None
    """

    if out_file:
        out = open(out_file,'w')
    for label, sequence in sorted_seq:
        if not out_file:
            print(">{}\n{}".format(label, sequence))
        else:
            out.write(">{}\n{}\n".format(label, sequence))
    if out_file:
        out.close()
    return None

def main():
    """Main function of the module
    """
    # put command line arguments into variables
    num_sequences, descending, output_file = process_input()
    # generate list of protein sequences
    gen_sequences = generate_sequences(num_sequences)
    # sort list of protein sequences
    sorted_seqs = sort_seq(gen_sequences, d=descending)
    #step 4: print list in fasta format to output file
    write_fasta(sorted_seqs, output_file)

if __name__ == "__main__":

    main()

