# pdf2pdfa
A simple Ghostscript-based PDF to PDF/A-1B converter written in Python with validation. 

## Requirements

- A recent version of Python (at least [3.12.6](https://www.python.org/downloads/release/python-3126/))
- A recent version of Ghostscript (at least Ghostscript [10.05.1](https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10051/ghostpdl-10.05.1.tar.gz))
- A recent version of Java (at least [Java 21](https://jdk.java.net/archive/))

## Installation
Just download the repository as a ZIP file and extract it, or clone the repository:
1. Clone the repository:
   ```bash
   git clone https://github.com/kvnlnk/pdf2pdfa.git
   cd pdf2pdfa
   ```

## Usage
Take the PDF file you want to convert and run the following command:
```bash
python pdf2pdfa.py [-h] [-i INPUT] [-o OUTPUT] [-t {profile,independent}] [-pv {1,2,3}] [-v {True,False}]
```
You may or may not specify an output file name and location. If you don't, the output file will be saved in the same directory as the input file, with the same name but with a -pdfa extension. You also have a number of optional arguments:
```
  -h, --help            show this help message and exit

  -i INPUT, --input INPUT
                        Input PDF file with path

  -o OUTPUT, --output OUTPUT
                        Output path for the converted PDF/A-1B file. Default will be the current directory + '/[input_filename]_pdfa.pdf'

  -t {profile,independent}, --type {profile,independent}
                        Whether to use a color profile or device independent color.

  -pv {1,2,3}, --pdfaVersion {1,2,3}
                        PDF/A version (1, 2, or 3). Default is 1.

  -v {True,False}, --validate {True,False}
                        Validate the PDF/A file after conversion.  Default is False.                 
```

## Examples
Convert a PDF to PDF/A-1B using a color profile, PDF/A version 1, and validate the output:
```bash
python pdf2pdfa.py -i input.pdf -o output.pdf -t profile -pv 1 -v True
```

Convert a PDF to PDF/A-2B using a color profile, PDF/A version 2, and validate the output:
```bash
python pdf2pdfa.py -i input.pdf -o output.pdf -t profile -pv 2 -v True
```

Convert a PDF to PDF/A-3B using a device independent color, PDF/A version 3, and not validate the output:
```bash
python pdf2pdfa.py -i input.pdf -o output.pdf -t independent -pv 3 -v False
```

## Credits

This project was inspired by and references:
- [pdf2archive](https://github.com/matteosecli/pdf2archive) by matteosecli - A simple Ghostscript-based PDF/A-1B converter as Shell-Script.


## Licensing

- This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details. 
- Ghostscript is licensed under the GNU Affero General Public License - see the [Ghostscript License](https://artifex.com/licensing/gnu-agpl-v3) for details. Both `PDFA_def.ps` and `srgb.icc` are used from Ghostscript.
- VeraPDF is open source software dual licensed under MPL v2+ and GPL v3+ - see the [VeraPDF License](https://verapdf.org/home/) for details.