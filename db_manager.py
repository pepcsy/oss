import sqlite3

def initialize_database():
    """
    데이터베이스 초기화
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()

    # 기존 데이터 삭제
    cursor.execute("DROP TABLE IF EXISTS artists")
    cursor.execute("DROP TABLE IF EXISTS social_media")
    cursor.execute("DROP TABLE IF EXISTS daily_followers")

    # Artists 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        spotify_id TEXT,
        genres TEXT,
        followers INTEGER,
        social_id INTEGER,
        FOREIGN KEY(social_id) REFERENCES social_media(id)
    )
    """)

    # Social Media 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS social_media (
        id INTEGER PRIMARY KEY,
        twitter TEXT,
        instagram TEXT,
        youtube TEXT,
        twitter_followers INTEGER,
        instagram_followers INTEGER,
        youtube_followers INTEGER,
        UNIQUE(twitter, instagram, youtube) -- 중복 방지
    )
    """)

    # Daily Followers 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_followers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist_id INTEGER,
        platform TEXT, -- 'spotify' 또는 'youtube'
        date DATE DEFAULT (DATE('now')),
        followers INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
    )
    """)

    conn.commit()
    conn.close()

def save_artist_to_db(artist):
    """
    Artists 테이블에 아티스트 정보를 저장
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO artists (name, spotify_id, genres, followers)
    VALUES (?, ?, ?, ?)
    """, (artist["name"], artist["id"], ", ".join(artist["genres"]), artist["followers"]))
    conn.commit()
    conn.close()

def save_social_media_to_db(social_links):
    """
    소셜 미디어 정보를 저장하고 중복된 경우 기존 ID를 반환
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()

    # 중복 데이터 확인
    cursor.execute("""
    SELECT id FROM social_media 
    WHERE twitter = ? AND instagram = ? AND youtube = ?
    """, (social_links.get("twitter"), social_links.get("instagram"), social_links.get("youtube")))

    result = cursor.fetchone()
    if result:
        social_id = result[0]
    else:
        # 중복이 아닐 경우 데이터 삽입
        cursor.execute("""
        INSERT INTO social_media (twitter, instagram, youtube, twitter_followers, instagram_followers, youtube_followers)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (social_links.get("twitter"), social_links.get("instagram"), social_links.get("youtube"),
              social_links.get("twitter_followers"), social_links.get("instagram_followers"), social_links.get("youtube_followers")))
        social_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return social_id

def update_artist_social_id(artist_name, social_id):
    """
    Artists 테이블에 social_id를 업데이트
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE artists
    SET social_id = ?
    WHERE name = ?
    """, (social_id, artist_name))
    conn.commit()
    conn.close()

def update_followers_in_db(artist_name, platform, followers):
    """
    데이터베이스에서 특정 아티스트의 팔로워 수 업데이트
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    if platform == "spotify":
        cursor.execute("""
        UPDATE artists
        SET followers = ?
        WHERE name = ?
        """, (followers, artist_name))
    elif platform in ("youtube", "twitter", "instagram"):
        column_name = f"{platform}_followers"
        cursor.execute(f"""
        UPDATE social_media
        SET {column_name} = ?
        WHERE id = (SELECT social_id FROM artists WHERE name = ?)
        """, (followers, artist_name))
    conn.commit()
    conn.close()

def save_daily_followers(artist_id, platform, followers):
    """
    Daily Followers 테이블에 하루 팔로워 데이터를 저장
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO daily_followers (artist_id, platform, date, followers)
    VALUES (?, ?, DATE('now'), ?)
    """, (artist_id, platform, followers))
    conn.commit()
    conn.close()
