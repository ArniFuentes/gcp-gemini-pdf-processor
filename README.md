# GCP Gemini PDF Processor

Automated pipeline that reads PDF files from a Google Drive folder, extracts data using the Gemini API, and writes the results to a Google Sheet.

## What it does

The Cloud Function iterates over all PDFs in a specified Google Drive folder, skipping any files already processed (tracked by filename in the first column of the sheet). For each new PDF, it sends the file to Gemini with a prompt that extracts compliance checklist data — specifically, it identifies items under "ASPECT TO BE CONTROLLED" and classifies each as Compliant (C), Non-Compliant (NC), or Not Applicable (NA). The results are appended as rows to the Google Sheet.

## Prerequisites

- Python 3.12+
- A GCP project with the following APIs enabled:
  - Google Sheets API
  - Google Drive API
- Gemini API (In this case, Google AI Studio was used to obtain the API key).

## Environment variables

Create a `.env` file for local development:

```
GEMINI_API_KEY=your_gemini_api_key
SPREADSHEET_ID=your_google_sheet_id
FOLDER_ID=your_google_drive_folder_id
```
For GCP deployment, create an `env.yaml` with the same keys:

```yaml
GEMINI_API_KEY: "your_gemini_api_key"
SPREADSHEET_ID: "your_google_sheet_id"
FOLDER_ID: "your_google_drive_folder_id"
```
Both files should be listed in `.gitignore` and `.gcloudignore`.

## Local development

Authentication uses a `credentials.json` Service Account key file. Place it in the project root — it is ignored by both Git and GCP deployment.

## Deployment

Deploy to GCP as a 2nd generation Cloud Function:

```powershell
gcloud functions deploy gcp-gemini-pdf-processor `
  --gen2 `
  --runtime python312 `
  --region your-region `
  --source . `
  --entry-point main `
  --trigger-http `
  --timeout 3600 `
  --env-vars-file env.yaml
```

## GCP permissions

The Cloud Function runs under the **Default Compute Service Account** (`<project-number>-compute@developer.gserviceaccount.com`). 
This account must be granted access on both the target Google Sheet (as editor) and the Google Drive folder (as viewer).
