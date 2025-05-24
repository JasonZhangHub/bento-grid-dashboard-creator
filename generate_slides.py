import os
import argparse
import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv, find_dotenv
from prompts.prompt_v4 import REASONING_PROMPT, SLIDE_PROMPT
import re

def load_environment_variables():
    env_file_path = find_dotenv(raise_error_if_not_found=False, usecwd=True)
    if env_file_path:
        load_dotenv(env_file_path)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_model_id = os.getenv("GEMINI_MODEL_ID")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    if not gemini_model_id:
        raise ValueError("GEMINI_MODEL_ID not found in environment variables.")
    return gemini_api_key, gemini_model_id

def initialize_gemini_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)

def upload_file_to_gemini(file_path: str, client: genai.Client) -> types.File:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found at {file_path}")
    return client.files.upload(file=file_path)

def generate_content(client, model_id, uploaded_file, prompt_text, system_instruction, temperature=0.5):
    response = client.models.generate_content(
        model=model_id,
        contents=[uploaded_file, prompt_text],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature
        )
    )
    if hasattr(response, 'text'):
        return response.text
    return None

def extract_sections_from_response(response_text):
    # Expecting a list of sections with titles and summaries
    # Example: 1. Introduction: ...\n2. Key Trends: ...
    sections = []
    for match in re.finditer(r"\d+\.\s*(.+?):\s*(.+)", response_text):
        title, summary = match.group(1).strip(), match.group(2).strip()
        sections.append({"title": title, "summary": summary})
    return sections

def sanitize_filename(title: str) -> str:
    # Remove problematic characters and excessive length
    sanitized = re.sub(r'[^\w\- ]', '', title)  # Keep alphanumeric, dash, underscore, space
    sanitized = sanitized.replace(' ', '_')
    sanitized = sanitized.strip('_')
    return sanitized[:60]  # Limit length

def extract_html_from_response(response_text):
    # Try to extract from ```html ... ```
    match = re.search(r"```html(.*?)```", response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: try to extract first <html>...</html> block
    match = re.search(r"<html[\s\S]*?</html>", response_text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    # Log the first 500 chars for debugging
    print("[WARN] Could not extract HTML. Raw response (truncated):", response_text[:500])
    return None

def save_text_to_file(text_content: str, output_file_path: str):
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text_content)

def main():
    parser = argparse.ArgumentParser(description="Generate 16:9 HTML slides from a PDF document.")
    parser.add_argument("--pdf_file_path", type=str, required=True, help="The full path to the input PDF file.")
    args = parser.parse_args()
    input_file_path = args.pdf_file_path
    if not os.path.exists(input_file_path):
        print(f"Error: PDF file not found at '{input_file_path}'")
        return
    if not input_file_path.lower().endswith('.pdf'):
        print(f"Error: File '{input_file_path}' is not a PDF.")
        return
    OUTPUT_FOLDER = 'output'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    gemini_api_key, gemini_model_id = load_environment_variables()
    client = initialize_gemini_client(api_key=gemini_api_key)
    uploaded_pdf_file = upload_file_to_gemini(file_path=input_file_path, client=client)
    # Step 1: Reasoning and section breakdown
    print("Analyzing document and extracting key sections...")
    reasoning_response = generate_content(
        client=client,
        model_id=gemini_model_id,
        uploaded_file=uploaded_pdf_file,
        prompt_text="Summarize and break down this document into 3-5 key sections for a slide presentation.",
        system_instruction=REASONING_PROMPT,
        temperature=0.3
    )
    sections = extract_sections_from_response(reasoning_response)
    if not sections:
        print("Failed to extract sections from the document.")
        return
    print(f"Found {len(sections)} sections. Generating slides...")
    # Step 2: Generate a slide for each section
    for idx, section in enumerate(sections, 1):
        # The slide prompt now encourages flexible layouts and KPI highlighting (see prompt_v4.py)
        slide_prompt = f"""
        Create a 16:9 HTML presentation slide for the following section.\nSection Title: {section['title']}\nSection Summary: {section['summary']}\nGenerate 3-6 key bullet points for this section based on the document.\nIf there are any key metrics, numbers, or comparisons, highlight them in a visually engaging KPI chart or card as described in the prompt. Use a flexible layout that best fits the content.\n"""
        slide_response = generate_content(
            client=client,
            model_id=gemini_model_id,
            uploaded_file=uploaded_pdf_file,
            prompt_text=slide_prompt,
            system_instruction=SLIDE_PROMPT,
            temperature=0.4
        )
        html_slide = extract_html_from_response(slide_response)
        if not html_slide:
            print(f"Failed to generate slide for section: {section['title']}")
            print(f"[DEBUG] Model response (truncated): {slide_response[:500] if slide_response else 'None'}")
            continue
        safe_title = sanitize_filename(section['title'])
        slide_filename = f"slide_{idx:02d}_{safe_title}.html"
        output_path = os.path.join(OUTPUT_FOLDER, slide_filename)
        save_text_to_file(html_slide, output_path)
        print(f"Saved slide: {output_path}")
    print("All slides generated.")

if __name__ == '__main__':
    main() 