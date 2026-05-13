from extraction import text_from_pdf
from google import genai
from pathlib import Path
import asyncio
import json
import os
import sys

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_chunks(text : str) -> list[str]:
    '''
    Split text into fix size 'chunks' to respect LLMs context window
    '''
    size = 200
    words = text.split()

    if len(text) <= len(words): return [text]

    chunks = []
    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i + size])
        chunks.append(chunk)
    return chunks

async def process_chunk(chunk : str) -> dict:
    prompt = f'''
        Objective: extract the most relevant information from the text in JSON format. 
        No explanations, additional text or markdown format, the response have to be in the exact JSON format:
        {{
            "subjects" : [...],
            "key_data" : [...]
            "summary" : "...",
            "date" : "DD/MM/YY"
            "author" : "..."
        }} 
        In case of not enough information to complete a key, fill in "null".

        Text: {chunk}
        '''
    response = await client.models.generate_content(model='gemini-flash-lite-latest', contents=prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)

async def process_chunks(chunks: list[str]) -> dict:
    '''
    Get responses from the LLM for each chunk
    '''
    responses = [process_chunk(chunk) for chunk in chunks]
    return await asyncio.gather(**responses)

def write_responses(responses : list, output_path):
    '''
    Write out a JSON file with each response from the LLM
    '''
    output = []
    for i, response in enumerate(responses):
        output.append(dict(chunk=i+1, response=response))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':

    file_path = Path(sys.argv[1])
    output_path = f'./outputs/{file_path.stem}_summary.json'

    if file_path.suffix == '.pdf':
        text = text_from_pdf(file_path)
    elif file_path.suffix == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        print(f'File type not supported ({file_path.suffix})')
        sys.exit(1)

    chunks = get_chunks(text)
    print(f'Chunks Amount : {len(chunks)}')
    responses = asyncio.run(process_chunks(chunks))
    write_responses(responses, output_path)
    print(f'LLM Responses Saved')
