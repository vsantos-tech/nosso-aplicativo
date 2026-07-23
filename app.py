import base64
import json
import os
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageOps
import streamlit as st

st.set_page_config(
    page_title="Nosso Aplicativo 💗", page_icon="💗", layout="wide"
)

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
        bg_style = "background: transparent;"

    css = f"""
        <style>
        /* Remocao total de barras superiores, ropapes e marcas d'agua */
        [data-testid="stHeader"], header, footer, [data-testid="stEmbedFooter"], .viewerBadge_container__1323f {{
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }}

        /* Fundo transparente e expansivel */
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            {bg_style}
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            background-color: transparent !important;
        }}

        .block-container {{
            padding-top: 0.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }}

        [data-testid="stAppToolbar"], 
        [data-testid="stHeaderActionElements"],
        [data-testid="stStatusWidget"],
        [data-testid="stDecoration"],
        #MainMenu {{
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
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


DEFAULT_SENTIMENTOS = {"larissa": [], "vitoria": [], "historico": []}
DEFAULT_OPCOES_SENTIMENTOS = {
    "larissa": [
        "Contente 😊",
        "Triste 😢",
        "Desanimada 🫠",
        "Estressada 🤯",
        "Com enxaqueca 🤕",
        "Empolgada ✨",
        "Ansiosa 😰",
        "Cansada 🥱",
    ],
    "vitoria": [
        "Contente 😊",
        "Triste 😢",
        "Desanimada 🫠",
        "Irritada 😤",
        "Não verbal 🔕",
        "Ansiosa 😰",
        "Empolgada ✨",
        "Cansada 🥱",
    ],
}
DEFAULT_RECADO = {
    "hoje": "tô morrendo de saudade de você! 💕",
    "data_hora_hoje": "22/07/2026 às 18:40",
    "data_dia": "22/07/2026",
    "imagem_hoje": "",
    "resposta_larissa": "Você é minha vida!!",
    "imagem_resposta_larissa": "",
    "data_hora_resposta": "22/07/2026 às 19:00",
    "historico": [],
}
DEFAULT_MUSICAS = [
    {
        "nome": "Nossa Música Favorita",
        "link": "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",
        "data_hora": formatar_data_hora(),
        "autor": "Vitória",
    }
]
DEFAULT_FOTOS = [
    {
        "url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=600",
        "legenda": "Nosso passeio favorito 🌿",
        "data_hora": formatar_data_hora(),
    }
]
DEFAULT_DATAS = [
    {
        "titulo": "Primeiro Encontro",
        "data": "12/05/2023",
        "icone": "🥂",
        "data_hora_adicionado": formatar_data_hora(),
        "autor": "Nós",
    }
]
DEFAULT_COMIDAS = {
    "receitas": ["🍝 Massa Especial de Quinta-feira"],
    "restaurantes": [
        "🍣 Japonês: Nosso lugar favorito",
        "🍕 Pizzaria: Cantina Especial",
    ],
    "historico_sugestoes": [],
}
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

col_topo1, col_topo2 = st.columns([2, 2])
with col_topo1:
    nome_exib = (
        "☀️ Larissa"
        if st.session_state.usuario_atual == "larissa"
        else "🌙 Vitória"
    )
    st.write(f"Conectada como: **{nome_exib}**")
with col_topo2:
    if st.button("🔄 Trocar perfil", key="btn_trocar_usr"):
        st.session_state.usuario_atual = None
        st.session_state.e_admin = False
        st.rerun()

if "e_admin" not in st.session_state:
    st.session_state.e_admin = False

SENHA_CORRETA = "1234"

if st.session_state.usuario_atual == "vitoria":
    with st.expander(
        "🔑 Acessar Modo Edição (Exclusivo Vitória)",
        expanded=st.session_state.e_admin,
    ):
        if not st.session_state.e_admin:
            senha_input = st.text_input(
                "Digite a senha para editar o app:",
                type="password",
                key="pwd_input_main",
            )
            if st.button("Entrar no Modo Edição", key="btn_login_admin_main"):
                if senha_input == SENHA_CORRETA:
                    st.session_state.e_admin = True
                    st.success("Modo Edição Ativo!")
                    st.rerun()
                else:
                    st.error("Senha incorreta!")
        else:
            st.success("✨ Você está no Modo Edição!")
            if st.button(
                "🚪 SALVAR E SAIR DO MODO EDIÇÃO", key="btn_sair_admin_main"
            ):
                st.session_state.e_admin = False
                st.success("Edições concluídas!")
                st.rerun()

e_admin = (
    st.session_state.e_admin
    if st.session_state.usuario_atual == "vitoria"
    else False
)

(
    tab_sentimento,
    tab_recado,
    tab_musicas,
    tab_fotos,
    tab_datas,
    tab_comidas,
    tab_dates,
) = st.tabs(
    [
        "💭 Sentimento",
        "☀️ Recado",
        "🎶 Músicas",
        "📸 Fotos",
        "📅 Datas",
        "🍕 Comidas",
        "🥂 Encontros",
    ]
)

# ABA SENTIMENTO
with tab_sentimento:
    st.header("💭 Como estamos nos sentindo hoje?")
    sentimentos_salvos = carregar_json(FILE_SENTIMENTOS, DEFAULT_SENTIMENTOS)
    opcoes_sentimentos = carregar_json(
        FILE_OPCOES_SENTIMENTOS, DEFAULT_OPCOES_SENTIMENTOS
    )
    opcoes_larissa = opcoes_sentimentos.get("larissa", [])
    opcoes_vitoria = opcoes_sentimentos.get("vitoria", [])

    st.markdown("### 🌟 Destaque do Dia:")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        s_larissa = (
            ", ".join(sentimentos_salvos.get("larissa", []))
            if sentimentos_salvos.get("larissa")
            else "Não selecionado"
        )
        st.info(f"**Larissa está:**\n\n### {s_larissa}")
    with col_d2:
        s_vitoria = (
            ", ".join(sentimentos_salvos.get("vitoria", []))
            if sentimentos_salvos.get("vitoria")
            else "Não selecionado"
        )
        st.info(f"**Vitória está:**\n\n### {s_vitoria}")

    st.markdown("---")
    st.subheader("Marque como você está se sentindo agora:")
    data_agora = formatar_data_hora()

    if st.session_state.usuario_atual == "larissa":
        novo_larissa = []
        st.write("🌸 **Sua Lista (Larissa):**")
        for rotulo in opcoes_larissa:
            marcado_padrao = rotulo in sentimentos_salvos.get("larissa", [])
            if st.checkbox(rotulo, value=marcado_padrao, key=f"chk_l_{rotulo}"):
                novo_larissa.append(rotulo)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Salvar Meu Sentimento De Hoje", key="btn_salv_sent_l"):
            sentimentos_salvos["larissa"] = novo_larissa
            if "historico" not in sentimentos_salvos:
                sentimentos_salvos["historico"] = []
            sentimentos_salvos["historico"].insert(
                0,
                {
                    "autor": "Larissa",
                    "sentimento": ", ".join(novo_larissa)
                    if novo_larissa
                    else "Nada marcado",
                    "data_hora": data_agora,
                },
            )
            salvar_json(FILE_SENTIMENTOS, sentimentos_salvos)
            st.success("Seu sentimento foi atualizado!")
            st.rerun()
    else:
        novo_vitoria = []
        st.write("🌿 **Sua Lista (Vitória):**")
        for rotulo in opcoes_vitoria:
            marcado_padrao = rotulo in sentimentos_salvos.get("vitoria", [])
            if st.checkbox(rotulo, value=marcado_padrao, key=f"chk_v_{rotulo}"):
                novo_vitoria.append(rotulo)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Salvar Meu Sentimento De Hoje", key="btn_salv_sent_v"):
            sentimentos_salvos["vitoria"] = novo_vitoria
            if "historico" not in sentimentos_salvos:
                sentimentos_salvos["historico"] = []
            sentimentos_salvos["historico"].insert(
                0,
                {
                    "autor": "Vitória",
                    "sentimento": ", ".join(novo_vitoria)
                    if novo_vitoria
                    else "Nada marcado",
                    "data_hora": data_agora,
                },
            )
            salvar_json(FILE_SENTIMENTOS, sentimentos_salvos)
            st.success("Seu sentimento foi atualizado!")
            st.rerun()

    st.markdown("---")
    with st.expander("📜 Histórico de Sentimentos Registrados", expanded=False):
        hist_sent = sentimentos_salvos.get("historico", [])
        if not hist_sent:
            st.write("Nenhum histórico gravado ainda.")
        else:
            for item in hist_sent:
                st.markdown(
                    f'<div class="card-historico"><b>{item.get("autor")}:</b> {item.get("sentimento")}<br><small>🕒 {item.get("data_hora")}</small></div>',
                    unsafe_allow_html=True,
                )

    if e_admin:
        st.markdown("---")
        st.subheader("✏️ Gerenciar Lista de Sentimentos (Modo Edição)")
        tab_s1, tab_s2 = st.tabs(["🌸 Opções da Larissa", "🌿 Opções da Vitória"])
        with tab_s1:
            for idx_s, item_s in enumerate(opcoes_larissa):
                col_s_txt, col_s_del = st.columns([3, 1])
                with col_s_txt:
                    st.write(f"- {item_s}")
                with col_s_del:
                    if st.button(f"🗑️ Excluir", key=f"btn_del_sl_{idx_s}"):
                        opcoes_sentimentos["larissa"].pop(idx_s)
                        salvar_json(
                            FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos
                        )
                        st.rerun()
            add_sent_l = st.text_input(
                "Novo sentimento para a Larissa:", key="in_add_sl"
            )
            if st.button("➕ Adicionar Sentimento (Larissa)", key="btn_add_sl"):
                if add_sent_l:
                    opcoes_sentimentos["larissa"].append(add_sent_l)
                    salvar_json(
                        FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos
                    )
                    st.rerun()
        with tab_s2:
            for idx_s, item_s in enumerate(opcoes_vitoria):
                col_s_txt, col_s_del = st.columns([3, 1])
                with col_s_txt:
                    st.write(f"- {item_s}")
                with col_s_del:
                    if st.button(f"🗑️ Excluir", key=f"btn_del_sv_{idx_s}"):
                        opcoes_sentimentos["vitoria"].pop(idx_s)
                        salvar_json(
                            FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos
                        )
                        st.rerun()
            add_sent_v = st.text_input(
                "Novo sentimento para a Vitória:", key="in_add_sv"
            )
            if st.button("➕ Adicionar Sentimento (Vitória)", key="btn_add_sv"):
                if add_sent_v:
                    opcoes_sentimentos["vitoria"].append(add_sent_v)
                    salvar_json(
                        FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos
                    )
                    st.rerun()

# ABA RECADO (COM EXCLUSÃO NO MODO EDIÇÃO)
with tab_recado:
    st.header("☀️ Lembrete pro meu cheirinho")
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
                "imagem_resposta_larissa": recados.get(
                    "imagem_resposta_larissa", ""
                ),
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
        img_hoje = recados.get("imagem_hoje", "")
        if img_hoje:
            img_obj = carregar_imagem_correta(img_hoje)
            if img_obj:
                st.image(img_obj, use_container_width=True)

        if e_admin:
            if st.button("🗑️ Excluir Recado do Dia", key="btn_del_recado_hoje"):
                recados["hoje"] = ""
                recados["imagem_hoje"] = ""
                recados["data_hora_hoje"] = ""
                recados["resposta_larissa"] = ""
                recados["imagem_resposta_larissa"] = ""
                recados["data_hora_resposta"] = ""
                salvar_json(FILE_RECADO, recados)
                st.success("Recado excluído!")
                st.rerun()
    else:
        st.info("### Nenhum lembrete publicado para hoje ainda!")

    resp_atual = recados.get("resposta_larissa", "")
    img_resp_atual = recados.get("imagem_resposta_larissa", "")
    dt_resp = recados.get("data_hora_resposta", "")

    if resp_atual or img_resp_atual:
        st.markdown("---")
        st.markdown("#### 👇 Resposta da Larissa:")
        if resp_atual:
            st.success(f"💬 **Larissa:** {resp_atual}")
        if dt_resp:
            st.caption(f"🕒 **Respondido em:** {dt_resp}")
        if img_resp_atual:
            img_resp_obj = carregar_imagem_correta(img_resp_atual)
            if img_resp_obj:
                st.image(img_resp_obj, width=250, caption="Foto da Larissa 🌸")

    if st.session_state.usuario_atual == "larissa":
        st.markdown("---")
        st.markdown("### 👇 Resposta da Larissa:")
        texto_resposta = st.text_area(
            "Escreva aqui sua resposta se quiser:",
            value=resp_atual,
            key="input_resp_larissa",
        )
        tab_r_up1, tab_r_up2 = st.tabs(
            ["📁 Enviar Arquivo", "🔗 Colar Link de Imagem"]
        )
        up_img_resp, url_img_resp = None, ""
        with tab_r_up1:
            up_img_resp = st.file_uploader(
                "Escolha da galeria:",
                type=["png", "jpg", "jpeg", "webp"],
                key="up_img_resp_larissa",
            )
        with tab_r_up2:
            url_img_resp = st.text_input(
                "Link da imagem (https://...):", key="url_img_resp_larissa"
            )

        if st.button("💌 Enviar Resposta", key="btn_env_resposta"):
            recados["resposta_larissa"] = texto_resposta
            recados["data_hora_resposta"] = formatar_data_hora()
            if up_img_resp is not None:
                file_path = os.path.join(
                    UPLOADS_DIR, "resp_larissa_" + up_img_resp.name
                )
                with open(file_path, "wb") as f:
                    f.write(up_img_resp.getbuffer())
                recados["imagem_resposta_larissa"] = file_path
            elif url_img_resp:
                recados["imagem_resposta_larissa"] = url_img_resp
            salvar_json(FILE_RECADO, recados)
            st.success("Sua resposta foi enviada! 💕")
            st.rerun()

    if st.session_state.usuario_atual == "vitoria":
        st.markdown("---")
        st.subheader("✍️ Publicar Novo Lembrete Do Dia")
        novo_recado_vit = st.text_area(
            "Escreva o novo lembrete:",
            value=recados.get("hoje", ""),
            key="input_lembrete_vit_direto",
        )
        tab_l_up1, tab_l_up2 = st.tabs(
            ["📁 Enviar Arquivo", "🔗 Colar Link de Imagem"]
        )
        up_img_vit_direto, url_img_vit_direto = None, ""
        with tab_l_up1:
            up_img_vit_direto = st.file_uploader(
                "Escolha da galeria/PC:",
                type=["png", "jpg", "jpeg", "webp"],
                key="up_img_vit_direto",
            )
        with tab_l_up2:
            url_img_vit_direto = st.text_input(
                "Link da imagem (https://...):", key="url_img_vit_direto"
            )

        if st.button("💌 Publicar Lembrete Hoje", key="btn_pub_lembrete_vit"):
            if recados.get("hoje"):
                historico_item = {
                    "recado": recados.get("hoje", ""),
                    "data_hora_hoje": recados.get("data_hora_hoje", ""),
                    "imagem_hoje": recados.get("imagem_hoje", ""),
                    "resposta_larissa": recados.get("resposta_larissa", ""),
                    "imagem_resposta_larissa": recados.get(
                        "imagem_resposta_larissa", ""
                    ),
                    "data_hora_resposta": recados.get("data_hora_resposta", ""),
                }
                if "historico" not in recados:
                    recados["historico"] = []
                recados["historico"].insert(0, historico_item)

            recados["hoje"] = novo_recado_vit
            recados["data_hora_hoje"] = formatar_data_hora()
            recados["data_dia"] = formatar_apenas_data()

            if up_img_vit_direto is not None:
                file_path = os.path.join(
                    UPLOADS_DIR, "recado_hoje_" + up_img_vit_direto.name
                )
                with open(file_path, "wb") as f:
                    f.write(up_img_vit_direto.getbuffer())
                recados["imagem_hoje"] = file_path
            elif url_img_vit_direto:
                recados["imagem_hoje"] = url_img_vit_direto
            else:
                recados["imagem_hoje"] = ""

            recados["resposta_larissa"] = ""
            recados["imagem_resposta_larissa"] = ""
            recados["data_hora_resposta"] = ""
            salvar_json(FILE_RECADO, recados)
            st.success("Lembrete publicado!")
            st.rerun()

    st.markdown("---")
    with st.expander("📜 Histórico de Recados Anteriores", expanded=False):
        historico = recados.get("historico", [])
        if not historico:
            st.write("Ainda não há recados guardados no histórico.")
        else:
            for idx_h, item_h in enumerate(historico):
                st.markdown(
                    f'<div class="card-historico"><b>📌 Recado:</b> {item_h.get("recado", "")}<br><small>🕒 {item_h.get("data_hora_hoje", "")}</small></div>',
                    unsafe_allow_html=True,
                )
                if item_h.get("imagem_hoje"):
                    img_h_obj = carregar_imagem_correta(
                        item_h.get("imagem_hoje")
                    )
                    if img_h_obj:
                        st.image(img_h_obj, width=200)

                if item_h.get("resposta_larissa"):
                    st.write(
                        f"💬 **Resposta Larissa:** {item_h.get('resposta_larissa')}"
                    )
                    st.caption(
                        f"🕒 Respondido em: {item_h.get('data_hora_resposta', '')}"
                    )
                if item_h.get("imagem_resposta_larissa"):
                    img_hr_obj = carregar_imagem_correta(
                        item_h.get("imagem_resposta_larissa")
                    )
                    if img_hr_obj:
                        st.image(img_hr_obj, width=180)

                if e_admin:
                    if st.button(
                        f"🗑️ Excluir Recado #{idx_h+1} do Histórico",
                        key=f"btn_del_hist_rec_{idx_h}",
                    ):
                        recados["historico"].pop(idx_h)
                        salvar_json(FILE_RECADO, recados)
                        st.success("Recado removido!")
                        st.rerun()

                st.markdown(
                    "<hr style='margin: 8px 0;'>", unsafe_allow_html=True
                )

# ABA MÚSICAS
with tab_musicas:
    st.header("🎶 Músicas Que Lembram Nós")
    musicas = carregar_json(FILE_MUSICAS, DEFAULT_MUSICAS)
    for idx, m in enumerate(musicas):
        st.subheader(f"🎵 {m['nome']}")
        st.write(f"👉 [Ouvir no Spotify]({m['link']})")
        if "data_hora" in m:
            st.caption(
                f"🕒 Adicionado por {m.get('autor', 'Nós')} em {m['data_hora']}"
            )
        if e_admin:
            novo_nome = st.text_input(
                f"Nome #{idx+1}:", value=m["nome"], key=f"m_nome_{idx}"
            )
            novo_link = st.text_input(
                f"Link #{idx+1}:", value=m["link"], key=f"m_link_{idx}"
            )
            c_salv, c_del = st.columns(2)
            with c_salv:
                if st.button(
                    f"💾 Alterar Música #{idx+1}", key=f"btn_m_up_{idx}"
                ):
                    musicas[idx]["nome"] = novo_nome
                    musicas[idx]["link"] = novo_link
                    salvar_json(FILE_MUSICAS, musicas)
                    st.rerun()
            with c_del:
                if st.button(
                    f"🗑️ Excluir Música #{idx+1}", key=f"btn_m_del_{idx}"
                ):
                    musicas.pop(idx)
                    salvar_json(FILE_MUSICAS, musicas)
                    st.rerun()
        st.markdown("---")

    sugestao_musica = st.text_input("Música e Artista:", key="sugestao_m_input")
    link_sugestao = st.text_input(
        "Link do Spotify (opcional):", key="sugestao_m_link"
    )
    if st.button("💖 Enviar Música para a Lista", key="btn_add_musica_geral"):
        if sugestao_musica:
            m_link = (
                link_sugestao
                if link_sugestao
                else "https://open.spotify.com/search/"
                + sugestao_musica.replace(" ", "%20")
            )
            quem_enviou = (
                "Larissa"
                if st.session_state.usuario_atual == "larissa"
                else "Vitória"
            )
            musicas.append(
                {
                    "nome": sugestao_musica,
                    "link": m_link,
                    "data_hora": formatar_data_hora(),
                    "autor": quem_enviou,
                }
            )
            salvar_json(FILE_MUSICAS, musicas)
            st.rerun()

# ABA FOTOS
with tab_fotos:
    st.header("📸 Mural de Memórias")
    fotos = carregar_json(FILE_FOTOS, DEFAULT_FOTOS)
    col1, col2 = st.columns(2)
    for idx, foto in enumerate(fotos):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            img_obj = carregar_imagem_correta(foto["url"])
            if img_obj:
                st.image(
                    img_obj, caption=foto["legenda"], use_container_width=True
                )
            if e_admin:
                nova_legenda = st.text_input(
                    f"Legenda #{idx+1}:",
                    value=foto["legenda"],
                    key=f"f_leg_{idx}",
                )
                nova_url = st.text_input(
                    f"URL/Caminho #{idx+1}:",
                    value=foto["url"],
                    key=f"f_url_{idx}",
                )
                c_salv, c_exc = st.columns(2)
                with c_salv:
                    if st.button(
                        f"💾 Alterar #{idx+1}", key=f"btn_f_up_{idx}"
                    ):
                        fotos[idx] = {
                            "url": nova_url,
                            "legenda": nova_legenda,
                            "data_hora": foto.get("data_hora", ""),
                        }
                        salvar_json(FILE_FOTOS, fotos)
                        st.rerun()
                with c_exc:
                    if st.button(
                        f"🗑️ Excluir #{idx+1}", key=f"btn_f_del_{idx}"
                    ):
                        fotos.pop(idx)
                        salvar_json(FILE_FOTOS, fotos)
                        st.rerun()

    if e_admin:
        st.markdown("---")
        tab_up1, tab_up2 = st.tabs(["📁 Enviar do PC/Galeria", "🔗 Link da Web"])
        data_agora = formatar_data_hora()
        with tab_up1:
            uploaded_file = st.file_uploader(
                "Escolha a foto:",
                type=["png", "jpg", "jpeg", "webp"],
                key="upload_foto_file",
            )
            legenda_upload = st.text_input("Legenda:", key="legenda_upload_file")
            if st.button("📤 Upload Foto", key="btn_upload_foto_save"):
                if uploaded_file is not None:
                    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    fotos.append(
                        {
                            "url": file_path,
                            "legenda": legenda_upload,
                            "data_hora": data_agora,
                        }
                    )
                    salvar_json(FILE_FOTOS, fotos)
                    st.rerun()
        with tab_up2:
            add_f_url = st.text_input("Link/URL:", key="add_f_url")
            add_f_leg = st.text_input("Legenda:", key="add_f_leg")
            if st.button("➕ Adicionar Foto via Link", key="btn_add_foto_url"):
                if add_f_url:
                    fotos.append(
                        {
                            "url": add_f_url,
                            "legenda": add_f_leg,
                            "data_hora": data_agora,
                        }
                    )
                    salvar_json(FILE_FOTOS, fotos)
                    st.rerun()

# ABA DATAS
with tab_datas:
    st.header("📅 Datas Especiais")
    datas = carregar_json(FILE_DATAS, DEFAULT_DATAS)
    for idx, d in enumerate(datas):
        st.subheader(f"{d.get('icone', '🗓️')} {d['titulo']}")
        st.write(f"🗓️ **Data:** {d['data']}")
        if "data_hora_adicionado" in d:
            st.caption(
                f"🕒 Adicionado por {d.get('autor', 'Nós')} em {d['data_hora_adicionado']}"
            )
        if e_admin:
            n_ic = st.text_input(
                f"Ícone #{idx+1}:",
                value=d.get("icone", "🗓️"),
                key=f"d_ic_{idx}",
            )
            n_tit = st.text_input(
                f"Título #{idx+1}:", value=d["titulo"], key=f"d_tit_{idx}"
            )
            n_dt = st.text_input(
                f"Data #{idx+1}:", value=d["data"], key=f"d_dt_{idx}"
            )
            c_s, c_x = st.columns(2)
            with c_s:
                if st.button(
                    f"💾 Alterar #{idx+1}", key=f"btn_d_up_{idx}"
                ):
                    (
                        datas[idx]["titulo"],
                        datas[idx]["data"],
                        datas[idx]["icone"],
                    ) = (n_tit, n_dt, n_ic)
                    salvar_json(FILE_DATAS, datas)
                    st.rerun()
            with c_x:
                if st.button(
                    f"🗑️ Excluir #{idx+1}", key=f"btn_d_del_{idx}"
                ):
                    datas.pop(idx)
                    salvar_json(FILE_DATAS, datas)
                    st.rerun()
        st.markdown("---")

    add_d_ic = st.text_input("Emoji/Ícone:", value="❤️", key="add_d_ic_geral")
    add_d_tit = st.text_input("Título do Evento:", key="add_d_tit_geral")
    add_d_dt = st.text_input("Data:", key="add_d_dt_geral")
    if st.button("➕ Adicionar Data", key="btn_add_data_geral"):
        if add_d_tit and add_d_dt:
            quem_enviou = (
                "Larissa"
                if st.session_state.usuario_atual == "larissa"
                else "Vitória"
            )
            datas.append(
                {
                    "titulo": add_d_tit,
                    "data": add_d_dt,
                    "icone": add_d_ic,
                    "data_hora_adicionado": formatar_data_hora(),
                    "autor": quem_enviou,
                }
            )
            salvar_json(FILE_DATAS, datas)
            st.rerun()

# ABA COMIDAS
with tab_comidas:
    st.header("🍕 O Que Amamos Comer")
    comidas = carregar_json(FILE_COMIDAS, DEFAULT_COMIDAS)
    subtab1, subtab2 = st.tabs(["Receitas em Casa", "Restaurantes / Entregas"])
    with subtab1:
        for idx, item in enumerate(comidas.get("receitas", [])):
            st.write(f"- {item}")
            if e_admin:
                novo_item = st.text_input(
                    f"Editar #{idx+1}:", value=item, key=f"c_rec_{idx}"
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(
                        f"💾 Alterar #{idx+1}", key=f"btn_rec_up_{idx}"
                    ):
                        comidas["receitas"][idx] = novo_item
                        salvar_json(FILE_COMIDAS, comidas)
                        st.rerun()
                with c2:
                    if st.button(
                        f"🗑️ Excluir #{idx+1}", key=f"btn_rec_del_{idx}"
                    ):
                        comidas["receitas"].pop(idx)
                        salvar_json(FILE_COMIDAS, comidas)
                        st.rerun()
    with subtab2:
        for idx, item in enumerate(comidas.get("restaurantes", [])):
            st.write(f"- {item}")
            if e_admin:
                novo_item = st.text_input(
                    f"Editar #{idx+1}:", value=item, key=f"c_rest_{idx}"
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(
                        f"💾 Alterar #{idx+1}", key=f"btn_cr_up_{idx}"
                    ):
                        comidas["restaurantes"][idx] = novo_item
                        salvar_json(FILE_COMIDAS, comidas)
                        st.rerun()
                with c2:
                    if st.button(
                        f"🗑️ Excluir #{idx+1}", key=f"btn_cr_del_{idx}"
                    ):
                        comidas["restaurantes"].pop(idx)
                        salvar_json(FILE_COMIDAS, comidas)
                        st.rerun()

    sugestao_comida = st.text_input(
        "Sua Sugestão de Comida:", key="sugestao_comida_input"
    )
    tipo_comida_sug = st.radio(
        "Categoria:",
        ["🍝 Receita em Casa", "🍣 Restaurante / Delivery"],
        horizontal=True,
        key="sug_c_tipo",
    )
    if st.button("💌 Enviar Sugestão de Comida", key="btn_sug_comida_send"):
        if sugestao_comida:
            quem_enviou = (
                "Larissa"
                if st.session_state.usuario_atual == "larissa"
                else "Vitória"
            )
            texto_item = f"{sugestao_comida} (Sugerido por {quem_enviou} em {formatar_data_hora()})"
            if "Receita" in tipo_comida_sug:
                comidas["receitas"].append(texto_item)
            else:
                comidas["restaurantes"].append(texto_item)
            salvar_json(FILE_COMIDAS, comidas)
            st.rerun()

# ABA ENCONTROS
with tab_dates:
    st.header("🥂 Nossos Encontros (Feitos & A Fazer)")
    dates = carregar_json(FILE_DATES, DEFAULT_DATES)
    col_casa, col_rua = st.columns(2)
    with col_casa:
        st.subheader("🏠 Em Casa")
        for idx, item in enumerate(dates.get("casa", [])):
            st.checkbox(item, key=f"casa_{idx}_{item}")
            if e_admin:
                novo_date_c = st.text_input(
                    f"Editar #{idx+1}:", value=item, key=f"d_c_in_{idx}"
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(
                        f"💾 Alterar #{idx+1}", key=f"btn_dc_up_{idx}"
                    ):
                        dates["casa"][idx] = novo_date_c
                        salvar_json(FILE_DATES, dates)
                        st.rerun()
                with c2:
                    if st.button(
                        f"🗑️ Excluir #{idx+1}", key=f"btn_dc_del_{idx}"
                    ):
                        dates["casa"].pop(idx)
                        salvar_json(FILE_DATES, dates)
                        st.rerun()
    with col_rua:
        st.subheader("🌳 Fora de Casa")
        for idx, item in enumerate(dates.get("rua", [])):
            st.checkbox(item, key=f"rua_{idx}_{item}")
            if e_admin:
                novo_date_r = st.text_input(
                    f"Editar #{idx+1}:", value=item, key=f"d_r_in_{idx}"
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(
                        f"💾 Alterar #{idx+1}", key=f"btn_dr_up_{idx}"
                    ):
                        dates["rua"][idx] = novo_date_r
                        salvar_json(FILE_DATES, dates)
                        st.rerun()
                with c2:
                    if st.button(
                        f"🗑️ Excluir #{idx+1}", key=f"btn_dr_del_{idx}"
                    ):
                        dates["rua"].pop(idx)
                        salvar_json(FILE_DATES, dates)
                        st.rerun()

    sugestao_date = st.text_input("Ideia de Date:", key="sugestao_date_input")
    tipo_date_sug = st.radio(
        "Tipo de Encontro:",
        ["🏠 Em Casa", "🌳 Fora de Casa"],
        horizontal=True,
        key="sug_d_tipo",
    )
    if st.button("💌 Enviar Sugestão de Date", key="btn_sug_date_send"):
        if sugestao_date:
            quem_enviou = (
                "Larissa"
                if st.session_state.usuario_atual == "larissa"
                else "Vitória"
            )
            texto_formatado = f"{sugestao_date} (Sugerido por {quem_enviou} em {formatar_data_hora()})"
            if "Casa" in tipo_date_sug:
                dates["casa"].append(texto_formatado)
            else:
                dates["rua"].append(texto_formatado)
            salvar_json(FILE_DATES, dates)
            st.rerun()
