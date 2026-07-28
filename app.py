import base64
import json
import os
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageOps
import streamlit as st
from github import Github

st.set_page_config(
    page_title="Nosso Aplicativo 💗", page_icon="💗", layout="wide"
)

# Evita erro de tradução automática
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)


def obter_agora_brasilia():
    fuso_brasilia = timezone(timedelta(hours=-3))
    return datetime.now(fuso_brasilia)


def formatar_data_hora():
    return obter_agora_brasilia().strftime("%d/%m/%Y às %H:%M")


def formatar_apenas_data():
    return obter_agora_brasilia().strftime("%d/%m/%Y")


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

FILE_SENTIMENTOS = "sentimentos.json"
FILE_OPCOES_SENTIMENTOS = "opcoes_sentimentos.json"
FILE_RECADO = "recado.json"
FILE_MUSICAS = "musicas.json"
FILE_FOTOS = "fotos.json"
FILE_DATAS = "datas.json"
FILE_COMIDAS = "comidas.json"
FILE_DATES = "dates.json"


def carregar_json(filepath, default_data):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_data
    return default_data


def salvar_json(filepath, data):
    # 1. Salva localmente
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 2. Tenta fazer commit no GitHub
    if "GITHUB_TOKEN" not in st.secrets or "GITHUB_REPO" not in st.secrets:
        st.error("⚠️ Atenção: GITHUB_TOKEN ou GITHUB_REPO não estão configurados nos Secrets do Streamlit Cloud!")
        return

    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(st.secrets["GITHUB_REPO"])
        content = json.dumps(data, ensure_ascii=False, indent=4)
        try:
            contents = repo.get_contents(filepath)
            repo.update_file(contents.path, f"Atualizando {filepath}", content, contents.sha)
        except Exception:
            repo.create_file(filepath, f"Criando {filepath}", content)
    except Exception as e:
        st.error(f"Erro ao salvar no GitHub: {e}")


