import os
import argparse


parser = argparse.ArgumentParser(
    description="A simple Ghostscript-based PDF to PDF/A-1B converter written in Python."
)

# Required arguments
parser.add_argument("input", type=str, help="Input PDF file with path")

# Optional arguments
parser.add_argument("-o", "--output", help="Output path for the converted PDF/A-1B file.\n Default will be the current directory + '/[input_filename]_pdfa.pdf'")

args = parser.parse_args()
print(args)