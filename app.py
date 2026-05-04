import streamlit as st

st.set_page_config(page_title="Calculator Streamlit", page_icon="🔢", layout="centered")
st.title("Calculator")

# CUSTUMIZED CSS STYLE
st.markdown("""
<style>
    /* Style the dial (Input) */
    .stTextInput input {
        color: #FFFFFF !important;
        font-size: 2rem !important;
        text-align: right !important;
        background-color: #262730 !important;
        border: 2px solid #4B4B4B !important;
    }

    /* Style the buttons */
    div.stButton > button {
        border-radius: 10px !important;
        height: 3.5rem !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        transition: all 0.2s ease;
    }

    /* Style for numbers (Dark Gray) */
    div.stButton > button:not(:disabled) {
        background-color: #3D3D3D;
        color: white;
    }

    /* Style for operators (Orange) */
    button[key*="btn_＋"], button[key*="btn_−"], button[key*="btn_×"], 
    button[key*="btn_/"], button[key*="btn_←"] {
        background-color: #FF9F0A !important;
        color: white !important;
    }

    /* Style for the "=" button (Green) */
    button[key*="btn_="] {
        background-color: #28C76F !important;
        color: white !important;
        border: none !important;
    }

    /* Style for the "C" button (Red) */
    button[key*="btn_C"] {
        background-color: #EA5455 !important;
        color: white !important;
    }

    /* Style for Hover (hover over the button) */
    div.stButton > button:hover {
        border: 2px solid #FFFFFF !important;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)


if "dial" not in st.session_state:
    st.session_state.dial = "0"

if "history" not in st.session_state:
    st.session_state.history = []

if "just_calculated" not in st.session_state:
    st.session_state.just_calculated = False

OPERATORS = ["＋", "−", "×", "/"]

def press(value):
    if value == "=":
        try:
            expression = (
                st.session_state.dial
                .replace("×", "*")
                .replace("−", "-")
                .replace("＋", "+")
            )
            resultado = str(eval(expression))
            st.session_state.history.append(f"{st.session_state.dial} = {resultado}")
            st.session_state.dial = resultado
            st.session_state.just_calculated = True
        except:
            st.session_state.dial = "Error"
            st.session_state.just_calculated = True

    elif value == "C":
        st.session_state.dial = "0"
        st.session_state.just_calculated = False

    elif value == "←":
        if st.session_state.just_calculated:
            st.session_state.dial = "0"
        else:
            st.session_state.dial = st.session_state.dial[:-1]
            if st.session_state.dial == "" or st.session_state.dial == "-":
                st.session_state.dial = "0"
        st.session_state.just_calculated = False

    else:
        if st.session_state.just_calculated:
            if value in OPERATORS:
                st.session_state.dial += str(value)
            else:
                st.session_state.dial = str(value)
            st.session_state.just_calculated = False
        else:
            if st.session_state.dial == "0":
                if value in OPERATORS:
                    st.session_state.dial += str(value)
                else:
                    st.session_state.dial = str(value)
            else:
                st.session_state.dial += str(value)


buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "−"],
    ["C", "0", "←", "＋"],
    ["="]
]

tab_calc, tab_hist = st.tabs(["Calculator", "History"])

with tab_calc:
    st.markdown(f"""
<div style="
    background-color: #262730;
    border: 2px solid #4B4B4B;
    border-radius: 8px;
    padding: 10px 16px;
    text-align: right;
    font-size: 2rem;
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
">
    {st.session_state.dial}
</div>
""", unsafe_allow_html=True)

    for linha in buttons:
        cols = st.columns(len(linha))
        for i, char in enumerate(linha):
            cols[i].button(char, on_click=press, args=(char,),
                       use_container_width=True, key=f"btn_{char}")

with tab_hist:
    st.subheader("Last Operations")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            st.write(item)
        
        if st.button("Clean History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("History is empty.")