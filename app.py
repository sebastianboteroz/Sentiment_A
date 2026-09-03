import streamlit as st
from streamlit_lottie import st_lottie
import json
import os

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA (Interface limpia)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Explorador de Emociones ✨",
    page_icon="🎈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CARGA DE ANIMACIONES LOTTIE (JSON LOCAL)
# ---------------------------------------------------------
def load_lottie_file(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

lottie_fruits = load_lottie_file("Bouncing Fruits.json")
lottie_sad = load_lottie_file("sad emotion.json")
lottie_neutral = load_lottie_file("emotion changing.json")

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Diseño UI/UX Limpio y Responsive)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Ocultar barra lateral y reducir padding superior */
    [data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 2rem !important; padding-bottom: 2rem !important;}

    /* Fondo principal suave */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', sans-serif;
    }

    /* Encabezados */
    .hero-title {
        color: #2D3748;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 4px;
        text-align: left;
    }

    .hero-subtitle {
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 30px;
        text-align: left;
    }

    /* Transparencia para animaciones Lottie */
    div[data-testid="stLottie"] {
        background: transparent !important;
        mix-blend-mode: multiply;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Botones Interactivos Grandes */
    .stButton>button {
        border-radius: 18px !important;
        padding: 16px 10px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.06);
        transition: all 0.2s ease-in-out !important;
        width: 100%;
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
    }

    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.1);
        color: #FF6B6B !important;
    }

    /* Tarjetas de Resultado */
    .result-card {
        border-radius: 20px;
        padding: 24px;
        color: white;
        text-align: left;
        margin-top: 15px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.05);
    }
    
    /* Mensaje de espera inicial */
    .placeholder-box {
        border: 2px dashed #CBD5E0;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        color: #A0AEC0;
        margin-top: 20px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENCABEZADO PRINCIPAL
# ---------------------------------------------------------
st.markdown('<h1 class="hero-title">✨ Explorador de Emociones</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Haz clic en una opción para descubrir cómo se expresa cada sentimiento:</p>', unsafe_allow_html=True)

# Inicializar sesión en None (Sin animación por defecto al cargar la página)
if "selected_emotion" not in st.session_state:
    st.session_state.selected_emotion = None

# ---------------------------------------------------------
# BOTONES DE SELECCIÓN
# ---------------------------------------------------------
col_happy, col_neutral, col_sad = st.columns(3)

with col_happy:
    if st.button("😊 Feliz", key="btn_happy"):
        st.session_state.selected_emotion = "feliz"

with col_neutral:
    if st.button("😐 Neutral", key="btn_neutral"):
        st.session_state.selected_emotion = "neutral"

with col_sad:
    if st.button("😔 Triste", key="btn_sad"):
        st.session_state.selected_emotion = "triste"

st.write("")

# ---------------------------------------------------------
# DESPLIEGUE VISUAL CONDICIONAL
# ---------------------------------------------------------
current = st.session_state.selected_emotion

if current is None:
    # Estado inicial: Pantalla limpia esperando interacción
    st.markdown("""
        <div class="placeholder-box">
            👆 Toca cualquiera de los botones de arriba para iniciar la animación.
        </div>
    """, unsafe_allow_html=True)

else:
    # Asignación según emoción seleccionada
    if current == "feliz":
        title = "¡Un Sentimiento de Alegría! 😊"
        desc = "Expresa energía positiva, felicidad, diversión y entusiasmo."
        color = "#2ECC71"
        anim = lottie_fruits

    elif current == "triste":
        title = "Un Sentimiento de Tristeza 😔"
        desc = "Expresa desánimo, tristeza, molestia o malestar."
        color = "#FF6B6B"
        anim = lottie_sad

    elif current == "neutral":
        title = "Un Sentimiento Neutral 😐"
        desc = "Expresa una idea tranquila, objetiva o en constante cambio."
        color = "#F1C40F"
        anim = lottie_neutral

    # Renderizado de Animación Lottie
    if anim:
        st_lottie(anim, height=200, key=f"anim_{current}")

    # Renderizado de Tarjeta Informativa
    st.markdown(f"""
        <div class="result-card" style="background-color: {color};">
            <h2 style="margin: 0; color: white; font-size: 1.7rem;">{title}</h2>
            <p style="margin-top: 8px; margin-bottom: 0; font-size: 1.1rem; opacity: 0.95;">{desc}</p>
        </div>
    """, unsafe_allow_html=True)
