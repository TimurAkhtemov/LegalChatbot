# Project Progress

## 02/03/2025

### Notes

- Exploring ideas for project and what models to use and how to collect data for fine tuning
- Decided on Mistralai/Mistral-7B-Instruct (free to use and easy to fine tune as a beginner project)
- Need to decide on how my data is going to be structured 


## 02/04/2025

### Notes

- Data exploration and data structure selection
  - q&a format
  - Using general text documents
- Exploring possible datasets that already contain q&a formatted legal inquiries
- Potential manual extraction from legal sites q&a pages later
- Decided on https://huggingface.co/datasets/dzunggg/legal-qa-v1
  - Contains 3.74k rows of question and answer data 
  - Unverified as the datacard does not contain information about where this q&a comes from and accuracy
  - Potentially use rag to verify accuracy?

## 02/17/2025

### Notes

- When having a conversation with the chatbot have the bot, if referencing a document or a law, suggest that the user upload that specific law document for better context. As in the bot will mention a specific law in potentially one of its responses and may suggest something like "I can also analyze the law further if you would like, you can upload the [law x y z/bill etc.] document if you can find it and I may be able to break it down further (disclaimer maybe?)"  
...

## 02/26/2025

### Notes

- Ultimately decided to step away from fine tuning as it requires high up front computational cost and time. This will require a lot of trial and error as well as model finetuning and hyperparameter tuning which can take a substantial amount of time
- Emphasizing the release of a MVP by 03/14/2025 with core functionality in place
- Instead of fine tuning, opted for RAG with NJ legal statutes and using the model
  - Retriever: sentence-transformers/all-MiniLM-L6-v2 (fast, lightweight embeddings)
  - Generator: Mistral-7B via Hugging Face Inference API (cheap, efficient for legal Q&A)
- Downloaded 

## 02/27/2025

### Goals Today
- Verify regex is working correctly and properly extracts the headers and title pages
- Setup the vector database 
- Generate embeddings for the processed data 

### Notes
- Had issues with file processing, last section in title was being placed in next title
- Regex did not include appendix title section, adjust later
- In STATUTES.TXT some sections have their section # and header but then have their section number repeated causing duplicate section headers. i.e.

2A:52-1.     Action for change of name  
    2A:52-1.     Any person may institute an action in Superior Court, for authority to assume another name.  The complaint for a change of name shall be accompanied by a sworn affidavit stating the applicant's name, date of birth, social security number, whether or not the applicant has ever been convicted of a crime, and whether any criminal charges are pending against him and, if such convictions or pending charges exist, shall provide such details in connection therewith sufficient to readily identify the matter referred to. The sworn affidavit shall also recite that the action for a change of name is not being instituted for purposes of avoiding or obstructing criminal prosecution or for avoiding creditors or perpetrating a criminal or civil fraud. If criminal charges are pending, the applicant shall serve a copy of the complaint and affidavit upon any State or county prosecuting authority responsible for the prosecution of any pending charges. A person commits a crime of the fourth degree if he knowingly gives or causes to be given false information under this section.  


### Accomplished
- Verified regex is working properly
- Processed the STATUTES.TXT file to format the json into title, sections & text
- Problems still having was duplicate sections were getting skipped
- One section has a null text value, need to handle that

## 03/03/2025

### Goals Today
- Generate embeddings and insert into chromadb (first clear original embeddings)
  - Query a few sections to confirm proper indexing
- Implement chunking for longer sections (performance can be improved by breaking sections into smaller chunks)
- Test basic retrieval 
  - query = "What is the law regarding name changes in New Jersey?"
  - results = collection.query(query_texts=[query], n_results=3)
  - print(results)

### Notes
- Again had issues with preprocessing duplicate sections were still giving issues and handling empty sections
- resolved empty section and duplicate section numbers
- Utilized STATUTES_TEST.txt to test the preprocessing
- Still preprocessing - noticing spots of empty text and/or where the description of the sections describes they have been either: reallocated, repealed, ammended or both inclusive? 
  - Believe I should just remove these sections as they don't have any useful information
  - Might need to perform more deeper analyses because there seems to be revision notes in the sections themselve
