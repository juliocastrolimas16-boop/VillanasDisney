import streamlit as st
import random
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Villanas de Disney · Trivia",
    page_icon="🖤",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Crimson+Pro:ital,wght@0,300;0,400;1,300&display=swap');

/* ---------- global ---------- */
html, body, [class*="css"] {
    font-family: 'Crimson Pro', serif;
    background: #0a0005;
    color: #e8d5f5;
}

.stApp {
    background: radial-gradient(ellipse at 50% 0%, #2d0a3e 0%, #0a0005 60%);
    min-height: 100vh;
}

/* ---------- title ---------- */
.villain-title {
    font-family: 'Cinzel Decorative', cursive;
    font-size: clamp(1.6rem, 5vw, 2.8rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #c084fc, #f0abfc, #a855f7, #e879f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    letter-spacing: 0.04em;
    margin: 0.2em 0 0.1em;
    padding: 0;
    line-height: 1.2;
}

.villain-subtitle {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    font-size: 1.15rem;
    color: #c084fc99;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 0.15em;
}

/* ---------- question card ---------- */
.question-card {
    background: linear-gradient(135deg, #1a0928aa, #2d0a3eaa);
    border: 1px solid #7c3aed44;
    border-radius: 16px;
    padding: 2rem 2.2rem 1.6rem;
    margin: 1.5rem 0 1.2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 40px #7c3aed22, inset 0 1px 0 #c084fc22;
}

.question-number {
    font-family: 'Cinzel Decorative', cursive;
    font-size: 0.75rem;
    color: #a855f7;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

.question-text {
    font-size: 1.35rem;
    color: #f3e8ff;
    line-height: 1.5;
    font-weight: 400;
}

.villain-emoji {
    font-size: 2.8rem;
    text-align: center;
    display: block;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 12px #c084fc88);
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}

/* ---------- buttons ---------- */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #1e0733, #2d0a3e) !important;
    color: #e8d5f5 !important;
    border: 1px solid #7c3aed55 !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.2rem !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.1rem !important;
    text-align: left !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    margin-bottom: 0.3rem !important;
    box-shadow: 0 2px 12px #7c3aed11 !important;
}

div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #3b0764, #4c1d95) !important;
    border-color: #a855f7 !important;
    color: #f3e8ff !important;
    box-shadow: 0 0 20px #a855f744 !important;
    transform: translateX(4px) !important;
}

/* correct / wrong feedback */
.feedback-correct {
    background: linear-gradient(135deg, #064e3b, #065f46);
    border: 1px solid #10b981;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #6ee7b7;
    font-size: 1.1rem;
    margin: 0.5rem 0;
}

.feedback-wrong {
    background: linear-gradient(135deg, #450a0a, #7f1d1d);
    border: 1px solid #ef4444;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #fca5a5;
    font-size: 1.1rem;
    margin: 0.5rem 0;
}

/* ---------- progress ---------- */
.progress-bar-container {
    background: #1a0928;
    border-radius: 99px;
    height: 6px;
    margin: 0.8rem 0 1.6rem;
    overflow: hidden;
    border: 1px solid #7c3aed33;
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #7c3aed, #e879f9);
    border-radius: 99px;
    transition: width 0.4s ease;
    box-shadow: 0 0 8px #c084fc88;
}

/* ---------- score / result ---------- */
.score-display {
    font-family: 'Cinzel Decorative', cursive;
    font-size: 2.5rem;
    text-align: center;
    color: #f0abfc;
    margin: 0.5rem 0;
}

.result-card {
    background: linear-gradient(135deg, #1a0928cc, #2d0a3ecc);
    border: 1px solid #a855f766;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    box-shadow: 0 0 60px #7c3aed33;
}

/* ---------- confetti / sparkles animation ---------- */
.sparkle-container {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
}

@keyframes confetti-fall {
    0%   { transform: translateY(-20px) rotate(0deg);   opacity: 1; }
    100% { transform: translateY(300px) rotate(720deg); opacity: 0; }
}

@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 20px #c084fc55, 0 0 60px #7c3aed22; }
    50%       { box-shadow: 0 0 40px #f0abfc88, 0 0 100px #a855f755; }
}

.perfect-score-card {
    animation: glow-pulse 2s ease-in-out infinite;
}

.magic-text {
    font-family: 'Cinzel Decorative', cursive;
    font-size: clamp(1.3rem, 4vw, 2rem);
    background: linear-gradient(135deg, #fbbf24, #f0abfc, #34d399, #60a5fa, #f472b6);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: rainbow-shift 2s ease infinite;
}

@keyframes rainbow-shift {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
}

.firework {
    display: inline-block;
    animation: pop 0.6s ease forwards;
}
@keyframes pop {
    0%   { transform: scale(0) rotate(-10deg); opacity: 0; }
    60%  { transform: scale(1.3) rotate(5deg);  opacity: 1; }
    100% { transform: scale(1) rotate(0deg);    opacity: 1; }
}

/* ---------- misc ---------- */
.stRadio > div { display: none; }   /* hide default radios */
hr { border-color: #7c3aed22 !important; }

div[data-testid="stMarkdownContainer"] p { font-size: 1.05rem; }
</style>
""", unsafe_allow_html=True)


# ── Trivia data ───────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "emoji": "🍎",
        "villana": "La Reina Malvada",
        "pregunta": "¿Cuál es el verdadero nombre de la Reina Malvada en Blancanieves, según los materiales oficiales de Disney?",
        "opciones": [
            "Regina Mills",
            "Grimhilde",
            "Ravenna",
            "Maleficent",
        ],
        "correcta": "Grimhilde",
        "dato": "Su nombre oficial es la Reina Grimhilde — aunque la película nunca lo menciona directamente.",
    },
    {
        "emoji": "🐙",
        "villana": "Úrsula",
        "pregunta": "Úrsula es una cecaelia (mitad humana, mitad pulpo). ¿Cuántos tentáculos tiene?",
        "opciones": ["4", "6", "8", "10"],
        "correcta": "6",
        "dato": "¡Sorpresa! Úrsula tiene solo 6 tentáculos, no 8 como un pulpo real.",
    },
    {
        "emoji": "🐾",
        "villana": "Cruella de Vil",
        "pregunta": "En '101 Dálmatas', ¿cuántos cachorros roba Cruella para hacer su soñado abrigo?",
        "opciones": ["84", "97", "99", "101"],
        "correcta": "99",
        "dato": "Cruella roba 99 cachorros; sumados a los 2 de Pongo y Perdita hacen 101 dálmatas.",
    },
    {
        "emoji": "🌹",
        "villana": "Maléfica",
        "pregunta": "¿Qué don NO le otorgan las hadas buenas a la Bella Durmiente antes de que Maléfica la maldiga?",
        "opciones": [
            "Belleza",
            "Gracia en la danza y el canto",
            "Inteligencia",
            "Que su sueño sea roto por un beso de amor verdadero",
        ],
        "correcta": "Inteligencia",
        "dato": "Las hadas le dan belleza, voz melodiosa y romper el hechizo con un beso — la inteligencia no estaba en la lista.",
    },
    {
        "emoji": "🦁",
        "villana": "Scar",
        "pregunta": "¿Cuál es el nombre original swahili dado a Scar antes de que se convirtiera en el villano de El Rey León?",
        "opciones": ["Taka", "Mufasa", "Simba", "Kovu"],
        "correcta": "Taka",
        "dato": "Scar nació como 'Taka', que en swahili significa 'basura' o 'querer'. Se le llamó Scar tras la cicatriz que le dejó un búfalo.",
    },
]

# ── Session state init ────────────────────────────────────────────────────────
if "started" not in st.session_state:
    st.session_state.started = False
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "shuffled_options" not in st.session_state:
    st.session_state.shuffled_options = []
if "finished" not in st.session_state:
    st.session_state.finished = False
if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []


def start_game():
    st.session_state.started = True
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.finished = False
    st.session_state.wrong_answers = []
    shuffle_options(0)


def shuffle_options(idx):
    opts = QUESTIONS[idx]["opciones"][:]
    random.shuffle(opts)
    st.session_state.shuffled_options = opts


def answer(option):
    if st.session_state.answered:
        return
    st.session_state.selected = option
    st.session_state.answered = True
    q = QUESTIONS[st.session_state.q_index]
    if option == q["correcta"]:
        st.session_state.score += 1
    else:
        st.session_state.wrong_answers.append(st.session_state.q_index)


def next_question():
    next_idx = st.session_state.q_index + 1
    if next_idx >= len(QUESTIONS):
        st.session_state.finished = True
    else:
        st.session_state.q_index = next_idx
        st.session_state.answered = False
        st.session_state.selected = None
        shuffle_options(next_idx)


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<p class="villain-title">Villanas de Disney</p>', unsafe_allow_html=True)
st.markdown('<p class="villain-subtitle">✦ Trivia Oscura ✦</p>', unsafe_allow_html=True)

# ── WELCOME SCREEN ────────────────────────────────────────────────────────────
if not st.session_state.started and not st.session_state.finished:
    st.markdown("""
    <div class="question-card" style="text-align:center;">
        <span class="villain-emoji">🖤</span>
        <p style="font-size:1.2rem; color:#e8d5f5; margin-bottom:0.5rem;">
            ¿Conoces a las villanas más icónicas del reino de Disney?
        </p>
        <p style="font-size:1rem; color:#a855f7; font-style:italic;">
            5 preguntas · alternativas aleatorias · animación épica si aciertas todo 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚡ Comenzar el juego", use_container_width=True):
            start_game()
            st.rerun()

# ── FINISHED SCREEN ───────────────────────────────────────────────────────────
elif st.session_state.finished:
    score = st.session_state.score
    total = len(QUESTIONS)
    perfect = score == total

    if perfect:
        # Sparkles / magic animation
        sparkles = "✨🌟💫⭐🌠✨🌟💫⭐🌠✨"
        st.markdown(f"""
        <div class="result-card perfect-score-card sparkle-container">
            <div style="font-size:3.5rem; margin-bottom:0.5rem; animation: float 2s ease-in-out infinite;">
                🏆
            </div>
            <p class="magic-text">¡Maestra de las Sombras!</p>
            <p style="font-size:1.5rem; color:#fbbf24; letter-spacing:0.2em; margin:0.3rem 0;">
                {sparkles}
            </p>
            <p style="font-size:1.1rem; color:#e8d5f5; margin: 1rem 0 0.3rem;">
                Puntuación perfecta
            </p>
            <div class="score-display">{score} / {total}</div>
            <p style="color:#c084fc; font-style:italic; font-size:1rem; margin-top:0.8rem;">
                Las villanas te reconocen como una de las suyas 🖤
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Animated confetti via streamlit balloons + custom overlay
        time.sleep(0.3)
        st.balloons()

    else:
        emoji_map = {5: "🏆", 4: "🌟", 3: "🌙", 2: "🌒", 1: "💀", 0: "🕸️"}
        msg_map = {
            5: "¡Perfecta!", 4: "¡Casi perfecta!", 3: "No está mal...",
            2: "Las villanas te miran con desconfianza.", 1: "Mmm... sigue intentando.",
            0: "Las villanas se ríen de ti 😈"
        }
        e = emoji_map.get(score, "🌙")
        msg = msg_map.get(score, "Sigue intentando.")

        st.markdown(f"""
        <div class="result-card">
            <div style="font-size:3rem; margin-bottom:0.5rem;">{e}</div>
            <p style="font-size:1.15rem; color:#c084fc;">{msg}</p>
            <p style="font-size:1rem; color:#e8d5f5; margin: 0.5rem 0 0.3rem;">Tu puntuación</p>
            <div class="score-display">{score} / {total}</div>
        </div>
        """, unsafe_allow_html=True)

    # Wrong answers review
    if st.session_state.wrong_answers:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📖 Revisar respuestas incorrectas"):
            for idx in st.session_state.wrong_answers:
                q = QUESTIONS[idx]
                st.markdown(f"""
                <div style="margin-bottom:1rem; padding:1rem; background:#1a0928; border-radius:10px; border-left:3px solid #7c3aed;">
                    <p style="color:#c084fc; font-weight:bold; margin:0 0 0.3rem;">{q['emoji']} {q['pregunta']}</p>
                    <p style="color:#6ee7b7; margin:0 0 0.2rem;">✅ Respuesta correcta: <strong>{q['correcta']}</strong></p>
                    <p style="color:#94a3b8; font-style:italic; margin:0; font-size:0.95rem;">💡 {q['dato']}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Jugar de nuevo", use_container_width=True):
            start_game()
            st.rerun()

# ── GAME SCREEN ───────────────────────────────────────────────────────────────
elif st.session_state.started:
    q_idx = st.session_state.q_index
    q = QUESTIONS[q_idx]
    total = len(QUESTIONS)

    # Progress bar
    progress_pct = int((q_idx / total) * 100)
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-bar-fill" style="width:{progress_pct}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Score tracker
    cols = st.columns([3, 1])
    with cols[1]:
        st.markdown(f"<p style='text-align:right; color:#a855f7; font-size:0.9rem;'>⭐ {st.session_state.score} pts</p>", unsafe_allow_html=True)

    # Question card
    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Pregunta {q_idx + 1} de {total} · {q['villana']}</div>
        <span class="villain-emoji">{q['emoji']}</span>
        <p class="question-text">{q['pregunta']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Answer options
    if not st.session_state.answered:
        for opt in st.session_state.shuffled_options:
            if st.button(f"  {opt}", key=f"opt_{q_idx}_{opt}", use_container_width=True):
                answer(opt)
                st.rerun()
    else:
        # Show result feedback
        correct = q["correcta"]
        selected = st.session_state.selected

        for opt in st.session_state.shuffled_options:
            if opt == correct:
                st.markdown(f'<div class="feedback-correct">✅ {opt}</div>', unsafe_allow_html=True)
            elif opt == selected and opt != correct:
                st.markdown(f'<div class="feedback-wrong">❌ {opt}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="padding:0.7rem 1.4rem; color:#6b7280; margin:0.3rem 0;">{opt}</div>', unsafe_allow_html=True)

        # Fun fact
        if selected == correct:
            st.markdown(f"""
            <div style="background:#0f2e1f; border:1px solid #10b981; border-radius:10px; padding:1rem 1.4rem; margin-top:0.8rem; color:#6ee7b7; font-style:italic; font-size:0.98rem;">
                💡 {q['dato']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#1a0928; border:1px solid #7c3aed55; border-radius:10px; padding:1rem 1.4rem; margin-top:0.8rem; color:#c084fc; font-style:italic; font-size:0.98rem;">
                💡 {q['dato']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        label = "🏁 Ver resultado" if q_idx == total - 1 else "➡️ Siguiente pregunta"
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(label, use_container_width=True):
                next_question()
                st.rerun()
