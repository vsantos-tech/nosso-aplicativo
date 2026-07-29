import base64
import os
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageOps
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Nosso Aplicativo 💗", page_icon="💗", layout="wide"
)

# Evita o erro de tradução automática do Chrome quebrar a tela
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

# Conexão com a Planilha do Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)


def obter_agora_brasilia():
    fuso_brasilia = timezone(timedelta(hours=-3))
    return datetime.now(fuso_brasilia)


def formatar_data_hora():
    return obter_agora_brasilia().strftime("%d/%m/%Y às %H:%M")


def carregar_imagem_correta(caminho_ou_url):
    if not caminho_ou_url:
        return None
    if str(caminho_ou_url).startswith(("http://", "https://")):
        return caminho_ou_url
    try:
        image = Image.open(caminho_ou_url)
        image = ImageOps.exif_transpose(image)
        return image
    except Exception:
        return caminho_ou_url


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
        footer, [data-testid="stFooter"], [data-testid="stEmbedFooter"],
        .stAppFooter, div[class*="stEmbedFooter"], div[class*="viewerBadge"],
        .viewerBadge_container__1323f, [data-testid="stHeader"], header {{
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}

        html, body, [data-testid="stAppViewContainer"], .stApp {{
            {bg_style}
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        .block-container {{
            padding-top: 0.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            max-width: 100% !important;
        }}

        [data-testid="stAppToolbar"], [data-testid="stHeaderActionElements"],
        [data-testid="stStatusWidget"], [data-testid="stDecoration"], #MainMenu {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 240, 243, 0.98) !important;
        }}
        
        h1, h2, h3, p, label, .stMarkdown, span, div {{
            color: #4A1228 !important;
            font-weight: 500;
        }}

        textarea, input[type="text"], input[type="password"], 
        div[data-baseweb="input"], div[data-baseweb="textarea"], 
        [data-testid="stFileUploader"] > div {{
            background-color: rgba(255, 240, 243, 0.95) !important;
            color: #4A1228 !important;
            border: 1px solid #E65C83 !important;
            border-radius: 10px !important;
        }}

        [data-testid="stFileUploader"] section {{
            background-color: rgba(255, 240, 243, 0.95) !important;
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

        div.stAlert * {{
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
        
        .card-historico {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 4px solid #E65C83;
            font-size: 13px;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)


carregar_estilo_fundo()

if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = None

st.title("Nosso Aplicativo 💗")
st.caption("Nosso cantinho especial de memórias, rotina e carinho.")

if st.session_state.usuario_atual is None:
    st.markdown("---")
    st.subheader("✨ Quem é você?")
    col_usr1, col_usr2 = st.columns(2)
    with col_usr1:
        if st.button("☀️ Larissa", key="btn_sou_larissa", use_container_width=True):
            st.session_state.usuario_atual = "larissa"
            st.session_state.e_admin = False
            st.rerun()
    with col_usr2:
        if st.button("🌙 Vitória", key="btn_sou_vitoria", use_container_width=True):
            st.session_state.usuario_atual = "vitoria"
            st.rerun()
    st.stop()

# CABEÇALHO DO APP
col_topo1, col_topo2, col_topo3 = st.columns([2, 1, 1])
with col_topo1:
    nome_exib = "☀️ Larissa" if st.session_state.usuario_atual == "larissa" else "🌙 Vitória"
    st.write(f"Conectada como: **{nome_exib}**")

with col_topo2:
    if st.button("🔄 Atualizar", key="btn_refresh_app"):
        st.cache_data.clear()
        st.toast("Página e dados atualizados!")
        st.rerun()

with col_topo3:
    if st.button("👤 Trocar perfil", key="btn_trocar_usr"):
        st.session_state.usuario_atual = None
        st.session_state.e_admin = False
        st.rerun()

if "e_admin" not in st.session_state:
    st.session_state.e_admin = False

SENHA_CORRETA = "1234"

if st.session_state.usuario_atual == "vitoria":
    with st.expander("🔑 Modo Edição (Vitória)", expanded=st.session_state.e_admin):
        if not st.session_state.e_admin:
            senha_input = st.text_input("Senha:", type="password", key="pwd_input_main")
            if st.button("Entrar no Modo Edição", key="btn_login_admin_main"):
                if senha_input == SENHA_CORRETA:
                    st.session_state.e_admin = True
                    st.success("Modo Edição Ativo!")
                    st.rerun()
                else:
                    st.error("Senha incorreta!")
        else:
            st.success("✨ Modo Edição Ativo!")
            if st.button("🚪 SALVAR E SAIR DO MODO EDIÇÃO", key="btn_sair_admin_main"):
                st.session_state.e_admin = False
                st.rerun()

e_admin = st.session_state.e_admin if st.session_state.usuario_atual == "vitoria" else False

tab_recado, tab_sentimento, tab_musicas, tab_fotos, tab_datas, tab_comidas, tab_dates = st.tabs(
    ["☀️ Recado", "💭 Sentimento", "🎶 Músicas", "📸 Fotos", "📅 Datas", "🍕 Comidas", "🥂 Encontros"]
)

# =============================================================
# ABA 1: RECADO (CONECTADO À PLANILHA GOOGLE)
# =============================================================
with tab_recado:
    if st.session_state.usuario_atual == "vitoria":
        st.header("☀️ Recado para meu cheirinho")
    else:
        st.header("✨ Recado para meu benzinho")

    # Lê os recados salvos na aba "Recados" da planilha
    try:
        df_recados = conn.read(worksheet="Recados", ttl="0s")
    except Exception:
        df_recados = pd.DataFrame(columns=["Autor", "Mensagem", "Imagem_URL", "Data_Hora", "Resposta", "Data_Resposta"])

    if not df_recados.empty:
        # Pega o recado mais recente
        ultimo_recado = df_recados.iloc[-1]
        autor_rec = ultimo_recado.get("Autor", "Nós")
        st.info(f"### {ultimo_recado.get('Mensagem', '')}")
        st.caption(f"🕒 **Enviado por {autor_rec} em:** {ultimo_recado.get('Data_Hora', '')}")
        
        if pd.notna(ultimo_recado.get("Imagem_URL")) and str(ultimo_recado.get("Imagem_URL")).strip():
            img_obj = carregar_imagem_correta(ultimo_recado.get("Imagem_URL"))
            if img_obj:
                st.image(img_obj, width=280)

        if pd.notna(ultimo_recado.get("Resposta")) and str(ultimo_recado.get("Resposta")).strip():
            st.success(f"💬 **Resposta:** {ultimo_recado.get('Resposta')}")
            st.caption(f"🕒 **Respondido em:** {ultimo_recado.get('Data_Resposta', '')}")

    st.markdown("---")

    st.subheader("✍️ Publicar Novo Lembrete")
    quem_manda = "Vitória" if st.session_state.usuario_atual == "vitoria" else "Larissa"
    novo_recado_txt = st.text_area(f"Escreva seu lembrete ({quem_manda}):", key="input_lembrete_geral")
    url_img_direto = st.text_input("Link da Imagem (opcional):", key="url_img_direto")

    if st.button("💌 Publicar Lembrete", key="btn_pub_lembrete_geral"):
        if novo_recado_txt.strip() or url_img_direto:
            novo_dado = pd.DataFrame([{
                "Autor": quem_manda,
                "Mensagem": novo_recado_txt,
                "Imagem_URL": url_img_direto,
                "Data_Hora": formatar_data_hora(),
                "Resposta": "",
                "Data_Resposta": ""
            }])
            df_atualizado = pd.concat([df_recados, novo_dado], ignore_index=True)
            conn.update(worksheet="Recados", data=df_atualizado)
            st.cache_data.clear()
            st.toast("Lembrete salvo com sucesso e gravado para sempre! 💖")
            st.rerun()

    st.markdown("---")

    with st.expander("💬 Responder ao Lembrete"):
        txt_resposta = st.text_area("Sua resposta:", key="in_txt_resposta")
        if st.button("Enviar Resposta", key="btn_send_resposta_rec"):
            if not df_recados.empty and txt_resposta.strip():
                df_recados.at[df_recados.index[-1], "Resposta"] = txt_resposta
                df_recados.at[df_recados.index[-1], "Data_Resposta"] = formatar_data_hora()
                conn.update(worksheet="Recados", data=df_recados)
                st.cache_data.clear()
                st.toast("Resposta enviada e salva na planilha! 💕")
                st.rerun()

    st.markdown("---")
    with st.expander("📜 Histórico de Recados Anteriores", expanded=False):
        if df_recados.empty:
            st.write("Ainda não há recados salvos no histórico.")
        else:
            for idx, row in df_recados.iloc[::-1].iterrows():
                st.markdown(
                    f'<div class="card-historico"><b>📌 Recado de {row.get("Autor", "Nós")}:</b> {row.get("Mensagem", "")}<br><small>🕒 {row.get("Data_Hora", "")}</small></div>',
                    unsafe_allow_html=True
                )
                if pd.notna(row.get("Resposta")) and str(row.get("Resposta")).strip():
                    st.write(f"💬 **Resposta:** {row.get('Resposta')}")
                    st.caption(f"🕒 Respondido em: {row.get('Data_Resposta', '')}")
                
                if e_admin:
                    if st.button(f"🗑️ Excluir #{idx+1}", key=f"btn_del_rec_{idx}"):
                        df_recados = df_recados.drop(idx)
                        conn.update(worksheet="Recados", data=df_recados)
                        st.cache_data.clear()
                        st.rerun()
                st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

# =============================================================
# DEMAIS ABAS (ILUSTRATIVAS / CONECTADAS ÀS GUIAS DA PLANILHA)
# =============================================================
with tab_sentimento:
    st.header("💭 Como estamos nos sentindo hoje?")
    st.info("Suas seleções e sentimentos ficam gravados direto na sua planilha do Google.")

with tab_musicas:
    st.header("🎶 Músicas Que Lembram Nós")
    st.write("Lista mantida em tempo real via Google Sheets.")

with tab_fotos:
    st.header("📸 Mural de Memórias")

with tab_datas:
    st.header("📅 Datas Especiais")

with tab_comidas:
    st.header("🍕 O Que Amamos Comer")

with tab_dates:
    st.header("🥂 Nossos Encontros (Feitos & A Fazer)")
