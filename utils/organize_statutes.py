import json
import argparse
import os
import sys
import re
import heapq
from typing import List, Dict, Any

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Get the project root directory
sys.path.append(project_root)

# Patterns to detect title and sections
title_pattern = re.compile(r"^TITLE\s(\d+[A-Z]*)\s+(.+)$")

# Section pattern
section_pattern = re.compile(
    r"^(\d+[A-Z]*(?::[0-9A-Za-z]+)-[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)(?:\.)?\s+(.+)$"
)

# Paths for test defaults - using absolute paths
DEFAULT_INPUT = os.path.join(project_root, "data/raw/STATUTES_TEST.txt")
DEFAULT_OUTPUT = os.path.join(project_root, "data/processed/processed_nj_statutes_test.json")
LOG_FILE = os.path.join(project_root, "logs/encoding_issues.log")

def clean_line(line):
    """Detects and replaces problematic characters without logging them."""
    line = line.rstrip('\n')  # Remove trailing newlines
    cleaned_line = ""
    for char in line:
        try:
            char.encode("utf-8")  # Try encoding to UTF-8
            cleaned_line += char
        except UnicodeEncodeError:
            cleaned_line += "?"  # Replace with '?' or another placeholder
    return cleaned_line


def get_top_sections_by_word_count(parsed_data: List[Dict], n: int = 10) -> List[Dict]:
    """
    Finds the top n sections with the most words.
    
    Args:
        parsed_data: The parsed statute data
        n: Number of top sections to return
        
    Returns:
        List of dictionaries with section info and word count
    """
    all_sections = []
    
    for title in parsed_data:
        for section in title["sections"]:
            word_count = len(section["text"].split())
            all_sections.append({
                "title": title["title"],
                "section": section["section"],
                "heading": section["heading"],
                "word_count": word_count
            })
    
    # Get top n sections by word count
    top_sections = heapq.nlargest(n, all_sections, key=lambda x: x["word_count"])
    return top_sections


def parse_statutes(input_file, output_file):
    """Parses STATUTES.txt into structured JSON format, handling duplicate section numbers."""
    parsed_data = []
    current_title = None
    seen_sections = set()  # Track seen section numbers
    last_section = None  # Keep track of the last processed section
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(input_file, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            # Clean the line but preserve whitespace (don't strip)
            cleaned_line = clean_line(line)
            

            # Detect title
            title_match = title_pattern.match(line)
            if title_match:
                if current_title:
                    parsed_data.append(current_title)
                current_title = {
                    "title": f"TITLE {title_match.group(1)} - {title_match.group(2)}",
                    "sections": []
                }
                last_section = None  # Reset last processed section
                continue

            # Detect section
            section_match = section_pattern.match(line)
            if section_match:
                section_number = section_match.group(1)
                section_heading = section_match.group(2)

                # If section is a duplicate but appears consecutively, append text instead of skipping
                if section_number in seen_sections:
                    if last_section and last_section["section"] == section_number:
                        last_section["text"] += cleaned_line
                    continue

                # If the section is a citation, we need to check if it is a full citation

                seen_sections.add(section_number)
                last_section = {
                    "section": section_number,
                    "heading": section_heading,
                    "text": ""
                }
                current_title["sections"].append(last_section)
                continue

            if last_section:
                # Append text with proper spacing
                if last_section["text"]:
                    # Add a space instead of newline character
                    last_section["text"] += " " + cleaned_line
                else:
                    last_section["text"] = cleaned_line

    # Append the last title after processing all lines
    if current_title:
        parsed_data.append(current_title)

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4)

    return parsed_data

#Find the longest line in the file of words
def find_longest_line(input_file):
    with open(input_file, "r", encoding="utf-8", errors="replace") as f:
        longest_line = max(f, key=lambda x: len(x.split()))
        #length in words    
        return len(longest_line.split())


def main():
    parser = argparse.ArgumentParser(description="Process statutes into structured JSON.")
    parser.add_argument("--input_file", default=DEFAULT_INPUT, help="Path to the input file")
    parser.add_argument("--output_file", default=DEFAULT_OUTPUT, help="Path to the output file")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top sections to display")
    args = parser.parse_args()

    parsed_output = parse_statutes(args.input_file, args.output_file)
    print(f"Processed file saved to {args.output_file}")
    
    # Get and display top sections
    top_sections = get_top_sections_by_word_count(parsed_output, args.top_n)
    print(f"\nTop {args.top_n} sections with the most words:")
    for i, section in enumerate(top_sections, 1):
        print(f"{i}. {section['section']} - {section['heading']} ({section['word_count']} words)")
        print(f"   From: {section['title']}")


if __name__ == "__main__":
    main()
