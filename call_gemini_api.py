from tenacity import retry, stop_after_attempt, wait_fixed
import json


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def call_gemini_API(model, prompt, pdf_content):
    response = model.generate_content(
        [prompt, {'mime_type': 'application/pdf', 'data': pdf_content}])
    return json.loads(response.text.replace('```json', '').replace('```', ''))
