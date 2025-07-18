# 🌸 AniRoom — The AI-Powered Community for Anime Enthusiasts

AniRoom is a smart, real-time social platform tailored for animation lovers. 
Upload and explore contents (excluding live-action), discover hidden gems, chat live with others in anime-themed rooms, and manage your own profile hub.

---

## 🌟 Core Features

- 🔐 **User Auth** — Register, log in, and manage your own rooms.
- 📥 **Content Upload** — Upload animated images, descriptions, clips.
- 🧠 **AI Tagging** — Hugging Face models auto-tag uploads based on anime genre/content.
- 🔍 **Smart Search** — Find anime using title, tags, or descriptions.
- 💬 **WebSocket-Powered Room Chat** — Real-time group chat inside animation-themed rooms.
- 🙋‍♂️ **User Profiles** — Each user gets a customizable profile with their uploads, likes, and room activity.

---

## 🧪 Under Development (Coming Soon)

- 🧵 **Anime-Based Room Matching** — Automatically suggest or create chat rooms based on user animation preferences.
- 🧠 **Recommendation Engine** — Suggest anime based on what users love.
- 🎨 **Anime Playlists/Folders** — Save and share anime collections (SQL for now, NoSQL later if needed).
- 🚫 **Live-Action Blocker** — Upload filter powered by custom-trained AI to avoid non-anime content.

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
