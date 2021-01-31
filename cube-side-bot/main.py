import asyncio
import aiosqlite
import aiohttp
import mcrcon

import discord
from discord.ext import commands
import discord_slash
import jishaku

import json
import random
import re

from .webhook import Webhook


GUILD_IDS = [804650085052055563]

client = commands.AutoShardedBot(
    "/",
    intents=discord.Intents.all(),
    owner_ids=[702818853306236989, 487845696100368384, 784648210832162826]
)
slash = discord_slash.SlashCommand(client, auto_register=True, auto_delete=True)

users = []

rules = Webhook("https://discord.com/api/webhooks/804673807251537962/o029o_6jGB2pUct2tC-crJsz4OLn1Vw_5heAJ1juaFD2q6nMBODN1OqpDyBLxjSXzV2o")
news = Webhook("https://discord.com/api/webhooks/804683405072662528/JKR9KeU-Fqb7JRJkOcLjyJtlNQ48sRhbYu9dCyXAA7Og08Z_93zNYk0P5nDMjRYAXVwS")
faqs = Webhook("https://discord.com/api/webhooks/804673617300291594/yKFqI2Us3IAOYkmYl0baZwtuNqqt9jr26vE-gBA_RignkTYwJzaVGC5GVQ63DhH5oGvp")
audit = Webhook("https://discord.com/api/webhooks/804671873249574942/J2lymeeIz7tfgqDihEIXANV1iw3U6w5iSoUh9U6N84CJSCffzNXI3ZxWnHWiVyWvz1gd")
join_track = Webhook("https://discord.com/api/webhooks/804724673677623326/Hnby6pAeIAX4qXJ3UPApsOfOobcdEjDd9XsceD7xnxPN2miGZFa0axMCGlhC3TCX4r8n")
leave_track = Webhook("https://discord.com/api/webhooks/805326685087596574/6FEku6lxhhpLNwulEXEZ8emByfgTVPJ5iyhReoH1ZBvgQxdiJKdVc9SLn_MCGCJ4VIjP")

async def get_token():
    async with aiosqlite.connect("info.db") as db:
        async with db.execute("SELECT * FROM info") as cur:
            async for row in cur:
                return row[0]

@slash.slash(
    name="пинг",
    description="Понг!",
    guild_ids=GUILD_IDS
)
async def ping(ctx):
    await ctx.ack()
    await ctx.send(f"Пинг-понг! Отправлено за {round(client.latency * 1000)}мс")

@slash.slash(
    name="сервер",
    description="Инфо о сервере",
    guild_ids=GUILD_IDS
)
async def server(ctx):
    await ctx.ack()

    embed = discord.Embed(
        title=f"Инфо о {ctx.guild.name}",
        color=ctx.author.color
    )
    embed.add_field(
        name="Участники",
        value=f"{client.get_emoji(804678841674629132)} {len(ctx.guild.members)}",
        inline=False
    )
    embed.add_field(
        name="Владелец",
        value=f"{client.get_emoji(804680946065735700)} {ctx.guild.owner.mention}",
        inline=False
    )
    embed.add_field(
        name="Текстовые каналы",
        value=f"{client.get_emoji(804680946158010398)} {len(ctx.guild.text_channels)}",
        inline=False
    )
    embed.add_field(
        name="Голосовые каналы",
        value=f"{client.get_emoji(804680946036899890)} {len(ctx.guild.voice_channels)}",
        inline=False
    )
    embed.set_thumbnail(
        url=ctx.guild.icon_url
    )

    await ctx.send(embed=embed)

@slash.slash(
    name="новость",
    description="Добавить новость. Только для админов!",
    guild_ids=GUILD_IDS
)
async def new(ctx, содержание: str):
    await ctx.ack(eat=True)
    embed = {
        "title": "Новость!",
        "description": содержание,
        "color": 0x7289DA
    }

    if ctx.author.guild_permissions.administrator:
        await news.execute(embeds=[embed])
    else:
        await ctx.send("У вас нет прав администратора для публикации новостей!", hidden=True)

@slash.slash(
    name="чаво",
    description="Новый ЧаВо(Часто задаваемый Вопрос)",
    guild_ids=GUILD_IDS
)
async def faq(ctx, вопрос: str, ответ: str):
    await ctx.ack(eat=True)
    embed = {
        "title": вопрос,
        "description": ответ,
        "color": 0x2ecc71
    }
    if ctx.guild.get_role(804721794053439569) in ctx.author.roles:
        await faqs.execute(embeds=[embed])
    else:
        await ctx.send("У вас нет роли для публикации ЧаВо!", hidden=True)

@slash.slash(
    name="майн_сервер",
    description="Чекнуть онлайн на сервере",
    guild_ids=GUILD_IDS
)
async def check_online(ctx, ip: str):
    await ctx.ack()
    embed = discord.Embed()
    url = f"https://api.mcsrvstat.us/2/{ip}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            server = json.loads(await r.read())

            if not server["online"]:
                embed.title = "Сервер не онлайн!"
                embed.color = discord.Color.dark_gray()
            else:
                embed.title = f"Сервер {server['ip']}:{server['port']} онлайн!"
                embed.color = discord.Color.blurple()
                players = server["players"]
                if "list" in players:
                    embed.add_field(
                        name=f"Сейчас играют",
                        value=", ".join(players["list"])
                    )

                if not isinstance(server["version"], list):
                    embed.description = f"Версия: {server['version']}"

                else:
                    embed.description = f"Версии: {', '.join(server['version'])}"
    
    await ctx.send(embed=embed)

