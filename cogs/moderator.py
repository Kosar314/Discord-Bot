import discord
from discord import app_commands
from discord.ext import commands
import config


class Moderator(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('moderator is ready')
	
	@commands.Cog.listener()
	async def on_command(self, bot: commands.Bot, interaction: discord.Interaction, msg: str):
		log_channel = discord.utils.get(interaction.guild.channels, name="logs")
		if log_channel is not None:
			await log_channel.send(msg)
			
	async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		if isinstance(error, app_commands.MissingPermissions):
			await interaction.response.send_message("Недостаточно прав!", ephemeral=True)
		elif isinstance(error, app_commands.BotMissingPermissions):
			await interaction.response.send_message("У Бота недостаточно прав на выполнение данной команды", ephemeral=True)
		else:
			await interaction.response.send_message("Произошла неизвестная ошибка", ephemeral=True)
			print(error, '\n', error.__class__, '\n')


	@app_commands.command(name="kick", description="Кикнуть участника")
	@app_commands.checks.has_permissions(manage_members=True)
	async def kick(self, interaction: discord.Interaction, *,
				member: discord.Member,
				reason: str = "просто потому-что"):
		await member.kick(reason=reason)
		self.bot.dispatch("command", self.bot, interaction, f"Пользователь {member} был кикнут, причина: {reason}")
		await interaction.response.send_message(f"Пользователь {member} был кикнут, причина: {reason}")

	@app_commands.command(name="ban", description="Забанить участника")
	@app_commands.checks.has_permissions(administrator=True)
	async def ban(self, interaction: discord.Interaction, *,
				member: discord.Member,
				reason: str = "просто потому-что"):
		await member.ban(reason=reason)
		self.bot.dispatch("command", self.bot, interaction, f"Пользователь {member} был забанен, причина: {reason}")
		await interaction.response.send_message(f"Пользователь {member} был забанен, причина: {reason}")

	@app_commands.command(name="unban", description="Разбанить участника")
	@app_commands.checks.has_permissions(administrator=True)
	async def unban(self, interaction: discord.Interaction, *,
				username_or_id: str):
		banned_users = interaction.guild.bans

		async for entry in banned_users():
			if entry.user.name == username_or_id or entry.user.id == username_or_id:
				await interaction.guild.unban(entry.user)
				self.bot.dispatch("command", self.bot, interaction, f"Пользователь {entry.user} был разбанен")
				await interaction.response.send_message(f"Пользователь {entry.user} был разбанен")
				return
			
		await interaction.response.send_message(f"Пользователь {username_or_id} не найден или не забанен", ephemeral=True)
	
	@app_commands.command(name="addrole", description="Добавить роль участнику")
	@app_commands.checks.has_permissions(manage_roles=True)
	async def addrole(self, interaction: discord.Interaction, *,
				   member: discord.Member,
				   role: discord.Role):
		for member_role in member.roles:
			if member_role == role:
				await interaction.response.send_message(f"Ошибка! У пользователя {member} уже есть роль {role}", ephemeral=True)
				return
			
		await member.add_roles(role)
		self.bot.dispatch("command", self.bot, interaction, f"Пользователю {member} была выдана роль {role}")
		await interaction.response.send_message(f"Пользователю {member} была выдана роль {role}")

	@app_commands.command(name="delrole", description="Удалить роль у участника")
	@app_commands.checks.has_permissions(manage_roles=True)
	async def delrole(self, interaction: discord.Interaction, *,
				   member: discord.Member,
				   role: discord.Role):
		for member_role in member.roles:
			if member_role == role:
				await member.remove_roles(role)
				self.bot.dispatch("command", self.bot, interaction, f"С пользователя {member} была снята роль {role}")
				await interaction.response.send_message(f"С пользователя {member} была снята роль {role}")
				return
		
		await interaction.response.send_message(f"Ошибка! У пользователя {member} нет роли {role}", ephemeral=True)


async def setup(bot):
	await bot.add_cog(Moderator(bot))