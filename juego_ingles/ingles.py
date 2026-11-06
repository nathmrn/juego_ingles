import streamlit as st
from gtts import gTTS
import io
import random

# Configuración de la página
st.set_page_config(
    page_title="English Quest | Aprende Inglés Jugando",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para una interfaz moderna y dinámica
st.markdown("""
<style>
    /* Estilo general y fondo */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }

    /* Contenedor principal de tarjetas */
    .game-card {
        background: rgba(30, 41, 59, 0.7);
        border: 2px solid #6366f1;
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }

    /* Títulos con gradiente */
    .gradient-text {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Badges de nivel */
    .level-badge {
        background: #4f46e5;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }

    /* Botones personalizados */
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        transition: all 0.2s ease;
        border: none;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BASE DE DATOS DE RECURSOS Y JUEGOS
# -----------------------------------------------------------------------------

LEVEL_DATA = {
    "A1 (Principiante)": {
        "audio_quiz": [
            {
                "word": "Apple",
                "options": ["Apple", "Pineapple", "Banana", "Grape"],
                "translation": "Manzana",
                "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400"
            },
            {
                "word": "Bicycle",
                "options": ["Car", "Bicycle", "Bus", "Train"],
                "translation": "Bicicleta",
                "img": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400"
            }
        ],
        "scramble": [
            {"sentence": "I like red apples", "translation": "Me gustan las manzanas rojas"},
            {"sentence": "She has a blue car", "translation": "Ella tiene un carro azul"}
        ],
        "wordsearch": ["DOG", "CAT", "SUN", "MILK", "BOOK"]
    },
    "A2 (Elemental)": {
        "audio_quiz": [
            {
                "word": "Breakfast",
                "options": ["Dinner", "Lunch", "Breakfast", "Snack"],
                "translation": "Desayuno",
                "img": "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400"
            },
            {
                "word": "Library",
                "options": ["Bookstore", "Library", "School", "Museum"],
                "translation": "Biblioteca",
                "img": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400"
            }
        ],
        "scramble": [
            {"sentence": "We went to the park yesterday", "translation": "Fuimos al parque ayer"},
            {"sentence": "He is listening to music", "translation": "Él está escuchando música"}
        ],
        "wordsearch": ["TRAVEL", "FRIEND", "SUMMER", "FLOWER"]
    },
    "B1 (Intermedio)": {
        "audio_quiz": [
            {
                "word": "Environment",
                "options": ["Pollution", "Environment", "Ecology", "Nature"],
                "translation": "Medio ambiente",
                "img": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400"
            }
        ],
        "scramble": [
            {"sentence": "If it rains we will stay home", "translation": "Si llueve nos quedaremos en casa"},
            {"sentence": "I have lived here for three years", "translation": "He vivido aquí durante tres años"}
        ],
        "wordsearch": ["JOURNEY", "WEATHER", "ADVICE", "SILENT"]
    },
    "B2 (Intermedio Alto)": {
        "audio_quiz": [
            {
                "word": "Entrepreneur",
                "options": ["Executive", "Manager", "Entrepreneur", "Investor"],
                "translation": "Emprendedor/a",
                "img": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=400"
            }
        ],
        "scramble": [
            {"sentence": "Had I known I would have helped you", "translation": "De haberlo sabido te habría ayudado"},
            {"sentence": "She insisted on paying for the dinner", "translation": "Ella insistió en pagar la cena"}
        ],
        "wordsearch": ["RESEARCH", "BEHAVIOR", "STRATEGY", "INSIGHT"]
    }
}


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------------------------------------------

def generate_audio_bytes(text: str) -> io.BytesIO:
    """Genera audio MP3 en inglés usando gTTS en memoria."""
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


def init_session_state():
    """Inicializa variables de estado globales."""
    if "xp" not in st.session_state:
        st.session_state.xp = 0
    if "streak" not in st.session_state:
        st.session_state.streak = 1
    if "ws_found" not in st.session_state:
        st.session_state.ws_found = set()


init_session_state()

# -----------------------------------------------------------------------------
# SIDEBAR / NAVEGACIÓN
# -----------------------------------------------------------------------------

with st.sidebar:
    st.markdown("<h1 class='gradient-text'>⚡ English Quest</h1>", unsafe_allow_html=True)

    # Marcadores de gamificación
    col_xp, col_streak = st.columns(2)
    col_xp.metric("⭐ Experiencia", f"{st.session_state.xp} XP")
    col_streak.metric("🔥 Racha", f"{st.session_state.streak} días")

    st.markdown("---")

    level = st.selectbox(
        "🎯 Selecciona tu Nivel:",
        options=list(LEVEL_DATA.keys())
    )

    game_mode = st.radio(
        "🎮 Modo de Juego:",
        options=["🖼️ Flashcards y Escucha", "🧩 Constructor de Oraciones", "🔍 Sopa de Letras"]
    )

# -----------------------------------------------------------------------------
# MODOS DE JUEGO
# -----------------------------------------------------------------------------

# --- MODO 1: FLASHCARDS, AUDIO E IMÁGENES ---
if game_mode == "🖼️ Flashcards y Escucha":
    st.markdown(f"## 🖼️ Reto Audiovisual - Level <span class='level-badge'>{level.split()[0]}</span>",
                unsafe_allow_html=True)
    st.write("Escucha la pronunciación, observa la imagen y selecciona la palabra correcta.")

    items = LEVEL_DATA[level]["audio_quiz"]

    for idx, item in enumerate(items):
        with st.container():
            st.markdown("<div class='game-card'>", unsafe_allow_html=True)
            col_img, col_quiz = st.columns([1, 1.5])

            with col_img:
                st.image(item["img"], use_container_width=True, caption="¿Qué representa esta imagen?")

            with col_quiz:
                st.markdown("### Escucha el audio:")
                audio_fp = generate_audio_bytes(item["word"])
                st.audio(audio_fp, format="audio/mp3")

                selected = st.radio(
                    f"¿Qué palabra escuchaste o viste?",
                    options=item["options"],
                    key=f"radio_{level}_{idx}"
                )

                if st.button(f"Comprobar #{idx + 1}", key=f"btn_{level}_{idx}"):
                    if selected == item["word"]:
                        st.success(f"¡Correcto! 🎉 '{item['word']}' significa '{item['translation']}'.")
                        st.session_state.xp += 15
                    else:
                        st.error(f"¡Casi! La opción correcta era **{item['word']}**.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- MODO 2: CONSTRUCTOR DE ORACIONES (SCRAMBLE) ---
elif game_mode == "🧩 Constructor de Oraciones":
    st.markdown(f"## 🧩 Oraciones Desordenadas - Level <span class='level-badge'>{level.split()[0]}</span>",
                unsafe_allow_html=True)
    st.write("Ordena las palabras para formar la oración correcta según la traducción dada.")

    scramble_items = LEVEL_DATA[level]["scramble"]

    for idx, s_data in enumerate(scramble_items):
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)
        st.markdown(f"**Traducción:** *\"{s_data['translation']}\"*")

        words = s_data["sentence"].split()

        # Desordenar palabras usando una semilla fija por índice para mantener consistencia
        random.seed(idx + len(level))
        shuffled_words = words.copy()
        random.shuffle(shuffled_words)

        st.write("Palabras disponibles:")
        st.info(" | ".join(shuffled_words))

        user_input = st.text_input(
            "Escribe la oración completa ordenada:",
            key=f"scramble_{level}_{idx}"
        )

        if st.button(f"Verificar Oración #{idx + 1}", key=f"s_btn_{level}_{idx}"):
            if user_input.strip().lower() == s_data["sentence"].lower():
                st.success("¡Excelente trabajo! 🌟 Oración correcta.")
                st.session_state.xp += 20
                # Escuchar la oración completa
                st.audio(generate_audio_bytes(s_data["sentence"]), format="audio/mp3")
            else:
                st.error(f"Sigue intentándolo. Respuesta esperada: **{s_data['sentence']}**")

        st.markdown("</div>", unsafe_allow_html=True)

# --- MODO 3: SOPA DE LETRAS ---
elif game_mode == "🔍 Sopa de Letras":
    st.markdown(f"## 🔍 Sopa de Letras Interactiva - Level <span class='level-badge'>{level.split()[0]}</span>",
                unsafe_allow_html=True)
    st.write("Encuentra las palabras ocultas de tu nivel en el tablero.")

    target_words = LEVEL_DATA[level]["wordsearch"]

    col_grid, col_words = st.columns([2, 1])

    with col_words:
        st.markdown("### Palabras a buscar:")
        for w in target_words:
            if w in st.session_state.ws_found:
                st.markdown(f"~{w}~ ✅")
            else:
                st.markdown(f"👉 **{w}**")

        word_found_input = st.text_input("¿Qué palabra encontraste?").strip().upper()
        if st.button("Validar Palabra"):
            if word_found_input in target_words and word_found_input not in st.session_state.ws_found:
                st.session_state.ws_found.add(word_found_input)
                st.session_state.xp += 25
                st.success(f"¡Encontraste **{word_found_input}**! +25 XP")
                st.rerun()
            elif word_found_input in st.session_state.ws_found:
                st.warning("Ya habías encontrado esa palabra.")
            else:
                st.error("Esa palabra no está en la lista o no es correcta.")

    with col_grid:
        # Generación visual de tablero 8x8 con las palabras
        grid = [
            ['T', 'R', 'A', 'V', 'E', 'L', 'O', 'P'],
            ['D', 'O', 'G', 'F', 'R', 'I', 'E', 'N'],
            ['S', 'U', 'N', 'L', 'M', 'I', 'L', 'K'],
            ['B', 'O', 'O', 'K', 'S', 'U', 'M', 'M'],
            ['C', 'A', 'T', 'F', 'L', 'O', 'W', 'E'],
            ['W', 'E', 'A', 'T', 'H', 'E', 'R', 'R'],
            ['J', 'O', 'U', 'R', 'N', 'E', 'Y', 'S'],
            ['R', 'E', 'S', 'E', 'A', 'R', 'C', 'H']
        ]

        st.markdown("<div class='game-card'>", unsafe_allow_html=True)
        # Mostrar matriz estilo tablero
        grid_html = "<table style='width:100%; text-align:center; font-family:monospace; font-size:1.4rem; border-collapse:collapse;'>"
        for row in grid:
            grid_html += "<tr>"
            for cell in row:
                grid_html += f"<td style='padding:8px; border:1px solid #475569; background:#1e293b;'>{cell}</td>"
            grid_html += "</tr>"
        grid_html += "</table>"
        st.markdown(grid_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)