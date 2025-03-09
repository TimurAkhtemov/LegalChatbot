import re

# ---- Updated Base Pattern ----
base_pattern = re.compile(r"""
    ^\s*
    (?:L\.\s*)?                         # Make the "L." optional
    (?P<year>\d{4})
    (?:\s*\((?P<ss>\d+(?:st|nd|rd|th)?\s*SS)\))?
    ,\s*c\.\s*(?P<chapter>\d+)
    # Allow any number of s.# or p.# in any order:
    (?:
        ,\s*(?:
            # Changed here: from (?P<section>\d+) to (?P<section>[0-9:\-]+)
            (?:s|ss)\.\s*(?P<section>[0-9:\-]+)
          | p\.?\s*(?P<page>\d+)
        )
    )*
    # Possibly an effective date:
    (?:
        ,\s*eff\.?\s*(?P<month>[A-Za-z]+\.?)\s*(?P<day>\d+),\s*(?P<eff_year>\d{4})
    )?
    \s*[\.;]?\s*$
""", re.VERBOSE | re.IGNORECASE)


# ---- Updated Amendment Pattern ----
amendment_pattern = re.compile(r"""
    ^\s*
    (?P<keyword>amended(?:\s+by)?|repealed)
    \s+
    (?:L\.\s*)?                         # "L." optional
    (?P<amend_year>\d{4})
    ,\s*c\.\s*(?P<amend_chapter>\d+)
    # Again, allow multiple "s.#" or "p.#" parts in any order:
    (?:
        ,\s*(?:
            # Changed here: from (?P<amend_section>\d+) to (?P<amend_section>[0-9:\-]+)
            (?:s|ss)\.\s*(?P<amend_section>[0-9:\-]+)
          | p\.?\s*(?P<amend_page>\d+)
        )
    )*
    # Possibly an effective date
    (?:
        ,\s*eff\.?\s*(?P<amend_month>[A-Za-z]+\.?)\s*(?P<amend_day>\d+),\s*(?P<amend_eff_year>\d{4})
    )?
    \s*[\.;]?\s*$
""", re.VERBOSE | re.IGNORECASE)


# -- More flexible splitting, allowing a segment to begin with "L.", a 4-digit year, "amended", or "repealed" --
    # Explanation:
    # 1) (?<![lL]\.)  = negative lookbehind; ensure we are NOT right after 'L.' (upper or lower)
    # 2) (?<=[.;])    = positive lookbehind; we do want a '.' or ';' behind us
    # 3) \s+          = match the whitespace
    # 4) (?=(?:L\.|\d{4}\b|amended|repealed)) = next chunk must start with L., year, 'amended', or 'repealed'
split_pattern = re.compile(
    # Negative lookbehind: make sure the '.' or ';' is NOT preceded by:
    #   L.
    #   c.
    #   p.
    #   s.
    # (in upper or lower case)
    # The \b ensures we only exclude them if they're separate tokens like L., c., etc.
    r'(?<!\b[lLcCsSpP]\.)(?<=[.;])\s+(?=(?:L\.|\d{4}\b|amended|repealed))',
    flags=re.IGNORECASE
)



# -- Function to see if a single segment matches either pattern --
def match_segment(text):
    text = text.strip()
    if base_pattern.fullmatch(text):
        return "Base Citation Matched"
    elif amendment_pattern.fullmatch(text):
        return "Amendment/Repeal Matched"
    else:
        return "No Match"


def match_full_citation(text):
    segments = split_pattern.split(text)
    print("\nDEBUG SPLIT:", segments)  # <-- Add this to see exactly how it's splitting!
    
    segments = [seg.strip() for seg in segments if seg.strip()]
    results = [match_segment(seg) for seg in segments]

    overall = "Composite Citation Matched" if all(r != "No Match" for r in results) else "No Match"
    return overall, results



def match_full_citation_on_file(text):
    
    segments = split_pattern.split(text)
    
    # We also might want to strip empty or leftover whitespace
    segments = [seg.strip() for seg in segments if seg.strip()]
    
    # See if there is a match for each segment
    # We don't care if there are other parts of the text that don't match since the regex is designed to match citations per line
    
    results = []
    for segment in segments:
        if match_segment(segment) != "No Match":
            results.append(segment)
    
    return results
    
# Function to run tests on full composite citations:
def run_tests(test_list, expected):
    for test in test_list:
        overall, results = match_full_citation(test)
        print(f"{test!r:140s} --> Expected: {expected}, Got: {overall}, Segment Results: {results}")

