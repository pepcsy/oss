
import discord
from discord.ext import commands

# 봇 토큰

# 모든 Intents 활성화
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# 봇이 온라인 상태가 되었을 때 실행
@bot.event
async def on_ready():
    print(f'봇이 활성화되었습니다! 봇 이름: {bot.user.name}, ID: {bot.user.id}')
    print('------')

# 간단한 명령어 정의
@bot.command()
async def hello(ctx):
    await ctx.send(f"안녕하세요, {ctx.author.name}님!")

@bot.event
async def on_command_error(ctx, error):
    print(f'Command error: {error}')

# 봇 실행
bot.run(TOKEN)

