# HireSense Deployment Guide

## ✅ **Setup Complete!**

Your frontend is now configured to automatically use the correct backend URL:

- **Local Development:** `http://localhost:8000`
- **Production:** `https://hiresense-1-4d5i.onrender.com`

---

## 📁 **Files Created/Modified:**

### Configuration Files:
- ✅ `frontend/.env.development` - Local development config
- ✅ `frontend/.env.production` - Production config  
- ✅ `frontend/src/config.js` - Centralized API configuration
- ✅ Updated all components to use `API_BASE_URL`

### Components Updated:
- ✅ `App.js`
- ✅ `ResumeUpload.jsx`
- ✅ `AIInterviewer.jsx`
- ✅ `AIAnalysis.jsx`
- ✅ `StarRewriter.jsx`

---

## 🚀 **How to Run:**

### **Local Development:**
```bash
cd frontend
npm install
npm run dev
```
✅ Uses `http://localhost:8000` automatically

### **Production Build:**
```bash
cd frontend
npm run build
```
✅ Uses `https://hiresense-1-4d5i.onrender.com` automatically

---

## 🌐 **Deploy Frontend:**

### **Option 1: Vercel (Recommended)**
```bash
cd frontend
npm install -g vercel
vercel
```
- Auto-detects React/Vite
- Environment variables automatically set
- ✅ Instant deployment

### **Option 2: Netlify**
1. Go to [netlify.com](https://netlify.com)
2. Connect GitHub repo
3. Build settings:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
4. Deploy!

### **Option 3: Render**
1. Create new "Static Site" on Render
2. Connect GitHub repo
3. Build settings:
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/dist`
4. Deploy!

---

## ⚙️ **Environment Variables:**

No manual setup needed! The `.env.development` and `.env.production` files handle everything.

**To use a different backend URL:**
Edit `frontend/.env.production`:
```bash
REACT_APP_API_URL=https://your-custom-backend-url.com
```

---

## 🧪 **Testing:**

### Test Local Setup:
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Test Production Build Locally:
```bash
npm run build
npm run preview
```

---

## 📝 **Important Notes:**

✅ **CORS is configured** in your backend for both local and production  
✅ **Environment files committed** to repo (safe - no secrets)  
✅ **Automatic switching** between local and production URLs  
✅ **Console logs** show which API URL is being used

---

## 🔍 **Troubleshooting:**

**Frontend can't connect to backend?**
- Check browser console for API URL
- Verify backend CORS allows your frontend domain
- Check backend is running on correct URL

**Production deployment not working?**
- Run `npm run build` locally first to test
- Check build logs for errors
- Verify environment variables are set correctly

---

## 🎯 **Next Steps:**

1. ✅ Backend already deployed: https://hiresense-1-4d5i.onrender.com
2. 🚀 Deploy frontend to Vercel/Netlify/Render
3. 🎉 Your full-stack app is live!

---

**Need help?** Check the console logs - they show which API URL is being used!
