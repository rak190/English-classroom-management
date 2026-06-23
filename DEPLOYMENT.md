# ECMS Step-by-Step Deployment Guide

This guide will walk you through exactly how to publish your English Class Management System to the internet using **Render.com**. Render is a free and reliable cloud hosting provider that works perfectly with Django.

## Step 1: Prepare Your Code (GitHub)
You need to put your code on GitHub so Render can read it.

1. Create an account at [GitHub.com](https://github.com/).
2. Create a **New Repository**. Name it `ecms` (or anything you like). Leave it as Public or Private. Do **NOT** initialize it with a README.
3. Open your terminal in VS Code (where your `Eng_classroom_management` folder is).
4. Run these exact commands one by one to push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for deployment"
   git branch -M main
   # IMPORTANT: Replace the URL below with the URL of your new GitHub repository
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## Step 2: Create a PostgreSQL Database (Render)
Render requires a production database. We will use their free PostgreSQL service.

1. Create a free account at [Render.com](https://render.com/).
2. Click **New +** and select **PostgreSQL**.
3. Fill out the form:
   - **Name**: `ecms-db`
   - **Region**: Choose the one closest to you (e.g., Singapore).
   - **Instance Type**: Free
4. Click **Create Database**.
5. Once it's created, look for the **"Internal Database URL"** (it starts with `postgresql://`). **Copy this link**.

## Step 3: Publish the Web App (Render)
Now we host the actual Django code.

1. Click **New +** and select **Web Service**.
2. Connect your GitHub account and select your `ecms` repository.
3. Fill out the form EXACTLY like this:
   - **Name**: `ecms-app` (this will be part of your live URL!)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn ecms_project.wsgi:application`
   - **Instance Type**: Free

## Step 4: Add Environment Variables
Scroll down to the **Advanced** section and click **Add Environment Variable**. You need to add exactly 4 variables:

1. **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.4` (Or whatever version you are using locally)
2. **Key**: `DEBUG`
   - **Value**: `False`
3. **Key**: `DATABASE_URL`
   - **Value**: *(Paste the Internal Database URL you copied in Step 2)*
4. **Key**: `SECRET_KEY`
   - **Value**: *(Click the "Generate" button to make a random secure password)*
5. **Key**: `GEMINI_API_KEY`
   - **Value**: *(Paste your Gemini API key here)*

## Step 5: Deploy!
Click **Create Web Service**. 
Render will now read your `build.sh` script, install Django, run the migrations, and start your server. It usually takes about 3-5 minutes.

Once it says "Live", click the URL at the top left of the dashboard. Your site is now on the internet!

---

### Important Note on Creating Your First Account
Because you are using a brand new database on Render, there are no users yet! You won't be able to log in to the live site until you create a teacher account.

To do this:
1. On your Render Web Service dashboard, click on the **Shell** tab (this gives you a terminal inside the cloud server).
2. Type this command and hit enter:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow the prompts to enter a username, email (optional), and password.
4. Go back to your live URL and log in with those credentials!