def run_tests_on_test_file():
    with open("data/raw/STATUTES_TEST.txt", "r", encoding="utf-8") as f:
        # Read the file line by line instead of the whole file at once
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                results = match_full_citation_on_file(line)
                if results:
                    print(f"{line!r:140s} --> Results: {results}")
                else:
                    print(f"{line!r:140s} --> No Results: {line}")
                

# ---------------------------
# Test cases that should evaluate to True:
true_cases = [
    "L.1951 (1st SS), c.344.",  
    "L.1951 (1st SS), c.344; amended by L.1982, c. 77, s. 31, eff. Dec. 31, 1983.",
    "L.2000, c.5.",
    "L.1995, c.40; amended by L.2010, c.15, eff. Jan. 1, 2012.",
    "L.2015, c.99, s. 10.",
    "L.1960 (1st SS), c.50, s.3.",
    "L.1988, c.22; amended by L.2005, c.10, s.5, eff. July 1, 2006.",
    "L.1970, c.5, s.7; amended by L.1985, c.12, eff. Mar. 15, 1986.",
    "L.2010, c.55; amended by L.2020, c.10, eff. Nov. 1, 2021.",
    "L.2022, c.1.",
    "L.1900 (1st SS), c.400, s.2.",
    "L.1955, c.300; amended by L.1965, c.100, s.2, eff. Oct. 15, 1966.",
    "L.1985 (1st SS), c.77, s.5; amended by L.1990, c.10, eff. May 1, 1991.",
    "L.2020, c.45.",
    "L.2030, c.12, s.8.",
    "L.2040 (2nd SS), c.77.",
    "L.2050, c.100; amended by L.2060, c.50, eff. Feb. 20, 2070.",
    "L.2070, c.33, s.4; amended by L.2080, c.44, s.2, eff. March 15, 2090.",
    "L.2090, c.66, s.9; amended by L.2100, c.77, eff. Apr. 1, 2110.",
    "L.1967, c.124, s.6, eff. June 21, 1967.  Amended by L.1983, c.562, s.2, eff. Jan. 17, 1984.",
    "L.1967,c.124,s.7; amended 1995,c.217,s.3.",
    "L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2); 1996, c.15, s.1; 1996, c.59, s.1; 1997, c.152, s.3 (repealed 2005, c.292, s.9.) 1997, c.152, s.5; 2005, c.292, s.1; 2009, c.1, s.1; 2011, c.107, s.1; 2015, c.67.",
    "Amended by L.1960, c.187, p.780, s.4.",
    "amended 1988, c.44, s.7; 2005, c.343; 2008, c.84, s.2; repealed 2019, c.276, s.20; amended 2021, c.16, s.62.",
    "L.1972, c. 45, s. 59:6-4.",
    "L.1958, c. 143, p. 647, s. 1.",
    "L.1958, c.143, s.3",
    "L.1958, c.143, s.3; amended by L.1961, c. 144, p. 820, s. 2, eff.  July 1, 1962; L.1969, c. 169, s. 3; L.1971, c. 139, s. 4, eff. May 12, 1971;  L.1977, c. 306, s. 2, eff. Dec. 27, 1977. ",
    "L.1958, c. 143, p. 647, s. 1.  Amended by L.1969, c. 169, s. 1;  L.1971, c. 139, s. 2, eff. May 12, 1971;  L.1975, c. 375, s. 1, eff. March 3, 1976; L.1977, c. 306, s. 1, eff. Dec. 27, 1977.",
    "L.1973, c. 249, s. 2, eff. Nov. 26, 1973.",
    "L.1967, c.124, s.6, eff. June 21, 1967.  Amended by L.1983, c.562, s.2, eff. Jan. 17, 1984.",
    "L. 1971, c. 197, s. 1, eff. July 1, 1971.  Amended by L. 1975, c. 306, s. 1, eff. March 3, 1976; L. 1986, c. 173, s. 2, eff. Dec. 8, 1986.",
    "L.1948, c. 375, p. 1544, s. 2.",
    "L.1948, c. 199, p. 998, s. 10.",
    "Amended by L.1948, c. 329, p. 1314, s. 6; L.1953, c. 4, p. 25, s. 9."
    
]

print("=== True Cases ===")
run_tests(true_cases, "Composite Citation Matched")

#run_tests_on_test_file()