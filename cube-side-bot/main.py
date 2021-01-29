import asyncio
import aiosqlite

import discord
import discord_slash

from .webhook import Webhook


GUILD_IDS = [804650085052055563]

client = discord.AutoShardedClient(
    intents=discord.Intents.all()
)
slash = discord_slash.SlashCommand(client, auto_register=True, auto_delete=True)

rules = Webhook("https://discord.com/api/webhooks/804673807251537962/o029o_6jGB2pUct2tC-crJsz4OLn1Vw_5heAJ1juaFD2q6nMBODN1OqpDyBLxjSXzV2o")
news = Webhook("https://discord.com/api/webhooks/804683405072662528/JKR9KeU-Fqb7JRJkOcLjyJtlNQ48sRhbYu9dCyXAA7Og08Z_93zNYk0P5nDMjRYAXVwS")
faqs = Webhook("https://discord.com/api/webhooks/804673617300291594/yKFqI2Us3IAOYkmYl0baZwtuNqqt9jr26vE-gBA_RignkTYwJzaVGC5GVQ63DhH5oGvp")
audit = Webhook("https://discord.com/api/webhooks/804671873249574942/J2lymeeIz7tfgqDihEIXANV1iw3U6w5iSoUh9U6N84CJSCffzNXI3ZxWnHWiVyWvz1gd")
join_track = Webhook("https://discord.com/api/webhooks/804724673677623326/Hnby6pAeIAX4qXJ3UPApsOfOobcdEjDd9XsceD7xnxPN2miGZFa0axMCGlhC3TCX4r8n")

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


@client.event
async def on_member_join(member):
    await join_track.execute(username=member.name, avatar=str(member.avatar_url), content="Зашел на сервер")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"CubeSide 1.12.2 | play.cubeside.ru | https://discord.gg/eknpGjgu8N", emoji=client.get_emoji(804651860869775391)))

    embed = {
        "title": "Священные правила сервера CubeSide",
        "description": "‼Данный свод правил может быть изменен в любой момент, и администрация оставляет на себе право не оповещать игроков об изменениях‼",
        "fields": [
            {
                "name": "Общие правила",
                "value": """
                Незнание правил не освобождает от ответственности;
                Деньги за купленную привилегию на сервере не возвращаются, и считается вкладом в работу проекта;
                Шутки на администрацией неприемлимы - она шуток не понимает, в основном;
                Все добавленные игроки являются равноправными владельцами региона;
                Администрация не несёт ответственность если вас загриферил человек которого вы добавили в регион;
                Если игрок с привилегией выдал ограничение, он обязан предоставить пруфы в течении часа;
                Владельцу группы по продаже аккаунтов/ресурсов/игровой валюты будет выдан перманентный бан на все аккаунты которыми он владеет/бан в сообществе сервера.
                """,
                "inline": False
            },
            {
                "name": ":arrow_down: Карается мутом :arrow_down:",
                "value": """
                Флуд/спам - 5 мин;
                Оскорбления - 10 мин;
                Маты - 10 мин;
                Реклама - 2-3 дня;
                Оск. админов - 15 мин;
                Капс - 5 мин;
                NSFW - 5 мин;
                Расизм/нацизм/фашизм - 10 мин;
                Угрозы жизни участникам - 10 мин.
                """,
                "inline": False
            },
            {
                "name": ":arrow_down: Карается баном :arrow_down:",
                "value": """
                Читы(типа X-ray, кликеры, макросы) - 14 д;
                Багоюз - 7 д;
                Передача акка третьим лицам - вечный;
                Продажа - покупка ресурсов, доната за реальные деньги 30 д;
                Причининение вреда серверу - 7 д;
                Порча спавна, залив ада и эндера - 3 д;
                Постройки: которые нагружают сервер, имеют NSFW контекст, маты - снос, 7д;
                Выдавать себя за админа - 10 д;
                Распространение багов, дюпов - 7 д;
                Нецензурный ник - 32 мин;
                NSFW скин - 5 ч;
                Сруб 5 и более деревьев на лесорубке в афк - 15 мин
                """,
                "inline": False
            },
            {
                "name": ":arrow_down: Карается баном *для привелегированных игроков* :arrow_down:",
                "value": """
                Подбор/воровство ресурсов в флае/годе - 5 ч;
                Бан/кик/мут по не корректной причине - 5/3 д/8 ч;
                Размут самого себя - 3 ч;
                Гриферство в режиме Бога(относится к Хелпер+) - 9 ч;
                Ходьба по пвп арене в режиме Бога - 12 ч;
                Воровство в режиме Бога - 2 д;
                Спам в `/bc` - мут на час;
                Разбан того, кто был забанен админами - 7 д.
                """,
                "inline": False
            }
        ],
        "color": 0x7289DA
    }

    await rules.execute(embeds=[embed])

async def get_token():
    async with aiosqlite.connect("info.db") as db:
        async with db.execute("SELECT * FROM info") as cur:
            async for row in cur:
                return row[0]
