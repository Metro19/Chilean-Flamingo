import pygsheets as pygsheets
from google.oauth2 import credentials
from src.config import SHEET_DOCUMENT_ID, COLUMN_CHARACTER

SCOPES = ['https://www.googleapis.com/auth/sheets']

COL_CHAR = COLUMN_CHARACTER

pygsheets_authorize = pygsheets.authorize()


def pull_column():
    # opens the sheet file with the provided key
    open_file = pygsheets_authorize.open_by_key(SHEET_DOCUMENT_ID)
    wks = open_file.sheet1

    # reading in the column of the sheet
    cell_num = 2
    cell_location = COL_CHAR + str(cell_num)
    cell_array = []
    for x in wks:
        if wks.cell(cell_location).value == "\n":
            pass
        else:
            cell_array.append(wks.cell(cell_location))
        cell_num += 1
        cell_location = COL_CHAR + str(cell_num)

    return cell_array
