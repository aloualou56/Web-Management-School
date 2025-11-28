# GitHub Actions Attendance Automation Setup

This guide explains how to set up automatic attendance generation using GitHub Actions (100% free).

## How It Works

- GitHub Actions runs a cron job every 5 minutes (free tier: 2,000 minutes/month)
- It calls your Django app via HTTP to trigger attendance commands
- No background worker needed on Render
- Completely free solution

## Setup Steps

### 1. Add Secrets to GitHub Repository

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these two secrets:

1. **RENDER_APP_URL**
   - Name: `RENDER_APP_URL`
   - Value: Your Render app URL (e.g., `https://your-app.onrender.com`)
   - Do NOT include trailing slash

2. **ATTENDANCE_API_TOKEN**
   - Name: `ATTENDANCE_API_TOKEN`
   - Value: A random secure token (generate one below)

**Generate a secure token:**
```bash
# On Linux/Mac:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use any random string generator
```

### 2. Update Render Environment Variables

In your Render dashboard → Your Service → Environment:

Add:
- **ATTENDANCE_API_TOKEN** = (same token you used in GitHub secrets)

### 3. Deploy to Render

The changes will be automatically deployed. The workflow will start running every 5 minutes.

### 4. Test the Setup

#### Manual Test via Browser/Postman:
```bash
curl -X POST https://your-app.onrender.com/api/trigger-attendance-generation/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Manual Trigger via GitHub:
1. Go to Actions tab in GitHub
2. Click "Attendance Automation"
3. Click "Run workflow"
4. Check the logs

## Monitoring

### Check GitHub Actions Logs:
- Go to your repository → Actions tab
- Click on any workflow run to see logs
- You should see successful responses every 5 minutes

### Check Render Logs:
- Go to Render dashboard → Your service → Logs
- You should see attendance generation messages

## Troubleshooting

### Workflow fails with 401 Unauthorized:
- Check that ATTENDANCE_API_TOKEN matches in both GitHub secrets and Render env vars
- Make sure the token doesn't have extra spaces

### Workflow fails with 404:
- Check that RENDER_APP_URL is correct
- Make sure there's no trailing slash

### Attendance not generating:
- Check that your grades have correct schedule (weekdays, class_time, or reset_time)
- Verify students are assigned and active
- Check Render logs for any errors

## Cost

- ✅ GitHub Actions: 2,000 minutes/month free (you'll use ~150 minutes/month)
- ✅ Render: Free tier
- ✅ Total: $0/month

## How to Disable

If you need to temporarily disable:
1. Go to `.github/workflows/attendance-automation.yml`
2. Comment out or remove the `schedule` section
3. Commit and push

Or delete the workflow file entirely.
