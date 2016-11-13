# OPTSbot
A telegram bot for keeping track of the official Objective Partners table soccer league

[Meet OPTSbot](https://web.telegram.org/#/im?p=@OPTSbot)

# Requirements:
Docker

docker-compose

# Instructions

1.Create a bot using the [botfather](https://web.telegram.org/#/im?p=@BotFather) and save the token in .env

2.Create Google Docs credentials using [these instructions](http://gspread.readthedocs.io/en/latest/oauth2.html) 

3.Put the json file in the root folder and use the .env file to specify the filename 

4.run "docker-compose up --build"
