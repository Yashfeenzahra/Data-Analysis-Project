# How to put this on Streamlit and get your live URL

You have 3 files: `app.py`, `requirements.txt`, `netflix_titles.csv`. They all need to sit in the **same folder/repo**. Steps below — no prior Streamlit knowledge needed, takes about 10 minutes.

## Step 1: Get a GitHub account (skip if you have one)
Go to **github.com** → Sign up. Free.

## Step 2: Create a new repository
1. Click the **+** icon (top right) → **New repository**
2. Name it anything, e.g. `netflix-dashboard`
3. Set it to **Public**
4. Click **Create repository**

## Step 3: Upload your files
1. On the new repo page, click **"uploading an existing file"** (or "Add file" → "Upload files")
2. Drag in all 3 files: `app.py`, `requirements.txt`, `netflix_titles.csv`
3. Scroll down, click **Commit changes**

## Step 4: Deploy on Streamlit Community Cloud (free)
1. Go to **share.streamlit.io**
2. Click **Sign in** → sign in with your GitHub account → authorize it
3. Click **"Create app"** (or "New app")
4. Pick:
   - Repository: the one you just made (`yourname/netflix-dashboard`)
   - Branch: `main`
   - Main file path: `app.py`
5. Click **Deploy**

## Step 5: Wait and grab your URL
It'll spin for 1–3 minutes installing packages. When it's done, your app opens automatically. The URL in your browser bar (something like `https://yourname-netflix-dashboard.streamlit.app`) is your **live demo URL** — copy that and submit it.

---

### If something goes wrong
- **"File not found: netflix_titles.csv"** → make sure the CSV was actually uploaded to the repo root (not in a subfolder).
- **Build/install error** → open "Manage app" → "Logs" on Streamlit Cloud to see the error message; it's almost always a typo in `requirements.txt`.
- App looks fine locally-style but blank online → click "Reboot app" in the Streamlit Cloud dashboard.

That's it — no command line, no installs on your own machine required.
