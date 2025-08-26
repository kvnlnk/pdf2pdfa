def get_gs_command(command_type:str, version:int, input_path:str, output_path:str):
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
        "pdf2pdfa_with_profile": [
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
            input_path
        ],
        "pdf2pdfa_with_independent_color": [
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
            input_path
        ]
    }
    
    if command_type not in commands:
        raise ValueError(f"Unknown command type: {command_type}")
    
    return commands[command_type]