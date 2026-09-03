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
# FUNCIÓN PARA CARGAR ANIMACIONES LOTTIE (JSON LOCAL)
# ---------------------------------------------------------
def load_lottie_file(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Cargar las animaciones de tu carpeta
lottie_happy = load_lottie_file("Bouncing Fruits.json")
lottie_sad = load_lottie_file("sad emotion.json")

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Alineado a la Izquierda)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Fondo principal */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', sans-serif;
    }
    
    /* Todo alineado estrictamente a la izquierda */
    .main-title {
        color: #FF6B6B;
        text-align: left;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #4A5568;
        text-align: left;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    /* Modificación de Inputs y Botones */
    .stTextInput input {
        border-radius: 15px !important;
        border: 2px solid #CBD5E0 !important;
        padding: 12px !important;
        font-size: 1.1rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #FF6B6B !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2) !important;
    }

    /* Sidebar con estilo suave */
    [data-testid="stSidebar"] {
        background-color: #FFF9EC;
        border-right: 2px solid #FFE66D;
    }

    /* Asegurar alineación izquierda en etiquetas */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        text-align: left !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INICIALIZACIÓN
# ---------------------------------------------------------
translator = Translator()

# ---------------------------------------------------------
# BARRA LATERAL (Educativa y Simple)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎈 ¿Cómo funciona?")
    
    # Animación pequeña en la barra lateral si existe la fruta
    if lottie_happy:
        st_lottie(lottie_happy, height=120, key="side_fruit")
        
    st.markdown("""
    **Polaridad:**  
    Muestra si la frase expresa algo **Feliz** (Positiva), **Triste/Enojada** (Negativa) o **Normal** (Neutral).

    ---
    **Subjetividad:**  
    Mide si es una **opinión personal** o un **hecho real**.
    """)

# ---------------------------------------------------------
# ÁREA PRINCIPAL (Encabezado + Animación en Columnas)
# ---------------------------------------------------------
col_header, col_anim = st.columns([2, 1])

with col_header:
    st.markdown('<h1 class="main-title">✨ Detector de Emociones</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Descubre la emoción que se esconde detrás de tus palabras.</p>', unsafe_allow_html=True)

with col_anim:
    # Muestra animación principal de bienvenida alineada a la derecha del título
    if lottie_happy:
        st_lottie(lottie_happy, height=140, key="hero_anim")

# ---------------------------------------------------------
# SECCIÓN DE ENTRADA Y BOTONES DE PRUEBA
# ---------------------------------------------------------
st.markdown("##### 📝 Escribe una frase o selecciona una de prueba:")

col_btn1, col_btn2, col_btn3 = st.columns(3)
sample_text = ""
if col_btn1.button("🌈 ¡Hoy es un gran día!"):
    sample_text = "¡Hoy es un gran día y me siento súper feliz!"
if col_btn2.button("🍕 La pizza está rica"):
    sample_text = "La pizza de queso es muy sabrosa."
if col_btn3.button("🌧️ Odio cuando llueve"):
    sample_text = "No me gusta cuando llueve porque no puedo jugar."

# Campo de texto principal
text_input = st.text_input("", value=sample_text, placeholder="Escribe aquí tu frase...")

# ---------------------------------------------------------
# RESULTADO Y PROCESAMIENTO
# ---------------------------------------------------------
if text_input:
    with st.spinner('Analizando los sentimientos... 🔍'):
        try:
            translation = translator.translate(text_input, src="es", dest="en")
            trans_text = translation.text
            blob = TextBlob(trans_text)
            
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)

            st.write("---")
            st.markdown("### 🎯 Resultado del Análisis")

            # Determinación del estado emocional y selección de animación Lottie
            if polarity > 0.1:
                emotion_label = "Sentimiento POSITIVO 😊"
                bg_color = "#2ECC71"
                message = "¡Esta frase transmite mucha alegría y buena energía!"
                selected_lottie = lottie_happy
            elif polarity < -0.1:
                emotion_label = "Sentimiento NEGATIVO 😔"
                bg_color = "#FF6B6B"
                message = "Esta frase parece expresar algo triste, enojado o molesto."
                selected_lottie = lottie_sad
            else:
                emotion_label = "Sentimiento NEUTRAL 😐"
                bg_color = "#F1C40F"
                message = "Esta frase es informativa o no expresa una emoción clara."
                selected_lottie = lottie_happy

            # Tarjeta de resultado con animación Lottie integrada
            col_res_text, col_res_lottie = st.columns([3, 1])

            with col_res_text:
                st.markdown(f"""
                    <div style="background-color: {bg_color}; border-radius: 20px; padding: 20px; text-align: left; color: white;">
                        <h2 style="margin: 0; color: white; text-align: left;">{emotion_label}</h2>
                        <p style="font-size: 1.05rem; margin-top: 5px; color: white; text-align: left;">{message}</p>
                    </div>
                """, unsafe_allow_html=True)

            with col_res_lottie:
                if selected_lottie:
                    st_lottie(selected_lottie, height=110, key="result_anim")

            st.write("")
            
            # Barras de progreso alineadas a la izquierda
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.markdown("**Nivel de Alegría / Ánimo**")
                norm_polarity = int(((polarity + 1) / 2) * 100)
                st.progress(norm_polarity)
                st.caption(f"Valor: {polarity} (Rango de -1 a 1)")

            with col_m2:
                st.markdown("**¿Es opinión u objetivo?**")
                norm_subj = int(subjectivity * 100)
                st.progress(norm_subj)
                st.caption(f"Subjetividad: {norm_subj}%")

        except Exception as e:
            st.error("Ocurrió un error al analizar la frase. Inténtalo de nuevo.")
