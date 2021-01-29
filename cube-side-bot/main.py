import asyncio
import aiosqlite
import aiohttp

import discord
import discord_slash


GUILD_IDS = [804650085052055563]
client = discord.AutoShardedClient(
    intents=discord.Intents.all()
)
slash = discord_slash.SlashCommand(client, auto_register=True, auto_delete=True)

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
    

    await ctx.ack()
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{client.get_emoji(804651860869775391)} CubeSide 1.12.2 | play.cubeside.ru | https://discord.gg/eknpGjgu8N"))

async def get_token():
    async with aiosqlite.connect("info.db") as db:
        async with db.execute("SELECT * FROM info") as cur:
            async for row in cur:
                return row[0]
