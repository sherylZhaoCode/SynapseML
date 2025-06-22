#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Splits long pages in a PDF into multiple letter-sized pages.
"""

import argparse
import math
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

# Standard US Letter size in points (1 inch = 72 points)
LETTER_WIDTH = 612  # 8.5 inches
LETTER_HEIGHT = 792  # 11 inches

def split_pdf_pages(input_pdf_path: str, output_pdf_path: str):
    """
    Reads a PDF, splits its long pages, and saves to a new PDF.

    Each page in the input PDF is checked. If its height exceeds
    standard letter height, it's split into multiple pages of
    letter height (or shorter for the last segment). The width of
    the output subpages will be the original page's width.
    """
    try:
        reader = PdfReader(input_pdf_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_pdf_path}'")
        return
    except Exception as e:
        print(f"Error reading PDF '{input_pdf_path}': {e}")
        return

    writer = PdfWriter()

    print(f"Processing '{input_pdf_path}'...")
    for page_num, original_page in enumerate(reader.pages):
        print(f"  Processing Page {page_num + 1}/{len(reader.pages)}...")
        try:
            original_mediabox = original_page.mediabox
            original_width = float(original_mediabox.width)
            original_height = float(original_mediabox.height)

            if original_height <= LETTER_HEIGHT:
                # Page is not longer than letter height, add as is
                writer.add_page(original_page)
                print(f"    Page {page_num + 1} is not long, adding as is.")
                continue

            num_subpages = math.ceil(original_height / LETTER_HEIGHT)
            print(f"    Page {page_num + 1} is long ({original_height:.2f} pts). Splitting into {num_subpages} subpages.")

            for i in range(num_subpages):
                # Calculate the coordinates of the slice on the original page
                # The PDF coordinate system has (0,0) at the bottom-left

                # Top of the current slice on the original page
                slice_y_top_on_original = original_height - (i * LETTER_HEIGHT)
                # Bottom of the current slice on the original page
                slice_y_bottom_on_original = original_height - ((i + 1) * LETTER_HEIGHT)
                slice_y_bottom_on_original = max(0, slice_y_bottom_on_original)

                # Effective height of this specific slice
                current_slice_height = slice_y_top_on_original - slice_y_bottom_on_original

                if current_slice_height <= 0:
                    continue

                # Create a new blank page for the output.
                # Its height will be standard letter height, content will be clipped if slice is smaller.
                # Or, make it the actual slice height to avoid empty space at the bottom of the last page.
                # For printing, consistent letter height is better.
                output_subpage = writer.add_blank_page(width=original_width, height=LETTER_HEIGHT)

                # The transformation should map the bottom-left of the slice
                # to the bottom-left of the new page (0,0).
                # So, we need to translate the original page's content upwards by -slice_y_bottom_on_original.
                transform = Transformation().translate(tx=0, ty=-slice_y_bottom_on_original)

                # Merge the transformed original page content onto the new blank page.
                # The new blank page's mediabox acts as a viewport.
                output_subpage.merge_transformed_page(original_page, transform)
                print(f"      Created subpage {i+1}/{num_subpages} from original page {page_num+1}.")

        except Exception as e:
            print(f"Error processing page {page_num + 1}: {e}")
            # Add the original page if processing fails to not lose it
            writer.add_page(original_page)
            print(f"    Added original page {page_num + 1} due to error.")


    try:
        with open(output_pdf_path, "wb") as fp:
            writer.write(fp)
        print(f"\nSuccessfully created '{output_pdf_path}' with split pages.")
    except Exception as e:
        print(f"Error writing output PDF '{output_pdf_path}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Split long PDF pages into letter-sized pages.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_pdf", help="Path to save the output PDF file.")

    args = parser.parse_args()
    split_pdf_pages(args.input_pdf, args.output_pdf)

if __name__ == "__main__":
    main()
