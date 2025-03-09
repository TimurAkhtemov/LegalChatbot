import json
import argparse
import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now import the regexes module
from regexes import title_pattern, section_pattern, amendment_pattern, split_pattern, base_pattern

# Paths for test defaults
DEFAULT_TEST_INPUT = "data/raw/STATUTES.txt"
DEFAULT_TEST_OUTPUT = "data/processed/processed_nj_statutes.json"
LOG_FILE = "logs/encoding_issues.log"


def clean_line(line):
    """Detects and replaces problematic characters while logging them."""
    cleaned_line = ""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        for char in line:
            try:
                char.encode("utf-8")  # Try encoding to UTF-8
                cleaned_line += char
            except UnicodeEncodeError:
                log.write(f"Non-UTF-8 character replaced: {repr(char)}\n")
                cleaned_line += "?"  # Replace with '?' or another placeholder
    return cleaned_line

def match_segment(text):
    text = text.strip()
    if base_pattern.fullmatch(text):
        return True # Base Citation Matched
    elif amendment_pattern.fullmatch(text):
        return True # Amendment/Repeal Matched
    else:
        return False # No Match

def match_full_citation_on_file(text):
    
    segments = split_pattern.split(text)

    # We also might want to strip empty or leftover whitespace
    segments = [seg.strip() for seg in segments if seg.strip()]
    
    # See if there is a match for each segment
    # We don't care if there are other parts of the text that don't match since the regex is designed to match citations per line
    
    for segment in segments:
        if match_segment(segment) == True: # If there is a match, continue to the next segment
            continue
        else: # If there is no match, return False
            return False
    
    return True

def parse_statutes(input_file, output_file):
    """Parses STATUTES.txt into structured JSON format, handling duplicate section numbers."""
    parsed_data = []
    current_title = None
    seen_sections = set()  # Track seen section numbers
    last_section = None  # Keep track of the last processed section
    
    with open(input_file, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = clean_line(line.strip())
            if not line:
                continue

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
                        last_section["text"] += (" " + section_heading)
                    continue

                seen_sections.add(section_number)
                last_section = {
                    "section": section_number,
                    "heading": section_heading,
                    "text": ""
                }
                current_title["sections"].append(last_section)
                continue

            # Check if line is a legislative history pattern before appending
            legislative_history_match = match_full_citation_on_file(line)
            if legislative_history_match == True:
                continue
            else:
                # Append law text (if inside a valid section)
                if last_section:
                    last_section["text"] += (" " + line if last_section["text"] else line)

    # Append the last title after processing all lines
    if current_title:
        parsed_data.append(current_title)


    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4)

    return parsed_data

def main():
    parser = argparse.ArgumentParser(description="Process statutes into structured JSON.")
    parser.add_argument("--input_file", default=DEFAULT_TEST_INPUT, help="Path to the input file")
    parser.add_argument("--output_file", default=DEFAULT_TEST_OUTPUT, help="Path to the output file")
    args = parser.parse_args()

    parsed_output = parse_statutes(args.input_file, args.output_file)
    print(f"Processed file saved to {args.output_file}")

if __name__ == "__main__":
    main()