- Certain parts of legal housekeeping text should be removed
Pattern Examples: 
1. L.1976, c. 47, s. 54A:9-19, eff. July 8, 1976, operative Aug. 30, 1976.
  - L.1976, c. 47, s. 54A:9-25.1, eff. July 8, 1976, operative Aug. 30, 1976. Amended by L.1980, c. 74, s. 16, eff. July 23, 1980.

### Accomplished
- More preprocessing in removing duplicates and consolidating sections
- Reassessed data preprocessing and need to remove more noise from dat

### 03/04/2025

### Goals Today
- More preprocessing steps
1. Figure out regex pattern to match legislative history foot notes at the ends of each section (L.1976, c. 47, s. 54A:9-25.1, eff. July 8, 1976, operative Aug. 30, 1976. Amended by L.1980, c. 74, s. 16, eff. July 23, 1980.)
2. Determine anymore patterns in the text that need to be removed

### Notes
- Realizing I need to do a lot more preprocessing as random legal metadata introduces noise that could affect performance of the vectordb
- Regex is annoying
- Should I just use 2 separate regex patterns?

### Accomplished
- Able to match majority of the legislative patterns with one regex 
  - However complexity of this regex is high, and still misses some test cases. Going to split into multiple to capture each pattern

### 03/05/2025

### Goals Today
- Create multiple regex instead of one giant one for legislative footnotes
- Successfully remove these footnotes from the data
- Discover anymore data patterns that need to be removed

### Notes
- Regex pattern to capture: L.1987, c.453, s.2; amended 1995,c.401, ss.45,17 (s.17 amended 1996, c.15, s.2); 1996, c.15, s.1; 1996, c.59, s.1; 1997, c.152, s.3 (repealed 2005, c.292, s.9.) 1997, c.152, s.5; 2005, c.292, s.1; 2009, c.1, s.1; 2011, c.107, s.1; 2015, c.67.' is overly complicated, doing manual bypass
- Otherwise regex pattern captures every other test case
- Now need to test on full statutes data 
- Log output and json outputting

### Accomplished
- Refined regex to match all but the mega citation test case

New pattern (Deleted by amendment, P.L.1991, c.91). d.   (Deleted by amendment, P.L.1991, c.91). e.   (Deleted by amendment, P.L.1991, c.91).


### 03/08/2025

### Still preprocessing for these damn footnotes
### Goals
Try to finish the getting rid of the legislative notes that never seemed to have a consistent pattern... 
Almost got them all now need a new regex for those not on their own line

Might just give up on such hardcore preprocessing, evaluating how valuable it could be for model performance and retrieval
Still need to potentially identify more useless legal patterns in the text

Need to explore other approaches than one brute force regular expression.

## 03/09/2025

- Upon considering using language models for processing came up with ideas of using zero shot/few shot classification with assistance from an LLM 
- Finally think I found a viable solution to have a model just clean each section/chunk for me instead of regexing the shit out of it
- Thanks and not thanks to chatgpt 
- Will use approach from https://www.youtube.com/watch?v=_R-ff4ZMLC8  10:52 - 21:00

### 03/10/2025

### Goals today
- No more using regular expressions. Work with what you got and move onto implementing cleaning and structuring with LLM
- Use a small model (4o mini, or something) to produce cleaned chunks of text with menaingful legal information for the user
- Test on subset of data (STATUTES_SAMPLE, or STATUTES_TEST) 

### Notes
- There are numerous references to other laws and documents, potential for agentic rag to search deep within references to extract even more information?


## 03/14/2025

