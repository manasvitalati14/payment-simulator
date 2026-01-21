# Deploying PaySim to Vercel

## ⚠️ Critical Warning: Database
Vercel is a "Serverless" platform with a **read-only filesystem**. 
- **SQLite (`site.db`) will NOT work** for persistent data. You might be able to register, but your account will vanish after a few minutes when the server sleeps.
- **Solution**: You MUST use an external Database like **Neon (Postgres)**, **Supabase**, or **PlanetScale**.

## Step 1: Get a Persistent Database (Free)
1.  Go to [Neon.tech](https://neon.tech) or [Supabase.com](https://supabase.com) and create a free project.
2.  Get the **Connection String** (URL). It looks like: `postgres://user:pass@ep-xyz.region.neon.tech/neondb`

## Step 2: Push Code to GitHub
1.  Initialize Git in your folder:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on [GitHub](https://github.com/new).
3.  Push your code:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    git push -u origin master
    ```

## Step 3: Deploy on Vercel
1.  Go to [Vercel.com](https://vercel.com) and sign up/login.
2.  Click **"Add New..."** -> **"Project"**.
3.  Select your GitHub repository (`payment_simulator`).
4.  **Configure Project**:
    - **Framework Preset**: Other (default is fine, it usually detects Python or you leave it).
    - **Environment Variables**:
      - Name: `DATABASE_URL`
      - Value: *(Paste your Postgres Connection String from Step 1)*
      - Name: `SECRET_KEY`
      - Value: *(Type a random long string for security)*
5.  Click **Deploy**.

## Debugging
- If the deployment fails, check the "Logs" tab in Vercel.
- Ensure your `requirements.txt` is present (it is included in this project).
