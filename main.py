import discord
import os
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def outro(ctx):
    if not ctx.author.voice:
        await ctx.send("ادخل روم صوتي أولاً.")
        return

    channel = ctx.author.voice.channel
    vc = await channel.connect()
    
    # تشغيل الصوت
    vc.play(discord.FFmpegPCMAudio('outro.mp3'))

    # انتظار انتهاء الصوت
    while vc.is_playing():
        await asyncio.sleep(1)

    # طرد الجميع (Disconnect)
    for member in channel.members:
        if member != bot.user: # عشان ما يطرد نفسه قبل ما يخلص اللوب
            try:
                await member.move_to(None) # None تعني الطرد من الفويس
            except:
                pass
    
    await vc.disconnect()

bot.run(os.getenv('DISCORD_TOKEN'))