DEFAULT_SENTIMENTOS = {"larissa": [], "vitoria": [], "historico": []}
DEFAULT_OPCOES_SENTIMENTOS = {
    "larissa": ["Contente 😊", "Triste 😢", "Desanimada 🫠", "Empolgada ✨", "Ansiosa 😰", "Cansada 🥱"],
    "vitoria": ["Contente 😊", "Triste 😢", "Desanimada 🫠", "Irritada 😤", "Ansiosa 😰", "Cansada 🥱"]
}
DEFAULT_RECADO = {
    "hoje": "",
    "data_hora_hoje": "",
    "imagem_hoje": "",
    "resposta_larissa": "",
    "data_hora_resposta": "",
    "imagem_resposta_larissa": "",
    "historico": []
}
DEFAULT_MUSICAS = []
DEFAULT_FOTOS = []
DEFAULT_DATAS = []
DEFAULT_COMIDAS = {"receitas": [], "restaurantes": [], "historico_sugestoes": []}
DEFAULT_DATES = {"casa": [], "rua": [], "historico_sugestoes": []}

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
        st.toast("Página atualizada!")
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
# ABA 1: RECADO
# =============================================================
with tab_recado:
    if st.session_state.usuario_atual == "vitoria":
        st.header("☀️ Recado para meu cheirinho")
    else:
        st.header("✨ Recado para meu benzinho")

    recados = carregar_json(FILE_RECADO, DEFAULT_RECADO)

    hoje_br = formatar_apenas_data()
    data_recado = recados.get("data_dia", "")

    if data_recado and data_recado != hoje_br and recados.get("hoje"):
        if "historico" not in recados:
            recados["historico"] = []
        recados["historico"].insert(
            0,
            {
                "recado": recados.get("hoje", ""),
                "data_hora_hoje": recados.get("data_hora_hoje", ""),
                "imagem_hoje": recados.get("imagem_hoje", ""),
                "resposta_larissa": recados.get("resposta_larissa", ""),
                "imagem_resposta_larissa": recados.get("imagem_resposta_larissa", ""),
                "data_hora_resposta": recados.get("data_hora_resposta", ""),
            },
        )
        recados["hoje"] = ""
        recados["imagem_hoje"] = ""
        recados["resposta_larissa"] = ""
        recados["imagem_resposta_larissa"] = ""
        recados["data_hora_resposta"] = ""
        recados["data_hora_hoje"] = ""
        recados["data_dia"] = hoje_br
        salvar_json(FILE_RECADO, recados)

    if recados.get("hoje"):
        st.info(f"### {recados.get('hoje', '')}")
        st.caption(f"🕒 **Publicado em:** {recados.get('data_hora_hoje', '')}")
        if recados.get("imagem_hoje"):
            img_obj = carregar_imagem_correta(recados.get("imagem_hoje"))
            if img_obj:
                st.image(img_obj, width=280)

    if recados.get("resposta_larissa"):
        st.success(f"💬 **Resposta:** {recados.get('resposta_larissa')}")
        st.caption(f"🕒 **Respondido em:** {recados.get('data_hora_resposta', '')}")
        if recados.get("imagem_resposta_larissa"):
            img_r_obj = carregar_imagem_correta(recados.get("imagem_resposta_larissa"))
            if img_r_obj:
                st.image(img_r_obj, width=220)

    st.markdown("---")

    st.subheader("✍️ Publicar Novo Lembrete")
    novo_recado_txt = st.text_area("Escreva seu lembrete:", value=recados.get("hoje", ""), key="input_lembrete_geral")
    
    tab_img1, tab_img2 = st.tabs(["📁 Anexar do Dispositivo", "🔗 Link da Imagem"])
    up_img_direto, url_img_direto = None, ""
    with tab_img1:
        up_img_direto = st.file_uploader("Escolha uma imagem:", type=["png", "jpg", "jpeg", "webp"], key="up_img_direto")
    with tab_img2:
        url_img_direto = st.text_input("Cole a URL da imagem:", key="url_img_direto")

    if st.button("💌 Publicar Lembrete", key="btn_pub_lembrete_geral"):
        if novo_recado_txt.strip() or up_img_direto or url_img_direto:
            if recados.get("hoje"):
                if "historico" not in recados:
                    recados["historico"] = []
                recados["historico"].insert(0, {
                    "recado": recados.get("hoje"),
                    "data_hora_hoje": recados.get("data_hora_hoje"),
                    "imagem_hoje": recados.get("imagem_hoje"),
                    "resposta_larissa": recados.get("resposta_larissa"),
                    "data_hora_resposta": recados.get("data_hora_resposta"),
                    "imagem_resposta_larissa": recados.get("imagem_resposta_larissa")
                })

            recados["hoje"] = novo_recado_txt
            recados["data_hora_hoje"] = formatar_data_hora()

            if up_img_direto is not None:
                file_path = os.path.join(UPLOADS_DIR, "recado_" + up_img_direto.name)
                with open(file_path, "wb") as f:
                    f.write(up_img_direto.getbuffer())
                recados["imagem_hoje"] = file_path
            elif url_img_direto:
                recados["imagem_hoje"] = url_img_direto
            else:
                recados["imagem_hoje"] = ""

            recados["resposta_larissa"] = ""
            recados["data_hora_resposta"] = ""
            recados["imagem_resposta_larissa"] = ""

            salvar_json(FILE_RECADO, recados)
            st.toast("Lembrete publicado! 💖")
            st.rerun()

    st.markdown("---")

    with st.expander("💬 Responder Recado Publicado"):
        txt_resposta = st.text_area("Sua resposta:", value=recados.get("resposta_larissa", ""), key="in_txt_resposta")
        if st.button("Enviar Resposta", key="btn_send_resposta_rec"):
            recados["resposta_larissa"] = txt_resposta
            recados["data_hora_resposta"] = formatar_data_hora()
            salvar_json(FILE_RECADO, recados)
            st.toast("Resposta enviada com sucesso! 💕")
            st.rerun()

    st.markdown("---")
    with st.expander("📜 Histórico de Recados Anteriores", expanded=False):
        historico = recados.get("historico", [])
        if not historico:
            st.write("Ainda não há recados salvos no histórico.")
        else:
            for idx_h, item_h in enumerate(historico):
                st.markdown(
                    f'<div class="card-historico"><b>📌 Recado:</b> {item_h.get("recado", "")}<br><small>🕒 {item_h.get("data_hora_hoje", "")}</small></div>',
                    unsafe_allow_html=True
                )
                if item_h.get("resposta_larissa"):
                    st.write(f"💬 **Resposta:** {item_h.get('resposta_larissa')}")
                    st.caption(f"🕒 Respondido em: {item_h.get('data_hora_resposta', '')}")
                if e_admin:
                    if st.button(f"🗑️ Excluir #{idx_h+1}", key=f"btn_del_h_{idx_h}"):
                        recados["historico"].pop(idx_h)
                        salvar_json(FILE_RECADO, recados)
                        st.rerun()
                st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

