import sqlite3

def initialize_database():
    """
    데이터베이스 초기화
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()

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
        youtube_followers INTEGER
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
    소셜 미디어 정보를 저장하고 social_id를 반환
    """
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO social_media (twitter, instagram, youtube, twitter_followers, instagram_followers, youtube_followers)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (social_links["twitter"], social_links["instagram"], social_links["youtube"],
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
