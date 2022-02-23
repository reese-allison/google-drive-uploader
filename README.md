A simple uploader to sync messages posted in Discord to a Google Drive

Create a .env file and add:

TOKEN={YOUR DISCORD BOT TOKEN}<br>
SCRIPT={YOUR GOOGLE WEB APP SCRIPT URL}

The bot implements the /upload command allowing up to 10 files to be added.
After they are uploaded to Discord, the bot responds with embeded thumbnails of image/video files and a link to upload them to the logged in users Google Drive.

![Example](https://i.imgur.com/5nN7gW3.png)
