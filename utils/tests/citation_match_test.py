def remove_citation(original_text, extracted_citation, buffer=2):
    # Truncate last N characters + buffer as a search window
    search_window = original_text[-(len(extracted_citation) + buffer):]

    # Remove whitespace in both the citation and search window
    stripped_citation = extracted_citation.replace(" ", "")
    
    # Replace original text with the search window with whitespace removed  
    original_text_whitespace_removed = original_text[:-(len(extracted_citation) + buffer)] + search_window.replace(" ", "")

    # Check if the citation is in the original text
    # If it is, remove the citation from original text
    if stripped_citation in original_text_whitespace_removed:
        print("✅ Direct match found after whitespace normalization")
        
        #remove the citation from the original text
        original_text_whitespace_removed = original_text_whitespace_removed.replace(stripped_citation, "")
        
        #return the cleaned text and a similarity score of 100
        return original_text_whitespace_removed, 100   
        
    else:
        print("❌ Match not found in original string despite normalization")
        return original_text, 0


# Batch Testing
def run_tests(test_cases):
    success_count = 0
    for i, test in enumerate(test_cases):
        print(f"\n=== Test Case {i + 1} ===")
        print(f"Original: {test['original_text'].strip()}")
        print(f"Extracted: {test['extracted_citation']}")

        cleaned_text, similarity = remove_citation(
            test['original_text'],
            test['extracted_citation']
        )

        if similarity == 100 and cleaned_text != test['original_text']:
            success_count += 1
            print(f"✅ Result: SUCCESS")
        else:
            print(f"❌ Result: FAILURE")

        print(f"Cleaned Text: {cleaned_text.strip()}\n{'-'*50}")

    total_tests = len(test_cases)
    success_rate = (success_count / total_tests) * 100
    print(f"\n✅ SUCCESS RATE: {success_rate:.2f}% ({success_count}/{total_tests})")

# Test Cases
test_cases = [
    {
        "original_text": "This section tests comma format variations. L.1967,c.124,s.7; amended 1995,c.217,s.3.\n\n",
        "extracted_citation": "L.1967, c.124, s.7; amended 1995, c.217, s.3."
    },
    {
        "original_text": "The Legislature finds that it is in the public interest to establish a process... L.1987, c.453, s.2; amended 1995, c.401, ss.45, 17.\n",
        "extracted_citation": "L.1987, c.453, s.2; amended 1995, c.401, ss.45, 17."
    },
    {
        "original_text": "Effective immediately. L.2022, c.101, s.5; repealed by L.2023, c.12, s.3.\n",
        "extracted_citation": "L.2022, c.101, s.5; repealed by L.2023, c.12, s.3."
    },
    {
        "original_text": "This is a complex example. L.1997,c.278,s.2; amended 1999,c.34,s.7; repealed 2019,c.276,s.20.\n",
        "extracted_citation": "L.1997, c.278, s.2; amended 1999, c.34, s.7; repealed 2019, c.276, s.20."
    },
    {
        "original_text": "This section refers to several amendments. Amended 1988, c.44, s.7; 2005, c.343; repealed 2019, c.276, s.20.\n",
        "extracted_citation": "Amended 1988, c.44, s.7; 2005, c.343; repealed 2019, c.276, s.20."
    },
    {
        "original_text": "Nothing was amended in this section.\n",
        "extracted_citation": "L.2000, c.11, s.4"
    },
    
]

# Run tests
run_tests(test_cases)
