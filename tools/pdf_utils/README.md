# PDF Page Splitter

A Python script to split oversized pages in a PDF document into multiple standard letter-sized pages. This is useful for printing PDFs that have very long pages, making them manageable for standard printers.

## Features

- Splits each vertically long page of an input PDF into several consecutive pages.
- Each new subpage aims for a standard US Letter height (11 inches / 792 points).
- The width of the subpages will be the same as the original page's width.
- Pages that are already shorter than or equal to letter height are kept as is.
- Command-line interface for specifying input and output PDF files.

## Requirements

The script uses the `pypdf` library. This will be installed if you use the main `requirements.txt` from the repository root.

To install dependencies if you haven't already:
```bash
pip install -r ../../requirements.txt
```
(Assuming you are running this from the `tools/pdf_utils` directory. Adjust path as needed or install from the repo root.)

Alternatively, to install just `pypdf`:
```bash
pip install pypdf
```

## Usage

Run the script from the command line, providing the input PDF path and the desired output PDF path.

```bash
python tools/pdf_utils/pdf_page_splitter.py <input_pdf_path> <output_pdf_path>
```

Or, if you are in the `tools/pdf_utils` directory:
```bash
./pdf_page_splitter.py <input_pdf_path> <output_pdf_path>
```
(Ensure the script is executable: `chmod +x pdf_page_splitter.py`)

### Example:

```bash
python tools/pdf_utils/pdf_page_splitter.py "my_long_document.pdf" "my_printable_document.pdf"
```

This will read `my_long_document.pdf`, process its pages, and save the result to `my_printable_document.pdf`.

## How it Works

1.  The script reads the input PDF page by page.
2.  For each page, it checks its height.
    *   If the height is less than or equal to US Letter height (792 points), the page is added to the output PDF without modification.
    *   If the page is taller, it's divided into vertical segments. Each segment is `LETTER_HEIGHT` tall, except possibly the last segment which might be shorter.
3.  For each segment, a new page is created in the output PDF. The content for this new page is taken from the corresponding segment of the original tall page.
4.  The output PDF will have the same page width as the original pages. If the original page width exceeds US Letter width (612 points / 8.5 inches), the output pages will also exceed this width; printer scaling might be necessary for such pages. The primary goal of this script is to handle excessive page *length*.

## Error Handling

- The script will print an error message if the input file is not found or cannot be read as a PDF.
- If an error occurs while processing a specific page, that page might be added to the output in its original form, and an error message will be printed.
- Errors during output file writing will also be reported.
