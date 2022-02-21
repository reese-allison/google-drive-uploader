import discord
import uploader
import mimetypes


class MyClient(discord.Client):
    SYNCED = False

    async def on_message(self, message):
        # Do not respond to ourselves
        if message.author == self.user:
            return

        if not self.SYNCED:
            last_id = 0
            try:
                with open("sync", "r") as file:
                    last_id = int(file.readline())
            except (FileNotFoundError, ValueError):
                pass 
            async for message in message.channel.history(
                limit=200
            ):
                if message.id > last_id and message.attachments:
                    for attachment in message.attachments:
                        if attachment.content_type is None:
                            attachment.content_type = mimetypes.guess_type(attachment.filename)
                        if 'image' in attachment.content_type or 'video' in attachment.content_type:
                            file_link = await uploader.upload(message, attachment)
                            await message.channel.send(file_link)
            self.SYNCED = True

        if message.content == 'gdu folder':
            folder_link = await uploader.get_drive(message)       
            await message.channel.send(folder_link)

        if message.attachments:
            for attachment in message.attachments:
                if 'image' in attachment.content_type or 'video' in attachment.content_type:
                    file_link = await uploader.upload(message, attachment)
                    await message.channel.send(file_link)

client = MyClient()
discord_token = None
try:
    with open("token", "r") as file:
        discord_token = file.readline()
except FileNotFoundError:
    print("Please create a token file with your Discord token") 
client.run(discord_token)
