import streamlit as st
from googletrans import Translator
from gtts import gTTS
from faster_whisper import WhisperModel
import tempfile
import os
import random
import time
import base64


st.markdown("""<style>
    .block-container {
        max-width: 880px;
        margin: auto;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, #0f111a, #1a1c29);
        border-radius: 25px;
        box-shadow: 0 0 40px rgba(0, 174, 255, 0.15);
        font-family: 'Segoe UI', sans-serif;
        backdrop-filter: blur(10px);
    }
    h1 {
        text-align: center;
        color: #cfe8ff;
        font-size: 2.8rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 8px rgba(0, 174, 255, 0.3);
    }
    .stTextArea textarea {
        background-color: #1d1f2e !important;
        color: #e3f6ff !important;
        border: 1px solid #2a2d3f;
        border-radius: 15px;
        box-shadow: inset 0 0 10px rgba(0, 174, 255, 0.05);
        padding: 1rem;
        font-size: 1rem;
    }
    .stSelectbox > div {
        background-color: #1d1f2e !important;
        color: #cfe8ff !important;
        border-radius: 12px;
        padding: 0.4rem 0.6rem;
        font-weight: 500;
        border: 1px solid #2a2d3f;
    }
    .stButton>button {
        background: rgba(0, 174, 255, 0.1);
        color: #e0f7ff;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        border: 1px solid rgba(0, 174, 255, 0.4);
        backdrop-filter: blur(6px);
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 12px rgba(0, 174, 255, 0.25);
    }
    .stButton>button:hover {
        background: rgba(0, 174, 255, 0.25);
        transform: scale(1.03);
        color: #ffffff;
        border-color: rgba(0, 174, 255, 0.6);
    }
    .audio-container {
        margin: 1.5rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1a1c29, #252837);
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid #2a2d3f;
    }
    .audio-title {
        color: #cfe8ff;
        margin-top: 0;
        font-size: 1.9rem;
    }
    audio {
        width: 100% !important;
        max-width: 100% !important;
    }
    .download-btn {
        background: rgba(0, 200, 100, 0.1) !important;
        color: #ccffe0 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.4rem !important;
        border: 1px solid rgba(0, 200, 100, 0.4) !important;
        backdrop-filter: blur(6px) !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(0, 200, 100, 0.25) !important;
        margin-top: 15px !important;
        display: inline-block;
        text-align: center;
        text-decoration: none;
        width: 100%;
    }
    .download-btn:hover {
        background: rgba(0, 200, 100, 0.2) !important;
        transform: scale(1.03) !important;
        color: #e0ffe0 !important;
        border-color: rgba(0, 200, 100, 0.6) !important;
    }
    .stButton>button {
        min-height: 48px;
        font-size: 1.1rem;
        letter-spacing: 0.04em;
    }
</style>""", unsafe_allow_html=True)


# Función para obtener traductor con fix de error
def get_translator():
    traductor = Translator()
    # Fix para un posible error en versiones antiguas de googletrans
    if hasattr(traductor, 'raise_Exception'):
        delattr(traductor, 'raise_Exception')
    return traductor

# Modelo Whisper cargado una sola vez para eficiencia
@st.cache_resource
def load_whisper_model():
    return WhisperModel("base")

whisper_model = load_whisper_model()

textos_ejemplo = [
    "Hola, ¿cómo estás hoy?",
    "El conocimiento es poder",
    "La vida es como una bicicleta, para mantener el equilibrio debes seguir adelante",
    "El único modo de hacer un gran trabajo es amar lo que haces",
    "La tecnología es mejor cuando une a las personas",
    "La creatividad es la inteligencia divirtiéndose",
    "La simplicidad es la máxima sofisticación",
    "El futuro pertenece a quienes creen en la belleza de sus sueños",
    "Cada día es una nueva oportunidad para cambiar tu vida.",
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "El único límite es el que tú te pongas.",
    "Nunca es tarde para ser quien podrías haber sido.",
    "El fracaso es solo la oportunidad de comenzar de nuevo con más experiencia.",
    "Haz hoy lo que tu futuro yo te agradecerá.",
    "No tengas miedo de renunciar a lo bueno para ir por lo grandioso.",
    "La disciplina tarde o temprano vencerá al talento.",
    "El verdadero cambio empieza dentro de ti.",
    "No hay viento favorable para quien no sabe a dónde va.",
    "El que quiere, encuentra una manera. El que no, una excusa.",
    "Cada paso cuenta, por pequeño que sea.",
    "No hay atajos para los lugares que valen la pena.",
    "El primer paso no te lleva a donde quieres ir, pero te saca de donde estás.",
    "Las grandes ideas nacen de la curiosidad.",
    "El aprendizaje nunca agota la mente.",
    "Todo lo que puedas imaginar es real.",
    "No importa lo lento que avances, mientras no te detengas.",
    "Confía en el proceso, incluso cuando no entiendas el camino.",
    "La actitud es una pequeña cosa que hace una gran diferencia.",
    "Lo que haces hoy puede mejorar todos tus mañanas.",
    "No tienes que ser perfecto, solo constante.",
    "Empieza donde estás, usa lo que tienes, haz lo que puedas.",
    "Los sueños no funcionan a menos que tú trabajes por ellos.",
    "El cambio comienza con una decisión.",
    "El éxito no es la clave de la felicidad, la felicidad es la clave del éxito.",
    "A veces perder es aprender por otro camino."
]

