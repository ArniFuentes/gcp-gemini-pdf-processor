import gspread


def get_sheet(creds, book_id, sheet_name):
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(book_id).worksheet(sheet_name)
    return sheet
