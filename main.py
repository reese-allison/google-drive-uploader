import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from functools import wraps
import mimetypes
import os

load_dotenv()


bot = commands.Bot()

def defer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await kwargs['inter'].response.defer()
        return await func(*args, **kwargs)
    return wrapper


class UploadView(disnake.ui.View):
  def __init__(self, urls):
    super().__init__()

    url = f'{os.getenv("SCRIPT")}?'
    for i, u in enumerate(urls):
        url += f'url{i}={u}&'
    supportServerButton = disnake.ui.Button(style=disnake.ButtonStyle.link, label='Upload to Drive', url=url)
    self.add_item(supportServerButton)


@bot.slash_command(description="Creates button to upload files to Google Drive")
@defer
async def upload(inter, 
                 file1: disnake.Attachment = commands.Param(name="file"),
                 file2: disnake.Attachment = commands.Param(None, name="2nd-file"),
                 file3: disnake.Attachment = commands.Param(None, name="3rd-file"),
                 file4: disnake.Attachment = commands.Param(None, name="4th-file"),
                 file5: disnake.Attachment = commands.Param(None, name="5th-file"),
                 file6: disnake.Attachment = commands.Param(None, name="6th-file"),
                 file7: disnake.Attachment = commands.Param(None, name="7th-file"),
                 file8: disnake.Attachment = commands.Param(None, name="8th-file"),
                 file9: disnake.Attachment = commands.Param(None, name="9th-file"),
                 file10: disnake.Attachment = commands.Param(None, name="10th-file"),
                 ):
    file_array = [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10]
    upload_count = 0
    urls = []
    embeds = []
    for f in file_array:
        if f:
            if f.content_type is None:
                f.content_type = mimetypes.guess_type(f.filename)
            if 'image' in f.content_type or 'video' in f.content_type:
                embed = disnake.Embed()
                embed.set_thumbnail(url=f.url)
                embeds.append(embed)
            urls.append(f.url)
            upload_count += 1
    
    message = "Uploaded 1 file to Discord"
    if upload_count > 1:
        message = f"Uploaded {upload_count} files Discord"
    await inter.followup.send(
        message,
        embeds=embeds,
        view=UploadView(urls)
    )

bot.run(os.getenv('TOKEN'))
