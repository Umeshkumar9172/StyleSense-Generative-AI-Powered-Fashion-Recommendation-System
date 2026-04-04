# StyleAI - AI-Powered Fashion Styling Advisor

StyleAI is a professional web application that leverages Groq's LLaMA 3.3 70B AI model to provide comprehensive personal styling recommendations. It analyzes user photos to detect skin tone and generates gender-specific fashion advice, including outfit ideas, color palettes, and curated shopping links.

## Features

- **🎯 Skin Tone Analysis:** Automatically detects skin tone (Fair, Medium, Olive, Deep) from user-uploaded photos
- **🤖 AI Fashion Consultant:** Uses LLaMA 3.3 70B via Groq API for personalized styling advice
- **👥 Gender-Specific Recommendations:** Tailored outfits for Men, Women, and Non-Binary users
- **🛍️ Smart Shopping:** Direct search links for Amazon.in, Myntra, and Zara
- **⚡ Fast & Professional:** Built with Flask and modern web technologies

## Prerequisites

- **Python 3.8+**
- **[Groq API Key](https://console.groq.com/keys)** (Free tier available)

## Installation

### Step 1: Navigate to Project Directory
```bash
cd Generative_AI_Powered_Fashion_Recommendation
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

#### Option A: Using Environment Variable (Recommended)
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/keys)

#### Option B: Enter in Web Interface
Leave the `.env` file empty. You can paste the API key directly in the web app when it loads.

## Running the Application

```bash
python app_flask.py
```

The application will be available at: **http://127.0.0.1:5000**

Open your browser and navigate to the URL above. The app will automatically load!

## How It Works

1. **Upload Photo** - Upload a clear facial photo (JPG or PNG)
2. **Select Gender** - Choose your gender (Female, Male, Non-Binary)
3. **AI Analysis** - System detects your skin tone using computer vision
4. **Get Styled** - LLaMA AI generates personalized recommendations
5. **Shop** - Direct links to buy suggested items from top retailers

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Vanilla JavaScript |
| **AI Model** | Groq LLaMA 3.3 70B |
| **Image Processing** | OpenCV, PIL, NumPy |

## Project Structure

```
Generative_AI_Powered_Fashion_Recommendation/
├── app_flask.py              # Flask application entry point
├── utils.py                  # Image processing & skin tone detection
├── groq_client.py            # Groq API integration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── templates/
│   └── index.html           # Main web interface
└── static/
    ├── style.css            # Professional styling
    └── script.js            # Interactive features
```

## Troubleshooting

### "No face detected"
- Ensure the photo shows your face clearly
- Try a front-facing, well-lit photo
- Remove sunglasses or hats

### "API Key is missing"
- Create a `.env` file with your Groq API key
- Or enter the API key in the web app sidebar
- Get it from [console.groq.com/keys](https://console.groq.com/keys)

### Port Already in Use
```bash
# Change port in app_flask.py (last line)
app.run(debug=True, host='127.0.0.1', port=5001)  # Change 5000 to 5001
```

## API & Dependencies

- **Groq API:** Free tier includes sufficient requests for testing
- **OpenCV:** Open-source computer vision library
- **Flask:** Lightweight Python web framework

## License

This project is open source.

## Support

For issues:
1. Check Groq documentation: [groq.com/docs](https://groq.com/docs)
2. Ensure Python 3.8+ is installed
3. Verify dependencies: `pip list`
