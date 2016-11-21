import gspread
import os

from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet:
    def __init__(self,url):
        self.url = url
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ["JSON_KEYFILE"], self.scope)
        
    
    def update(self):
        gc = gspread.authorize(self.credentials)
        self.sheet = gc.open_by_url(self.url)
        worksheet = self.sheet.worksheet("Top TablePeriod")
        self.players = [player for player in worksheet.col_values(3) if player != '']
        ranking = [contender for contender in self.players]
        self.ranking = ["{0}.{1}".format(rank+1,contender) for rank,contender in enumerate(ranking)]
    
    def get_ranking(self):
        return "\n".join(self.ranking)
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass