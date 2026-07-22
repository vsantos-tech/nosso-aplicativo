import base64
import json
import os
import streamlit as st
from PIL import Image, ImageOps

# Configuração da página
st.set_page_config(
    page_title="Nosso Aplicativo 💗", page_icon="💗", layout="centered"
)

UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)


# -------------------------------------------------------------
# TRATAMENTO DE IMAGEM PARA RESPEITAR A ORIENTAÇÃO DA GALERIA
# -------------------------------------------------------------
def carregar_imagem_correta(caminho_imagem):
    try:
        image = Image.open(caminho_imagem)
        image = ImageOps.exif_transpose(image)
        return image
    except Exception:
        return caminho_imagem


# -------------------------------------------------------------
# IMAGEM DE FUNDO E ÍCONE DO IOS (COM icone.jpg)
# -------------------------------------------------------------
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
        /* OCULTA BARRA SUPERIOR, MENU E FOOTER DO STREAMLIT */
        header, 
        [data-testid="stHeader"], 
        [data-testid="stAppToolbar"], 
        [data-testid="stHeaderActionElements"],
        div[class*="stAppHeader"], 
        div[class*="stAppToolbar"],
        [data-testid="stStatusWidget"],
        .viewerBadge_container__1323f,
        #MainMenu,
        footer {{
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }}
        
        [data-testid="stDecoration"] {{ display: none !important; }}
        
        .stApp {{
            {bg_style}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            margin-top: 0px !important;
            padding-top: 10px !important;
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
            padding: 4px 6px !important;
            font-size: 11px !important;
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
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Injeta a tag do ícone icone.jpg para o iOS via HTML
    st.components.v1.html(
        """
        <script>
            var link = parent.document.createElement('link');
            link.rel = 'apple-touch-icon';
            link.href = 'app/static/icone.jpg';
            parent.document.getElementsByTagName('head')[0].appendChild(link);
        </script>
        """,
        height=0,
    )


carregar_estilo_fundo()

# -------------------------------------------------------------
# PERSISTÊNCIA DOS DADOS
# -------------------------------------------------------------
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


DEFAULT_SENTIMENTOS = {"larissa": [], "vitoria": []}
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
    "hoje": "Não se esquece de tomar seu psyllium e tô morrendo de saudade de você! 💕",
    "imagem_hoje": "",
    "amanha": "",
    "imagem_amanha": "",
    "resposta_larissa": "",
}
DEFAULT_MUSICAS = [
    {
        "nome": "Nossa Música Favorita",
        "link": "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",
    }
]
DEFAULT_FOTOS = [
    {
        "url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=600",
        "legenda": "Nosso passeio favorito 🌿",
    },
    {
        "url": "https://images.unsplash.com/photo-1522673607200-164d1b6ce486?q=80&w=600",
        "legenda": "Momento aconchego ☕",
    },
]
DEFAULT_DATAS = [
    {"titulo": "Primeiro Encontro", "data": "12/05/2023", "icone": "🥂"},
    {"titulo": "Início do Namoro", "data": "20/06/2023", "icone": "💍"},
]
DEFAULT_COMIDAS = {
    "restaurantes": [
        "🍣 Japonês: Nosso lugar favorito",
        "🍕 Pizzaria: Cantina Especial",
    ],
    "receitas": ["🍝 Massa Especial de Quinta-feira"],
}
DEFAULT_DATES = {
    "casa": [
        "Noite do hambúrguer caseiro com filme",
        "Montar um quebra-cabeça no chão da sala",
        "Noite do vinho e jogos de tabuleiro",
    ],
    "rua": [
        "Piquenique no parque no fim da tarde",
        "Conhecer uma cafeteria artesanal nova",
        "Sessão de cinema no meio da semana",
    ],
}

# -------------------------------------------------------------
# IDENTIFICAÇÃO DE USUÁRIA ("QUEM É VOCÊ?")
# -------------------------------------------------------------
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
    nome_exib = "☀️ Larissa" if st.session_state.usuario_atual == "larissa" else "🌙 Vitória"
    st.write(f"Conectada como: **{nome_exib}**")
with col_topo2:
    if st.button("🔄 Trocar perfil", key="btn_trocar_usr"):
        st.session_state.usuario_atual = None
        st.session_state.e_admin = False
        st.rerun()

# -------------------------------------------------------------
# MODO EDIÇÃO E SENHA (EXCLUSIVO VITÓRIA)
# -------------------------------------------------------------
if "e_admin" not in st.session_state:
    st.session_state.e_admin = False

SENHA_CORRETA = "1234"

if st.session_state.usuario_atual == "vitoria":
    with st.expander("🔑 Acessar Modo Edição (Exclusivo Vitória)", expanded=st.session_state.e_admin):
        if not st.session_state.e_admin:
            senha_input = st.text_input(
                "Digite a senha para editar o app:", type="password", key="pwd_input_main"
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
            if st.button("🚪 SALVAR E SAIR DO MODO EDIÇÃO", key="btn_sair_admin_main"):
                st.session_state.e_admin = False
                st.success("Edições concluídas!")
                st.rerun()

e_admin = (
    st.session_state.e_admin if st.session_state.usuario_atual == "vitoria" else False
)

# -------------------------------------------------------------
# NAVEGAÇÃO POR ABAS
# -------------------------------------------------------------
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

# =============================================================
# ABA 1: COMO ESTÁ SE SENTINDO
# =============================================================
with tab_sentimento:
    st.header("💭 Como estamos nos sentindo hoje?")

    sentimentos_salvos = carregar_json(
        FILE_SENTIMENTOS, DEFAULT_SENTIMENTOS
    )
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

    col_l, col_v = st.columns(2)

    novo_larissa = list(sentimentos_salvos.get("larissa", []))
    novo_vitoria = list(sentimentos_salvos.get("vitoria", []))

    # Lista da Larissa
    with col_l:
        st.write("🌸 **Lista da Larissa:**")
        if st.session_state.usuario_atual == "larissa":
            novo_larissa = []
            for rotulo in opcoes_larissa:
                marcado_padrao = rotulo in sentimentos_salvos.get("larissa", [])
                if st.checkbox(rotulo, value=marcado_padrao, key=f"chk_l_{rotulo}"):
                    novo_larissa.append(rotulo)
        else:
            for rotulo in opcoes_larissa:
                st.checkbox(
                    rotulo,
                    value=(rotulo in sentimentos_salvos.get("larissa", [])),
                    disabled=True,
                    key=f"dis_l_{rotulo}",
                )

    # Lista da Vitória
    with col_v:
        st.write("🌿 **Lista da Vitória:**")
        if st.session_state.usuario_atual == "vitoria":
            novo_vitoria = []
            for rotulo in opcoes_vitoria:
                marcado_padrao = rotulo in sentimentos_salvos.get("vitoria", [])
                if st.checkbox(rotulo, value=marcado_padrao, key=f"chk_v_{rotulo}"):
                    novo_vitoria.append(rotulo)
        else:
            for rotulo in opcoes_vitoria:
                st.checkbox(
                    rotulo,
                    value=(rotulo in sentimentos_salvos.get("vitoria", [])),
                    disabled=True,
                    key=f"dis_v_{rotulo}",
                )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Salvar Meu Sentimento De Hoje"):
        sentimentos_salvos["larissa"] = novo_larissa
        sentimentos_salvos["vitoria"] = novo_vitoria
        salvar_json(FILE_SENTIMENTOS, sentimentos_salvos)
        st.success("Seu sentimento foi atualizado!")
        st.rerun()

    # MODO EDIÇÃO: ADICIONAR E REMOVER OPÇÕES DE SENTIMENTOS
    if e_admin:
        st.markdown("---")
        st.subheader("✏️ Gerenciar Lista de Sentimentos (Modo Edição)")
        
        tab_s1, tab_s2 = st.tabs(["🌸 Opções da Larissa", "🌿 Opções da Vitória"])
        
        with tab_s1:
            st.write("**Opções Atuais da Larissa:**")
            for idx_s, item_s in enumerate(opcoes_larissa):
                col_s_txt, col_s_del = st.columns([3, 1])
                with col_s_txt:
                    st.write(f"- {item_s}")
                with col_s_del:
                    if st.button(f"🗑️ Excluir", key=f"btn_del_sl_{idx_s}"):
                        opcoes_sentimentos["larissa"].pop(idx_s)
                        salvar_json(FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos)
                        st.success("Opção removida!")
                        st.rerun()
            
            add_sent_l = st.text_input("Novo sentimento para a Larissa (ex: Radiante ✨):", key="in_add_sl")
            if st.button("➕ Adicionar Sentimento (Larissa)", key="btn_add_sl"):
                if add_sent_l:
                    opcoes_sentimentos["larissa"].append(add_sent_l)
                    salvar_json(FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos)
                    st.success("Novo sentimento adicionado à lista da Larissa!")
                    st.rerun()

        with tab_s2:
            st.write("**Opções Atuais da Vitória:**")
            for idx_s, item_s in enumerate(opcoes_vitoria):
                col_s_txt, col_s_del = st.columns([3, 1])
                with col_s_txt:
                    st.write(f"- {item_s}")
                with col_s_del:
                    if st.button(f"🗑️ Excluir", key=f"btn_del_sv_{idx_s}"):
                        opcoes_sentimentos["vitoria"].pop(idx_s)
                        salvar_json(FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos)
                        st.success("Opção removida!")
                        st.rerun()
            
            add_sent_v = st.text_input("Novo sentimento para a Vitória (ex: Com preguiça 😴):", key="in_add_sv")
            if st.button("➕ Adicionar Sentimento (Vitória)", key="btn_add_sv"):
                if add_sent_v:
                    opcoes_sentimentos["vitoria"].append(add_sent_v)
                    salvar_json(FILE_OPCOES_SENTIMENTOS, opcoes_sentimentos)
                    st.success("Novo sentimento adicionado à lista da Vitória!")
                    st.rerun()

# =============================================================
# ABA 2: RECADO
# =============================================================
with tab_recado:
    st.header("☀️ Lembrete pro meu cheirinho")

    recados = carregar_json(FILE_RECADO, DEFAULT_RECADO)
    st.info(f"### {recados.get('hoje', '')}")

    img_hoje = recados.get("imagem_hoje", "")
    if img_hoje and os.path.exists(img_hoje):
        st.image(carregar_imagem_correta(img_hoje), use_container_width=True)

    resp_atual = recados.get("resposta_larissa", "")
    if resp_atual:
        st.markdown("#### 👇 Resposta da Larissa:")
        st.success(f"💬 **Larissa:** {resp_atual}")

    # RESPOSTA EXCLUSIVA DA LARISSA
    if st.session_state.usuario_atual == "larissa":
        st.markdown("---")
        st.markdown("### 👇 Resposta:")
        texto_resposta = st.text_area(
            "Escreva aqui sua resposta se quiser:",
            value=resp_atual,
            key="input_resp_larissa",
            placeholder="Digite algo para responder o recado...",
        )

        if st.button("💌 Enviar Resposta", key="btn_env_resposta"):
            recados["resposta_larissa"] = texto_resposta
            salvar_json(FILE_RECADO, recados)
            st.success("Sua resposta foi enviada com sucesso! 💕")
            st.rerun()

    # ADICIONAR NOVO LEMBRETE + FOTO (PERFIL VITÓRIA SEM PRECISAR DE MODO EDIÇÃO)
    if st.session_state.usuario_atual == "vitoria":
        st.markdown("---")
        st.subheader("✍️ Adicionar Lembrete do Dia")
        novo_recado_vit = st.text_area(
            "Escreva o novo lembrete:",
            value=recados.get("hoje", ""),
            key="input_lembrete_vit_direto",
        )
        up_img_vit_direto = st.file_uploader(
            "Adicionar uma imagem ao lembrete (opcional):",
            type=["png", "jpg", "jpeg", "webp"],
            key="up_img_vit_direto",
        )

        if st.button("💌 Publicar Lembrete Hoje", key="btn_pub_lembrete_vit"):
            recados["hoje"] = novo_recado_vit
            if up_img_vit_direto is not None:
                file_path = os.path.join(
                    UPLOADS_DIR, "recado_hoje_" + up_img_vit_direto.name
                )
                with open(file_path, "wb") as f:
                    f.write(up_img_vit_direto.getbuffer())
                recados["imagem_hoje"] = file_path
            recados["resposta_larissa"] = ""
            salvar_json(FILE_RECADO, recados)
            st.success("Novo lembrete publicado no app!")
            st.rerun()

    if recados.get("amanha"):
        st.caption(
            "📌 *Existe um recado agendado preparado para carregar amanhã!*"
        )

    # MODO EDIÇÃO DA VITÓRIA (GERENCIAR / AGENDAR)
    if e_admin:
        st.markdown("---")
        st.subheader("✏️ Gerenciar Recados (Modo Edição)")

        st.markdown("**1. Editar Recado de Hoje (Exibido Agora):**")
        recado_hoje_edit = st.text_area(
            "Mensagem Atual:",
            value=recados.get("hoje", ""),
            key="recado_hoje_text",
        )
        up_img_hoje = st.file_uploader(
            "Adicionar/Trocar Imagem do Recado de Hoje:",
            type=["png", "jpg", "jpeg", "webp"],
            key="up_img_hoje_file",
        )

        if st.button("💾 Alterar Recado e Imagem de Hoje", key="btn_salvar_hoje"):
            recados["hoje"] = recado_hoje_edit
            if up_img_hoje is not None:
                file_path = os.path.join(
                    UPLOADS_DIR, "recado_hoje_" + up_img_hoje.name
                )
                with open(file_path, "wb") as f:
                    f.write(up_img_hoje.getbuffer())
                recados["imagem_hoje"] = file_path
            recados["resposta_larissa"] = ""
            salvar_json(FILE_RECADO, recados)
            st.success("Recado atualizado!")
            st.rerun()

        st.markdown("---")

        st.markdown("**2. Agendar / Criar Recado para Amanhã:**")
        recado_amanha_edit = st.text_area(
            "Digite o recado que será exibido amanhã:",
            value=recados.get("amanha", ""),
            key="recado_amanha_text",
        )
        up_img_amanha = st.file_uploader(
            "Adicionar Imagem para o Recado de Amanhã:",
            type=["png", "jpg", "jpeg", "webp"],
            key="up_img_amanha_file",
        )

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button(
                "➕ Agendar Recado e Imagem para Amanhã",
                key="btn_salvar_amanha",
            ):
                recados["amanha"] = recado_amanha_edit
                if up_img_amanha is not None:
                    file_path = os.path.join(
                        UPLOADS_DIR, "recado_amanha_" + up_img_amanha.name
                    )
                    with open(file_path, "wb") as f:
                        f.write(up_img_amanha.getbuffer())
                    recados["imagem_amanha"] = file_path
                salvar_json(FILE_RECADO, recados)
                st.success("Recado de amanhã guardado!")
                st.rerun()
        with col_r2:
            if recados.get("amanha"):
                if st.button(
                    "🚀 Promover Recado de Amanhã para Hoje",
                    key="btn_promover",
                ):
                    recados["hoje"] = recados["amanha"]
                    recados["imagem_hoje"] = recados.get("imagem_amanha", "")
                    recados["amanha"] = ""
                    recados["imagem_amanha"] = ""
                    recados["resposta_larissa"] = ""
                    salvar_json(FILE_RECADO, recados)
                    st.success("Recado de amanhã promovido a Recado Atual!")
                    st.rerun()

# =============================================================
# ABA 3: MÚSICAS
# =============================================================
with tab_musicas:
    st.header("🎶 Músicas Que Lembram Nós")

    musicas = carregar_json(FILE_MUSICAS, DEFAULT_MUSICAS)

    for idx, m in enumerate(musicas):
        st.subheader(f"🎵 {m['nome']}")
        st.write(f"👉 [Ouvir no Spotify]({m['link']})")

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
                    musicas[idx] = {"nome": novo_nome, "link": novo_link}
                    salvar_json(FILE_MUSICAS, musicas)
                    st.success("Música alterada!")
                    st.rerun()
            with c_del:
                if st.button(
                    f"🗑️ Excluir Música #{idx+1}", key=f"btn_m_del_{idx}"
                ):
                    musicas.pop(idx)
                    salvar_json(FILE_MUSICAS, musicas)
                    st.success("Música removida!")
                    st.rerun()
        st.markdown("---")

    st.subheader(
        "✍️ Escreva aqui quais músicas que te lembram nós: Nome da música / Artista"
    )
    sugestao_musica = st.text_input(
        "Música e Artista:",
        key="sugestao_m_larissa",
        placeholder="Ex: Metamorfose Ambulante - Raul Seixas",
    )
    link_sugestao = st.text_input(
        "Link do Spotify (opcional):",
        key="sugestao_m_link",
        placeholder="https://open.spotify.com/track/...",
    )

    if st.button("💖 Enviar Música para a Lista"):
        if sugestao_musica:
            m_link = (
                link_sugestao
                if link_sugestao
                else "https://open.spotify.com/search/"
                + sugestao_musica.replace(" ", "%20")
            )
            musicas.append({"nome": sugestao_musica, "link": m_link})
            salvar_json(FILE_MUSICAS, musicas)
            st.success("Música adicionada à nossa lista com sucesso! 🎶")
            st.rerun()

# =============================================================
# ABA 4: FOTOS
# =============================================================
with tab_fotos:
    st.header("📸 Mural de Memórias")

    fotos = carregar_json(FILE_FOTOS, DEFAULT_FOTOS)
    col1, col2 = st.columns(2)

    for idx, foto in enumerate(fotos):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.image(
                carregar_imagem_correta(foto["url"]),
                caption=foto["legenda"],
                use_container_width=True,
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
                        fotos[idx] = {"url": nova_url, "legenda": nova_legenda}
                        salvar_json(FILE_FOTOS, fotos)
                        st.success("Foto alterada!")
                        st.rerun()
                with c_exc:
                    if st.button(
                        f"🗑️ Excluir #{idx+1}", key=f"btn_f_del_{idx}"
                    ):
                        fotos.pop(idx)
                        salvar_json(FILE_FOTOS, fotos)
                        st.success("Foto removida!")
                        st.rerun()

    if e_admin:
        st.markdown("---")
        st.subheader("➕ Adicionar Nova Foto ao Mural")

        tab_up1, tab_up2 = st.tabs(
            ["📁 Enviar do PC/Galeria do Celular", "🔗 Usar Link da Web"]
        )

        with tab_up1:
            uploaded_file = st.file_uploader(
                "Escolha uma foto da galeria ou computador:",
                type=["png", "jpg", "jpeg", "webp"],
                key="upload_foto_file",
            )
            legenda_upload = st.text_input(
                "Legenda da Foto (Galeria):", key="legenda_upload_file"
            )

            if st.button("📤 Upload e Adicionar Foto", key="btn_upload_foto_save"):
                if uploaded_file is not None:
                    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    fotos.append({"url": file_path, "legenda": legenda_upload})
                    salvar_json(FILE_FOTOS, fotos)
                    st.success("Foto enviada da galeria e salva no mural!")
                    st.rerun()
                else:
                    st.warning(
                        "Selecione um arquivo de imagem da sua galeria primeiro."
                    )

        with tab_up2:
            add_f_url = st.text_input(
                "Link/URL da Imagem da Web:", key="add_f_url"
            )
            add_f_leg = st.text_input("Legenda da Foto (Web):", key="add_f_leg")
            if st.button("➕ Adicionar Foto via Link", key="btn_add_foto_url"):
                if add_f_url:
                    fotos.append({"url": add_f_url, "legenda": add_f_leg})
                    salvar_json(FILE_FOTOS, fotos)
                    st.success("Nova foto da web adicionada!")
                    st.rerun()

# =============================================================
# ABA 5: DATAS
# =============================================================
with tab_datas:
    st.header("📅 Datas Especiais")

    datas = carregar_json(FILE_DATAS, DEFAULT_DATAS)

    for idx, d in enumerate(datas):
        st.subheader(f"{d.get('icone', '🗓️')} {d['titulo']}")
        st.write(f"🗓️ **Data:** {d['data']}")

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
                    f"💾 Alterar Data #{idx+1}", key=f"btn_d_up_{idx}"
                ):
                    datas[idx] = {"titulo": n_tit, "data": n_dt, "icone": n_ic}
                    salvar_json(FILE_DATAS, datas)
                    st.success("Data alterada!")
                    st.rerun()
            with c_x:
                if st.button(
                    f"🗑️ Excluir Data #{idx+1}", key=f"btn_d_del_{idx}"
                ):
                    datas.pop(idx)
                    salvar_json(FILE_DATAS, datas)
                    st.success("Data removida!")
                    st.rerun()
        st.markdown("---")

    if e_admin:
        st.subheader("➕ Adicionar Novo Marco/Data")
        add_d_ic = st.text_input(
            "Emoji/Ícone (ex: 💍, ✈️):", value="❤️", key="add_d_ic"
        )
        add_d_tit = st.text_input("Título do Evento:", key="add_d_tit")
        add_d_dt = st.text_input("Data (ex: 12/05/2023):", key="add_d_dt")

        if st.button("➕ Adicionar Data", key="btn_add_data"):
            if add_d_tit and add_d_dt:
                datas.append(
                    {"titulo": add_d_tit, "data": add_d_dt, "icone": add_d_ic}
                )
                salvar_json(FILE_DATAS, datas)
                st.success("Nova data adicionada!")
                st.rerun()

# =============================================================
# ABA 6: COMIDAS
# =============================================================
with tab_comidas:
    st.header("🍕 O Que Amamos Comer")

    comidas = carregar_json(FILE_COMIDAS, DEFAULT_COMIDAS)
    subtab1, subtab2 = st.tabs(["Restaurantes / Entregas", "Receitas em Casa"])

    with subtab1:
        st.subheader("Restaurantes & Entregas Favoritas")
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

        if e_admin:
            st.markdown("---")
            add_rest = st.text_input(
                "Novo Restaurante / Delivery:", key="add_rest"
            )
            if st.button("➕ Adicionar Restaurante", key="btn_add_rest"):
                if add_rest:
                    comidas["restaurantes"].append(add_rest)
                    salvar_json(FILE_COMIDAS, comidas)
                    st.rerun()

    with subtab2:
        st.subheader("Receitas Que Fazemos Juntos")
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

        if e_admin:
            st.markdown("---")
            add_rec = st.text_input("Nova Receita:", key="add_rec")
            if st.button("➕ Adicionar Receita", key="btn_add_rec"):
                if add_rec:
                    comidas["receitas"].append(add_rec)
                    salvar_json(FILE_COMIDAS, comidas)
                    st.rerun()

# =============================================================
# ABA 7: ENCONTROS (DATES)
# =============================================================
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

    st.markdown("---")
    st.subheader("✍️ Deixe aqui sua sugestão de date:")
    tipo_date_sug = st.radio(
        "Tipo de Encontro:",
        ["🏠 Em Casa", "🌳 Fora de Casa"],
        horizontal=True,
        key="sug_d_tipo",
    )
    sugestao_date = st.text_input(
        "Ideia de Date:",
        key="sugestao_date_input",
        placeholder="Ex: Noite da pizza brotinho artesanal...",
    )

    if st.button("💌 Enviar", key="btn_sug_date_send"):
        if sugestao_date:
            if "Casa" in tipo_date_sug:
                dates["casa"].append(sugestao_date)
            else:
                dates["rua"].append(sugestao_date)
            salvar_json(FILE_DATES, dates)
            st.success("Sua sugestão de date foi enviada com sucesso! 💖")
            st.rerun()

    if e_admin:
        st.markdown("---")
        st.subheader("➕ Adicionar Nova Ideia de Encontro (Modo Edição)")
        tipo_date = st.radio(
            "Tipo de Encontro Admin:",
            ["🏠 Em Casa", "🌳 Fora de Casa"],
            horizontal=True,
            key="add_d_tipo",
        )
        nova_ideia = st.text_input("Descrição do Encontro:", key="add_d_desc")

        if st.button("➕ Adicionar Encontro", key="btn_add_date_main"):
            if nova_ideia:
                if "Casa" in tipo_date:
                    dates["casa"].append(nova_ideia)
                else:
                    dates["rua"].append(nova_ideia)
                salvar_json(FILE_DATES, dates)
                st.success("Nova ideia de encontro adicionada!")
                st.rerun()
