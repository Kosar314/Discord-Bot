import discord
from discord import app_commands
from discord.ext import commands


class Everyone(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('everyone is ready')
		

	@app_commands.command(name="ping", description="pong")
	async def ping(self, interaction: discord.Interaction):
		bot_latency = round(self.bot.latency * 1000)
		await interaction.response.send_message(f"Pong! {bot_latency} ms.")


async def setup(bot):
	await bot.add_cog(Everyone(bot))