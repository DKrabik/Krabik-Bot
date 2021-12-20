import discord
from random import choice, randint
from os import environ
from discord.ext import commands, tasks
from sg_modules.parse import parse
from psql import mypsql_commands

TOKEN = environ.get('TOKEN')
PREFIX = '.'
HOST = environ.get('HOST')
USER = environ.get('USER')
PASSWORD = environ.get('PASSWORD')
DATABASE = environ.get('DATABASE')

intents = discord.Intents()
bot = commands.Bot(command_prefix=PREFIX, intents=intents.all())
connection = mypsql_commands.create_connection(HOST, USER, PASSWORD, DATABASE)
connection.autocommit = True

@bot.event
async def on_ready():
    if (connection):
        mypsql_commands.query(connection, 'CREATE TABLE users(id BIGSERIAL NOT NULL PRIMARY KEY, user_id BIGINT NOT NULL, server_id BIGINT NOT NULL, nickname VARCHAR(32), money INT NOT NULL) ;')
        mypsql_commands.query(connection, 'CREATE TABLE settings(server_id BIGINT NOT NULL PRIMARY KEY, news_chat_id BIGINT, last_article VARCHAR(100)) ;')
        for guild in bot.guilds:
            for member in guild.members:
                if not member.bot:
                    if (not mypsql_commands.query(connection, f'SELECT user_id, server_id FROM users WHERE user_id = {member.id} AND server_id = {member.guild.id} ;', get=True)):
                        mypsql_commands.query(connection, f"INSERT INTO users(user_id, server_id, nickname, money) VALUES ({member.id}, {member.guild.id}, '{member}', 0)")             
        mypsql_commands.query(connection, f"INSERT INTO settings(server_id) VALUES ({guild.id}) ON CONFLICT (server_id) DO NOTHING;")
    sg_parse.start()
    print("I'm ready!")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id in [440050080968605696, 417248973548683265, 416229787997175820]:
        if not before.channel and not member.bot and after.channel and (randint(1,100)==1):
            await member.move_to(None)
            await member.send(f"Пошел нахуй, пидарас! Удачи тебе зайти с шансом 1%")
    else:
        if not before.channel and not member.bot and after.channel and choice([True, False]):
            await member.move_to(None)
            await member.send(f"Ops.. I did it again. Try again :crab:")


# .clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# .set_news_chat_id
@bot.command()
@commands.has_permissions(administrator=True)
async def set_news_chat_id(ctx, msg = None):
    try:
        mypsql_commands.change_settings(connection, "news_chat_id", msg, ctx.guild.id)
        if (mypsql_commands.select_from_settings(connection,"news_chat_id", ctx.guild.id) == int(msg)):
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")
    except:
        await ctx.message.add_reaction("❌")


# .sg_parse
@tasks.loop(hours=3)
async def sg_parse():
    for setting in mypsql_commands.query(connection, "SELECT server_id, news_chat_id, last_article FROM settings WHERE news_chat_id IS NOT NULL;", get=True):
        channel = bot.get_channel(setting[1])
        last_title = setting[2]
        articles = parse(last_title)
        if articles:
            for article in articles[::-1]:
                if article['text'] is None:
                    print(f'''"[log] {article['title']}" не была опубликованна из-за больльшого количества символов''')
                else:
                    emb = discord.Embed(title=article['title'], colour=article['color'])
                    emb.set_author(name=article['author'], icon_url=article['author_img'])
                    emb.add_field(name='Дата:', value=article['date'])
                    emb.add_field(name='Ссылка на источник:', value=article['link'])
                    emb.add_field(name='Теги:', value=article['tags'])
                    if article['img']:
                        emb.set_image(url=article['img'])
                    emb.description = article['text']
                    await channel.send(embed=emb)
                    print(f'''"[log] {article['title']}" - новость была успешно опубликованна''')
            mypsql_commands.query(connection, f"UPDATE settings SET last_article = \'{articles[0]['title']}\' WHERE server_id = {setting[0]}") 
        print("[log] Все новости опубликованны")


bot.run(TOKEN)