# Idiomas disponibles con sus banderas
idiomas = {
    "es": "🇪🇸 Español",
    "en": "🇬🇧 Inglés",
    "fr": "🇫🇷 Francés",
    "de": "🇩🇪 Alemán",
    "it": "🇮🇹 Italiano",
    "pt": "🇵🇹 Portugués",
    "ru": "🇷🇺 Ruso",
    "zh-cn": "🇨🇳 Chino (simplificado)",
}
idiomas_lista = ["🌐 Elegir idioma de traducción"] + list(idiomas.values())

st.markdown("""
<h1 class="titulo-rainbow">🗣️ Traductor con Voz y Descarga</h1>

<style>
.titulo-rainbow {
    font-size: 3rem;
    text-align: center;
    background: linear-gradient(270deg, red, orange, yellow, green, cyan, blue, violet, red);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: arcoiris 12s linear infinite;
    font-family: 'Segoe UI', sans-serif;
    margin-bottom: 1rem;
    text-shadow: 0 0 8px rgba(0,0,0,0.2);
}

@keyframes arcoiris {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
""", unsafe_allow_html=True)


# ---------------------------- Transcripción de Audio ----------------------------
st.markdown("## 🎙️ Transcripción de Audio y Traducción")

audio_file = st.file_uploader("🔊 Sube un archivo de audio (.wav o .mp3)", type=["wav", "mp3"])
idioma_destino_audio = st.selectbox("🌐 Idioma de destino para la transcripción", idiomas_lista, index=0, key="idioma_audio_destino")

