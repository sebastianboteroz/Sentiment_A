import streamlit as st
from textblob import TextBlob
from googletrans import Translator
from streamlit_lottie import st_lottie
import json
import os

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Detector de Emociones ✨",
    page_icon="😊",
    layout="centered"
)

# ---------------------------------------------------------
# CARGA DE ARCHIVOS LOTTIE
# ---------------------------------------------------------
def load_lottie_file(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

lottie_fruits = load_lottie_file("Bouncing Fruits.json")
lottie_sad = load_lottie_file("sad emotion.json")

# ---------------------------------------------------------
# CSS PERSONALIZADO Y RESPONSIVE (Transparencias & Limpieza)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Fondo limpio unificado */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', sans-serif;
    }

    /* Tipografía y Alineación a la Izquierda */
    .main-title {
        color: #2D3748;
        text-align: left;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #718096;
        text-align: left;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }

    /* Forzar transparencia en los contenedores Lottie para evitar recuadros blancos */
    div[data-testid="stLottie"] {
        background: transparent !important;
        mix-blend-mode: multiply;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Diseño amigable para botones de muestra */
    .stButton>button {
        border-radius: 12px !important;
        border: 1.5px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        color: #4A5568 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        border-color: #FF6B6B !important;
        color: #FF6B6B !important;
        transform: translateY(-2px);
    }

    /* Input estilizado */
    .stTextInput input {
        border-radius: 14px !important;
        border: 2px solid #CBD5E0 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        background-color: #FFFFFF !important;
    }

    /* Sidebar minimalista */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INICIALIZACIÓN
# ---------------------------------------------------------
translator = Translator()

# ---------------------------------------------------------
# BARRA LATERAL (Limpia sin exceso de imágenes)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎈 Guía Rápida")
    st.markdown("""
    **Polaridad:**
    Indica si el texto expresa un sentimiento **Positivo**, **Negativo** o **Neutral**.

    ---
    **Subjetividad:**
    Mide qué tanto es una **opinión personal** frente a un **hecho concreto**.
    """)

# ---------------------------------------------------------
# ENCABEZADO PRINCIPAL
# ---------------------------------------------------------
st.markdown('<h1 class="main-title">✨ Detector de Emociones</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Escribe cualquier texto y descubre al instante la emoción que transmite.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN DE ENTRADA DE TEXTO Y EJEMPLOS
# ---------------------------------------------------------
st.markdown("**📝 Escribe una frase o selecciona una de prueba:**")

col_b1, col_b2, col_b3 = st.columns(3)
sample_text = ""

if col_b1.button("🌈 ¡Hoy es un gran día!"):
    sample_text = "¡Hoy es un gran día y me siento súper feliz!"
if col_b2.button("🍕 La pizza está rica"):
    sample_text = "La pizza de queso es muy sabrosa."
if col_b3.button("🌧️ Odio cuando llueve"):
    sample_text = "No me gusta cuando llueve porque no puedo jugar."

text_input = st.text_input("", value=sample_text, placeholder="Escribe aquí tu frase...")

# ---------------------------------------------------------
# ANÁLISIS Y RESULTADOS
# ---------------------------------------------------------
if text_input:
    with st.spinner('Analizando emoción... 🔍'):
        try:
            translation = translator.translate(text_input, src="es", dest="en")
            trans_text = translation.text
            blob = TextBlob(trans_text)
            
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)

            st.write("")
            st.markdown("### 🎯 Resultado del Análisis")

            # Lógica exacta de asignación de animación y colores
            if polarity > 0.05:
                emotion_title = "¡Sentimiento POSITIVO! 😊"
                bg_color = "#2ECC71"  # Verde brillante y limpio
                message = "¡Esta frase está llena de energía positiva y alegría!"
                active_anim = lottie_fruits
            elif polarity < -0.05:
                emotion_title = "Sentimiento NEGATIVO 😔"
                bg_color = "#FF6B6B"  # Rojo/Coral suave
                message = "Esta frase expresa tristeza, malestar o enojo."
                active_anim = lottie_sad
            else:
                emotion_title = "Sentimiento NEUTRAL 😐"
                bg_color = "#F1C40F"  # Amarillo cálido
                message = "Esta frase es neutra, informativa o no muestra emociones marcadas."
                active_anim = None

            # Disposición Responsive: Animación arriba (sin choques de fondo) y resultado debajo
            if active_anim:
                st_lottie(active_anim, height=180, key="emotion_animation")

            # Tarjeta de resultado limpia
            st.markdown(f"""
                <div style="background-color: {bg_color}; border-radius: 16px; padding: 22px; margin-top: 10px; color: white; text-align: left;">
                    <h2 style="margin: 0; color: white; font-size: 1.6rem;">{emotion_title}</h2>
                    <p style="margin-top: 8px; margin-bottom: 0; font-size: 1rem; color: white; opacity: 0.95;">{message}</p>
                </div>
            """, unsafe_allow_html=True)

            st.write("")
            
            # Barras de medición estilizadas
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.markdown("**Nivel de Alegría / Positividad**")
                norm_polarity = int(((polarity + 1) / 2) * 100)
                st.progress(norm_polarity)
                st.caption(f"Puntaje: {polarity} (de -1 a 1)")

            with col_m2:
                st.markdown("**Grado de Opinión (Subjetividad)**")
                norm_subj = int(subjectivity * 100)
                st.progress(norm_subj)
                st.caption(f"Subjetividad: {norm_subj}%")

        except Exception as e:
            st.error("No se pudo analizar la frase en este momento. Inténtalo de nuevo.")
