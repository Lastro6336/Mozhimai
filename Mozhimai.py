import streamlit as st
from openai import OpenAI
import time
import base64
import requests 

def add_bg(image_source):
    """Add background image from either local file or online URL."""
    try:
        if image_source.startswith("http"):
            data = requests.get(image_source).content
        else:
            with open(image_source, "rb") as f:
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
            background: transparent;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load background image: {e}")
        
        
add_bg("https://raw.githubusercontent.com/Lastro6336/Mozhimai/main/bg_4.jpg")


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




st.markdown("<h1 style='color:#002E4B;text-align:center;'>Welcome to MOZHIMAI </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#F08729;text-align:center;'>Your bridge to the Tamizh world!""</h3>", unsafe_allow_html=True)


OPENAI_API_KEY = "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"

st.set_page_config(
    page_title="MOZHIMAI",
    page_icon="logo only.jpg" 
)


custom_styles = """
    <style>
    /* Force main app background to ensure visibility if user's browser is dark mode */
    [data-testid="stAppViewContainer"] > .main {
        background-color: #F0F2F6; /* Light gray for contrast */
    }

    /* Button Styling */
    .stButton > button:first-child {
        background-color: #002E4B;
        color: #FD8419;
        font-size: 20px;
        padding: 15px 40px;
        border-radius: 12px;
        border: none;
        transition: 0.3s;
    }
    
    /* Input Field Styling */
    div[data-testid="stTextInput"] {
        position: fixed;
        bottom: 12vh;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        z-index: 9999;
    }

    div[data-testid="stTextInput"] > div > div > input {
        background-color: #002E4B;
        color: #f8f8f8;
        border-radius: 50px; /* Note: Changed 50pxt to 50px */
        padding: 14px 24px;
        font-size: 20px;
        width: 100%;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.25);
        transition: all 0.25s ease-in-out;
    }

    
    div[data-testid="stTextInput"] > div > div > input::placeholder {
        color: #FD8419; /* Changed placeholder color for better contrast */
        opacity: 0.8;
    }
    
    .custom-result-box {
        background-color: #002E4B; 
        color: #FD8419;          
        border-left: 5px solid #F08729;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        white-space: pre-wrap; /* Ensures line breaks in the output are respected */
    }
    </style>
    """ 
st.markdown(custom_styles, unsafe_allow_html=True)   

# --- OpenAI Client and Correction Function ---

def get_openai_client():
    """Initializes and caches the OpenAI client."""
    return OpenAI(api_key=OPENAI_API_KEY)

def correct(string):
    """
    Performs the multi-step correction process using the OpenAI API:
    1. Classifies the input (Code Mixing/Switching/Casual).
    2. Corrects grammar/spelling based on classification.
    3. Corrects emojis.
    """
    client = get_openai_client()
    text = string
    
    try:
        # --- Step 1: Classification ---
        prompt_1 = f"check the tamil sentence has code mixing or code switching or casual code switching and give output as 1 for code mixing and 2 for code switching and output as 0 for casual code switching:\n\n{text}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_1}]
        )
        a = response.choices[0].message.content.strip()
        
        # --- Step 2: Select Correction Prompt ---
        
        prompt_2 = f"check for spelling, grammar mistake in the tamil code switched sentence and correct them and give only corrected sentence as tamil output:\n\n{text}"
        prompt_3 = f"check for spelling, grammar mistake in the tamil code mixed sentence and correct them and give only corrected sentence as tamil output:\n\n{text}"
        prompt_4 = f"check for spelling, grammar mistake in the tamil Casual Code-Switching sentence and correct them and give only corrected sentence as tamil output:\n\n{text}"
        
        prompt_to_use = ""

        if a == "2":
            prompt_to_use = prompt_2
        elif a == "1":
            prompt_to_use = prompt_3
        else: # Handles '0' and unexpected outputs
            prompt_to_use = prompt_4
        
        # --- Step 3: Grammar/Spelling Correction ---
        response_1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_to_use}]
        )
        corrected_text = response_1.choices[0].message.content.strip()

        # --- Step 4: Emoji Correction (Final Output) ---
        response_2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"correct the emoji in the given sentence:\n\n{corrected_text}"}]
        )
        
        return response_2.choices[0].message.content.strip()

    except Exception as e:
        # Return an error message if the API call fails
        # Added explicit error logging to console for user
        st.error(f"Error during API call: {e}. Check your API key and network connection.")
        return f"An error occurred during correction: {e}"


# --- Page Navigation Logic ---

if "page" not in st.session_state:
    st.session_state.page = "home"
if "corrected_text" not in st.session_state:
    st.session_state.corrected_text = None
if "last_input" not in st.session_state:
    st.session_state.last_input = None

def go_to_spell_corrector():
    st.session_state.page = "spell"

# --- Home Page ---
if st.session_state.page == "home":

    col1, col2, col3 = st.columns([1.45, 2, 1])
    with col2:
        st.button("Go to Spell Corrector", on_click=go_to_spell_corrector)

# --- Spell Corrector Page ---
elif st.session_state.page == "spell":
    # Reset background style for the spell page
    st.markdown(
        """
        <style>
        /* This overrides the page background to a lighter color */
        [data-testid="stAppViewContainer"] {
            background-color: #D3D2D1 !important;
            background-image: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<h1 style='color:#002E4B;text-align:center;'>SPELL CORRECTOR</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#F08729;text-align:center;'>Where Tamizh meets Perfection!</h3>", unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1.45,2,1])  
    with col2:
        if st.button("⬅ Back to Home"):
            st.session_state.page = "home"
            # Clear previous results when returning home
            st.session_state.corrected_text = None
            st.session_state.last_input = None
            st.rerun()

    # Place the input field at the bottom
    user_text = st.text_input(
        "Type in your input...", 
        key="spell_input", 
        label_visibility="collapsed", 
        placeholder ="Type in your text...."
    )
    
    # Check if the user has entered new text
    if user_text and user_text != st.session_state.last_input:
        
        # 1. Update session state with the new input
        st.session_state.last_input = user_text
        
        # 2. Call the API function with a spinner (loading indicator)
        with st.spinner('Analyzing and correcting Tamil text...'):
            corrected_text = correct(user_text)
        
        # 3. Store the result in session state
        st.session_state.corrected_text = corrected_text
        
        # Rerun to display the result above the text box
        st.rerun()

    # Display the result if it exists in the session state
    if st.session_state.corrected_text is not None:
        # Displaying the input text
        st.markdown(
            f"""
            <div style="margin-bottom: 20px;">
                <p style='color:#002E4B; font-size: 18px; font-weight: bold;'>Your Input:</p>
                <div class="custom-result-box" style="background-color: #F0F2F6; color: #002E4B; border-left: 5px solid #002E4B;">{st.session_state.last_input}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Displaying the corrected text
        st.markdown(
            f"""
            <p style='color:#002E4B; font-size: 18px; font-weight: bold;'>Corrected Output:</p>
            <div class="custom-result-box">{st.session_state.corrected_text}</div>
            """, 
            unsafe_allow_html=True
        )