if audio_file and idioma_destino_audio != "🌐 Elegir idioma de traducción":
    # Obtener el código de idioma a partir del texto seleccionado
    codigo_idioma_audio = None
    for codigo, texto_idioma in idiomas.items():
        if texto_idioma == idioma_destino_audio:
            codigo_idioma_audio = codigo
            break

    if st.button("🎧 Transcribir y Traducir Audio"):
        with st.spinner("Procesando audio..."):
            try:
                # Guardar el archivo de audio temporalmente
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(audio_file.read())
                    tmp_audio_path = tmp_file.name

                # Transcribir el audio usando Whisper
                segments, _ = whisper_model.transcribe(tmp_audio_path)
                texto_transcripto = " ".join([seg.text for seg in segments])

                # Traducir el texto transcripto
                traductor = get_translator()
                traduccion_audio = traductor.translate(texto_transcripto, dest=codigo_idioma_audio)

                st.markdown(f"**📝 Texto original:** {texto_transcripto}")
                st.markdown(f"**🌍 Traducción:** {traduccion_audio.text}")

                # Generar audio de la traducción
                tts = gTTS(text=traduccion_audio.text, lang=codigo_idioma_audio)
                audio_output = "audio_traducido.mp3"
                tts.save(audio_output)

                # Leer el audio y codificarlo en base64 para incrustarlo en HTML
                with open(audio_output, "rb") as f:
                    audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

                # Mostrar el reproductor de audio y el botón de descarga
                st.markdown(f"""
                <div class="audio-container">
                    <h2 class="audio-title">🎧 Audio de la Traducción</h2>
                    <div style='width: 100%;'>
                        <audio controls style='width: 100%; max-width: 100%;'>
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                    </div>
                    <div style='margin-top: 1rem; text-align: center;'>
                        <a href='data:audio/mp3;base64,{audio_base64}' download='traduccion.mp3' class='download-btn'>
                            ⬇️ Descargar Audio
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Limpiar archivos temporales
                os.remove(tmp_audio_path)
                os.remove(audio_output)
            except Exception as e:
                st.error(f"❌ Error al procesar audio: {e}")

# ---------------------------- Texto manual + ejercicios ----------------------------
st.markdown("## ✍️ Traducción Manual y Ejercicio")

# Inicialización de variables de sesión
if 'random_text' not in st.session_state:
    st.session_state.random_text = ""
if 'user_manual_text_input' not in st.session_state:
    st.session_state.user_manual_text_input = ""
if 'prev_idioma' not in st.session_state:
    st.session_state.prev_idioma = "🌐 Elegir idioma de traducción"

if 'typing' not in st.session_state:
    st.session_state.typing = False

if 'show_exercise' not in st.session_state:
    st.session_state.show_exercise = False

if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None

if 'exercise_options' not in st.session_state:
    st.session_state.exercise_options = []

if 'prev_idioma' not in st.session_state:
    st.session_state.prev_idioma = "🌐 Elegir idioma de traducción"

if 'audio_base64' not in st.session_state:
    st.session_state.audio_base64 = None

if 'audio_filename' not in st.session_state:
    st.session_state.audio_filename = None

# Lógica para el botón "Texto Aleatorio" — antes del text_area
if st.session_state.get("activar_aleatorio", False):
    nuevo_texto = random.choice(textos_ejemplo)
    st.session_state.user_manual_text_input = nuevo_texto
    st.session_state.activar_aleatorio = False

# Área de texto que reacciona al session_state
texto = st.text_area(
    "✍️ Escribe el texto que deseas traducir:",
    value=st.session_state.get("user_manual_text_input", ""),
    height=150,
    key="consistent_text_area_key"  # Key única y consistente
)

# Verificar si el texto ha sido borrado completamente
if texto.strip() == "" and st.session_state.get("user_manual_text_input", "").strip() != "":
    st.session_state.user_manual_text_input = ""
    st.session_state.show_exercise = False
    st.session_state.translation_result = None
    st.session_state.exercise_options = []
    st.session_state.selected_option = None
    st.session_state.audio_base64 = None
    st.session_state.audio_filename = None
    st.session_state.pop("texto_actual_ejercicio", None)
    st.session_state.pop("ejercicio_1_respuesta", None)
    st.session_state.pop("ejercicio_1_opciones", None)
    st.session_state.pop("ejercicio_2_datos", None)
    st.session_state.pop("ejercicio_3_datos", None)
    st.rerun()

# Selector de idioma de destino para la traducción manual
idioma_destino_texto = st.selectbox("🌐 Idioma de destino", idiomas_lista, index=0, key="idioma_destino")
codigo_idioma = None
if idioma_destino_texto != "🌐 Elegir idioma de traducción":
    for codigo, texto_idioma in idiomas.items():
        if texto_idioma == idioma_destino_texto:
            codigo_idioma = codigo
            break

# Resetear el ejercicio si el idioma de destino cambia
if idioma_destino_texto != st.session_state.prev_idioma:
    st.session_state.show_exercise = False
    st.session_state.translation_result = None
    st.session_state.exercise_options = []
    st.session_state.selected_option = None
    st.session_state.audio_base64 = None
    st.session_state.audio_filename = None
    st.session_state.prev_idioma = idioma_destino_texto
    st.session_state.pop("texto_actual_ejercicio", None)
    st.session_state.pop("ejercicio_1_respuesta", None)
    st.session_state.pop("ejercicio_1_opciones", None)
    st.session_state.pop("ejercicio_2_datos", None)
    st.session_state.pop("ejercicio_3_datos", None)
    st.rerun()

col1, col2 = st.columns([1, 1])
with col1:
    traducir = st.button("✨ Traducir y Escuchar", use_container_width=True)
with col2:
    import html

with col2:
    if st.button("🎲 Texto Aleatorio", use_container_width=True, key="random_btn"):
        nuevo_texto = random.choice(textos_ejemplo)
        st.session_state.user_manual_text_input = nuevo_texto
        st.session_state.translation_result = None
        st.session_state.exercise_options = []
        st.session_state.selected_option = None
        st.session_state.show_exercise = False
        st.session_state.audio_base64 = None
        st.session_state.audio_filename = None
        st.session_state.pop("texto_actual_ejercicio", None)
        st.session_state.pop("ejercicio_1_respuesta", None)
        st.session_state.pop("ejercicio_1_opciones", None)
        st.session_state.pop("ejercicio_2_datos", None)
        st.session_state.pop("ejercicio_3_datos", None)
        st.experimental_rerun()


# Lógica para el botón "Traducir y Escuchar"
if traducir:
    if not texto.strip():
        st.markdown("""<div style='background: rgba(0, 140, 255, 0.1); border-left: 6px solid #00b4ff; color: #a9dfff; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-weight: 500;'>⚠️ Por favor, escribe un texto para traducir.</div>""", unsafe_allow_html=True)
        st.session_state.show_exercise = False
    elif not codigo_idioma:
        st.markdown("""<div style='background: rgba(0, 140, 255, 0.1); border-left: 6px solid #00b4ff; color: #a9dfff; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-weight: 500;'>⚠️ Por favor, selecciona un idioma de destino.</div>""", unsafe_allow_html=True)
        st.session_state.show_exercise = False
    else:
        st.session_state.show_exercise = True
        st.session_state.selected_option = None

        with st.spinner("Traduciendo y generando audio..."):
            archivo_audio = None
            try:
                traductor = get_translator()
                st.session_state.translation_result = traductor.translate(texto, dest=codigo_idioma)

                opciones = [st.session_state.translation_result.text]
                while len(opciones) < 5:
                    falsa = random.choice(textos_ejemplo)
                    traduccion_falsa = get_translator().translate(falsa, dest=codigo_idioma).text
                    if traduccion_falsa not in opciones:
                        opciones.append(traduccion_falsa)
                random.shuffle(opciones)
                st.session_state.exercise_options = opciones

                tts = gTTS(text=st.session_state.translation_result.text, lang=codigo_idioma)
                archivo_audio = "traduccion_audio.mp3"
                tts.save(archivo_audio)

                with open(archivo_audio, "rb") as f:
                    audio_bytes = f.read()
                    st.session_state.audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                    st.session_state.audio_filename = archivo_audio

            except Exception as e:
                st.error(f"❌ Error al traducir o generar audio: {str(e)}")
                st.session_state.show_exercise = False
            finally:
                if archivo_audio and os.path.exists(archivo_audio):
                    os.remove(archivo_audio)
        st.rerun()

# Mostrar el ejercicio y el reproductor de audio
if st.session_state.show_exercise and st.session_state.translation_result:
    st.markdown("""<h3 class="audio-title">🧩 Ejercicios Prácticos</h3>""", unsafe_allow_html=True)

    texto_traduccion_clave = st.session_state.translation_result.text.strip()
    st.session_state.user_manual_text_input = st.session_state.translation_result.origin.strip()

    # Resetear ejercicios si cambia la traducción
    if st.session_state.get("texto_actual_ejercicio") != texto_traduccion_clave:
        st.session_state["texto_actual_ejercicio"] = texto_traduccion_clave
        st.session_state.pop("ejercicio_1_respuesta", None)
        st.session_state.pop("ejercicio_1_opciones", None)
        st.session_state.pop("ejercicio_2_datos", None)
        st.session_state.pop("ejercicio_3_datos", None)

    # EJERCICIO 1: Traducción correcta
    with st.expander("🧠 Traducción Correcta", expanded=False):
        if "ejercicio_1_respuesta" not in st.session_state:
            opciones = [texto_traduccion_clave]
            while len(opciones) < 4:
                falsa = random.choice(textos_ejemplo)
                traduccion_falsa = get_translator().translate(falsa, dest=codigo_idioma).text
                if traduccion_falsa not in opciones:
                    opciones.append(traduccion_falsa)
            random.shuffle(opciones)
            st.session_state.ejercicio_1_respuesta = texto_traduccion_clave
            st.session_state.ejercicio_1_opciones = opciones

        opcion_seleccionada = st.radio("Selecciona la traducción correcta:", st.session_state.ejercicio_1_opciones, key="opciones_traduccion")
        
        col1, col2 = st.columns([1, 1], gap="medium")
        verificar_click = col1.button("✅ Verificar", key="verificar_btn_1")
        ver_respuesta_click = col2.button("👁️ Ver Respuesta", key="ver_respuesta_btn_1")

        if verificar_click:
            if opcion_seleccionada == st.session_state.ejercicio_1_respuesta:
                st.success("✅ ¡Correcto! Has seleccionado la opción adecuada.")
            else:
                st.error("❌ Lo siento, esa no es la opción correcta.")

        if ver_respuesta_click:
            st.info(f"✅ Respuesta correcta: {st.session_state.ejercicio_1_respuesta}")

    # EJERCICIO 2: Completa la oración
    with st.expander("✍️ Completa Oración", expanded=False):
        if "ejercicio_2_datos" not in st.session_state: 
            partes = texto_traduccion_clave.split()

            if len(partes) < 3:
               st.warning("⚠️ El texto es demasiado corto para generar un ejercicio de completar. Usa uno más largo.")
            else:
               index_vacio = random.randint(1, len(partes) - 2)
               respuesta = partes[index_vacio]
               partes[index_vacio] = "_____"
               oracion = " ".join(partes)
               opciones = [respuesta]
               while len(opciones) < 4:
                   palabra_falsa = random.choice(random.choice(textos_ejemplo).split())
                   if palabra_falsa not in opciones:
                       opciones.append(palabra_falsa)
               random.shuffle(opciones)
               st.session_state.ejercicio_2_datos = {
                  "oracion": oracion,
                  "respuesta": respuesta,
                  "opciones": opciones
                }                              
            partes[index_vacio] = "_____"
            oracion = " ".join(partes)
            opciones = [respuesta]
            while len(opciones) < 4:
                palabra_falsa = random.choice(random.choice(textos_ejemplo).split())
                if palabra_falsa not in opciones:
                    opciones.append(palabra_falsa)
            random.shuffle(opciones)
            st.session_state.ejercicio_2_datos = {"oracion": oracion, "respuesta": respuesta, "opciones": opciones}

        st.markdown(f"**📝 {html.escape(st.session_state.ejercicio_2_datos['oracion'])}**")
        seleccion = st.radio("Elige la palabra que completa la oración:", st.session_state.ejercicio_2_datos['opciones'], key="completar_radio")

        col1, col2 = st.columns([1, 1], gap="medium")
        verificar_click = col1.button("✅ Verificar", key="verificar_completar")
        ver_respuesta_click = col2.button("👁️ Ver Respuesta", key="ver_respuesta_completar")

        if verificar_click:
            if seleccion == st.session_state.ejercicio_2_datos['respuesta']:
                st.success("✅ Correcto! Has completado la oración correctamente.")
            else:
                st.error("❌ Incorrecto. Esa no es la palabra correcta.")

        if ver_respuesta_click:
            st.info(f"✅ Respuesta correcta: '{st.session_state.ejercicio_2_datos['respuesta']}'")

    # EJERCICIO 3: Ordena la frase
    with st.expander("🔀 Ordena Frase", expanded=False):
        if "ejercicio_3_datos" not in st.session_state:
            palabras = texto_traduccion_clave.split()

            if len(palabras) < 2:
                st.warning("⚠️ El texto es demasiado corto para generar un ejercicio de ordenar. Escribe al menos dos palabras.")
            else:
                desordenadas = palabras.copy()
                random.shuffle(desordenadas)
                st.session_state.ejercicio_3_datos = {"correcta": " ".join(palabras), "desordenadas": desordenadas}


        st.markdown(f"**🔁 Palabras desordenadas:** {' | '.join(st.session_state.ejercicio_3_datos['desordenadas'])}")
        orden_usuario = st.text_input("✍️ Escribe la frase ordenada correctamente:", key="orden_frase")

        col1, col2 = st.columns([1, 1], gap="medium")
        verificar_click = col1.button("✅ Verificar", key="verificar_orden")
        ver_respuesta_click = col2.button("👁️ Ver Respuesta", key="ver_respuesta_orden")

        if verificar_click:
            if orden_usuario.strip().lower() == st.session_state.ejercicio_3_datos['correcta'].strip().lower():
                st.success("✅ Correcto! Has ordenado la frase correctamente.")
            else:
                st.error("❌ Incorrecto. Esa no es la frase ordenada correctamente.")

        if ver_respuesta_click:
            st.info(f"✅ Frase correcta: {st.session_state.ejercicio_3_datos['correcta']}")

    # AUDIO DE LA TRADUCCIÓN
    if st.session_state.get('audio_base64') and st.session_state.get('audio_filename'):
        st.markdown(f"""
        <div class=\"audio-container\">
            <h2 class=\"audio-title\">🎧 Audio de la Traducción</h2>
            <div style='width: 100%;'>
                <audio controls style='width: 100%; max-width: 100%;'>
                    <source src="data:audio/mp3;base64,{st.session_state.audio_base64}" type="audio/mp3">
                </audio>
            </div>
            <div style='margin-top: 1rem; text-align: center;'>
                <a href='data:audio/mp3;base64,{st.session_state.audio_base64}' download='{st.session_state.audio_filename}' class='download-btn'>
                    ⬇️ Descargar Audio
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

if idioma_destino_texto != st.session_state.prev_idioma:
    st.session_state.prev_idioma = idioma_destino_texto
    st.session_state.pop("texto_actual_ejercicio", None)
    st.session_state.pop("ejercicio_1_respuesta", None)
    st.session_state.pop("ejercicio_1_opciones", None)
    st.session_state.pop("ejercicio_2_datos", None)
    st.session_state.pop("ejercicio_3_datos", None)
    st.rerun()