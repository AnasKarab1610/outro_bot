import discord
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_message(message):
    # تجاهل رسائل البوت نفسه
    if message.author.bot:
        return

    # تحقق من الكلمة
    if message.content.lower() != "out":
        return

    # لازم يكون الكاتب داخل روم صوتي
    if not message.author.voice:
        await message.channel.send("❌ ادخل روم صوتي أولاً.")
        return

    channel = message.author.voice.channel
    vc = await channel.connect()

    # تشغيل الصوت
    vc.play(discord.FFmpegPCMAudio("outro.mp3"))

    # ⏱️ انتظر 15 ثانية (والصوت شغال)
    await asyncio.sleep(15)

    # طرد الجميع من الروم
    for member in channel.members:
        if member != client.user:
            try:
                await member.move_to(None)
            except:
                pass

    await vc.disconnect()

client.run(os.getenv("DISCORD_TOKEN"))
