# E-Commerce Sales Dashboard (Streamlit)

An interactive web dashboard version of your `ecommerce_analysis.ipynb` notebook.
Upload a raw sales CSV and it will clean the data and show revenue, category,
payment method, order status, top products, and a daily sales trend — all in
the browser, no VS Code needed.

## Files
- `app.py` — the Streamlit app
- `requirements.txt` — Python packages needed to run it

## Option A: Run it locally first (recommended to test)

1. Install Python 3.9+ if you don't have it.
2. Open a terminal in this folder and install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. It opens automatically in your browser at `http://localhost:8501`.
   Upload your CSV there to test it.

## Option B: Deploy for free on Streamlit Community Cloud

This gives you a public URL (e.g. `https://your-app-name.streamlit.app`) that
anyone can open — no install needed on their end.

### Step 1 — Put this project on GitHub
1. Go to [github.com](https://github.com) and create a free account if you don't have one.
2. Create a new **public** repository, e.g. `ecommerce-sales-dashboard`.
3. Upload `app.py` and `requirements.txt` to that repository
   (GitHub's web UI has an "Add file → Upload files" button — no command line needed).

### Step 2 — Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository, branch (`main`), and set the main file path to `app.py`.
4. Click **"Deploy"**.
5. Wait 1–2 minutes while it installs dependencies and starts your app.
6. You'll get a public link you can share with anyone — they just visit the
   link, upload their CSV, and see the dashboard. No coding or installs needed
   on their side.

### Updating the app later
Any time you push changes to `app.py` in your GitHub repo, Streamlit Community
Cloud automatically redeploys the updated version within a minute or two.

## Notes
- The app expects columns similar to your original dataset: `Order_Date`,
  `Quantity`, `Price`, `Category`, `Total`, `Payment_Method`, `Status`, `Product`.
  It gracefully skips any chart if a required column is missing.
- The cleaning logic (currency symbol stripping, missing value handling,
  duplicate removal) mirrors exactly what your notebook does.
- If you later want the sales-prediction (RandomForest) feature added to this
  same dashboard, that can be a second page/tab in the app.
