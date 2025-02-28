import json
import re

# Paths
input_file = "data/raw/STATUTES.txt"
output_file = "data/processed/nj_statutes.json"
log_file = "logs/encoding_issues.log"

# Patterns to detect title and sections
title_pattern = re.compile(r"^TITLE\s(\d+[A-Z]*)\s+(.+)$")
section_pattern = re.compile(r"^(\d+[A-Z]*(?::[0-9A-Za-z]+)-[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*\.?)\s+(.+)$")

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

def parse_statutes():
    """Parses STATUTES.txt into structured JSON format, handling duplicate section numbers."""
    parsed_data = []
    current_title = None
    current_section = None
    last_seen_section = None  # Track the last seen section number

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
                    current_title["sections"].append(current_section)
                    current_section = None
                current_title = {
                    "title": f"TITLE {title_match.group(1)} - {title_match.group(2)}",
                    "sections": []
                }
                continue
            
            # Detect section
            section_match = section_pattern.match(line)
            if section_match:
                if current_section:
                    current_title["sections"].append(current_section)
                current_section = {
                    "section": section_match.group(1),
                    "heading": section_match.group(2),
                    "text": ""
                }
                continue
            
            # Append law text
            if current_section:
                current_section["text"] += (" " + line if current_section["text"] else line)
    
    # Append last section and title
    if current_section:
        current_title["sections"].append(current_section)
    if current_title:
        parsed_data.append(current_title)
    
    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4)

    print(f"Processed statutes saved to {output_file}")
    print(f"Non-UTF-8 characters logged in {log_file}")

if __name__ == "__main__":
    parse_statutes()


