import discord
from discord.ext import commands
import asyncio
import os

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# دالة الطرد وتشغيل الصوت (تستخدم للزرين)
async def play_and_kick(interaction: discord.Interaction, sound_file: str):
    # التأكد أن الشخص في روم صوتي
    if not interaction.user.voice:
        await interaction.response.send_message("يا حب ادخل روم صوتي بالأول!", ephemeral=True)
        return

    # الرد السريع عشان الزر ما يعلق
    await interaction.response.defer()

    channel = interaction.user.voice.channel
    
    # محاولة الاتصال (لو البوت مو موجود بالروم)
    if interaction.guild.voice_client is None:
        vc = await channel.connect()
    else:
        vc = interaction.guild.voice_client

    # تشغيل الصوت المختار
    if vc.is_playing():
        vc.stop()
        
    vc.play(discord.FFmpegPCMAudio(sound_file))

    # انتظار انتهاء الصوت (التشيك السريع)
    while vc.is_playing():
        await asyncio.sleep(0.1)

    # طرد الجميع
    for member in channel.members:
        if member != bot.user:
            try:
                await member.move_to(None)
            except:
                pass
    
    # خروج البوت
    await vc.disconnect()

# تصميم الأزرار
class OutroView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # عشان الأزرار ما تخرب بعد وقت

    # الزر الأول (لونه أحمر)
    @discord.ui.button(label="طرد 1 (Outro 1)", style=discord.ButtonStyle.danger, custom_id="outro_btn_1")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # غير اسم الملف هنا
        await play_and_kick(interaction, "outro1.mp3")

    # الزر الثاني (لونه أزرق)
    @discord.ui.button(label="طرد 2 (Outro 2)", style=discord.ButtonStyle.primary, custom_id="outro_btn_2")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # غير اسم الملف هنا
        await play_and_kick(interaction, "outro2.mp3")

@bot.event
async def on_ready():
    # تسجيل الأزرار عشان تشتغل حتى لو طفيت البوت وشغلته
    bot.add_view(OutroView())
    print(f'Bot is Ready: {bot.user}')

# أمر لإنشاء لوحة التحكم
@bot.command()
async def setup(ctx):
    await ctx.send("🎛️ **لوحة التحكم بالطررد** 🎛️\nاختر الصوت المناسب:", view=OutroView())

bot.run(os.getenv('DISCORD_TOKEN'))