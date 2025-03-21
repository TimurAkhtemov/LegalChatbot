import requests
import json

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "qwen2.5-coder-7b-instruct"
DRAFT_MODEL = "qwen2.5-coder-0.5b-instruct"

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

def process_statute_text(text):
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
  L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2)  
Output:  
  L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2)  

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

if __name__ == "__main__":
    
    with open('data/processed/processed_nj_statutes_test.json', 'r') as f:
        file = json.load(f)

    for title in file:

        for section in title['sections']:
            text = section['text']
            truncated_text = text[-300:]
            
            print("="*25)
            print(f"Original text: {section['section']}")
            print(truncated_text+"\n")
            print("Citations:")
            try:
                print(process_statute_text(truncated_text) + "\n")
            except Exception as e:
                print(f"Error: {e}")
