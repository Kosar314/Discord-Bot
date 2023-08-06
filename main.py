import asyncio
import discord
from discord.ext import commands
import config
import os


bot_intents = discord.Intents.all()
bot_intents.members = True


bot = commands.Bot(command_prefix=config.prefix, intents=bot_intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Genshin Impact"))
    await bot.wait_until_ready()


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    print(f"load module: cogs.{extension}")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"unload module: cogs.{extension}")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print(f"reload module: cogs.{extension}")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    print('PA6OTAET')
    await load_extensions()
    await bot.start(config.token)


if __name__ == "__main__":
    asyncio.run(main())