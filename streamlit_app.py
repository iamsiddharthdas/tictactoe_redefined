# streamlit_app.py
import streamlit as st

# --- Page config & CSS ---
st.set_page_config(
    page_title="Tic-Tac-Toe Arena",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .game-grid button {
        width: 80px;
        height: 80px;
        font-size: 2.5rem;
        margin: 4px;
        border-radius: 12px;
        background: #FFFFFF;
        border: 2px solid #DDD;
        transition: transform 0.1s ease-in-out, background 0.2s;
    }
    .game-grid button:hover {
        transform: scale(1.05);
        background: #F0F0F0;
    }
    .game-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        max-width: 280px;
        margin: auto;
    }
    .win-cell {
        background: #A8E6A3 !important;
        border-color: #6CBA6C !important;
    }
    .title {
        font-size: 3rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .header {
        background: linear-gradient(135deg, #7e5bef, #5a31f4);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .btn-reset {
        margin-top: 1rem;
        background: white;
        color: #5a31f4;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .btn-reset:hover {
        background: #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.moves = {"X": [], "O": []}
    st.session_state.player = "X"
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}
    st.session_state.winning_line = None

# --- Game Logic Functions ---
def check_win(player):
    b = st.session_state.board
    # rows, cols, diags
    lines = []
    for i in range(3):
        lines.append([(i, j) for j in range(3)])
        lines.append([(j, i) for j in range(3)])
    lines.append([(i, i) for i in range(3)])
    lines.append([(i, 2 - i) for i in range(3)])
    for line in lines:
        if all(b[r][c] == player for r, c in line):
            return line
    return None

def check_draw():
    return all(cell for row in st.session_state.board for cell in row)

def make_move(r, c):
    # ignore if occupied or game over
    if st.session_state.board[r][c] or st.session_state.winning_line:
        return

    # FIFO removal if player has 3 on board
    moves = st.session_state.moves[st.session_state.player]
    if len(moves) == 3:
        old_r, old_c = moves.pop(0)
        st.session_state.board[old_r][old_c] = ""
    # place new move
    st.session_state.board[r][c] = st.session_state.player
    moves.append((r, c))

    # check win
    line = check_win(st.session_state.player)
    if line:
        st.session_state.winning_line = line
        st.session_state.scores[st.session_state.player] += 1
        return

    # check draw
    if check_draw():
        st.session_state.scores["Draw"] += 1
        return

    # switch player
    st.session_state.player = "O" if st.session_state.player == "X" else "X"

def reset_game():
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.moves = {"X": [], "O": []}
    st.session_state.player = "X"
    st.session_state.winning_line = None

# --- UI Rendering ---
st.markdown('<div class="header"><span class="title">Tic-Tac-Toe Arena</span></div>', unsafe_allow_html=True)

# Scoreboard & Turn Indicator
cols = st.columns(3)
cols[0].metric("X Score", st.session_state.scores["X"])
cols[1].metric("O Score", st.session_state.scores["O"])
cols[2].metric("Draws", st.session_state.scores["Draw"])
st.markdown(f"**Current Player:** {st.session_state.player}", unsafe_allow_html=True)

# Game Grid
grid_html = '<div class="game-grid">'
for r in range(3):
    for c in range(3):
        cell = st.session_state.board[r][c]
        # assign CSS class for winning cells
        extra = ""
        if st.session_state.winning_line and (r, c) in st.session_state.winning_line:
            extra = ' class="win-cell"'
        key = f"btn_{r}_{c}_{cell}"
        # render each button
        if st.button(cell or " ", key=key, on_click=make_move, args=(r,c), disabled=bool(cell) or bool(st.session_state.winning_line)):
            pass
        # wrapping manually with CSS grid container
    # newline handled by flex wrapping
grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)

# Display win/draw messages
if st.session_state.winning_line:
    st.success(f"Player {st.session_state.player} wins!")
elif check_draw() and not st.session_state.winning_line:
    st.info("It's a draw!")

# Reset button
st.button("🔄 New Game", on_click=reset_game, help="Start a fresh game", key="reset", css_class="btn-reset")