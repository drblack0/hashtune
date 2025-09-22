# Render Deployment Steps

## Prerequisites
1. Create a [Render account](https://render.com)
2. Connect your GitHub repository to Render
3. Ensure your code is pushed to GitHub

## Deployment Process

### Step 1: Deploy Backend (Web Service)

1. **Go to Render Dashboard**
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Connect your `hashtune` repository
   - Select the repository

3. **Configure Backend Service**
   - **Name**: `hashtune-backend`
   - **Environment**: `Docker`
   - **Region**: Choose closest to your users
   - **Branch**: `master` (or your main branch)
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.`

4. **Environment Variables**
   - `PORT`: Will be auto-set by Render
   - `FLASK_ENV`: `production`
   - `PYTHONPATH`: `/app`
   - Add any API keys your backend needs

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - **Note the URL** (e.g., `https://hashtune-backend.onrender.com`)

### Step 2: Deploy Frontend (Static Site)

1. **Go to Render Dashboard**
   - Click "New +" → "Static Site"

2. **Connect Repository**
   - Connect your `hashtune-frontend` repository
   - Select the repository

3. **Configure Frontend Service**
   - **Name**: `hashtune-frontend`
   - **Environment**: `Static`
   - **Region**: Choose closest to your users
   - **Branch**: `master` (or your main branch)
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

4. **Environment Variables**
   - `REACT_APP_API_URL`: `https://hashtune-backend.onrender.com` (use your actual backend URL)

5. **Deploy**
   - Click "Create Static Site"
   - Wait for deployment to complete
   - **Note the URL** (e.g., `https://hashtune-frontend.onrender.com`)

### Step 3: Update Backend URL (if needed)

If your backend URL is different from `https://hashtune-backend.onrender.com`:

1. Go to your frontend service settings
2. Update the `REACT_APP_API_URL` environment variable
3. Redeploy the frontend

## Alternative: Using render.yaml Files

If you prefer, you can use the `render.yaml` files I created:

### For Backend:
1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your `hashtune` repository
4. Render will automatically detect and use `render.yaml`

### For Frontend:
1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your `hashtune-frontend` repository
4. Render will automatically detect and use `render.yaml`

## Testing Your Deployment

1. **Test Backend**: Visit `https://your-backend-url.onrender.com/`
   - Should return a health check response

2. **Test Frontend**: Visit `https://your-frontend-url.onrender.com/`
   - Should load your React application

3. **Test Integration**: Try using the app features
   - Frontend should successfully communicate with backend

## Troubleshooting

### Common Issues:

1. **Frontend can't reach backend**
   - Check `REACT_APP_API_URL` environment variable
   - Ensure backend URL is correct and accessible

2. **Backend deployment fails**
   - Check Docker logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`

3. **Frontend build fails**
   - Check build logs in Render dashboard
   - Ensure all dependencies are in `package.json`

4. **CORS errors**
   - Your backend already has CORS configured for all origins
   - If issues persist, check backend CORS settings

### Monitoring:

1. **Health Checks**: Both services have health check endpoints
2. **Logs**: Check service logs in Render dashboard
3. **Metrics**: Monitor usage in Render dashboard

## Cost Optimization

- **Free Tier**: Both services can run on Render's free tier
- **Static Site**: Frontend as static site is more cost-effective
- **Auto-sleep**: Free tier services sleep after 15 minutes of inactivity
- **Cold starts**: First request after sleep may be slower

## Next Steps

1. Set up custom domain (optional)
2. Configure SSL certificates (automatic with Render)
3. Set up monitoring and alerts
4. Configure CI/CD for automatic deployments

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
