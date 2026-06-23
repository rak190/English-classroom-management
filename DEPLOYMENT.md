# ECMS Step-by-Step Deployment Guide

This guide will walk you through exactly how to publish your English Class Management System to the internet using **Vercel** and **Neon**. Vercel is an excellent serverless hosting provider, and Neon provides a free, incredibly easy-to-use PostgreSQL database perfectly suited for Django.

## Step 1: Prepare Your Code (GitHub)
You need to put your code on GitHub so Vercel can read it.

1. Create an account at [GitHub.com](https://github.com/).
2. Create a **New Repository**. Name it `ecms` (or anything you like). Leave it as Public or Private. Do **NOT** initialize it with a README.
3. Open your terminal in VS Code (where your `Eng_classroom_management` folder is).
4. Run these exact commands one by one to push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for deployment to Vercel"
   git branch -M main
   # Your specific GitHub repository:
   git remote add origin https://github.com/rak190/English-classroom-management
   git push -u origin main
   ```

## Step 2: Create a PostgreSQL Database (Neon)
Vercel's environment requires a production database. We will use Neon's free serverless PostgreSQL service because it is incredibly simple and doesn't have the IPv4/IPv6 pooling issues.

1. Create a free account at [Neon.tech](https://neon.tech/).
2. Click **Create a project**.
3. Fill out the form:
   - **Name**: `ecms-db`
   - **Database Version**: 15 or 16
   - **Region**: Choose the one closest to you (e.g., Singapore).
4. Click **Create project**.
5. Once your project is created, you will see a **Connection Details** box right on the dashboard.
6. Make sure the dropdown is set to **Postgres** (or Connection String) and click the "Copy" icon. 
7. The link you copied will look something like this: `postgresql://neondb_owner:RandomPassword123@ep-cool-butterfly-a1bcdef.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`. **This is your `DATABASE_URL`**.

## Step 3: Publish the Web App (Vercel)
Now we host the actual Django code on Vercel.

1. Create a free account at [Vercel.com](https://vercel.com/) and log in with your GitHub account.
2. Click **Add New...** and select **Project**.
3. Import your `English-classroom-management` repository from GitHub.
4. In the **Configure Project** section, open **Build and Output Settings**.
   - Override the **Build Command** and type:
     ```bash
     python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - (Leave the Output Directory as is, Vercel will handle the `api/index.py` serverless functions automatically due to our `vercel.json`).

## Step 4: Add Environment Variables
Before clicking Deploy, expand the **Environment Variables** section. You need to add exactly 4 variables:

1. **Key**: `DEBUG`
   - **Value**: `False`
2. **Key**: `DATABASE_URL`
   - **Value**: *(Paste the full Neon Connection String you copied in Step 2)*
3. **Key**: `SECRET_KEY`
   - **Value**: *(Type a long random string of letters, numbers, and symbols)*
4. **Key**: `GEMINI_API_KEY`
   - **Value**: *(Paste your Gemini API key here)*

## Step 5: Deploy!
Click **Deploy**. 
Vercel will now install your packages, collect static files, run the database migrations on Neon, and deploy your serverless functions.

Once it says "Congratulations!", click to go to your dashboard, and click your live domain (e.g., `ecms.vercel.app`). Your site is now on the internet!

---

### Important Note on Creating Your First Account
Because you are using a brand new database on Neon, there are no users yet! You won't be able to log in to the live site until you create a teacher account.

To do this locally connected to your live database:
1. Open your local VS Code terminal.
2. Run this command to connect your local Django to the Neon database (replace the URL with your exact Neon URL):
   ```bash
   # On Windows PowerShell:
   $env:DATABASE_URL="postgresql://neondb_owner:YOUR_PASSWORD@ep-cool-butterfly-a1bcdef.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
   ```
3. Then run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow the prompts to enter a username, email (optional), and password.
5. Go back to your live Vercel URL and log in with those credentials!

> **Warning about File Uploads:** Vercel uses a serverless, read-only file system. Any files (like student photos or materials) uploaded through the site will not be permanently saved. In the future, you should configure an external storage bucket (like AWS S3 or Supabase Storage) to handle media file uploads permanently.
