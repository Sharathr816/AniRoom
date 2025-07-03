# 🌸 AniRepo — The AI-Powered Social Platform for Anime Lovers

AniRepo is a smart, AI-enhanced anime content hub built for true anime lovers.  
Upload anime content (no live-actions), discover gems through AI-powered tagging, and soon — chat with others who vibe with your taste.

---

## 🌟 Core Features

- 🔐 **User Auth** — Register, log in, and manage your own anime content.
- 📥 **Content Upload** — Upload anime images, descriptions, clips (no live-action).
- 🧠 **AI Tagging** — Hugging Face models auto-tag uploads based on anime genre/content.
- 🔍 **Smart Search** — Find anime using title, tags, or descriptions.

---

## 🧪 Under Development (Coming Soon)

- 🧵 **WebSocket-Powered Anime Rooms** — Real-time chat for users with similar taste.
- 🧠 **Recommendation Engine** — Suggest anime based on what users love.
- 🎨 **Anime Playlists/Folders** — Save and share anime collections (SQL for now, NoSQL later if needed).
- 🚫 **Live-Action Blocker** — Upload filter powered by custom-trained AI to avoid non-anime content.

---

## 💻 Tech Stack

- Backend: **Django**
- Frontend: **HTML/CSS/JS**
- AI: **Hugging Face Transformers**
- DB: **SQLite (dev)** → **PostgreSQL (prod)**  
- Realtime: **Django Channels (WebSocket)** (planned)
- Deployment: **Render / Railway / Vercel**

---

## 🚀 MVP Milestones

| Feature | Status |
|--------|--------|
| User Auth | ✅ Done |
| Upload Anime | 🛠️ In Progress |
| AI Tagging | 🛠️ Next |
| Smart Search | 🔜 Soon |

---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/yourusername/anirepo.git
cd anirepo
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

