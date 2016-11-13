# OPTSbot
a telegram bot for keeping track of the official Objective Partners table soccer league

[Meet OPTSbot](https://web.telegram.org/#/im?p=@OPTSbot)

# Requirements:
Docker
docker-compose

# Instructions

1.Create a bot using the [botfather](https://web.telegram.org/#/im?p=@BotFather) and save the token in .env
2.Create Google Docs credentials using [these instructions](http://gspread.readthedocs.io/en/latest/oauth2.html) 
3.Put the json file in the root folder and use the .env file to specify the filename 
3.run "docker-compose up --build"

TOKEN=220436155:AAHs2Ufij-VGLunYm7d3qIl4D5pUZUHTEZ4
SHEET_URL=https://docs.google.com/spreadsheets/d/1Uva0pl_2VYjTfwL0M49siFczq-zTqYxFH2kD2L2sCt0/edit?ts=57dab508#gid=1140046172
JSON_KEYFILE=OPTSbot-2e4ebbb4d31b.json
