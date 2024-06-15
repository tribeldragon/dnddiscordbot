import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables from .env file
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ROLE_NAME = os.getenv('ROLE_NAME')

# Debug: Print the loaded environment variables
print(f'DISCORD_BOT_TOKEN: {DISCORD_BOT_TOKEN}')
print(f'ROLE_NAME: {ROLE_NAME}')

if not DISCORD_BOT_TOKEN:
    raise ValueError("No DISCORD_BOT_TOKEN found in environment variables.")
if not ROLE_NAME:
    raise ValueError("No ROLE_NAME found in environment variables.")

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  # Request the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    
    if role is None:
        await ctx.send(f'Role "{ROLE_NAME}" not found.')
        return
    
    members = role.members
    for member in members:
        if member.voice:
            try:
                await member.edit(mute=True)
            except discord.Forbidden:
                await ctx.send(f"Missing permissions to mute {member.display_name}.")
    await ctx.send(f'Muted all members with the "{ROLE_NAME}" role.')

@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    
    if role is None:
        await ctx.send(f'Role "{ROLE_NAME}" not found.')
        return
    
    members = role.members
    for member in members:
        if member.voice:
            try:
                await member.edit(mute=False)
            except discord.Forbidden:
                await ctx.send(f"Missing permissions to unmute {member.display_name}.")
    await ctx.send(f'Unmuted all members with the "{ROLE_NAME}" role.')

bot.run(DISCORD_BOT_TOKEN)
