import gspread
import os

from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet:
    def __init__(self,url):
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ["JSON_KEYFILE"], self.scope)
        gc = gspread.authorize(self.credentials)
        self.sheet = gc.open_by_url(url)

    
    def ranking(self):
        worksheet = self.sheet.worksheet("Top TablePeriod")
        ranking = [contender for contender in worksheet.col_values(3) if contender != '']
        ranking = ["{0}.{1}".format(rank+1,contender) for rank,contender in enumerate(ranking)]
        return "\n".join(ranking)
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass