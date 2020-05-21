import discord
import asyncio
from discord.ext import commands
from sg_modules.parse import *

TOKEN = 'Njc5MzYyMDkxNjAxMjMxODcy.Xr2pkQ.6TmkWNAg1XOyNOBrOM-bNKb--M0'
PREFIX = '.'
NEWS_ID = 706513284383113316
CLIPS_ID = 711891819750752297

bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('I`m ready!')


# .english_motherfucker_do_you_speak_it
@bot.command()
async def english_motherfucker_do_you_speak_it(ctx):
    author = ctx.message.author
    await ctx.send(f'fuck you {author.mention}')


# .clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# .help
@bot.command()
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам', colour=0x00FF00)
    emb.add_field(name='{}sg_parse(admin)'.format(PREFIX), value='Постить все новые новости из сайта StopGame.com',
                  inline=False)
    emb.add_field(name='{}clear(admin)'.format(PREFIX), value='Очистка чата', inline=False)
    emb.add_field(name='{}english_motherfucker_do_you_speak_it'.format(PREFIX), value='Проверь сам', inline=False)
    await ctx.author.send(embed=emb)


# .sg_parse
@bot.command()
@commands.has_permissions(administrator=True)
async def sg_parse(ctx, delay):
    while True:
        articles = parse()
        last_article = ''
        if articles:
            channel = bot.get_channel(NEWS_ID)
            for article in articles[::-1]:
                if article['text'] is None:
                    await ctx.send(f'''"{article['title']}" не была опубликованна из-за больльшого количества символов''')
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
                    await ctx.send(f'''"{article['title']}" - новость была успешно опубликованна''')
                last_article = article['title']
            open('sg_modules/Last_Article.txt', 'w').write(last_article)
        await ctx.send("Все новости опубликованны")
        await asyncio.sleep(3600*int(delay))


bot.run(TOKEN)
