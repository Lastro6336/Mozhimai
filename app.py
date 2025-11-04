import streamlit as st
import base64
st.set_page_config(
    page_title="MOZHIMAI",
    page_icon="bg_3.jpg"
)


button_style = """
    <style>
    .center-button {
        display: flex;
        justify-content: center;
    }
    div.stButton > button:first-child {
        background-color: #002E4B;
        color: #F08729;
        font-size: 20px;
        padding: 15px 40px;
        border-radius: 12px;
        border: none;
        transition: 0.3s;
    }
    }
    </style>
    """ 
st.markdown(button_style , unsafe_allow_html= True)   


def add_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    page_bg = f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        height: 100%;
        width: 100%;
        background: url("data:image/png;base64,{encoded}") no-repeat center center fixed;
        background-size: cover;
    }}

    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="stApp"] {{
        background: transparent !important;
    }}

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stSidebar"] {{
        background: transparent 
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

add_bg("bg_4.jpg")

st.markdown("<h1 style='color:#002E4B;text-align:center;'>Welcome to MOZHIMAI </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#F08729;text-align:center;'>Your bridge to the Tamil world!""</h3>", unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 1, 1]) 
with col2: 
    if "page" not in st.session_state:
        st.session_state.page = "home"

def go_to_spell_corrector():
    st.session_state.page = "spell"
if st.session_state.page == "home":
    st.markdown("<style>.stButton>button{background-color:#002E4B;color:#F08729;}</style>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.45, 2, 1])
    with col2:
        st.button("Go to Spell Corrector", on_click=go_to_spell_corrector)

elif st.session_state.page == "spell":
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background:#D3D2D1;
            background-image: none !important;
        }

        [data-testid="stMainBlockContainer"],
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        [data-testid="stApp"] {
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h1 style='color:#002E4B;text-align:center;'>SPELL CORRECTOR</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#F08729;text-align:center;'>Where Tamizh meets Perfection!""</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.45,2,1])  
    with col2:
        if st.button("⬅ Back to Home"):
            st.session_state.page = "home"
    st.markdown("""
<style>
/* --- Container positioning --- */
div[data-testid="stTextInput"] {
    position: fixed;
    bottom: 12vh;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    z-index: 9999;
}

/* --- Outer container (make edges round) --- */
div[data-testid="stTextInput"] > div {
    border-radius: 50px !important;   
}

/* --- Inner text input field styling --- */
div[data-testid="stTextInput"] > div > div > input {
    background-color: #002E4B;  /* background color */
    color: #f8f8f8;                   /* text color */
    
    border-radius: 50pxt;   /* round the actual field */
    padding: 14px 24px;
    font-size: 20px;
    width: 100%;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.25);
    transition: all 0.25s ease-in-out;
}


}

/* --- Placeholder color --- */
div[data-testid="stTextInput"] > div > div > input::placeholder {
    color:#002E4B;
    opacity: 1.0;
}
</style>
""", unsafe_allow_html=True) 
    
    st.markdown(
        """
        <style>
        /* This is the existing background override */
        html, body, [data-testid="stAppViewContainer"] {
            background:#D3D2D1;
            background-image: none !important;
        }

        [data-testid="stMainBlockContainer"],
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        [data-testid="stApp"] {
            background: transparent !important;
        }
        
        /* --- NEW: Custom Result Box Class --- */
        .custom-result-box {
            background-color: #002E4B; /* Dark Blue Background */
            color: #F08729;          /* Orange Text */
            border-left: 5px solid #F08729;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        /* --- END NEW CSS --- */
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Existing input bar styling...
    st.markdown("""
<style>
/* ... (Your existing stTextInput CSS here) ... */
</style>
""", unsafe_allow_html=True) 

    user_text = st.text_input("Type in your input...", key="spell_input", label_visibility="collapsed", placeholder ="Type in your text....")
    
    if user_text:
        st.session_state["last_input"] = user_text
        
        # *** THIS IS THE CRITICAL CHANGE ***
        # Using custom markdown instead of st.success
        st.markdown(f'<div class="custom-result-box">You entered: {user_text}</div>', unsafe_allow_html=True)


    

