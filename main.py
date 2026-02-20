import functions_framework
from call_gemini_api import call_gemini_API
from get_model import get_model
from get_sheet import get_sheet
from config import API_KEY, SPREADSHEET_ID, FOLDER_ID, drive_service, creds


@functions_framework.http
def main(request=None):
    try:
        print("Starting...")

        sheet = get_sheet(creds, SPREADSHEET_ID, sheet_name='data')

        # list of dictionaries
        drive_pdfs = drive_service.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed = false").execute().get('files', [])

        model = get_model(API_KEY, model_name='gemini-3-flash-preview')

        prompt_text = '''Extract the following data: in the file, look where it says "ASPECT TO BE CONTROLLED". 
            Below are texts that always begin with a capital letter followed by a ".", for example "A.". 
            So I want the key to be just the uppercase letter, and the value is "C", "NC" or "NA", depending 
            if the checkbox is below "COMPLIANT", "NON-COMPLIANT" or "NOT APPLICABLE". 
            Respond with an array of JSON objects. Do not use Markdown.'''

        # get first column
        existing_docs = sheet.col_values(1)

        all_new_rows = []

        for pdf in drive_pdfs:
            if pdf['name'] in existing_docs:
                continue

            pdf_content = drive_service.files().get_media(
                fileId=pdf['id']).execute()

            extracted_data = call_gemini_API(model, prompt_text, pdf_content)

            rows = [[pdf['name'], list(row.keys())[0], list(row.values())[0]]
                    for row in extracted_data]

            all_new_rows.extend(rows)

        sheet.append_rows(all_new_rows)

        print(f"Added {len(all_new_rows)} rows.")

        return "Process completed", 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500
