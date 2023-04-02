from turtle import right
import discord
import os
from dotenv import load_dotenv
from webscraper import get_roster, get_schedule

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def display_data(data: dict, left_boundary = 1, right_boundary = 1) -> str:
    assert left_boundary >= 1 or right_boundary >= 1
    output = ""
    if left_boundary == 1 and right_boundary == 1:
        for key, value in data.items():
            output += f"{key}\n"
            for description, info in value.items():
                output += f"{description}: {info}\n"
            output += "----------------------------\n"
    else:
        for i in range(left_boundary, right_boundary + 1):
            output += f"{i}\n"
            for key, value in data[str(i)].items():
                output += f"{key}: {value}\n"
            output += "----------------------------\n"
    return output

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$team"):
        team_name = message.content.split("$team ", 1)[1]
        data_to_send = display_data(get_roster(f"{team_name}.html"))
        await message.channel.send("```" + data_to_send[:len(data_to_send) // 2] + "```")
        await message.channel.send("```" + data_to_send[len(data_to_send) // 2:] + "```")

    if message.content.startswith("$schedule"):
        split_message = message.content.split("$schedule ", 1)[1]
        team_name = split_message.split()[0]
        game_range_left = 0
        game_range_right = 0
        try:
            game_range_left = int(split_message.split()[1])
            game_range_right = int(split_message.split()[2])
            print(game_range_left)
            print(game_range_right)
        except:
            data_to_send = display_data(get_schedule(f"{team_name}_schedule.html"))
            right_boundary = 1
            while right_boundary < 21:
                await message.channel.send("```" + data_to_send[(right_boundary - 1) * len(data_to_send) // 20 : right_boundary * len(data_to_send) // 20] + "```")
                right_boundary += 1
        else:
            data_to_send = display_data(get_schedule(f"{team_name}_schedule.html"), game_range_left, game_range_right)
            right_boundary = 1
            divisor = (game_range_right - game_range_left) // 4
            while right_boundary < divisor + 1:
                await message.channel.send("```" + data_to_send[(right_boundary - 1) * len(data_to_send) // divisor : right_boundary * len(data_to_send) // divisor] + "```")
                right_boundary += 1
            
        

client.run(os.environ["TOKEN"])