### Goals Today
- Preprocessing process:
  1. First organize text into json format with title, section, and text (already handled by organize_statutes.py)
  2. Next with llm, remove citations, footnotes and irrelevant information to general public. And pass full text contents through LLM to determine if there is valuable legal information within the text. Irrelevant information will be that of legislative information only for legal housekeeping i.e.:
  54:8A-123.  Effective date;  time of application
    This act shall take effect immediately and shall be applicable to income received or accrued subject to taxation by virtue of P.L.1976, c. 66.

     L.1976, c. 126, s. 2, eff. Dec. 20, 1976.
     which is useless information to general public. 
     Then:
    - Assign labels to each section 1: valid (valid legal text), 2: invalid (not useful for general public), 3: review (review the text)
    - **This will assist in further preprocsessing the data to clean it

  {
"id": <section number without appendix since we are not dividing the chunks for now>
"title": <TITLE # - title heading>
"section_id": <section number with the name>
"text": <with footnotes/citations removed>
"classification": <valid, invalid (if invalid, we just remove/not include), review>
}

    - Instances where text size is too long for the context window or >500 tokens we run through a chunking function to do a simple chunking (not chunked yet for vector db which we will use a more advanced system). Likely will split on paragraphs or bullet points or some other split without middle of word or sentence cutoff.
    - For each of these smaller chunks we decide whether or not we should keep them in the rest of the text. If valid include, if not valid remove, and no review
    - Then concatenate them back together into the full text and since we already classified the simple chunks we can move onto the next section.

  3. Chunking. Now we need to chunk the data according to semantic meaning and logically what pieces of text within token lengths longer than a certain amount or a varying length without cutting meaning.
    - Agentic chunking from: https://mer.vin/2024/03/chunking-strategy/ 


## 03/18/2025
### Goals Today
- select a model that will accuratley remove citations
- Test the model on some sample data, (lm studio)
- Get a sample run on the test and sample data set

### Notes
- qwen 2.5 32b coding instruct seems to handle recognizing these exact citation patterns very effectively
- Changed desired output from being the entire text with citations removed to just the citations themselves to reduce token output
  - Instead of having the model remove all of the citations and having to reprint the entire text, have model print the citations and then programatically remove them with .replace()
  - Can much more easily retain the citations in the json if decided to keep for more advanced rag in the future. 
- New strategy of only submitting in the last 200-250 tokens of the text for the model to read the text and extract citations
  - improves model performance and accuracy
  - Use speculative decoding for even faster inference
- Sometimes the model outputs white spaces in between the extracted citations which can cause issues with matching

### Accomplished
- Optimized performance of model choice qwen 2.5 7B with reducing token input and using smaller models with speculative decoding with qwen 2.5 3b
- Seems to handle test cases very accuratley
- Accomplished further optimzation with using qwen 2.5 7B with qwen 2.5 0.5B draft
- From testing, we can fully extract the citations from the model, remove the white spaces and then remove from original text
  More specifically
    1. Model extracts citaions and provides them as output
    2. Remove any white spaces from original text from the end to the length of extracted citation original_text[-(len(extracted_citation))] + small buffer to account for any potential missed part of the citation if the model output is in fact shorter than the original
    3. Remove any white spaces from extracted citation
    4. Match and remove from original text and return

- Just discovered eyecite an open source library "for extracting legal citations from text. It is used, among other things, to process millions of legal documents in the collections of CourtListener and Harvard's Caselaw Access Project, and has been developed in collaboration with both projects." 
  - **not useful for this case


## 03/20/2025
### Notes
- Had trouble with structured output not returning None and hallucinating output citations
- Tried removing structured output json resulted in model gibberish
- Spent substanital amount of time understanding why this was happening
  - Reverted a lot of previous changes, will include back the tests.
- Optimal approach using /v1/chat/completions endpoint with structured output gave consistent results

- Opted for 7B with 0.5B speculative decoding - much faster inference but looking for faster optimizations

## 04/15/2025
### Notes

- Moving past citation extraction for now. Too big of a headache, building mvp
- Indexed the statutes into chroma db and queried with gemini
- Responses seem valid so far


