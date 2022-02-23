import disnake
import mimetypes
from dotenv import load_dotenv
import os

load_dotenv()


client = disnake.Client()


class UploadView(disnake.ui.View):
  def __init__(self, urls):
    super().__init__()

    url = f'{os.getenv("SCRIPT")}?'
    for i, u in enumerate(urls):
        url += f'url{i}={u}&'
    supportServerButton = disnake.ui.Button(style=disnake.ButtonStyle.link, label='Upload to Drive', url=url)
    self.add_item(supportServerButton)
    


@client.event
async def on_message(message):
    # Do not respond to ourselves
    if message.author == client.user:
        return

    if message.attachments and message.content == 'upload':
        urls = []
        for attachment in message.attachments:
            if attachment.content_type is None:
                attachment.content_type = mimetypes.guess_type(attachment.filename)
            if 'image' in attachment.content_type or 'video' in attachment.content_type:
                urls.append(attachment.url)
        await message.reply(view=UploadView(urls))


client.run(os.getenv('TOKEN'))
