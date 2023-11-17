import discord
from discord import app_commands
from discord.ext import commands


class Moderator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print('moderator is ready')
	
	#@commands.Cog.listener()
	#async def on_command_error(self, interaction: discord.Interaction, error):
	#	await print("error")
	#	if isinstance(error, app_commands.MissingPermissions):
	#		await interaction.response.send_message("Недостаточно прав!")
	#		await print("error perm")
	#	else:
	#		raise error


	@app_commands.command(name="kick", description="kick member from the server")
	@app_commands.checks.has_permissions(administrator=True)
	async def kick(self, interaction: discord.Interaction, *,
				member: discord.Member,
				reason: str = "просто потому-что"):
		await member.kick(reason=reason)
		await interaction.response.send_message(f"Пользователь {member} был кикнут потому-что {reason}")
	
	# СДЕЛАТЬ ГЛОБАЛЬГЫЙ ЕРРОР ХАНДЛЕР, ЭТО ВСЁ ПОД СНОС
	@kick.error
	async def kick_error(self, interaction: discord.Interaction, error):
		if isinstance(error, app_commands.MissingPermissions):
			await interaction.response.send_message("Недостаточно прав!")
		else:
			raise error

async def setup(bot):
	await bot.add_cog(Moderator(bot))