import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# دالة الطرد مع مؤقت زمني (Duration)
async def play_and_kick(interaction: discord.Interaction, sound_file: str, duration: int):
    if not interaction.user.voice:
        await interaction.response.send_message("يا حب ادخل روم صوتي بالأول!", ephemeral=True)
        return

    await interaction.response.defer()

    channel = interaction.user.voice.channel
    
    if interaction.guild.voice_client is None:
        vc = await channel.connect()
    else:
        vc = interaction.guild.voice_client

    if vc.is_playing():
        vc.stop()
        
    vc.play(discord.FFmpegPCMAudio(sound_file))

    # هنا التعديل: الانتظار حسب الوقت المحدد
    await asyncio.sleep(duration)

    # طرد الجميع
    for member in channel.members:
        if member != bot.user:
            try:
                await member.move_to(None)
            except:
                pass
    
    await vc.disconnect()

class OutroView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # الزر الأول: 15 ثانية
    @discord.ui.button(label="تسجيل خروج اسطوري", style=discord.ButtonStyle.danger, custom_id="outro_btn_1")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # الرقم 15 هو عدد الثواني
        await play_and_kick(interaction, "outro1.mp3", 15)

    # الزر الثاني: 12 ثانية
    @discord.ui.button(label="الى هنا تنتهي سهرتنا", style=discord.ButtonStyle.primary, custom_id="outro_btn_2")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # الرقم 12 هو عدد الثواني
        await play_and_kick(interaction, "outro2.mp3", 9)

@bot.event
async def on_ready():
    bot.add_view(OutroView())
    print(f'Bot is Ready: {bot.user}')

@bot.command()
async def setup(ctx):
    # غير الكلام العربي هنا للي عجبك من فوق
    await ctx.send("🚕 **خدمة أوبر إلى خارج السيرفر** 🚕\nالرحلة مجانية، اختار المود:", view=OutroView())

bot.run(os.getenv('DISCORD_TOKEN'))