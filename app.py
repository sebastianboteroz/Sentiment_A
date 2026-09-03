import streamlit as st
from streamlit_lottie import st_lottie
import json
import os

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA (Sin barra lateral)
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

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Diseño Limpio, Espacioso y Responsive)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Ocultar barra lateral y padding superior */
    [data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 2rem !important; padding-bottom: 2rem !important;}

    /* Fondo principal */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', sans-serif;
    }

    /* Encabezado */
    .hero-title {
        color: #2D3748;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 4px;
        text-align: left;
    }

    .hero-subtitle {
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 25px;
        text-align: left;
    }

    /* Transparencia Lottie limpia */
    div[data-testid="stLottie"] {
        background: transparent !important;
        mix-blend-mode: multiply;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Estilo de Botones Interactivos Grandes */
    .stButton>button {
        border-radius: 18px !important;
        padding: 16px 10px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.06);
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.1);
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
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENCABEZADO PRINCIPAL
# ---------------------------------------------------------
st.markdown('<h1 class="hero-title">✨ Explorador de Emociones</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Selecciona una emoción para ver cómo se expresa:</p>', unsafe_allow_html=True)

# Manejo de estado de la emoción seleccionada
if "selected_emotion" not in st.session_state:
    st.session_state.selected_emotion = "feliz"

# ---------------------------------------------------------
# BOTONES DE SELECCIÓN DE EMOCIÓN
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
# DESPLIEGUE VISUAL Y ANIMACIÓN
# ---------------------------------------------------------
current = st.session_state.selected_emotion

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

else:  # neutral
    title = "Un Sentimiento Neutral 😐"
    desc = "Expresa una idea tranquila, objetiva o sin emociones marcadas."
    color = "#F1C40F"
    anim = None

# Renderizado de la Animación Lottie
if anim:
    st_lottie(anim, height=200, key=f"anim_{current}")

# Renderizado de la Tarjeta Informativa
st.markdown(f"""
    <div class="result-card" style="background-color: {color};">
        <h2 style="margin: 0; color: white; font-size: 1.7rem;">{title}</h2>
        <p style="margin-top: 8px; margin-bottom: 0; font-size: 1.1rem; opacity: 0.95;">{desc}</p>
    </div>
""", unsafe_allow_html=True)
