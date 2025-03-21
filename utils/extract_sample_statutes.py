import json
import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

input_file = "data/raw/STATUTES.txt"
output_file = "data/processed/STATUTES_SAMPLE.txt"

# Read the input file
# Extract 1000 lines every 25000 lines
# And write to the output file

with open(input_file, "r") as f:
    text = f.read()

# Split the text into chunks of 25000 lines
chunks = text.split("\n")

# Extract 1000 lines every 25000 lines
for i in range(0, len(chunks), 25000):
    with open(output_file, "a") as f:
        # Join the chunks with newlines before writing
        f.write("\n".join(chunks[i:i+1000]))
        f.write("\n")


#run with python extract_sample_statutes.py