# =============================================================
# ABA 2: SENTIMENTO
# =============================================================
with tab_sentimento:
    st.header("💭 Como estamos nos sentindo hoje?")
    sentimentos_salvos = carregar_json(FILE_SENTIMENTOS, DEFAULT_SENTIMENTOS)
    opcoes_sentimentos = carregar_json(FILE_OPCOES_SENTIMENTOS, DEFAULT_OPCOES_SENTIMENTOS)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        s_larissa = ", ".join(sentimentos_salvos.get("larissa", [])) or "Não selecionado"
        st.info(f"**Larissa está:**\n\n### {s_larissa}")
    with col_d2:
        s_vitoria = ", ".join(sentimentos_salvos.get("vitoria", [])) or "Não selecionado"
        st.info(f"**Vitória está:**\n\n### {s_vitoria}")

    st.markdown("---")
    st.subheader("Marque como você está se sentindo agora:")
    data_agora = formatar_data_hora()

    if st.session_state.usuario_atual == "larissa":
        novo_larissa = []
        for rotulo in opcoes_sentimentos.get("larissa", []):
            if st.checkbox(rotulo, value=(rotulo in sentimentos_salvos.get("larissa", [])), key=f"chk_l_{rotulo}"):
                novo_larissa.append(rotulo)
        if st.button("💾 Salvar Meu Sentimento", key="btn_salv_sent_l"):
            sentimentos_salvos["larissa"] = novo_larissa
            salvar_json(FILE_SENTIMENTOS, sentimentos_salvos)
            st.toast("Sentimento atualizado!")
            st.rerun()
    else:
        novo_vitoria = []
        for rotulo in opcoes_sentimentos.get("vitoria", []):
            if st.checkbox(rotulo, value=(rotulo in sentimentos_salvos.get("vitoria", [])), key=f"chk_v_{rotulo}"):
                novo_vitoria.append(rotulo)
        if st.button("💾 Salvar Meu Sentimento", key="btn_salv_sent_v"):
            sentimentos_salvos["vitoria"] = novo_vitoria
            salvar_json(FILE_SENTIMENTOS, sentimentos_salvos)
            st.toast("Sentimento atualizado!")
            st.rerun()

