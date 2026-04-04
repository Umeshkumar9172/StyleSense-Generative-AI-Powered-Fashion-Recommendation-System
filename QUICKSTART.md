## 🚀 QUICK START GUIDE

### To Run StyleAI (Flask Version) - PROFESSIONAL WEBSITE ✨

**Windows CMD:**
```cmd
cd Generative_AI_Powered_Fashion_Recommendation
pip install -r requirements.txt
python app.py
```

**Then open your browser to:** http://127.0.0.1:5000

---

### Before First Run ⚙️

**Option 1: Create .env file with Groq API Key**
```
1. Create a file named ".env" in the project folder
2. Add this line:
   GROQ_API_KEY=your_api_key_here
3. Get your API key from: https://console.groq.com/keys
```

**Option 2: Enter API Key in the Web App**
```
1. Just run the app without .env
2. You'll see a field to enter it in the sidebar
3. The app will work right away
```

---

### What You'll See 👀

✅ Modern professional website design
✅ Image upload feature
✅ Real-time skin tone detection
✅ AI-powered fashion recommendations
✅ Shopping links to Amazon, Myntra, Zara
✅ Responsive mobile-friendly design

---

### Folder Structure 📁

```
Generative_AI_Powered_Fashion_Recommendation/
├── app.py                    // Start here! Flask backend
├── templates/
│   └── index.html           // Web interface
├── static/
│   ├── style.css            // Beautiful styling
│   └── script.js            // Interactive features
├── groq_client.py           // AI Model integration
├── utils.py                 // Image processing
├── requirements.txt         // Dependencies
└── .env                     // Your API key (create this)
```

---

### Features in This Version 🎯

- **Pure Flask** - No Streamlit, lightweight and fast
- **Modern UI** - Bootstrap 5 + Custom CSS for professional look
- **Responsive** - Works on desktop, tablet, mobile
- **Fast** - Direct API calls, no stream buffering
- **Beautiful** - Gradient backgrounds, smooth animations, clean layout

---

### Troubleshooting 🔧

**Port 5000 already in use?**
```cmd
python app.py  // Will automatically show which port is available
```

**Module not found error?**
```cmd
pip install -r requirements.txt --upgrade
```

**No face detected?**
- Use a clear, well-lit photo
- Face should be clearly visible
- Try front-facing angle

---

Made with ❤️ using Flask + Groq LLaMA AI
