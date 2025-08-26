import subprocess
import os
import argparse


parser = argparse.ArgumentParser(
    description="A simple Ghostscript-based PDF to PDF/A-1B converter written in Python. "
)

# Arguments
parser.add_argument("-i", "--input", help="Input PDF file with path")
# Optional arguments
parser.add_argument("-o", "--output", help="Output path for the converted PDF/A-1B file.\n Default will be the current directory + '/[input_filename]_pdfa.pdf'")

args = parser.parse_args()

def convert_pdf_to_pdfa(input_path, output_path):
    if output_path is None:
        base, ext = os.path.splitext(os.path.basename(input_path))
        output_path = os.path.join(os.getcwd(), f"{base}_pdfa.pdf")
        
    # Construct the Ghostscript command
    gs_command = [
        "gswin64c",
        "--permit-file-read=C:\\source\\pdf2pdfa\\srgb.icc",
        "--permit-file-read=C:\\source\\pdf2pdfa\\PDFA_def.ps",
        "--permit-file-read=" + input_path,
        "-dPDFA=1",
        "-dBATCH",
        "-dNOPAUSE",
        "-dNOOUTERSAVE",
        "-dCompatibilityLevel=1.4",
        "-dPDFACompatibilityPolicy=1",
        "-sColorConversionStrategy=RGB",
        "-sDEVICE=pdfwrite",
        "-sDefaultRGBProfile=C:\\source\\pdf2pdfa\\srgb.icc",
        f"-sOutputFile={output_path}",
        "C:\\source\\pdf2pdfa\\PDFA_def.ps",
        input_path
    ]
    
    # Execute the Ghostscript command
    try:
        subprocess.run(gs_command, check=True)
        print(f"Successfully converted '{input_path}' to '{output_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while converting PDF to PDF/A-1B: {e}")
        

if args.input:
    print(f"Input file: {args.input}")
    convert_pdf_to_pdfa(args.input, args.output)