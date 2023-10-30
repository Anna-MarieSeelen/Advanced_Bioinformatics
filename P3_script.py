#!/usr/bin/env python3

"""
Author: Anna-Marie Seelen
Studentnr: 1008970
Description: Script parsing argonaut formatted genbank file and outputs (1) tab delimited file with info such as
GC content and (2) a file in fasta format.
"""

from sys import argv
import subprocess
import os.path
import re
import string

def parse_input(filename):
    """Parses argonaut formatted file to extract accession number, organism name and DNA_seq and stores those in dict.

    filename: str, name of argonaut formatted input file
    return: nested dictionary with {accession_number:{organism_name:DNA-seq}}
    """

    lines=(open(filename))
    origin = False
    gb_dict= {}
    for line in lines:
        line=line.strip()
        if line.startswith("ACCESSION"):
            line = line.replace("ACCESSION   ", "")
            gb_dict[line] = []
        elif line.startswith("ORGANISM"):
            organism_dict = {}
            line = line.replace("ORGANISM  ", "")
            key = list(gb_dict)[-1]
            organism_dict[line] = ""
            gb_dict[key] = organism_dict
        elif "ORIGIN" in line:
            origin=True
        elif "//" in line:
            origin=False
        if origin:
            line=line.replace(" ", "")
            line=''.join(filter(lambda ch: not ch.isdigit(), line))
            #https://www.studytonight.com/python-howtos/remove-numbers-from-string-in-python
            line = line.replace("ORIGIN", "")
            key = list(gb_dict)[-1]
            dict=gb_dict[key]
            last_key=list(dict)[-1]
            gb_dict[key][last_key]+=line
        else:
            pass
    return gb_dict

def cal_GC_content(gb_dict):
    """Calculates the GC content of each DNA sequence and returns a nested list with information on the DNA sequence

    gb_dict: nested dictionary with {accession_number:{organism_name:DNA-seq}}
    return: nested list with [[accession_number, organism name, GC_content, length], etc.]
    """
    long_list=[]
    for key in gb_dict:
        sequence = []
        for second_key in list(gb_dict[key]):
            lenght_seq=len(gb_dict[key][second_key])
            sequence.append(key)
            sequence.append(second_key)
            count=0
            for character in gb_dict[key][second_key]:
                if character == "g":
                    count+=1
                elif character=="c":
                    count+=1
                else:
                    pass
            GC_content=(count/lenght_seq)*100
            sequence.append(GC_content)
            sequence.append(lenght_seq)
        long_list.append(sequence)
    return long_list

def sort_nested_list(long_list):
    """Takes a nested list and sorts the list based on a particular value in the sublist

    long_list: nested list with [[accession_number, organism name, GC_content, length], etc.]
    return: nested list with [[accession_number, organism name, GC_content, length], etc.] sorted
    in ascending GC content order
    """
    long_list.sort(key = lambda x: x[2], reverse=True)
    #https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
    return long_list

def to_output_tab_file(sorted_list):
    """Takes a nested sorted list and outputs a tab delimited file with the contents of each sub list on a line

    sorted_list: nested list with [[accession_number, organism name, GC_content, length], etc.] sorted
    in ascending GC content order
    return: tab delimited text file with the contents of each sub list on a line
    """
    tab_file=open("P3_out_tab_delimited.txt", "w")
    for organism in sorted_list:
        tab_file.write("{0}\t{1}\t{2:.2f}\t{3}".format(organism[0], organism[1], organism[2], organism[3]))
        tab_file.write("\n")
    return None

def to_output_fasta_file(gb_dict, sorted_list):
    """Outputs a fasta file sorted in ascending GC content based on a nested dictionary and sorted list

    gb_dict: nested dictionary with {accession_number:{organism_name:DNA-seq}}
    sorted_list: nested list with [[accession_number, organism name, GC_content, length], etc.]
    return: text file in fasta format sorted in ascending GC content
    """
    sorted_acc_num = [item[0] for item in sorted_list]
    #https://www.geeksforgeeks.org/python-get-first-element-of-each-sublist/
    fasta_file=open("P3_out_fasta.txt", "w")
    for acc_num in sorted_acc_num:
        organism_name=list(gb_dict[acc_num])[-1]
        DNA_seq=gb_dict[acc_num][organism_name].upper()
        fasta_file.write(">{0} {1}\n{2}\n".format(acc_num, organism_name, DNA_seq))
    return None

def main():
    """ This is the main function of this module
    """
    #step 1: parse the file and put accession num, organism name and dna sequence in a nested dict
    gb_dict=parse_input(argv[1])
    #step 2: calculate the GC content and return a nested list with gc accession num, organism name, gc content and lenght
    long_list=cal_GC_content(gb_dict)
    #step 3: sort the nested list based in accending order of GC content
    sorted_list=sort_nested_list((long_list))
    #step 4: output the nested list to a tab delimited file
    to_output_tab_file(sorted_list)
    #step 5: output the contents of the nested dict in ascending order of GC content to a fasta file
    to_output_fasta_file(gb_dict, sorted_list)

if __name__ == "__main__":
    main()
