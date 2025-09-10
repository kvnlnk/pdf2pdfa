import logging
import os
import tempfile


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_gs_command(command_type: str, version: int, input_path: str, output_path: str):
    """
    Generates Ghostscript command arrays for PDF/A conversion.

    Args:
        command_type (str): The type of Ghostscript command to generate.
        version (int): The version of PDF/A to generate.
        input_path (str): The path to the input PDF file.
        output_path (str): The path to the output PDF/A file.

    Raises:
        ValueError: If the command type is unknown.

    Returns:
        list: A list of Ghostscript command arguments.
    """

    commands = {
        "profile": [
            "gswin64c",
            "--permit-file-read=C:\\source\\pdf2pdfa\\srgb.icc",
            "--permit-file-read=C:\\source\\pdf2pdfa\\PDFA_def.ps",
            f"--permit-file-read={input_path}",
            f"-dPDFA={version}",
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
            input_path,
        ],
        "independent": [
            "gswin64c",
            f"-dPDFA={version}",
            "-dBATCH",
            "-dNOPAUSE",
            "-dNOOUTERSAVE",
            "-dCompatibilityLevel=1.4",
            "-dPDFACompatibilityPolicy=1",
            "-sColorConversionStrategy=UseDeviceIndependentColor",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={output_path}",
            input_path,
        ],
    }

    if command_type not in commands:
        raise ValueError(f"Unknown command type: {command_type}")

    return commands[command_type]


def replace_icc_path(ps_file_path: str, icc_file_name: str) -> str:
    """
    Replace the placeholder in the PostScript file with the actual ICC profile path
    since Ghostscript on Windows does not support relative paths for ICC profiles.

    Args:
        ps_file_path (str): The path to the PostScript file.
        icc_file_name (str): The name of the ICC profile file.

    Returns:
        str: The path to the temporary PostScript file with the replaced ICC profile path.
    """
    current_working_dir = os.getcwd()

    # Read ps-file
    with open(ps_file_path, "r") as file:
        file_content = file.read()

    file_content = file_content.replace(
        "ICC_PROFILE_PATH", os.path.join(current_working_dir, icc_file_name)
    )

    # Write to a temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".ps", delete=False
    ) as temp_ps_file:
        temp_ps_file.write(file_content)
        temp_file_path = temp_ps_file.name

    return temp_file_path


def cleanup_temp_file(file_path: str):
    """
    Cleans up the temporary PostScript file.

    Args:
        file_path (str): The path to the temporary PostScript file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Temporary file '{file_path}' has been deleted.")
    else:
        logging.warning(f"Temporary file '{file_path}' does not exist.")