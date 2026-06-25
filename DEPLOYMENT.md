# The Ultimate ECMS Deployment Guide (Vercel & Neon)

This guide provides foolproof, step-by-step instructions to get your English Classroom Management System (ECMS) live on the internet. 

Because we are deploying to **Vercel** (a serverless environment) and **Neon** (a cloud database), it is completely free, but you must follow these steps **exactly in order**.

---

## 🛑 Important Concepts to Understand First
1. **Vercel is Read-Only**: Once your app is live on Vercel, it cannot write to local files. This means the default `db.sqlite3` database **will crash your app**.
2. **You MUST use Neon**: You must connect your Vercel app to an external PostgreSQL database (Neon) to store your data.
3. **Environment Variables**: Whenever you add or change an environment variable (like your database connection string) in Vercel, **it will not take effect until you manually click "Redeploy".**

---

## Step 1: Put Your Code on GitHub
Vercel needs to pull your code from a GitHub repository to build your app.

1. Go to [GitHub.com](https://github.com/) and log in or create an account.
2. Click **New Repository** (the `+` icon in the top right).
3. Name it `English-classroom-management` (or anything you prefer).
4. **CRITICAL:** Do NOT check the box that says "Add a README file". Leave the repository completely blank. Click **Create repository**.
5. Open your terminal in VS Code (where your project folder is open).
6. Run these exact commands to push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   git branch -M main
   # IMPORTANT: Replace the URL below with YOUR actual GitHub repository URL
   git remote add origin https://github.com/rak190/English-classroom-management
   git push -u origin main
   ```

---

## Step 2: Create Your Free Cloud Database (Neon)
Since Vercel cannot use SQLite, we must use Neon for our database.

1. Go to [Neon.tech](https://neon.tech/) and create a free account.
2. Click **Create a project**.
3. Fill out the project details:
   - **Name**: `ecms-db`
   - **Database Version**: 15 or 16
   - **Region**: Choose the one closest to you (e.g., Singapore for Southeast Asia).
4. Click **Create project**.
5. You will see a popup with your **Connection Details**.
6. Ensure the dropdown is set to **Connection string** (or Postgres) and click the **Copy icon**.
   - *Example of what it looks like:* `postgresql://neondb_owner:RandomPassword123@ep-cool-butterfly-a1bcdef.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`
7. **Paste this string somewhere safe (like a notepad). You will need it in Step 4.**

---

## Step 3: Connect Vercel to Your GitHub
Now we will tell Vercel to host the code from GitHub.

1. Go to [Vercel.com](https://vercel.com/) and log in using your GitHub account.
2. Go to your Dashboard, click **Add New...** and select **Project**.
3. You will see a list of your GitHub repositories. Find `English-classroom-management` and click **Import**.
4. You will be taken to the "Configure Project" screen.
   - Leave the **Framework Preset** as "Other".
   - Leave the **Root Directory** as `./`.
5. **DO NOT CLICK DEPLOY YET!** Proceed directly to Step 4.

---

## Step 4: Add Environment Variables (CRITICAL)
Before you deploy, you must give Vercel your Database URL so it knows where to save your data.

1. On the "Configure Project" screen, click to expand the **Environment Variables** section.
2. You need to add **two** exact variables:

   **Variable 1 (To turn off debug mode):**
   - **Key**: `DEBUG`
   - **Value**: `False`
   - Click **Add**.

   **Variable 2 (Your Neon Database):**
   - **Key**: `DATABASE_URL`
   - **Value**: *(Paste the exact URL you copied from Neon in Step 2)*
   - Click **Add**.

3. Now, finally, click the large **Deploy** button.
4. Wait about 1-2 minutes for Vercel to finish building your application.

---

## Step 5: The "Setup Database" Trick
If you visit your live Vercel URL right now, you might see an error, or if you try to log in, you won't have an account. Why? Because your new Neon database is **completely empty**. It has no tables and no users.

To fix this automatically:
1. Go to your Vercel Dashboard and click on your newly deployed project to find its live URL (e.g., `https://english-classroom-management.vercel.app/`).
2. Add `/setup/` to the very end of your URL and press Enter.
   - Example: `https://english-classroom-management.vercel.app/setup/`
3. The screen will say "Starting database migrations..."
4. Wait a few seconds. The page will eventually say: **Setup complete! You can now go to /accounts/login/ and login with admin / admin123**.
5. This script just built all your database tables for you and created an Administrator account!

---

## 🛠️ Troubleshooting (The Vercel 500 Error)

**Problem:** "I added my `DATABASE_URL` to Vercel, but I still see a 500 Server Error!"

**Why this happens:** When you add a new environment variable to a project that is *already deployed*, Vercel does not automatically restart the app. The running app still has no idea the variable exists.

**The Fix:** You must manually trigger a **Redeploy**.
1. Open your project on the Vercel Dashboard.
2. Click the **Deployments** tab at the top of the screen.
3. Find the most recent deployment at the top of the list.
4. Click the **three vertical dots (⋮)** on the right side of that deployment row.
5. Click **Redeploy** (Do not click Promote to Production, click Redeploy).
6. A popup will appear. Check the box if it asks about using existing build cache, and click **Redeploy**.
7. Wait 1 minute for the new build to finish.
8. Your environment variable is now active! Return to Step 5 to run `/setup/`.
