# K-POP Artist Follower Tracker

A Python-based project to track K-POP artists' Spotify and YouTube followers and provide their social media links. This project integrates a Discord bot for user interaction and a scheduler for automated daily updates.

---

## Features

- **Spotify and YouTube Follower Updates**:
  - Automatically updates Spotify and YouTube followers daily.
  - Provides accurate, up-to-date data.

- **Discord Bot Integration**:
  - Retrieve artist information via Discord commands.
  - Commands:
    - `/artist <name>`: Display Spotify and YouTube follower counts, along with social media links.
    - `/rank <platform>`: Display top 100 artists ranked by followers for Spotify or YouTube.

- **Daily Scheduler**:
  - Automated updates every 24 hours for Spotify and YouTube followers.

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Clone the Repository
```bash
# Clone the repository
git clone <repository-url>
cd <repository-folder>
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up Environment Variables
1. Create a `.env` file in the project root.
2. Add the following:
   ```plaintext
   DISCORD_BOT_TOKEN=your_discord_bot_token
   YOUTUBE_API_KEY=your_youtube_api_key
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   ```

---

## Usage

### Database Initialization and Data Collection
To initialize the database and fetch artist and social media data, run:
```bash
python main.py 
```
This will:
- Initialize the SQLite database.
- Fetch all artists and their social media data (Spotify, YouTube, Twitter, Instagram).
- Save the data to the database.

### Update Follower Counts
To update the follower counts for all artists in the database, use:
```bash
python main.py update
```
This wil:
- fetch the latest follower counts for Spotify artists stored in the database. 

### Update YouTube Subscribers
To update YouTube subscribers for all artists with YouTube channels, run:
```bash
python main.py youtube
```
This will:
- Fetch the latest YouTube subscriber count for artists with valid YouTube channels.

### Run the Discord BOt
```bash
python bot_with_scheduler.py
```

### Discord Commands
1. `/artist <name>`
   - Example: `/artist BTS`
   - Returns:
     - Spotify and YouTube follower counts.
     - Links to YouTube, Twitter, and Instagram profiles.

2. `/rank <platform>`
   - Example: `/rank spotify`
   - Returns the top 100 artists ranked by Spotify or YouTube followers.

---

## Limitations

- **Server Deployment**:
  - Due to time constraints, the project is not hosted on a remote server.
  - Instead, it runs locally and requires the host computer to remain powered on.

- **Future Improvements**:
  - Host the project on a cloud platform like Heroku or AWS for 24/7 uptime.
  - Extend the functionality to include Twitter and Instagram follower updates.

---

## Project Structure
```plaintext
.
├── bot_with_scheduler.py    # Main script for Discord bot and scheduler integration
├── spotify_api.py           # Spotify API interaction
├── youtube_api.py           # YouTube API interaction
├── db_manager.py            # SQLite database management
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (excluded from Git)
├── data/
│   └── kpop.db              # SQLite database file
└── README.md                # Project documentation
```

---

## Contributors
- **Your Name**: Project developer and maintainer.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
- Inspired by various open-source projects and the K-POP fan community.

---

## References

Here are some references that were helpful during the development of this project:

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/)
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Discord.py Documentation](https://discordpy.readthedocs.io/en/stable/)
- [Schedule Python Library](https://schedule.readthedocs.io/en/stable/)
- [SQLite Official Documentation](https://www.sqlite.org/docs.html)

---

## Screenshots

### 1. `/commands_list`
Displays the list of available commands.

![Commands List](./스크린샷%202024-12-11%20234004.png)

### 2. `/artist <name>`
Displays detailed information about a specific artist.

![Artist Command](./스크린샷%202024-12-11%20234032.png)

### 3. `/rank spotify`
Lists the top 100 artists by Spotify followers.

![Rank Spotify](./스크린샷%202024-12-11%20234052.png)

### 4. `/rank youtube`
Lists the top 100 artists by YouTube followers.

![Rank YouTube](./스크린샷%202024-12-11%20234112.png)

---

## Demo video
[![Video Link](http://img.youtube.com/vi/n7qgDWUe3pA/0.jpg)](https://youtu.be/n7qgDWUe3pA)

