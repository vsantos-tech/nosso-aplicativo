def carregar_estilo_fundo():
    bg_image_path = None
    for ext in ["fundo.png", "fundo.jpg", "fundo.jpeg"]:
        if os.path.exists(ext):
            bg_image_path = ext
            break

    if bg_image_path:
        with open(bg_image_path, "rb") as f:
            bin_str = base64.b64encode(f.read()).decode()
        bg_style = f'background-image: url("data:image/png;base64,{bin_str}");'
    else:
        bg_style = "background: linear-gradient(135deg, #FFD1DC 0%, #FFB07C 50%, #E65C83 100%);"

    css = f"""
        <style>
        /* Oculta o topo do Streamlit */
        [data-testid="stHeader"], header {{
            display: none !important;
            height: 0px !important;
        }}

        /* Garante que o fundo cubra a tela inteira de ponta a ponta sem sobras */
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            {bg_style}
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            min-height: 100vh !important;
            height: 100% !important;
        }}

        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }}

        [data-testid="stAppToolbar"], 
        [data-testid="stHeaderActionElements"],
        [data-testid="stStatusWidget"],
        [data-testid="stDecoration"],
        #MainMenu, footer {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 240, 243, 0.98) !important;
        }}
        
        h1, h2, h3, p, label, .stMarkdown {{
            color: #4A1228 !important;
            font-weight: 500;
        }}
        
        div[data-baseweb="tab-list"] {{
            gap: 2px !important;
            display: flex !important;
            justify-content: space-between !important;
            width: 100% !important;
        }}
        
        button[data-baseweb="tab"] {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            color: #4A1228 !important;
            font-weight: bold;
            border-radius: 8px 8px 0px 0px;
            padding: 6px 8px !important;
            font-size: 12px !important;
            flex-grow: 1 !important;
            text-align: center !important;
            min-width: 0 !important;
        }}
        
        button[aria-selected="true"] {{
            border-bottom-color: #E65C83 !important;
            color: #E65C83 !important;
            background-color: rgba(255, 255, 255, 0.98) !important;
        }}
        
        div.stAlert {{
            background: linear-gradient(90deg, #E65C83 0%, #FF8A65 100%);
            color: white !important;
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        div.stAlert h3, div.stAlert p {{
            color: white !important;
        }}
        
        .stButton>button {{
            background: linear-gradient(90deg, #E65C83 0%, #F07865 100%);
            color: white !important;
            border-radius: 10px;
            border: none;
            font-weight: bold;
            padding: 8px 16px;
        }}
        
        .stButton>button:hover {{
            background: linear-gradient(90deg, #D44B72 0%, #E06754 100%);
            color: white !important;
        }}
        
        .card-historico {{
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 4px solid #E65C83;
            font-size: 13px;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)
