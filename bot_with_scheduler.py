import discord
from discord.ext import commands
import sqlite3
import schedule
import time
from threading import Thread
from main import update_followers, update_youtube_subscribers
from config import DISCORD_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("--- 연결 성공 ---")
    print(f"Bot Name : {bot.user.name}")
    print(f"Bot ID : {bot.user.id}")
    print(f"Server : {len(bot.guilds)}개")
    await bot.change_presence(activity=discord.Game("k-pop 아이돌에 대한 가장 객관적인 지표!"))

@bot.event
async def on_member_join(member):
    """
    서버에 새 멤버가 입장했을 때 환영 메시지를 전송합니다.
    """
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"{member.mention}님 환영합니다")

@bot.event
async def on_member_remove(member):
    """
    서버에서 멤버가 나갈 때 메시지를 전송합니다.
    """
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"{member.mention}님이 나갔습니다.")

@bot.command(name='commands_list')
async def commands_list(ctx):
    """
    봇의 명령어 목록을 보여줍니다.
    """
    help_message = (
        "K-POP Info Bot 명령어 목록\n"
        "`/artist <아티스트 이름>`: 특정 아티스트의 정보를 검색합니다.\n"
        "`/rank <platform>`: Spotify 또는 YouTube 팔로워 순위를 표시합니다.\n"
        "`/commands_list`: 이 도움말을 표시합니다."
    )
    await ctx.send(help_message)


@bot.command()
async def artist(ctx, *, artist_name):
    """
    아티스트 정보를 검색하여 Spotify와 YouTube 팔로워 및 링크 제공
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT a.name, a.followers, sm.youtube, sm.youtube_followers, sm.twitter, sm.instagram
        FROM artists a
        LEFT JOIN social_media sm ON a.social_id = sm.id
        WHERE a.name = ?
    """, (artist_name,))
    artist = cursor.fetchone()
    conn.close()

    if artist:
        name, spotify_followers, youtube_link, youtube_followers, twitter_link, instagram_link = artist
        response = (
            f"**{name}**\n"
            f"Spotify Followers: {spotify_followers}\n"
            f"YouTube Followers: {youtube_followers}\n"
            f"YouTube: {youtube_link or 'N/A'}\n"
            f"Twitter: {twitter_link or 'N/A'}\n"
            f"Instagram: {instagram_link or 'N/A'}"
        )
    else:
        response = f"아티스트 '{artist_name}' 정보를 찾을 수 없습니다."

    await ctx.send(response)

@bot.command()
async def rank(ctx, platform):
    """
    Spotify 또는 YouTube 팔로워 순위를 높은 순서로 표시
    """
    if platform not in ["spotify", "youtube"]:
        await ctx.send("지원되는 플랫폼은 'spotify' 또는 'youtube'입니다.")
        return

    try:
        conn = sqlite3.connect("data/kpop.db")
        cursor = conn.cursor()

        if platform == "spotify":
            cursor.execute("""
                SELECT name, followers
                FROM artists
                ORDER BY followers DESC
                LIMIT 100
            """)
        else:  # platform == "youtube"
            cursor.execute("""
                SELECT a.name, sm.youtube_followers
                FROM artists a
                JOIN social_media sm ON a.social_id = sm.id
                ORDER BY sm.youtube_followers DESC
                LIMIT 100
            """)

        ranks = cursor.fetchall()
        conn.close()

        if not ranks:
            await ctx.send(f"{platform.capitalize()} 데이터가 없습니다.")
            return

        # 메시지를 2000자 이하로 나누어 전송
        response = f"**Top 100 {platform.capitalize()} Followers**\n"
        chunks = []
        for i, (name, followers) in enumerate(ranks, start=1):
            line = f"{i}. {name} - {followers}\n"
            if len(response) + len(line) > 2000:
                chunks.append(response)
                response = ""
            response += line
        chunks.append(response)  # 마지막 남은 메시지 추가

        for chunk in chunks:
            await ctx.send(chunk)

    except sqlite3.Error as e:
        await ctx.send(f"데이터베이스 오류가 발생했습니다: {e}")
    except Exception as e:
        await ctx.send(f"오류가 발생했습니다: {e}")

# 스케줄러 작업
def daily_update():
    print("[INFO] Starting daily update...")
    try:
        update_followers()  # Spotify 팔로워 업데이트
        update_youtube_subscribers()  # YouTube 구독자 업데이트
        print("[INFO] Daily update completed successfully.")
    except Exception as e:
        print(f"[ERROR] An error occurred during daily update: {e}")

# 스케줄러 실행 함수
def run_scheduler():
    schedule.every().day.at("00:00").do(daily_update)  # 매일 자정 실행
    print("[INFO] Scheduler started. Waiting for tasks...")
    while True:
        schedule.run_pending()
        time.sleep(1)

# 스케줄러를 별도 스레드에서 실행
scheduler_thread = Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# 봇 실행
bot.run(DISCORD_BOT_TOKEN)
