# 🧿 AniRoom — The 2D-Only Social Chill Zone

AniRoom is a WebSocket-powered social platform where people connect through 2D-themed content — anime, animation, or stylized art.  
It’s your escape from reality: chill, share what’s inside, and find people who vibe with your world.

---


## 🔩 Core Features

- **Real-Time Room Chat** – Powered by WebSockets for instant communication.
- **User Profiles** – Create and customize your identity.
- **Public Room Hosting** – Anyone can create a room around a theme.
- **Media Sharing** – Share anime posters, trailers, and more.
- **Room-Based Discussions** – Post, comment, and vibe around 2D content.
- **Search & Discover Rooms** – Find active rooms by tags or titles.
- **Authentication** – Register/login system using Django’s auth framework.

---

## 🧪 Under Development (Coming Soon)

- 🧵 **Anime-Based Room Matching** — Automatically suggest or create chat rooms based on user animation preferences.
- 🧠 **Recommendation Engine** — Suggest animations based on what users love.
- 🎨 **Playlists/Folders** — Save and share collections (SQL for now, NoSQL later if needed).
- 🚫 **Live-Action Blocker** — Upload filter powered by custom-trained AI to avoid non-animated content(only images).

---

## 💻 Tech Stack

- Backend: **Django**
- Frontend: **HTML/CSS/JS**
- AI: **Hugging Face Transformers**
- DB: **SQLite (dev)** → **PostgreSQL (prod)**  
- Realtime: **Django Channels (WebSocket)**
- Deployment: **Render / Railway / Vercel**

---

## 🚀 MVP Milestones

| Feature | Status |
|--------|--------|
| User Auth | ✅ Done |
| Upload Anime | ✅ Done |
| Room Chat (WebSocket) | 🛠️ In Progress |
| AI Tagging | 🛠️ Next |
| Smart Search | 🔜 Soon |
| Profiles | 🔜 Soon |

---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/yourusername/aniroom.git
cd aniroom
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
