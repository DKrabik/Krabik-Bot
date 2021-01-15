import discord
from random import choice
from os import environ
from discord.ext import commands, tasks
from sg_modules.parse import parse

TOKEN = environ.get('TOKEN')
PREFIX = '.'
NEWS_ID = int(environ.get('NEWS_ID'))

bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_ready():
    sg_parse.start()
    print("I'm ready!")


@bot.event
async def on_voice_state_update(member, before, after):

    if not before.channel and not member.bot and after.channel and choice([True, False]):
        await member.move_to(None)
        await member.send(f"Ops.. I did it again. Try again :crab:")


# .clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# .sg_parse
@tasks.loop(hours=3)
async def sg_parse():
    channel = bot.get_channel(NEWS_ID)
    last_title = await (channel.fetch_message(channel.last_message_id))
    last_title = last_title.embeds[0].title
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
    print("[log] Все новости опубликованны")


bot.run(TOKEN)
