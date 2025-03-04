import json
import re

# Paths
test_input_file = "data/raw/STATUTES.txt"
test_output_file = "data/processed/processed_nj_statutes.json"
log_file = "logs/encoding_issues.log"

# Patterns to detect title and sections
title_pattern = re.compile(r"^TITLE\s(\d+[A-Z]*)\s+(.+)$")
section_pattern = re.compile(
    r"^(\d+[A-Z]*(?::[0-9A-Za-z]+)-[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)(?:\.)?\s+(.+)$"
)


def clean_line(line):
    """Detects and replaces problematic characters while logging them."""
    cleaned_line = ""
    with open(log_file, "a", encoding="utf-8") as log:
        for char in line:
            try:
                char.encode("utf-8")  # Try encoding to UTF-8
                cleaned_line += char
            except UnicodeEncodeError:
                log.write(f"Non-UTF-8 character replaced: {repr(char)}\n")
                cleaned_line += "?"  # Replace with '?' or another placeholder
    return cleaned_line

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

            # Append law text (if inside a valid section)
            if last_section:
                last_section["text"] += (" " + line if last_section["text"] else line)

    # **Filter out sections with empty text**
    for title in parsed_data:
        title["sections"] = [section for section in title["sections"] if section["text"].strip()]

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4)

    return parsed_data

# Run the updated parser on the test file
parsed_output = parse_statutes(test_input_file, test_output_file)

# Return the path of the generated JSON file
test_output_file