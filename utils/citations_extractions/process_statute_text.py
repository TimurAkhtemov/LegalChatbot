import requests
import json

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "qwen2.5-coder-7b-instruct"
DRAFT_MODEL = "qwen2.5-coder-0.5b-instruct"

#Add logging of missed citations to a file
missed_citations = []

def log_missed_citation(citation, original_text, search_window):
    missed_citations.append({
        "citation": citation,
        "original_text": original_text,
        "search_window": search_window
    })
    with open('data/processed/missed_citations.json', 'w') as f:
        json.dump(missed_citations, f)

def generate_response(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a legal document cleaner. Return citations exactly as found or 'None'."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "top_k": 20,
        "max_tokens": 300,
        "draft_model": DRAFT_MODEL,
        "draft": True,
        "speculative_depth": 6,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "citations": {
                            "type": "string",
                            "description": "Extracted citations exactly as they appear, or 'None' if none found"
                        }
                    },
                    "required": ["citations"]
                }
            }
        }
    }

    response = requests.post(API_URL, json=payload)
    return response.json()

def extract_citations(text):
    prompt = f"""
Extract citations and legislative footnotes from the text matching the following patterns:
- "L.[year], c.[number], s.[number]"
- "(C.[number])"
- "eff. [month] [day], [year]"
- "Repealed by L.[year], c.[number], s.[number]"
- Combined amendments/repeals (e.g., "amended 1988, c.44, s.7; ...").
- Footnotes referencing prior cases or legislative actions.
- **Multiple citations in a single line** (e.g., "L.2010, c.55; amended by L.2020, c.10, eff. Nov. 1, 2021").
- **Nested amendments** (e.g., "amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2)").
- **Page number references** (e.g., "L.1960, c.187, p.780, s.4").

### **Instructions**:
- Return citations **EXACTLY** as they appear in the text.  
- Maintain original capitalization, spacing, and punctuation.  
- If none are found, return `"None"`.  
- Do **NOT** modify or format the citations.  
- Include all amendments and effective dates if present.  

### **Example 1**  
Text:  
  Findings, declarations relative to remediation of contaminated sites…  
  L.1997,c.278,s.2.  

Output:  
  L.1997,c.278,s.2  

### **Example 2**  
Text:  
  …establish a surplus…  
  Amended by L.1983, c. 111, s.1, eff. March 16, 1983.  

Output:  
  Amended by L.1983, c.111, s.1, eff. March 16, 1983.  

### **Example 3**  
Text:  
  L.1960, c.187, p.780, s.4  
Output:  
  L.1960, c.187, p.780, s.4  

### **Example 4**  
Text:  
  This is a test with legal words and information. L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2)  
Output:  
  L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2)  

### **Example 5**
Text:
  This section tests complex citation formats. L.1967, c.124, s.6, eff. June 21, 1967. Amended by L.1983, c.562, s.2, eff. Jan. 17, 1984.
Output:
  L.1967, c.124, s.6, eff. June 21, 1967. Amended by L.1983, c.562, s.2, eff. Jan. 17, 1984.
  
### **Example 6**
Text:
  that put others in danger unless otherwise stated. L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2); 1996, c.15, s.1; 1996, c.59, s.1; 1997, c.152, s.3 (repealed 2005, c.292, s.9.) 1997, c.152, s.5; 2005, c.292, s.1; 2009, c.1, s.1; 2011, c.107, s.1; 2015, c.67.
Output:
  L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2); 1996, c.15, s.1; 1996, c.59, s.1; 1997, c.152, s.3 (repealed 2005, c.292, s.9.) 1997, c.152, s.5; 2005, c.292, s.1; 2009, c.1, s.1; 2011, c.107, s.1; 2015, c.67.

### **Example 7**
Text:
  sign and prosecute the application.       Amended by L.1948, c. 329, p. 1312, s. 1;  L.1953, c. 4, p. 24, s. 4, eff. March 19, 1953. 

Output:
  Amended by L.1948, c. 329, p. 1312, s. 1;  L.1953, c. 4, p. 24, s. 4, eff. March 19, 1953.

---

### **Text:**
{text}
"""

    response = generate_response(prompt)

    if "choices" in response and response["choices"]:
        try:
            content = response["choices"][0]["message"]["content"]
            # Parse the JSON response to extract the citations field
            parsed_content = json.loads(content)
            return parsed_content["citations"].strip()
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Could not parse response content: {e}")
    else:
        raise ValueError(f"Unexpected response format: {response}")
    
def remove_citation(original_text, extracted_citation, buffer=8):
    # Truncate last N characters + buffer as a search window
    search_window = original_text[-(len(extracted_citation) + buffer):]

    # Remove whitespace in both the citation and search window
    stripped_citation = extracted_citation.replace(" ", "")
    
    # Replace original text with the search window with whitespace removed  
    original_text_whitespace_removed = original_text[:-(len(extracted_citation) + buffer)] + search_window.replace(" ", "")

    # Check if the citation is in the original text
    # If it is, remove the citation from original text
    if stripped_citation in original_text_whitespace_removed:
        
        #remove the citation from the original text
        original_text_whitespace_removed = original_text_whitespace_removed.replace(stripped_citation, "")
        
        #return the cleaned text and a similarity score of 100
        return original_text_whitespace_removed
        
    else:
        print("❌ Match not found in original string despite normalization")
        log_missed_citation(extracted_citation, original_text, search_window)
        print(f"Search window: {search_window}")
        return original_text


'''
Output file format: Json

[
    {
        "id": "1:1-1" (section numer)
        "title": <TITLE>,
        "section_id": <section number and heading>,
        "text": <text without citations>,
        "citations": <citations found in the text or "None">
    },
    ...
]

'''

def process_statute_citations(file):
    processed_file = []
    for title in file:
        for section in title['sections']:
            text = section['text']
            truncated_text = text[-300:]
            
            print("="*25)
            print(f"Original text: {section['section']}")
            print(truncated_text+"\n")
            print("Citations:")
            try:
                citations = extract_citations(truncated_text)
                print(citations + "\n")
                
                text_removed_citations = remove_citation(text, citations) if citations != "None" else (text, "")
                print(f"Text removed citations: \n{text_removed_citations} \n")
                print("="*25)
                
            except Exception as e:
                print(f"Error: {e}")
            
            processed_file.append({
                "id": section['section'],
                "title": title['title'],
                "section_id": section['section'] + " " + section['heading'],
                "text": truncated_text,
                "citations": citations
            })
            
    # Write the processed text to a new file
    with open('data/processed/citations_removed_nj_statutes_sample.json', 'w') as f:
        json.dump(processed_file, f)


if __name__ == "__main__":
    with open('data/processed/processed_nj_statutes_sample.json', 'r') as f:
        file = json.load(f)
    
    process_statute_citations(file)

    
