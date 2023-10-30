#!/usr/bin/env python3

"""
Author:
Description:
Usage:
"""

from sys import argv
import subprocess
import os.path

def main():

    commands = []
    
    # build an index of the reference genome
    commands.append('bwa index -p gen yeast/chr3.fasta')

    # how do you map the reads of imw004 on the reference genome using bwa? 
    commands.append('bwa mem gen yeast/imw004-chr3_1.fastq yeast/imw004-chr3_2.fastq > outtextA1.sam')
    
    # how do you convert the SAM file to a sorted BAM file using samtools?
    commands.append('samtools sort outtextA1.bam -o outtextA1sort.bam')
    #'samtools view -S -b outtextA1.sam > outtextA1.bam'
    
    # how do you get all variants w.r.t. the reference, using bcftools?
    commands.append('bcftools mpileup -f yeast/chr3.fasta outtextA1sort.bam -o bcfout.txt') #bamfile omzetten naar iets
    commands.append('bcftools call -m -v -o result bcfout.txt') #v is alleen de variance, o is output naam
    
    print('Getting ready to execute the following commands:')
    
    for c in commands:
        print(c)
    
    # START EXECUTION
    for cmd in commands:
        print('Executing:', cmd)
        subprocess.check_call(cmd, shell=True)
        print('Succes')
    #132273 to 133124 is the mutation somewhere because thatś the location of the ADY2 protein
    #and you can find that in the VCF file where the mutation is.
    #VCF in 132370 is a mutation from G --> C

if __name__ == "__main__":

    main()
