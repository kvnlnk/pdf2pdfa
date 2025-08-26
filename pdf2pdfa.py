import subprocess
import os
import argparse

from config import *


parser = argparse.ArgumentParser(
    description="A simple Ghostscript-based PDF to PDF/A-1B converter written in Python. "
)

# Arguments
parser.add_argument("-i", "--input", help="Input PDF file with path")
# Optional arguments
parser.add_argument("-o", "--output", help="Output path for the converted PDF/A-1B file.\n Default will be the current directory + '/[input_filename]_pdfa.pdf'")

parser.add_argument("-v", "--version", type=int, choices=[1, 2, 3], default=1, help="PDF/A version (1, 2, or 3). Default is 1.")

args = parser.parse_args()

def convert_pdf_to_pdfa(input_path, output_path):
    if output_path is None:
        base, ext = os.path.splitext(os.path.basename(input_path))
        output_path = os.path.join(os.getcwd(), f"{base}_pdfa.pdf")
        
    # Construct the Ghostscript command
    gs_command = get_gs_command("pdf2pdfa_with_profile", args.version, input_path, output_path)

    # Execute the Ghostscript command
    try:
        subprocess.run(gs_command, check=True)
        print(f"Successfully converted '{input_path}' to '{output_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while converting PDF to PDF/A-1B: {e}")
        

if args.input:
    print(f"Input file: {args.input}")
    convert_pdf_to_pdfa(args.input, args.output)