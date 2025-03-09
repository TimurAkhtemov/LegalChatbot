import re

# Patterns to detect title and sections
title_pattern = re.compile(r"^TITLE\s(\d+[A-Z]*)\s+(.+)$")

# Section pattern
section_pattern = re.compile(
    r"^(\d+[A-Z]*(?::[0-9A-Za-z]+)-[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)(?:\.)?\s+(.+)$"
)


# Legislative History Regexes
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
# split_pattern = re.compile(
#     # Explanation:
#     # 1) (?<![lL]\.)  = negative lookbehind; ensure we are NOT right after 'L.' (upper or lower)
#     # 2) (?<=[.;])    = positive lookbehind; we do want a '.' or ';' behind us
#     # 3) \s+          = match the whitespace
#     # 4) (?=(?:L\.|\d{4}\b|amended|repealed)) = next chunk must start with L., year, 'amended', or 'repealed'
#     r'(?<![lL]\.)(?<=[.;])\s+(?=(?:L\.|\d{4}\b|amended|repealed))',
#     flags=re.IGNORECASE
# )

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
