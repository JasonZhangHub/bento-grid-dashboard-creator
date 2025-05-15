import os
import argparse
import datetime
from google import genai
from google.genai import types
import os
import re
from dotenv import load_dotenv, find_dotenv
from prompts.prompt_v1 import MASTER_PROMPT


def load_environment_variables():
    """Loads environment variables from a .env file."""
    env_file_path = find_dotenv(raise_error_if_not_found=False, usecwd=True)
    if env_file_path:
        load_dotenv(env_file_path)
        print(f"Loaded environment variables from: {env_file_path}")
    else:
        print("No .env file found. Relying on system environment variables.")

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_model_id = os.getenv("GEMINI_MODEL_ID")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    if not gemini_model_id:
        raise ValueError("GEMINI_MODEL_ID not found in environment variables.")

    return gemini_api_key, gemini_model_id


def initialize_gemini_client(api_key: str) -> genai.Client:
    """Initializes and returns the Gemini API client."""
    try:
        client = genai.Client(api_key=api_key)
        print("Gemini API configured successfully.")
        return client
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        raise


def upload_file_to_gemini(file_path: str, client: genai.Client) -> types.File | None:
    """
    Uploads a file to Google's File API for use with Gemini.
    """
    if not os.path.exists(file_path):
        print(f"Error: Input file not found at {file_path}")
        return None
    try:
        print(f"Uploading file: {file_path}...")
        uploaded_file = client.files.upload(file=file_path)
        print(
            f"File uploaded successfully: {uploaded_file.name} (URI: {uploaded_file.uri})")
        return uploaded_file
    except Exception as e:
        print(f"Error uploading file '{file_path}': {e}")
        raise


def generate_content_from_file(
    client: genai.Client,
    model_id: str,
    uploaded_file: types.File,
    prompt_text: str,
    system_instruction: str = MASTER_PROMPT,
    temperature: float = 0.5
) -> str | None:
    """
    Generates content using the Gemini model based on an uploaded file and a prompt.
    """
    try:
        print(f"Generating content with model: {model_id}...")
        response = client.models.generate_content(
            model=model_id,
            contents=[uploaded_file,
                      prompt_text],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature
            )
        )

        print("Content generated successfully.")

        if hasattr(response, 'text'):
            return response.text
        else:
            print("Warning: Response did not contain text attribute.")

    except Exception as e:
        print(f"Error generating content: {e}")
        if hasattr(e, 'response'):
            print(f"API Error Response: {e.response}")
        raise


def extract_html_from_response(response_text):
    match = re.search(r"```html(.*?)```", response_text,
                      re.DOTALL | re.IGNORECASE)
    if match:
        html_page = match.group(1).strip()
        return html_page
    else:
        start_delimiter = "```html"
        end_delimiter = "```"
        start_index = response_text.find(start_delimiter)
        if start_index != -1:
            start_index += len(start_delimiter)
            end_index = response_text.find(end_delimiter, start_index)
            if end_index != -1:
                html_page = response_text[start_index:end_index]
                return html_page
    return None


def save_text_to_file(text_content: str, output_file_path: str):
    """Saves the given text content to the specified file path."""
    try:
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"Output successfully saved to: {output_file_path}")
    except IOError as e:
        print(f"Error saving output to file '{output_file_path}': {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Generate a bento-grid HTML announcement page from a PDF.")
    parser.add_argument("--pdf_file_path", type=str, required=True,
                        help="The full path to the input PDF file.")
    args = parser.parse_args()

    input_file_path = args.pdf_file_path

    # --- Validate PDF Path ---
    if not os.path.exists(input_file_path):
        print(f"Error: PDF file not found at '{input_file_path}'")
        return
    if not input_file_path.lower().endswith('.pdf'):
        print(f"Error: File '{input_file_path}' is not a PDF.")
        return

    print(f"Processing PDF: {input_file_path}")

    OUTPUT_FOLDER = 'output'
    if not os.path.exists(OUTPUT_FOLDER):
        try:
            os.makedirs(OUTPUT_FOLDER)
            print(f"Created output folder: {OUTPUT_FOLDER}")
        except Exception as e:
            print(f"Error creating output folder '{OUTPUT_FOLDER}': {e}")
            return

    try:
        # 1. Load Configuration
        gemini_api_key, gemini_model_id = load_environment_variables()

        # 2. Initialize Gemini (configure the library)
        client = initialize_gemini_client(api_key=gemini_api_key)

        # 3. Save the generated HTML
        base_filename = os.path.splitext(os.path.basename(input_file_path))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_html_filename = f"{base_filename}_{timestamp}.html"
        output_html_path = os.path.join(OUTPUT_FOLDER, output_html_filename)
        user_prompt = '''
        Create a bento-grid HTML page structure based on the key sections and information in this PDF.
        Focus on summarizing the main points for each section into a bento box.
        Ensure the HTML is self-contained and well-formatted.
        '''
        # 4. Upload PDF
        uploaded_pdf_file = upload_file_to_gemini(
            file_path=input_file_path, client=client)
        if not uploaded_pdf_file:
            print("Halting process due to file upload failure.")
            return

        # 5. Generate HTML content
        generated_html = generate_content_from_file(
            client=client,
            model_id=gemini_model_id,
            uploaded_file=uploaded_pdf_file,
            prompt_text=user_prompt,
            system_instruction=MASTER_PROMPT,
            temperature=0.5
        )

        # 6. Extract html from the response
        html_page = extract_html_from_response(generated_html)
        if not html_page:
            print("Halting process due to HTML extraction failure.")
            return

        # 7. Write HTML to file
        save_text_to_file(html_page, output_html_path)
        print(f"\nSuccessfully generated HTML announcement page!")
        print(f"Output saved to: {output_html_path}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
