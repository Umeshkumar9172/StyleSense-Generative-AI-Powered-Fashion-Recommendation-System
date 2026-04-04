from utils import analyze_skin_tone
from groq_client import GroqService
import os
from dotenv import load_dotenv
from PIL import Image
from typing import List

load_dotenv()

st.set_page_config(
    page_title="Styling AI",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'groq_service' not in st.session_state:
    st.session_state.groq_service = GroqService()

def get_collage_images(gender: str) -> List[str]:
    if gender == "Male":
        return [
            "https://images.unsplash.com/photo-1519741491150-5b9f43f49a04?w=800&q=80",
            "https://images.unsplash.com/photo-1497800933327-3f1e1e69f7c6?w=800&q=80",
            "https://images.unsplash.com/photo-1520975669260-3f9a2e45f8f1?w=800&q=80",
            "https://images.unsplash.com/photo-1516822003754-cca485356ecb?w=800&q=80",
            "https://images.unsplash.com/photo-1519340241580-0f5f5d182e8f?w=800&q=80",
            "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&q=80",
        ]
    if gender == "Non-Binary":
        return [
            "https://images.unsplash.com/photo-1520975603325-d11a5d1f01f2?w=800&q=80",
            "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80",
            "https://images.unsplash.com/photo-1521335629791-ce4aecb9deb0?w=800&q=80",
            "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=800&q=80",
            "https://images.unsplash.com/photo-1463107971871-fbac9ddb920f?w=800&q=80",
            "https://images.unsplash.com/photo-1475274047050-1f64b8cf58f0?w=800&q=80",
        ]
    return [
        "https://images.unsplash.com/photo-1519741491150-5b9f43f49a04?w=800&q=80",
        "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=800&q=80",
        "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80",
        "https://images.unsplash.com/photo-1521335629791-ce4aecb9deb0?w=800&q=80",
        "https://images.unsplash.com/photo-1463107971871-fbac9ddb920f?w=800&q=80",
        "https://images.unsplash.com/photo-1475274047050-1f64b8cf58f0?w=800&q=80",
    ]

st.markdown("""
    <style>
    .main { padding: 0; }
    .nav { position: sticky; top:0; z-index:5; width:100%; background: rgba(255,255,255,0.7); backdrop-filter: blur(8px); border-bottom: 1px solid #eee; }
    .nav-inner { max-width: 1200px; margin: 0 auto; display:flex; align-items:center; justify-content:space-between; padding: 0.75rem 1.25rem; }
    .brand { font-weight: 700; color: #6a1b9a; }
    .links a { margin-left: 1rem; color:#333; text-decoration:none; font-weight:600; }
    .links a:hover { color:#6a1b9a; }
    .hero { background: linear-gradient(135deg, #e056fd 0%, #ff7979 60%, #ffbe76 100%); padding: 5rem 1.5rem; color: #fff; position: relative; }
    .hero-inner { max-width: 1200px; margin: 0 auto; display:grid; grid-template-columns: 1.2fr 0.8fr; gap:2rem; align-items:center; }
    .hero h1 { font-size: 3rem; line-height:1.1; margin:0; }
    .hero p { font-size: 1.1rem; margin-top: 1rem; }
    .cta { display:inline-block; margin-top: 1.2rem; background:#ffd166; color:#222; padding:0.75rem 1.25rem; border-radius:999px; text-decoration:none; font-weight:700; }
    .collage { display:grid; grid-template-columns: repeat(2,1fr); gap:12px; }
    .tile { background-size: cover; background-position: center; border-radius: 16px; border: 1px solid rgba(255,255,255,0.6); box-shadow: 0 14px 28px rgba(0,0,0,0.25); transition: transform .2s ease, box-shadow .2s ease; }
    .tile:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 22px 44px rgba(0,0,0,0.35); }
    .section { max-width:1200px; margin: 0 auto; padding: 2rem 1.5rem; }
    .features-title { text-align:center; font-size:2rem; margin-bottom:1rem; color:#fff; }
    .feature-grid { display:grid; grid-template-columns: repeat(4,1fr); gap:1.25rem; }
    .feature-card { border-radius:18px; padding:1.5rem; text-align:center; color:#222; box-shadow: 0 20px 60px rgba(0,0,0,0.20); transition: transform .2s ease, box-shadow .2s ease; border: 0; }
    .feature-card h3 { margin:.5rem 0 0.25rem; font-size:1.15rem; color:#111; }
    .feature-card p { margin:0; color:#333; }
    .feature-card:nth-child(1){ background: linear-gradient(135deg,#ffffff 0%,#f0f4ff 100%); }
    .feature-card:nth-child(2){ background: linear-gradient(135deg,#ffffff 0%,#fff0f5 100%); }
    .feature-card:nth-child(3){ background: linear-gradient(135deg,#ffffff 0%,#f7fff0 100%); }
    .feature-card:nth-child(4){ background: linear-gradient(135deg,#ffffff 0%,#fff9f0 100%); }
    .feature-card:hover { transform: translateY(-6px); box-shadow: 0 30px 70px rgba(0,0,0,0.25); }
    .feature-icon { display:inline-flex; align-items:center; justify-content:center; width:52px; height:52px; border-radius:999px; background: rgba(106,27,154,0.08); font-size:1.4rem; }
    .upload-title { font-size:1.5rem; font-weight:700; }
    .stButton>button { width:100%; background-color:#6a1b9a; color:#fff; border:none; }
    .stButton>button:hover { background-color:#8e24aa; }
    </style>
    """, unsafe_allow_html=True)

collage_imgs = get_collage_images(st.session_state.get("gender", "Female"))
collage_html = f"""
<div class="collage">
  <div class="tile" style="height:120px;background-image:url('{collage_imgs[0]}');"></div>
  <div class="tile" style="height:160px;background-image:url('{collage_imgs[1]}');"></div>
  <div class="tile" style="height:110px;background-image:url('{collage_imgs[2]}');"></div>
  <div class="tile" style="height:150px;background-image:url('{collage_imgs[3]}');"></div>
  <div class="tile" style="height:130px;background-image:url('{collage_imgs[4]}');"></div>
  <div class="tile" style="height:120px;background-image:url('{collage_imgs[5]}');"></div>
</div>
"""

st.markdown(
    """
    <div class="nav">
      <div class="nav-inner">
        <div class="brand">Styling AI</div>
        <div class="links"><a href="#home">Home</a><a href="#features">Features</a><a href="#tryit">Try It</a><a href="#about">About</a></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<a id="home"></a>', unsafe_allow_html=True)
hero_html = f"""
<section class="hero">
  <div class="hero-inner">
    <div>
      <h1>Your Personal AI Fashion Stylist</h1>
      <p>Upload your photo and get personalized styling recommendations based on your skin tone.</p>
      <a class="cta" href="#tryit">Get Started</a>
    </div>
    {collage_html}
  </div>
  </section>
"""
st.markdown(hero_html, unsafe_allow_html=True)

st.markdown('<a id="features"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section"><div class="features-title">Why Choose Styling AI?</div>'
    '<div class="feature-grid">'
    '<div class="feature-card"><div class="feature-icon">📷</div><h3>Instant Analysis</h3><p>Upload a photo and get AI-powered results in seconds.</p></div>'
    '<div class="feature-card"><div class="feature-icon">🎨</div><h3>Color Matching</h3><p>Recommendations matched to your skin tone and complexion.</p></div>'
    '<div class="feature-card"><div class="feature-icon">🛍️</div><h3>Product Links</h3><p>Direct shopping links from top retailers.</p></div>'
    '<div class="feature-card"><div class="feature-icon">⭐</div><h3>Professional Tips</h3><p>Hairstyle, accessories, and expert styling advice.</p></div>'
    '</div></div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("Settings")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        user_api_key = st.text_input("Enter Groq API Key", type="password")
        if user_api_key:
            st.session_state.groq_service.set_api_key(user_api_key)
            st.success("API Key set!")
    st.markdown("---")
    st.header("Profile Details")
    gender = st.selectbox("Select Gender", ["Female", "Male", "Non-Binary"])
    st.session_state.gender = gender
    st.markdown("---")
    st.markdown("### About")
    st.info("Styling AI uses Groq's LLaMA 3.3 70B to generate tailored fashion advice based on detected skin tone.")

st.markdown('<a id="tryit"></a>', unsafe_allow_html=True)
st.markdown('<div class="section"><div class="upload-title">Try It</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("Upload a clear facial photo...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Photo', use_container_width=True)
        
        if st.button("Analyze & Style Me!"):
            with st.spinner("Analyzing skin tone..."):
                analysis_result = analyze_skin_tone(uploaded_file)
                
                if analysis_result['success']:
                    st.session_state.skin_tone = analysis_result['skin_tone']
                    st.session_state.avg_color = analysis_result['average_color']
                    st.success(f"Detected Skin Tone: **{analysis_result['skin_tone']}**")
                    
                    r, g, b = analysis_result['average_color']
                    st.markdown(
                        f'<div style="background-color: rgb({r},{g},{b}); height: 50px; width: 100px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #ddd;"></div>', 
                        unsafe_allow_html=True
                    )
                    st.caption("Average Face Color")
                    
                    with st.spinner("Consulting AI Stylist (Llama 3.3)..."):
                        recommendations = st.session_state.groq_service.get_fashion_recommendations(
                            st.session_state.skin_tone,
                            gender
                        )
                        st.session_state.recommendations = recommendations
                else:
                    st.error(analysis_result['message'])

with col2:
    if 'recommendations' in st.session_state:
        st.subheader("Your Personalized Style Guide")
        st.markdown(st.session_state.recommendations)
        
        st.markdown("---")
        st.markdown("### Quick Links")
        st.markdown("Use the links in the guide above to shop directly.")
    else:
        st.info("👈 Upload a photo and click 'Analyze & Style Me!' to get started.")
        
        st.markdown("### How it works")
        st.markdown("""
        1. **Skin Tone Analysis**: We detect your skin tone category (Fair, Medium, Olive, Deep).
        2. **AI Consultation**: Groq's LLaMA 3 model generates a tailored style guide.
        3. **Shop the Look**: Get curated links to buy the recommended items.
        """)

st.markdown('<a id="about"></a>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section">
      <h3>About</h3>
      <p>Styling AI is an intelligent fashion advisor that analyzes your photo to detect skin tone and uses Groq's LLaMA 3.3 to craft personalized outfits, color palettes, and shopping guides from top retailers. Built for fast responses and practical style you can buy today.</p>
    </div>
    """,
    unsafe_allow_html=True
)
