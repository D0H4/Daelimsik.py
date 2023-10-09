import discord
import cafeteria
import json
from discord import app_commands
from discord.ext import commands
from datetime import date

GUILDS = [discord.Object(id) for id in ("YOUR SERVER ID",)]

token = "YOUR BOT TOKEN"

today = date.today()
days = ["월", "화", "수", "목", "금", "토", "일"]
weekday_today = today.weekday()  # 월요일 0 일요일 6
file_weekday = {"월": "mon", "화": "tue", "수": "wed", "목": "thu", "금": "fri"}

def read_menu():
    with open(f"./out/student/m_student_today.json", 'r', encoding='utf-8') as outfile:
        data = json.load(outfile)
        title = data['template']['outputs'][0]['simpleText']['date']
        text = data['template']['outputs'][0]['simpleText']['text']
        embed = discord.Embed(title=title)
        embed.add_field(value=text, inline=False)
    return embed

def read_weekday_menu(weekday):
    with open(f"./out/student/m_student_{file_weekday[weekday]}.json", 'r', encoding='utf-8') as outfile:
        data = json.load(outfile)
        title = data['template']['outputs'][0]['simpleText']['date']
        text = data['template']['outputs'][0]['simpleText']['text']
        embed = discord.Embed(title=title, description=f"```{text}```")
    return embed

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all()
        )

    async def on_ready(self):
        print(f"{self.user.name}으로 로그인")
        
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game("시험 공부")
        )
    
    async def setup_hook(self):
        for guild in GUILDS:
            await self.tree.sync(guild=guild)

bot = Bot()

# 명령어

# 학식 정보 출력 명령어
@bot.tree.command(
    name="학식",
    description="학식 정보를 불러옵니다.",
    guilds=GUILDS
)
@app_commands.rename(
    weekday = "요일"
)
@app_commands.describe(
    weekday = "학식을 확인할 요일을 선택해주세요. (월, 화, 수, 목, 금)"
)
async def send_menu(interaction: discord.Interaction, weekday: str):
    temp = read_weekday_menu(weekday)
    await interaction.response.send_message(embed=temp)

# 학식 데이터 수동 갱신 명령어
@bot.tree.command(
    name="학식갱신",
    description="학식 정보를 갱신합니다.",
    guilds=GUILDS
)
@commands.has_role('ADMIN ROLE NAME')
async def refresh_menu(interaction: discord.Interaction):
    await interaction.response.send_message("학식 데이터를 갱신합니다.")
    cafeteria.writeData()

bot.run(token)