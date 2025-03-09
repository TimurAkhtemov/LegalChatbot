import os
import sys
import json
import shutil
import tempfile

# Add the project root directory to Python path so that utils.process_statutes can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.process_statutes import parse_statutes

def main():
    # Define paths
    input_file = "data/raw/STATUTES_TEST.txt"
    output_file = "data/processed/processed_nj_statutes_test.json"
    
    # Run the parser function directly on the actual files
    parsed_data = parse_statutes(input_file, output_file)
    
    # Print confirmation message
    print(f"Processed JSON file written to: {output_file}")
    print(f"Number of titles processed: {len(parsed_data)}")
    print(f"Number of sections processed: {sum(len(title['sections']) for title in parsed_data)}")

if __name__ == "__main__":
    main()
