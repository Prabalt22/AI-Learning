import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv 

# Load environment variables load_dotenv()
load_dotenv() 
my_secret = os.environ['SECRET_KEY']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

chat = ""
with open("chat.txt", "r") as f:
    chat = f.read()


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        chat += f"{message.author}: {message.content}\n"
        print(f'Message from {message.author}: {message.content}')

        if self.user != message.author:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(f"{chat}\nPrabalGpt")
                response_text = response.text
                if len(response_text) > 2000:
                    for i in range(0, len(response_text), 2000):
                        await message.channel.send(response_text[i:i + 2000])
                else:
                    await message.channel.send(response_text)

            except Exception as e:
                print(e)
                chat = ""


intents = discord.Intents.default()
intents.message_content = True

print("hello")
client = MyClient(intents=intents)
client.run(my_secret)
