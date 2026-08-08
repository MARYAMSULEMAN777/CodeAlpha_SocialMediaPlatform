# SocialMediaProject (Thread)

**CodeAlpha Full Stack Development Internship — Task 2: Social Media Platform**

A full-stack mini social media app: user profiles, posts with photos, likes, comments, and a follow system.

## Tech Stack
- **Backend:** Django 5
- **Database:** SQLite (single file, no separate DB server needed)
- **Frontend:** Django templates + vanilla CSS/JS (AJAX for likes and comments — no page reloads)
- **Media:** Pillow for image uploads (profile pictures, post photos)

## Features
- Register / login / logout
- Editable profile: bio + profile photo
- Create posts with a photo, caption, or both
- Like/unlike posts instantly via AJAX (no page reload)
- Comment on posts instantly via AJAX
- Follow / unfollow other users
- Two feed views: **All Posts** and **Following**
- Followers / following lists per profile
- Search for people (username/bio) and posts (caption)
- Edit or delete your own posts

## Project Structure
```
SocialMediaProject/
├── manage.py
├── requirements.txt
├── SocialMediaProject/        # project settings, urls, wsgi/asgi
├── users/                     # Profile model, auth, profile pages
├── posts/                     # Post/Comment/Like models, feed, detail, search
├── followers/                 # Follow model, follow/unfollow, followers/following lists
├── templates/base.html        # shared layout (navbar, messages)
├── static/                    # global css/js
└── media/                     # uploaded profile pics & post images (created at runtime)
```

## Setup & Run Locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

## Notable Design Decisions
- Profile pictures are optional — users without one get a colored initial-letter avatar instead of a broken image link.
- A post needs either a photo or a caption (or both) — empty posts are rejected server-side.
- The `Follow` model has a database constraint preventing a user from following themselves.
- Likes use a `unique_together` constraint so a user can only like a post once; the like button is a toggle.

## Submission Checklist (per CodeAlpha instructions)
- [ ] Push this folder to a **public** GitHub repo named `CodeAlpha_SocialMediaPlatform`
- [ ] Post your internship status on LinkedIn, tagging **@CodeAlpha**
- [ ] Record a short video walking through the app (register → post → like → comment → follow), post it on LinkedIn with the GitHub link
- [ ] Submit through the CodeAlpha submission form shared in your WhatsApp group
