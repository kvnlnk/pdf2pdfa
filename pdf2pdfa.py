import subprocess
import os
import argparse
import logging

from gs_utils import get_gs_command, replace_icc_path, cleanup_temp_file

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

current_working_dir = os.path.dirname(os.path.abspath(__file__))
logging.info(f"Current working directory: {current_working_dir}")

parser = argparse.ArgumentParser(
    description="A simple Ghostscript-based PDF to PDF/A-1B converter written in Python. "
)

# Arguments
parser.add_argument("-i", "--input", type=str, help="Input PDF file with path")
# Optional arguments
parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output path for the converted PDF/A-1B file.\n Default will be the current directory + '/[input_filename]_pdfa.pdf'",
)
parser.add_argument(
    "-t",
    "--type",
    type=str,
    choices=["profile", "independent"],
    default="profile",
    help="Whether to use a color profile or device independent color.",
)
parser.add_argument(
    "-pv",
    "--pdfaVersion",
    type=int,
    choices=[1, 2, 3],
    default=1,
    help="PDF/A version (1, 2, or 3). Default is 1.",
)
parser.add_argument(
    "-v",
    "--validate",
    type=bool,
    choices=[True, False],
    default=False,
    help="Validate the PDF/A file after conversion.",
)

args = parser.parse_args()


def convert_pdf_to_pdfa(input_path: str, output_path: str):
    """
    Converts a PDF file to PDF/A format.

    Args:
        input_path (str): The path to the input PDF file.
        output_path (str): The path to the output PDF/A file.

    Returns:
        str: The path to the output PDF/A file.
    """

    logging.info(f"Converting PDF to PDF/A: {input_path} -> {output_path}")

    # Create output path if not provided
    if output_path is None:
        logging.info(
            "No output path provided. Using default naming convention in current directory."
        )
        base, ext = os.path.splitext(os.path.basename(input_path))
        output_path = os.path.join(os.getcwd(), f"{base}_pdfa.pdf")

    logging.info("Constructing Ghostscript command...")

    icc_file_path = os.path.join(current_working_dir, "resources\\srgb.icc")
    ps_file_path = os.path.join(current_working_dir, "resources\\PDFA_def.ps")

    logging.info("Creating temporary PostScript file with ICC profile path...")
    temp_ps_file_path = replace_icc_path(
        ps_file_path=ps_file_path, icc_file_name=icc_file_path
    )
    logging.info(f"Temporary PostScript file created at: {temp_ps_file_path}")

    gs_command = get_gs_command(
        command_type=args.type,
        version=args.pdfaVersion,
        icc_profile_path=os.path.join(current_working_dir, icc_file_path),
        ps_file_path=temp_ps_file_path,
        input_path=input_path,
        output_path=output_path,
    )

    # Execute the Ghostscript command
    try:
        logging.info("Executing Ghostscript command...")
        subprocess.run(gs_command, check=True)
        logging.info(f"Successfully converted '{input_path}' to '{output_path}'")
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Error occurred while converting PDF to PDF/A-{args.pdfaVersion}B: {e}"
        )
    finally:
        cleanup_temp_file(temp_ps_file_path)

    return output_path


def validate_pdfa(output_path: str):
    """
    Validates the PDF/A file.

    Args:
        output_path (str): The path to the output PDF/A file.
    """

    logging.info(f"Validating PDF/A file: {output_path}")
    validation_command = [".\\veraPDF\\verapdf.bat", output_path, "--format", "text"]

    try:
        subprocess.run(validation_command, check=True)
        logging.info(f"Validation completed for '{output_path}'")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while validating PDF/A file: {e}")


# Main execution
if args.input:
    logging.info(f"Input file: {args.input}")
    output_path = convert_pdf_to_pdfa(args.input, args.output)
    logging.info(f"Output file: {output_path}")

    if args.validate:
        validate_pdfa(output_path)
