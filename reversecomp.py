#!/usr/bin/python

import argparse
import tqdm
import subprocess
from Bio import SeqIO
import re
import textwrap
import os
import sys

parser = argparse.ArgumentParser(prog='python reversecomp.py',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\

    Author: Murat Buyukyoruk
    Associated lab: Wiedenheft lab

        reversecomp help:

This script is developed to get reverse complementary of sequences in a multifasta/fasta file .

SeqIO package from Bio is required to fetch flank sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        
Syntax:

        python reversecomp.py -i demo.fasta

fasta_unalignr dependencies:

	Bio module and SeqIO available in this package          refer to https://biopython.org/wiki/Download
	tqdm                                                    refer to https://pypi.org/project/tqdm/
	
Input Paramaters (REQUIRED):
----------------------------
	-i/--input		FASTA			Specify a fasta file.
	
	-o/--output		FASTA			Specify a fasta output.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.
	
      	'''))

parser.add_argument('-i', '--input', required=True, type=str, dest='filename', help='Specify a fastafile.\n')

parser.add_argument('-o', '--output', required=True, dest='out', help='Specify a output fasta file name.\n')

results = parser.parse_args()
filename = results.filename
out = results.out

os.system('> ' + out)

proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, )
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length)) as pbar:
    pbar.set_description('Getting Reverse Comp...')
    for record in SeqIO.parse(filename, "fasta"):
        pbar.update()
        f = open(out, 'a')
        sys.stdout = f
        rev = record.seq.reverse_complement()
        print ">" + record.description + " | Reverse strand"
        print re.sub("(.{60})", "\\1\n", str(rev), 0, re.DOTALL)

