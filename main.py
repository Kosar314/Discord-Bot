import asyncio
import discord
from discord.ext import commands
import config
import os

bot_intents = discord.Intents.all()
bot_intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=bot_intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Следит за пользователями"))
    await bot.wait_until_ready()


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.command(name="sync")
@commands.has_permissions(administrator=True)
async def sync(ctx):
    synced = await bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} command(s).")


async def main():
    print('working')
    await load_extensions()
    await bot.start(config.token)

    guild = bot.guilds
    await bot.tree.copy_global_to(guild=guild)

if __name__ == "__main__":
    asyncio.run(main())