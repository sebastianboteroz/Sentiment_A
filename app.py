import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Detector de Emociones ✨",
    page_icon="😊",
    layout="centered"
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Diseño Emocional + UX Infantil)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Fondo principal */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', sans-serif;
    }
    
    /* Header principal */
    .main-title {
        color: #FF6B6B;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #4A5568;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 25px;
    }

    /* Tarjetas de contenido */
    .css-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 2px solid #EDF2F7;
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

    /* Resultados */
    .result-box {
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
        color: white;
        font-weight: bold;
    }

    /* Sidebar con estilo suave */
    [data-testid="stSidebar"] {
        background-color: #FFF9EC;
        border-right: 2px solid #FFE66D;
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
    st.image("https://cdn-icons-png.flaticon.com/512/4152/4152757.png", width=120)
    
    st.markdown("""
    **¿Qué es la Polaridad?**  
    Es si la frase está **Feliz** (Positiva), **Triste/Enojada** (Negativa) o **Normal** (Neutral).

    ---
    **¿Qué es la Subjetividad?**  
    Nos dice si es una **opinión personal** (Subjetivo) o un **hecho real** (Objetivo).
    """)

# ---------------------------------------------------------
# ÁREA PRINCIPAL
# ---------------------------------------------------------
st.markdown('<h1 class="main-title">✨ Detector de Emociones ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">¡Descubre la emoción que se esconde detrás de tus palabras!</p>', unsafe_allow_html=True)

# Banner interactivo superior
st.image("https://img.freepik.com/vector-gratis/ilustracion-concepto-emociones-dibujados-mano_23-2149151525.jpg", use_container_width=True)

st.write("")

# Contenedor interactivo principal
with st.container():
    st.markdown("##### 📝 Escribe una frase o selecciona una de prueba:")
    
    # Atajo visual: Botones de prueba para reducir la carga de escribir
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    sample_text = ""
    if col_btn1.button("🌈 ¡Hoy es un gran día!"):
        sample_text = "¡Hoy es un gran día y me siento súper feliz!"
    if col_btn2.button("🍕 La pizza está rica"):
        sample_text = "La pizza de queso es muy sabrosa."
    if col_btn3.button("🌧️ Odio cuando llueve"):
        sample_text = "No me gusta cuando llueve porque no puedo jugar."

    # Campo de texto principal
    text_input = st.text_input("", value=sample_text, placeholder="Escribe aquí tu frase... Ej: ¡Me encanta jugar en el parque!")

if text_input:
    with st.spinner('Analizando los sentimientos... 🔍'):
        try:
            # Traducción e inferencia de sentimiento
            translation = translator.translate(text_input, src="es", dest="en")
            trans_text = translation.text
            blob = TextBlob(trans_text)
            
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)

            st.write("---")
            st.markdown("### 🎯 Resultado del Análisis")

            # Determinación de estado emocional
            if polarity > 0.1:
                emotion_label = "¡Sentimiento POSITIVO! 😊"
                bg_color = "#2ECC71"  # Verde amigable
                message = "¡Esta frase transmite mucha alegría y buena energía!"
            elif polarity < -0.1:
                emotion_label = "Sentimiento NEGATIVO 😔"
                bg_color = "#FF6B6B"  # Coral / Rojo suave
                message = "Esta frase parece expresar algo triste, enojado o molesto."
            else:
                emotion_label = "Sentimiento NEUTRAL 😐"
                bg_color = "#F1C40F"  # Amarillo
                message = "Esta frase es informativa o no expresa una emoción clara."

            # Visualización de la emoción principal
            st.markdown(f"""
                <div style="background-color: {bg_color}; border-radius: 20px; padding: 20px; text-align: center; color: white;">
                    <h2 style="margin: 0; color: white;">{emotion_label}</h2>
                    <p style="font-size: 1.1rem; margin-top: 5px;">{message}</p>
                </div>
            """, unsafe_allow_html=True)

            st.write("")
            
            # Medidores visuales de apoyo (Reducción de carga cognitiva)
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.markdown("**Nivel de Alegría/Ánimo**")
                # Escalado simple para barra (de -1..1 a 0..100)
                norm_polarity = int(((polarity + 1) / 2) * 100)
                st.progress(norm_polarity)
                st.caption(f"Valor: {polarity} (Rango de -1 a 1)")

            with col_m2:
                st.markdown("**¿Es opinión u objetivo?**")
                norm_subj = int(subjectivity * 100)
                st.progress(norm_subj)
                st.caption(f"Subjetividad: {norm_subj}%")

        except Exception as e:
            st.error("¡Ups! Ocurrió un pequeño problema al traducir la frase. Inténtalo de nuevo.")