# =============================================================
# ABA 3: MÚSICAS
# =============================================================
with tab_musicas:
    st.header("🎶 Músicas Que Lembram Nós")
    musicas = carregar_json(FILE_MUSICAS, DEFAULT_MUSICAS)

    for idx, m in enumerate(musicas):
        st.markdown(f'<div class="card-historico">🎵 <b>{m["nome"]}</b><br><a href="{m["link"]}" target="_blank">👉 Ouvir no Spotify</a><br><small>Por: {m.get("autor", "Nós")} em {m.get("data_hora", "")}</small></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("➕ Adicionar Nova Música")
    sugestao_musica = st.text_input("Música e Artista:", key="sugestao_m_input")
    link_sugestao = st.text_input("Link do Spotify (opcional):", key="sugestao_m_link")
    if st.button("💖 Enviar Música", key="btn_add_m"):
        if sugestao_musica:
            m_link = link_sugestao if link_sugestao else f"https://open.spotify.com/search/{sugestao_musica.replace(' ', '%20')}"
            musicas.append({"nome": sugestao_musica, "link": m_link, "data_hora": formatar_data_hora(), "autor": st.session_state.usuario_atual})
            salvar_json(FILE_MUSICAS, musicas)
            st.toast("Música adicionada!")
            st.rerun()

# =============================================================
# ABA 4: FOTOS
# =============================================================
with tab_fotos:
    st.header("📸 Mural de Memórias")
    fotos = carregar_json(FILE_FOTOS, DEFAULT_FOTOS)

    for foto in fotos:
        img_obj = carregar_imagem_correta(foto["url"])
        if img_obj:
            st.image(img_obj, caption=foto["legenda"], width=300)

    st.markdown("---")
    st.subheader("➕ Adicionar Nova Foto ao Mural")
    add_f_url = st.text_input("Link/URL da imagem:", key="add_f_url")
    add_f_leg = st.text_input("Legenda da foto:", key="add_f_leg")
    if st.button("➕ Adicionar Foto", key="btn_add_f"):
        if add_f_url:
            fotos.append({"url": add_f_url, "legenda": add_f_leg, "data_hora": formatar_data_hora()})
            salvar_json(FILE_FOTOS, fotos)
            st.toast("Nova foto adicionada!")
            st.rerun()

# =============================================================
# ABA 5: DATAS
# =============================================================
with tab_datas:
    st.header("📅 Datas Especiais")
    datas = carregar_json(FILE_DATAS, DEFAULT_DATAS)
    for d in datas:
        st.subheader(f"{d.get('icone', '🗓️')} {d['titulo']}")
        st.write(f"🗓️ **Data:** {d['data']}")
        st.caption(f"🕒 Adicionado em {d.get('data_hora_adicionado', '')}")

    st.markdown("---")
    st.subheader("➕ Adicionar Nova Data Especial")
    add_d_tit = st.text_input("Título do Evento:", key="add_d_tit")
    add_d_dt = st.text_input("Data (DD/MM/AAAA):", key="add_d_dt")
    if st.button("➕ Adicionar Data", key="btn_add_d"):
        if add_d_tit and add_d_dt:
            datas.append({"titulo": add_d_tit, "data": add_d_dt, "icone": "❤️", "data_hora_adicionado": formatar_data_hora(), "autor": st.session_state.usuario_atual})
            salvar_json(FILE_DATAS, datas)
            st.toast("Data adicionada!")
            st.rerun()

# =============================================================
# ABA 6: COMIDAS
# =============================================================
with tab_comidas:
    st.header("🍕 O Que Amamos Comer")
    comidas = carregar_json(FILE_COMIDAS, DEFAULT_COMIDAS)
    
    st.subheader("🍝 Receitas em Casa")
    for item in comidas.get("receitas", []):
        st.write(f"- {item}")
        
    st.subheader("🍣 Restaurantes / Entregas")
    for item in comidas.get("restaurantes", []):
        st.write(f"- {item}")

    st.markdown("---")
    st.subheader("➕ Adicionar Comida / Restaurante")
    sug_comida = st.text_input("Nome da Comida/Restaurante:", key="sug_c_in")
    cat_c = st.radio("Categoria:", ["Receita em Casa", "Restaurante"], horizontal=True, key="cat_c_in")
    if st.button("💌 Salvar Comida", key="btn_sug_c"):
        if sug_comida:
            if "Casa" in cat_c:
                comidas["receitas"].append(sug_comida)
            else:
                comidas["restaurantes"].append(sug_comida)
            salvar_json(FILE_COMIDAS, comidas)
            st.toast("Comida salva!")
            st.rerun()

# =============================================================
# ABA 7: ENCONTROS / DATES
# =============================================================
with tab_dates:
    st.header("🥂 Nossos Encontros (Feitos & A Fazer)")
    dates = carregar_json(FILE_DATES, DEFAULT_DATES)
    
    col_c, col_r = st.columns(2)
    with col_c:
        st.subheader("🏠 Em Casa")
        for item in dates.get("casa", []):
            st.checkbox(item, key=f"c_{item}")
    with col_r:
        st.subheader("🌳 Fora de Casa")
        for item in dates.get("rua", []):
            st.checkbox(item, key=f"r_{item}")

    st.markdown("---")
    st.subheader("➕ Adicionar Ideia de Encontro")
    sug_date = st.text_input("Ideia de Date:", key="sug_d_in")
    cat_d = st.radio("Tipo:", ["Em Casa", "Fora de Casa"], horizontal=True, key="cat_d_in")
    if st.button("💌 Salvar Ideia", key="btn_sug_d"):
        if sug_date:
            if "Casa" in cat_d:
                dates["casa"].append(sug_date)
            else:
                dates["rua"].append(sug_date)
            salvar_json(FILE_DATES, dates)
            st.toast("Ideia de Date salva!")
            st.rerun()

