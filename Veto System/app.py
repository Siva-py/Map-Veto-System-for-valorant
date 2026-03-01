import streamlit as st
import random
import base64
import time
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "resources", "logo.png")
st.set_page_config(
    page_title="Valorant Map Veto",
    page_icon=logo_path,   
    layout="wide"
)

# ---------- IMAGE LOADER ----------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# ---------- MAP BACKGROUNDS ----------
default_background = os.path.join(BASE_DIR, "resources", "default screen.jpg")
map_backgrounds = {
    "Ascent": os.path.join(BASE_DIR, "resources", "ascent.jpg"),
    "Bind": os.path.join(BASE_DIR, "resources", "bind.jpg"),
    "Haven": os.path.join(BASE_DIR, "resources", "heaven.jpg"),
    "Split": os.path.join(BASE_DIR, "resources", "split.jpg"),
    "Lotus": os.path.join(BASE_DIR, "resources", "lotus.webp"),
    "Sunset": os.path.join(BASE_DIR, "resources", "sunset.webp"),
    "Breeze": os.path.join(BASE_DIR, "resources", "breeze.webp"),
}

default_background = os.path.join(BASE_DIR, "resources", "default screen.jpg")
deciding_background = os.path.join(BASE_DIR, "resources", "deceider screen.jpg")
# ---------- SESSION STATE ----------
if "available_maps" not in st.session_state:
    st.session_state.available_maps = [
        "Ascent", "Bind", "Haven",
        "Split", "Lotus", "Sunset", "Breeze"
    ]

if "ban_stage" not in st.session_state:
    st.session_state.ban_stage = "Team 1"

if "final_map" not in st.session_state:
    st.session_state.final_map = None

if "reveal_phase" not in st.session_state:
    st.session_state.reveal_phase = None

# ---------- DECIDING TRANSITION ----------
# ---------- DECIDING TRANSITION ----------
if st.session_state.reveal_phase == "deciding":

    deciding_bg = get_base64_image(deciding_background)

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{deciding_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        background: rgba(0,0,0,0.65);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:70px;
        font-weight:900;
        color:#FF4655;
        text-shadow:0 0 30px black;
        z-index:9999;
    ">
        DECIDING MAP...
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1.8)

    st.session_state.final_map = random.choice(st.session_state.available_maps)
    st.session_state.reveal_phase = None
    st.rerun()

# ---------- CHOOSE BACKGROUND ----------
if st.session_state.final_map:
    bg_image = get_base64_image(map_backgrounds[st.session_state.final_map])
else:
    bg_image = get_base64_image(default_background)

# ---------- CSS ----------
st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(5, 10, 20, 0.75);
    z-index: -1;
}}

header {{visibility: hidden;}}
footer {{visibility: hidden;}}

div[data-testid="stMarkdownContainer"] h1 {{
    color: #FFFFFF !important;
    text-align: center;
    font-weight: 900;
    letter-spacing: 3px;
}}

h2 {{
    color: #FFFFFF !important;
    text-align: center;
}}

.stButton>button {{
    background-color: rgba(15, 25, 35, 0.85);
    color: #FFFFFF;
    border: 2px solid #FF4655;
    border-radius: 14px;
    padding: 18px;
    font-weight: bold;
    transition: 0.3s ease-in-out;
}}

.stButton>button:hover {{
    background-color: #FF4655;
    color: black;
    transform: scale(1.05);
    box-shadow: 0 0 25px #FF4655;
}}

</style>
""", unsafe_allow_html=True)

st.title("VALORANT MAP VETO SYSTEM")

# ---------- IF MAP NOT DECIDED ----------
if not st.session_state.final_map:

    if st.session_state.ban_stage == "Team 1":
        phase = "TEAM 1 — BAN PHASE"
    elif st.session_state.ban_stage == "Team 2":
        phase = "TEAM 2 — BAN PHASE"
    else:
        phase = "MAP DECIDER READY"

    st.markdown(f"## {phase}")
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4)

    for i, map_name in enumerate(st.session_state.available_maps):
        with cols[i % 4]:
            if st.button(map_name, use_container_width=True):
                if st.session_state.ban_stage == "Team 1":
                    st.session_state.available_maps.remove(map_name)
                    st.session_state.ban_stage = "Team 2"
                elif st.session_state.ban_stage == "Team 2":
                    st.session_state.available_maps.remove(map_name)
                    st.session_state.ban_stage = "Done"
                st.rerun()

    if st.session_state.ban_stage == "Done":
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("INITIATE MAP DECIDER", use_container_width=True):
            st.session_state.reveal_phase = "deciding"
            st.rerun()

# ---------- REVEAL SCREEN ----------
else:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:70px;
            font-weight:900;
            color:white;
            text-shadow:0 0 40px black;
        ">
            MAP LOCKED IN
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:80px;
            font-weight:900;
            color:#FF4655;
            text-shadow:0 0 40px black;
        ">
            {st.session_state.final_map}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("RESET VETO"):
        st.session_state.available_maps = [
            "Ascent", "Bind", "Haven",
            "Split", "Lotus", "Sunset", "Breeze"
        ]
        st.session_state.ban_stage = "Team 1"
        st.session_state.final_map = None
        st.rerun()










