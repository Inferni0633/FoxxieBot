import discord
from discord.ext import commands
import datetime, pyowm
from discord.utils import get
import random

import os
from time import sleep
import io
import requests
from PIL import Image, ImageFont, ImageDraw

bot = commands.Bot(command_prefix = "ф!", help_command=None, intents=discord.Intents.all())
var = [':full_moon: Выпал орел!', ':new_moon: Выпала решка!', ':last_quarter_moon: Ребро!']

OWNERID = 705299890665816117

@bot.event # запуск бота
async def on_ready(pass_context=True):
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("ф!хелп"))

@bot.event
async def on_message(message):
	await bot.process_commands(message)

	msg = message.content.lower()
	greeting_words = [" "]
	censored_words = [" "]

	if msg in greeting_words:
		await message.channel.send(f"{message.author.name}, прив)")

	for bad_content in msg.split(" "):
		if bad_content in censored_words:
			await message.channel.send(f"{message.author.mention}, **вам был дан пинок под зад, по причине: её нет!**")

@bot.event
async def on_command_error(ctx, error):

	print(error)

	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
	elif isinstance(error, commands.UserInputError):
		await ctx.send(embed=discord.Embed(
			description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
		))

@bot.command(name="юзер", brief="Карточка юзера", usage="Юзер <member>")
async def info(ctx, member: discord.Member):
    emb = discord.Embed(title='Информация о пользователе', color=0x39d0d6)
    emb.add_field(name='Когда присоединился:', value=member.joined_at, inline=True)
    emb.add_field(name='Имя:', value=member.display_name, inline=False)
    emb.add_field(name='Айди:', value=member.id, inline=False)
    emb.add_field(name='Аккаунт был создан:', value=member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"), inline=False)
    emb.set_thumbnail(url=member.avatar_url)
    emb.set_footer(text=f"Вызвано:{ctx.message.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command(name="лис", brief="Показать фоточку лисы", usage="Лиса") # фотки лис
async def лиса(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Рандомная лися') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command(name="кот", brief="Показать фоточку кота", usage="Кот") # фотки котов
async def кот(ctx):
    response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xf2f3f4, title = 'Рандомная кися') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command(name="пёсик", brief="Показать фоточку пёсика", usage="Пёсик") # фотки котов
async def пёс(ctx):
    response = requests.get('https://some-random-api.ml/img/dog') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xf2f3f4, title = 'Рандомный пёсик') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command(name="клир", brief="Очистить чат от сообщений, по умолчанию 10 сообщений", usage="clear <amount=10>")
async def clear(ctx, amount: int=10):
	await ctx.channel.purge(limit=amount)
	await ctx.send(f"Was deleted {amount} messages...")


@bot.command(name="кик", brief="Выгнать пользователя с сервера", usage="kick <@user> <reason=None>")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
	await ctx.message.delete(delay=1) # Если желаете удалять сообщение после отправки с задержкой

	await member.send(f"You was kicked from server") # Отправить личное сообщение пользователю
	await ctx.send(f"Member {member.mention} was kicked from this server!")
	await member.kick(reason=reason)


@bot.command(name="бан", brief="Забанить пользователя на сервере", usage="ban <@user> <reason=None>")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	await member.send(f"You was banned on server") # Отправить личное сообщение пользователю
	await ctx.send(f"Member {member.mention} was banned on this server")
	await member.ban(reason=reason)


@bot.command(name="разбан", brief="Разбанить пользователя на сервере", usage="unban <user_id>")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
	user = await bot.fetch_user(user_id)
	await ctx.guild.unban(user)

@bot.command(name="мут", brief="Запретить пользователю писать (настройте роль и канал)", usage="mute <member>")
async def mute_user(ctx, member: discord.Member):
	mute_role = discord.utils.get(ctx.message.guild.roles, name="Мут")

	await member.add_roles(mute_role)
	await ctx.send(f"{ctx.author} gave role mute to {member}")

@bot.command(name="размут", brief="Разрешить пользователю писать (настройте роль и канал)", usage="unmute <member>")
async def mute_user(ctx, member: discord.Member):
	mute_role = discord.utils.get(ctx.message.guild.roles, name="Мут")

	await member.remove_roles(mute_role)
	await ctx.send(f"{ctx.author} remove role mute to {member}")

@bot.command(name="монетка")
async def flip(ctx):
    response = random.choice(var)
    await ctx.send(response)

@bot.command(name="хелп", usage="хэлп")
async def help(ctx):
    emb = discord.Embed(title='Команды:', color=0x39d0d6)
    emb.add_field(name='юзер', value='Карточка пользователя')
    emb.add_field(name='лис', value='Показать лису')
    emb.add_field(name='кот', value='Показать котика')
    emb.add_field(name='пёсик', value='Показать собачку')
    emb.add_field(name='мут', value='Замьютить юзера')
    emb.add_field(name='размут', value='Размьютить юзера')
    emb.add_field(name='кик', value='Кикнуть юзера')
    emb.add_field(name='бан', value='Забанить юзера')
    emb.add_field(name='разбан', value='Разбанить юзера')
    emb.add_field(name='клир', value='Удалить сообщения')
    emb.add_field(name='монетка', value='Орёл или Решка')
    emb.add_field(name='хелп', value='Выводит это сообщение')
    emb.set_footer(text=f"Мой создатель: Enmu(и да, он человек)", icon_url="https://cdn.discordapp.com/avatars/705299890665816117/9c068671a121835d72b9be09e8eeea01.png?size=4096")
    
    await ctx.send(embed=emb)

@bot.event 
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
        await ctx.send(embed=embed)
    else:
        embed.add_field(name = f':x: Terminal Error', value = f"```{error}```")
        await ctx.send(embed = embed)
        raise error

bot.run('ODMzMjc0ODYwMDM3NDcyMjk2.YHv9sA.PFgDp6OM2cQQfoUw8bDph2cp0dQ')
