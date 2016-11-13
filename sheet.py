import gspread
import os

from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ["JSON_KEYFILE"], scope)

gc = gspread.authorize(credentials)

SHEET = gc.open_by_url(os.environ["SHEET_URL"])