import streamlit as st

st.set_page_config(page_title="The Hollow House", page_icon="🕯️")

# HTML and CSS elements
st.markdown("""
<style>
.stApp {
    background: #09090d;
    color: #ded6ca;
}
h1, h2, h3 {
    color: #c84545 !important;
}
.story {
    background: #15151c;
    border-left: 4px solid #8b2020;
    padding: 22px;
    margin: 18px 0;
    border-radius: 6px;
    font-size: 18px;
    line-height: 1.7;
}
.whisper {
    color: #9a8a8a;
    font-style: italic;
    text-align: center;
}
</style>
<h1 style="text-align:center;">🕯️ The Hollow House</h1>
<p class="whisper">The house remembers everyone who enters.</p>
""", unsafe_allow_html=True)

ROOMS = {
    "entrance": {
        "text": (
            "Rain lashes the windows behind you. The front door slams shut. "
            "A staircase creaks upstairs, though you cannot see anyone."
        ),
        "choices": [
            ("Enter the library", "library"),
            ("Walk into the kitchen", "kitchen"),
            ("Climb the stairs", "landing"),
        ],
    },
    "library": {
        "text": (
            "Dust blankets the books. Inside an open drawer lies a brass key. "
            "Something scratches behind the shelves."
        ),
        "choices": [
            ("Take the brass key", "take_key"),
            ("Return to the entrance", "entrance"),
        ],
    },
    "kitchen": {
        "text": (
            "A candle burns beside a cold stove. Beneath your feet, "
            "a voice whispers through a locked cellar door."
        ),
        "choices": [
            ("Take the candle", "take_candle"),
            ("Open the cellar door", "open_cellar"),
            ("Return to the entrance", "entrance"),
        ],
    },
    "landing": {
        "text": (
            "At the end of the hallway stands a tall mirror. "
            "Your reflection smiles before you do."
        ),
        "choices": [
            ("Touch the mirror", "mirror"),
            ("Retreat downstairs", "entrance"),
        ],
    },
    "cellar": {
        "text": (
            "Your candle reveals a narrow passage. At its end, "
            "a red door pulses like a beating heart."
        ),
        "choices": [
            ("Open the red door", "escape"),
            ("Return to the kitchen", "kitchen"),
        ],
    },
}

DEFAULTS = {
    "room": "entrance",
    "health": 100,
    "inventory": [],
    "message": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value


def act(action):
    state = st.session_state
    state.message = ""

    if action == "take_key":
        if "Brass key" not in state.inventory:
            state.inventory.append("Brass key")
            state.message = "You pocket the key. The scratching stops."
        else:
            state.message = "The drawer is empty."

    elif action == "take_candle":
        if "Candle" not in state.inventory:
            state.inventory.append("Candle")
            state.message = "The flame leans toward you, against the draft."
        else:
            state.message = "You already have the candle."

    elif action == "open_cellar":
        if "Brass key" not in state.inventory:
            state.message = "The cellar is locked. You need a key."
        elif "Candle" not in state.inventory:
            state.message = "The darkness is too thick. Find a light."
        else:
            state.room = "cellar"

    elif action == "mirror":
        state.health = max(0, state.health - 35)
        state.message = "A freezing hand grips yours. You tear yourself away."
        if state.health == 0:
            state.room = "dead"

    else:
        state.room = action


with st.sidebar:
    st.header("Your survival")
    st.progress(st.session_state.health / 100)
    st.write(f"Health: {st.session_state.health}/100")
    st.subheader("Inventory")

    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"• {item}")
    else:
        st.caption("Your pockets are empty.")

    if st.button("Restart game", use_container_width=True):
        for key in DEFAULTS:
            del st.session_state[key]
        st.rerun()

if st.session_state.message:
    st.info(st.session_state.message)

room = st.session_state.room

if room == "escape":
    st.success(
        "You open the red door and stumble into the dawn. "
        "Behind you, the house exhales. You survived."
    )
    st.balloons()

elif room == "dead":
    st.error(
        "Your reflection steps out of the mirror. "
        "You take its place behind the glass. Game over."
    )

else:
    scene = ROOMS[room]
    st.markdown(
        f'<div class="story">{scene["text"]}</div>',
        unsafe_allow_html=True,
    )

    for label, action in scene["choices"]:
        st.button(
            label,
            key=f"{room}_{action}",
            on_click=act,
            args=(action,),
            use_container_width=True,
        )