@slash.slash(
    name="шар",
    description="Спросите у волшебного шара что угодно!",
    guild_ids=GUILD_IDS
)
async def eight_ball(ctx, вопрос):
    await ctx.ack()

    answers = [
        "Бесспорно",
        "Предрешено",
        "Никаких сомнений",
        "Определённо да",
        "Можешь быть уверен в этом",
        "Мне кажется — «да»",
        "Вероятнее всего",
        "Хорошие перспективы",
        "Знаки говорят — «да»",
        "Да",
        "Пока не ясно, попробуй снова",
        "Спроси позже",
        "Лучше не рассказывать",
        "Сейчас нельзя предсказать",
        "Сконцентрируйся и спроси опять",
        "Даже не думай",
        "Мой ответ — «нет»",
        "По моим данным — «нет»",
        "Перспективы не очень хорошие",
        "Весьма сомнительно"
    ]
    answer = random.choice(answers)

    embed = discord.Embed(
        title=f"«{вопрос}»",
        description=f"**{answer}**",
        color=discord.Color.blurple()
    )
    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )

    await ctx.send(embed=embed)

@slash.slash(
    name="добавить", 
    description="Добавить пользователя RCON",
    guild_ids=GUILD_IDS
)
async def rcon_add_user(ctx, id: int):
    await ctx.ack(eat=True)
    if ctx.author.id in client.owner_ids:
        try:
            user = await client.fetch_user(id)
            users.append(id)
            await ctx.send(f"**{user.display_name}** добавлен в список RCON пользователей", hidden=True)
        except:
            await ctx.send("Не удалось добавить пользователя", hidden=True)
    else:
        await ctx.send("У вас нет прав на добавление пользователей RCON", hidden=True)

@slash.slash(
    name="удалить",
    description="Удалить пользователя RCON",
    guild_ids=GUILD_IDS
)
async def rcon_remove_user(ctx, id: int):
    await ctx.ack(eat=True)
    if ctx.author.id in client.owner_ids:
        try:
            user = await client.fetch_user(id)
            users.remove(id)
            await ctx.send(f"**{user.display_name}** удалён из списка RCON пользователей", hidden=True)
        except:
            await ctx.send("Не удалось удалить пользователя", hidden=True)
    else:
        await ctx.send("У вас нет прав на удаление пользователей RCON", hidden=True)

@slash.slash(
    name="rcon",
    description="Запустить REPL RCON сервера",
    guild_ids=GUILD_IDS
)
async def rcon_start(ctx):
    await ctx.ack(eat=True)
    def check(m):
        return m.author.id == ctx.author.id

    if ctx.author.id in users or ctx.author.id in client.owner_ids:
        rcon = mcrcon.MCRcon("95.216.62.180", "41097498AA47969E1B", port=28582)
        rcon.connect()
        await ctx.send("Сессия RCON запущена! Вводите команды, для выхода `exit`", hidden=True)
        while True:
            msg = await client.wait_for("message", check=check)
            if msg.content != "exit":
                cmd = rcon.command(msg.content)
                try:
                    await ctx.send(f"""
                ```
                {cmd}
                ```
                """, hidden=True)
                except:
                    await ctx.send("*пустой вывод*", hidden=True)

            else:
                rcon.disconnect()
                await ctx.send("Сессия закрыта")
                break

    else:
        await ctx.send("Вас не добавили в список RCON пользователей", hidden=True)

@client.event
async def on_slash_command(ctx: discord_slash.SlashContext):
    embed = {
        "title": f"Использована команда `/{ctx.name}`",
        "description": f"ID: {ctx.command_id}, пользователь: {ctx.author.mention}",
        "color": 0x7289DA
    }

    await audit.execute(embeds=[embed])

@client.event
async def on_slash_command_error(ctx, ex):
    embed = discord.Embed(
        title=f"Произошла ошибка во время исполнения команды `/{ctx.name}`",
        description=f"""
```py
{ex}
```
        """
    )

    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, message.content)
    urls = [x[0] for x in url]
    if urls:
        if not message.author.guild_permissions.administrator:
            await message.delete()
            await message.channel.send(f"Сообщение от {message.author.mention} было удалено из-за содержания ссылки.")
        else:
            pass

@client.event
async def on_member_join(member):
    await join_track.execute(username=member.name, avatar=str(member.avatar_url), content="Зашел на сервер")

@client.event
async def on_member_remove(member):
    await leave_track.execute(username=member.name, avatar=str(member.avatar_url), content="*тихо ушёл*")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"CubeSide 1.12.2 | play.cubeside.ru | https://discord.gg/eknpGjgu8N", emoji=client.get_emoji(804651860869775391)))
    client.load_extension("jishaku")
    print("cube-side-bot started")
