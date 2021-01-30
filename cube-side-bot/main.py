import asyncio
import aiosqlite
import aiohttp

import discord
from discord.ext import commands
import discord_slash
import jishaku
import json

from .webhook import Webhook


GUILD_IDS = [804650085052055563]

client = commands.AutoShardedBot(
    "/",
    intents=discord.Intents.all(),
    owner_ids=[702818853306236989, 487845696100368384]
)
slash = discord_slash.SlashCommand(client, auto_register=True, auto_delete=True)

rules = Webhook("https://discord.com/api/webhooks/804673807251537962/o029o_6jGB2pUct2tC-crJsz4OLn1Vw_5heAJ1juaFD2q6nMBODN1OqpDyBLxjSXzV2o")
news = Webhook("https://discord.com/api/webhooks/804683405072662528/JKR9KeU-Fqb7JRJkOcLjyJtlNQ48sRhbYu9dCyXAA7Og08Z_93zNYk0P5nDMjRYAXVwS")
faqs = Webhook("https://discord.com/api/webhooks/804673617300291594/yKFqI2Us3IAOYkmYl0baZwtuNqqt9jr26vE-gBA_RignkTYwJzaVGC5GVQ63DhH5oGvp")
audit = Webhook("https://discord.com/api/webhooks/804671873249574942/J2lymeeIz7tfgqDihEIXANV1iw3U6w5iSoUh9U6N84CJSCffzNXI3ZxWnHWiVyWvz1gd")
join_track = Webhook("https://discord.com/api/webhooks/804724673677623326/Hnby6pAeIAX4qXJ3UPApsOfOobcdEjDd9XsceD7xnxPN2miGZFa0axMCGlhC3TCX4r8n")

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
async def new(ctx, содержание):
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
async def faq(ctx, вопрос, ответ):
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
async def check_online(ctx, ip):
    await ctx.ack()
    embed = discord.Embed()
    url = f"https://api.mcsrvstat.us/2/{ip}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            server = json.loads(await r.read())
            print(server)

            if not server["online"]:
                embed.title = "Сервер не онлайн!"
                embed.color = discord.Color.dark_gray()
            else:
                embed.title = f"Сервер {server['ip']}:{server['port']} онлайн!"
                players = server["players"]
                if players["list"]:
                    embed.add_field(
                        name=f"Сейчас играют",
                        value=", ".join(players["list"])
                    )

                if not isinstance(server["version"], list):
                    embed.description = f"Версия: {server['version']}"

                else:
                    embed.description = f"Версии: {', '.join(server['version'])}"
    
    await ctx.send(embed=embed)

@client.event
async def on_member_join(member):
    await join_track.execute(username=member.name, avatar=str(member.avatar_url), content="Зашел на сервер")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"CubeSide 1.12.2 | play.cubeside.ru | https://discord.gg/eknpGjgu8N", emoji=client.get_emoji(804651860869775391)))
    client.load_extension("jishaku")


