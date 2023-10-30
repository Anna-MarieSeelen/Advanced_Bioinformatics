#!/usr/bin/env python3
"""
Author: Anna-Marie Seelen
Studentnumber:1008970
Description: alignment of protein sequences to a reference protein sequence
and returning stats
Usage: python3
"""
# import statement
from sys import argv
import re
import subprocess
import os.path

# functions
def parse_input(fileref, filerelated):
    """Return protein sequences from two input files

    fileref: str, name of input file with the reference protein sequence
    in fasta format
    filerelated: str, name of input file with the protein sequences to compare
    to the reference protein sequence in fasta format
    return: dict, with name of sequence as key and protein sequence as value
    """
    lines=(open(fileref))
    dict={}
    for line in lines:
        line=line.strip()
        if line.startswith(">"):
            line=line.replace(">", "")
            occur = re.search(r'Guanine', line)
            index=occur.start()
            line=line[0:index-1]
            dict[line]=""
        else:
            key=list(dict)[-1]
            dict[key]+=line
    lines=(open(filerelated))
    for line in lines:
        line=line.strip()
        if line.startswith(">"):
            line=line.replace(">", "")
            occur = re.search(r'Guanine', line)
            index=occur.start()
            line=line[0:index-1]
            dict[line]=""
        else:
            key=list(dict)[-1]
            dict[key]+=line
    return dict

def lenght_seq(dict):
    """Calculates the lenght of a protein seq

    dict: dict, with name of sequence as key and protein sequence as value
    return: dict, with name of sequence as key and sequence 
    lenght as value
    """
    dict_with_lenght={}
    for key in dict:
        lenght_seq=len(dict[key])
        dict_with_lenght[key]=lenght_seq
    return dict_with_lenght
    
def write_files(dict):
    #for i in range(1,len(dict))
    file_ref=open("ref.fasta", "w")
    file_ref.write(">{}\n".format(list(dict.keys())[0]))
    file_ref.write(dict[list(dict.keys())[0]])
    
    file_rel=open("rel.fasta", "w")
    file_rel.write(">{}\n".format(list(dict.keys())[1]))
    file_rel.write(dict[list(dict.keys())[1]])
    
    file_ref.close()
    file_rel.close()
    return (file_ref, file_rel)
    #these new files didn work when in inputted them on the comand line for 
    #the needle programm so I ended up using P6ref.fasta as the files.

def run_needle():
    out_fn = "out.needle"
    cmd = 'needle {} {}'\
        .format("P6ref.fasta", "P6ref.fasta")
    #I couldn't give all arguments because needle would
    # give an error 8.0, 0.5 and out.needle have to be typed into the command
    #line.
    res = subprocess.check_output(cmd, shell=True)
    return res
    
    #out=needle(ref, rel, 8.0, 0.5, out.needle)
    #print(out.needle)

def extract_alignments(out_fn):
    lines=(open(out_fn))
    clean_lines=[]
    for line in lines:
        line=line.strip()
        if line.startswith("GPA1"):
            line=''.join(filter(lambda ch: not ch.isdigit(), line))
            line = line.replace(" ", "")
            line = line.replace("GPA_ARATH", "")
            clean_lines.append(line)
        else:
            pass
    #for an even line join them, for an odd line join them
    ref_lines = []
    pro_lines = []
    for i,line in enumerate(clean_lines):
        if i%2==0:
            pro_lines.append(line)
        else:
            ref_lines.append(line)
    string_ref=""
    string_rel=""
    for i in ref_lines:
        string_ref+=i
    for i in pro_lines:
        string_rel+=i    
    list_of_string=[]
    list_of_string.append(string_ref)
    list_of_string.append(string_rel)
    return list_of_string

def hamming_distance(list_of_string):
    """Return the number of corresponding nucleotides that differ in two DNA sequences.

    DNA_seq: list of strings with two DNA sequences
    return: int, count of different corresponding nucleotides
    """
    count=0
    for i in range(len(list_of_string[1])):
        if list_of_string[0][i] != list_of_string[1][i]:
            count+=1
        else:
            pass
    return count

def to_output_tab_file(lenght_dict, h_distance):
    """Takes a nested sorted list and outputs a tab delimited file with the contents of each sub list on a line

    sorted_list: nested list with [[accession_number, organism name, GC_content, length], etc.] sorted
    in ascending GC content order
    return: tab delimited text file with the contents of each sub list on a line
    """
    tab_file=open("P6_out_tab_delimited.txt", "w")
    for key in lenght_dict:
        tab_file.write("{0}\t{1}\t{2}".format(key, lenght_dict[key], h_distance))
        tab_file.write("\n")
    return None

def main():
    """Main function of this module"""
    # step 1: parse the protein sequence from file 1 and file 2 into dict
    dict=parse_input(argv[1], argv[2])
    # step 2: determine the lenght of the sequences
    lenght_dict=lenght_seq(dict)
    # step 3: make the files for needle
    file_ref, file_rel=write_files(dict)
    # step 4: align protein sequences from file 1 to the other species in file 2
    run_needle()
    # step 5: parse needle output to extract pairwise alignments
    list_of_string=extract_alignments(argv[3])
    # step 5: calculate hamming distance between pairwise alignments
    h_distance=hamming_distance(list_of_string)
    # step 7: tab delimited file for with the alignments, containing: sequence
    to_output_tab_file(lenght_dict, h_distance)

if __name__=="__main__":
    main()
