import streamlit as st
from github import Github
import json
from datetime import datetime, timedelta, timezone
import base64

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Nosso Aplicativo 💗", page_icon="💗", layout="centered")

# Impede erros de tradução do Chrome
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

# Fundo em CSS + CSS para imagens nítidas
css = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFD1DC 0%, #FFB07C 50%, #E65C83 100%) !important;
        background-attachment: fixed !important;
    }
    
    .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] {
        color: #1A1A1A !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #1A1A1A !important;
        border-radius: 8px !important;
    }
    
    .stButton>button { 
        background: linear-gradient(90deg, #E65C83 0%, #F07865 100%); 
        color: white !important; 
        border-radius: 10px; 
        border: none; 
        font-weight: bold; 
    }
    
    .historico-card { 
        background-color: #FFFFFF !important; 
        padding: 15px; 
        border-radius: 10px; 
        margin-bottom: 10px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        border-left: 5px solid #E65C83;
        color: #1A1A1A !important;
    }
    
    .destaque-card { 
        background-color: #FFFFFF !important; 
        padding: 15px; 
        border-radius: 10px; 
        margin-bottom: 10px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        border-left: 5px solid #FFD700;
        color: #1A1A1A !important;
    }

    .historico-card b, .destaque-card b {
        color: #4A1228 !important;
        font-weight: bold;
    }

    .historico-card p, .destaque-card p {
        color: #1A1A1A !important;
        font-size: 1rem;
        margin-top: 8px;
        margin-bottom: 0px;
    }

    .historico-card small, .destaque-card small {
        color: #666666 !important;
    }

    /* Garante exibição de foto com nitidez total */
    .img-nitida {
        width: 100%;
        max-width: 100%;
        border-radius: 12px;
        margin-top: 10px;
        margin-bottom: 10px;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

# 2. FUNÇÕES DE DATA E IMAGEM
def obter_fuso_horario():
    return timezone(timedelta(hours=-3))

def obter_data_hora():
    return datetime.now(obter_fuso_horario()).strftime("%d/%m/%Y às %H:%M")

def obter_data_hoje():
    return datetime.now(obter_fuso_horario()).strftime("%d/%m/%Y")

def processar_imagem(uploaded_file):
    if uploaded_file is not None:
        try:
            # Lê os bytes originais da foto SEM NENHUMA COMPRESSÃO
            bytes_data = uploaded_file.getvalue()
            tipo_mime = uploaded_file.type if uploaded_file.type else "image/jpeg"
            img_str = base64.b64encode(bytes_data).decode()
            return f"data:{tipo_mime};base64,{img_str}"
        except Exception:
            return None
    return None

def exibir_foto_nitida(foto_b64):
    if foto_b64:
        st.markdown(f'<img src="{foto_b64}" class="img-nitida" />', unsafe_allow_html=True)

# 3. CONEXÃO SEGURA COM O GITHUB
@st.cache_data(ttl=600)
def ler_dados_github(token, repo_name):
    opcoes_padrao = ["Feliz 😊", "Ansiosa 😰", "Cansada 🥱", "Empolgada ✨", "Triste 😢", "Com Saudade ❤️", "Estressada 🤯", "Querendo colinho 😭"]
    estrutura_padrao = {
        "recados": [], "sentimentos": [], "musicas": [], "fotos": [], 
        "datas": [], "comidas": [], "dates": [], 
        "opcoes_sentimentos": opcoes_padrao
    }
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        file_content = repo.get_contents("dados_app.json")
        dados = json.loads(file_content.decoded_content.decode())
        if "opcoes_sentimentos" not in dados:
            dados["opcoes_sentimentos"] = opcoes_padrao
        return dados
    except Exception:
        return estrutura_padrao

def ler_dados():
    if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
        return ler_dados_github(st.secrets["GITHUB_TOKEN"], st.secrets["GITHUB_REPO"])
    return {
        "recados": [], "sentimentos": [], "musicas": [], "fotos": [], 
        "datas": [], "comidas": [], "dates": [], 
        "opcoes_sentimentos": ["Feliz 😊", "Ansiosa 😰", "Cansada 🥱", "Empolgada ✨", "Triste 😢", "Com Saudade ❤️", "Estressada 🤯", "Querendo colinho 😭"]
    }

def salvar_dados(dados):
    try:
        if "GITHUB_TOKEN" not in st.secrets or "GITHUB_REPO" not in st.secrets:
            st.error("Configure as chaves GITHUB_TOKEN e GITHUB_REPO nos Secrets!")
            return False
            
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(st.secrets["GITHUB_REPO"])
        content_str = json.dumps(dados, indent=2)
        try:
            contents = repo.get_contents("dados_app.json")
            repo.update_file(contents.path, "Atualizando dados", content_str, contents.sha)
        except Exception:
            repo.create_file("dados_app.json", "Criando banco de dados", content_str)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados no GitHub: {e}")
        return False

def deletar_item(categoria, index):
    st.session_state.dados[categoria].pop(index)
    salvar_dados(st.session_state.dados)
    st.rerun()

if "dados" not in st.session_state:
    st.session_state.dados = ler_dados()

if "editando" not in st.session_state:
    st.session_state.editando = None

# 4. TELA DE LOGIN
if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = None

if st.session_state.usuario_atual is None:
    st.title("Nosso Aplicativo 💗")
    st.write("Bem-vinda ao nosso cantinho! Quem está acessando?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☀️ Larissa", use_container_width=True):
            st.session_state.usuario_atual = "Larissa"
            st.rerun()
    with col2:
        if st.button("🌙 Vitória", use_container_width=True):
            st.session_state.usuario_atual = "Vitória"
            st.rerun()
    st.stop()

# 5. CABEÇALHO DO APP E MODO EDIÇÃO
col_topo1, col_topo2 = st.columns([2, 1])
with col_topo1:
    st.title("Nosso Aplicativo 💗")
    st.write(f"Logada como: **{st.session_state.usuario_atual}**")

with col_topo2:
    if st.button("Sair / Trocar", use_container_width=True):
        st.session_state.usuario_atual = None
        st.rerun()
        
e_admin = False
if st.session_state.usuario_atual == "Vitória":
    e_admin = st.toggle("🛠️ Modo Edição (Apenas Vitória)")

hoje = obter_data_hoje()

# 6. AS 7 ABAS
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["💌 Recados", "💭 Sentimentos", "🎵 Músicas", "📸 Fotos", "📅 Datas", "🍕 Comidas", "🥂 Dates"])

# --- ABA 1: RECADOS ---
with t1:
    st.header("💌 Mural de Recados")
    texto_recado = st.text_area("Escreva seu recado:")
    foto_recado = st.file_uploader("Anexar foto (opcional)", type=["png", "jpg", "jpeg", "webp"], key="up_recado")
    
    if st.button("Publicar Recado"):
        if texto_recado or foto_recado:
            img_b64 = processar_imagem(foto_recado)
            st.session_state.dados["recados"].insert(0, {
                "autor": st.session_state.usuario_atual,
                "texto": texto_recado,
                "foto": img_b64,
                "data": obter_data_hora()
            })
            if salvar_dados(st.session_state.dados):
                st.success("Publicado!")
                st.rerun()
    
    st.divider()
    
    recados_hoje = [item for item in st.session_state.dados["recados"] if item['data'].startswith(hoje)]
    if recados_hoje:
        st.subheader("🌟 Destaques de Hoje")
        for item in recados_hoje:
            st.markdown(f"""
            <div class="destaque-card">
                <b>{item['autor']}</b> - <small>{item['data']}</small><br>
                <p>{item['texto']}</p>
            </div>
            """, unsafe_allow_html=True)
            if item.get('foto'):
                exibir_foto_nitida(item['foto'])
        st.divider()

    with st.expander("📜 Ver Histórico Completo de Recados", expanded=False):
        if not st.session_state.dados["recados"]:
            st.write("Ainda não há recados salvos.")
        else:
            for i, item in enumerate(st.session_state.dados["recados"]):
                st.markdown(f"""
                <div class="historico-card">
                    <b>{item['autor']}</b> - <small>{item['data']}</small><br>
                    <p>{item['texto']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if item.get('foto'):
                    exibir_foto_nitida(item['foto'])
                    
                if e_admin:
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🗑️ Excluir", key=f"del_rec_{i}"):
                            deletar_item("recados", i)
                    with c2:
                        key_edit = f"recados_{i}"
                        if st.button("✏️ Alterar", key=f"btn_edit_rec_{i}"):
                            st.session_state.editando = key_edit if st.session_state.editando != key_edit else None
                            st.rerun()

                    if st.session_state.editando == f"recados_{i}":
                        novo_texto = st.text_area("Editar recado:", value=item['texto'], key=f"edit_rec_txt_{i}")
                        c_s1, c_s2 = st.columns(2)
                        with c_s1:
                            if st.button("Salvar Alteração", key=f"save_rec_{i}"):
                                st.session_state.dados["recados"][i]['texto'] = novo_texto
                                salvar_dados(st.session_state.dados)
                                st.session_state.editando = None
                                st.rerun()
                        with c_s2:
                            if st.button("Cancelar", key=f"canc_rec_{i}"):
                                st.session_state.editando = None
                                st.rerun()

# --- ABA 2: SENTIMENTOS ---
with t2:
    st.header("💭 Como estamos hoje?")
    opcoes_atuais = st.session_state.dados.get("opcoes_sentimentos", [])
    
    if e_admin:
        if st.button("🛠️ Adicionar Nova Opção de Sentimento", key="btn_add_opt_sen"):
            st.session_state.editando = "add_opcao_sentimento" if st.session_state.editando != "add_opcao_sentimento" else None
            st.rerun()

        if st.session_state.editando == "add_opcao_sentimento":
            novo_sentimento_opcao = st.text_input("Escreva o novo sentimento (ex: Animada 🥳):")
            c_opt1, c_opt2 = st.columns(2)
            with c_opt1:
                if st.button("➕ Adicionar à Lista", key="btn_save_opt_sen"):
                    if novo_sentimento_opcao and novo_sentimento_opcao not in opcoes_atuais:
                        st.session_state.dados["opcoes_sentimentos"].append(novo_sentimento_opcao)
                        if salvar_dados(st.session_state.dados):
                            st.success(f"Opção '{novo_sentimento_opcao}' adicionada com sucesso!")
                            st.session_state.editando = None
                            st.rerun()
            with c_opt2:
                if st.button("Cancelar", key="canc_opt_sen"):
                    st.session_state.editando = None
                    st.rerun()

    sentimento_escolhido = st.multiselect("Selecione seus sentimentos:", opcoes_atuais)
    
    if st.button("Salvar Sentimento"):
        if sentimento_escolhido:
            st.session_state.dados["sentimentos"].insert(0, {
                "autor": st.session_state.usuario_atual,
                "sentimentos": ", ".join(sentimento_escolhido),
                "data": obter_data_hora()
            })
            if salvar_dados(st.session_state.dados):
                st.success("Sentimento registrado!")
                st.rerun()

    st.divider()
    st.subheader("📜 Feed de Sentimentos")
    for i, sen in enumerate(st.session_state.dados["sentimentos"]):
        st.markdown(f"<div class='historico-card'><b>{sen['autor']}</b> se sentiu: <b>{sen['sentimentos']}</b> <br><small>Adicionado em {sen['data']}</small></div>", unsafe_allow_html=True)
        if e_admin:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🗑️ Excluir", key=f"del_sen_{i}"):
                    deletar_item("sentimentos", i)
            with c2:
                key_edit = f"sentimentos_{i}"
                if st.button("✏️ Alterar", key=f"btn_edit_sen_{i}"):
                    st.session_state.editando = key_edit if st.session_state.editando != key_edit else None
                    st.rerun()

            if st.session_state.editando == f"sentimentos_{i}":
                novo_sen = st.text_input("Editar sentimento:", value=sen['sentimentos'], key=f"edit_sen_txt_{i}")
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    if st.button("Salvar Alteração", key=f"save_sen_{i}"):
                        st.session_state.dados["sentimentos"][i]['sentimentos'] = novo_sen
                        salvar_dados(st.session_state.dados)
                        st.session_state.editando = None
                        st.rerun()
                with c_s2:
                    if st.button("Cancelar", key=f"canc_sen_{i}"):
                        st.session_state.editando = None
                        st.rerun()

# --- ABA 3: MÚSICAS ---
with t3:
    st.header("🎵 Nossas Músicas")
    nome_musica = st.text_input("Nome da Música e Artista:")
    link_musica = st.text_input("Link do Spotify (opcional):")
    
    if st.button("Adicionar Música"):
        if nome_musica:
            st.session_state.dados["musicas"].insert(0, {
                "autor": st.session_state.usuario_atual,
                "nome": nome_musica,
                "link": link_musica,
                "data": obter_data_hora()
            })
            if salvar_dados(st.session_state.dados):
                st.success("Música salva!")
                st.rerun()

    st.divider()
    st.subheader("📜 Músicas Adicionadas")
    for i, mus in enumerate(st.session_state.dados["musicas"]):
        link_str = f" - <a href='{mus['link']}' target='_blank'>Ouvir no Spotify</a>" if mus.get('link') else ""
        st.markdown(f"<div class='historico-card'>🎵 <b>{mus['nome']}</b>{link_str}<br><small>Adicionado por {mus['autor']} em {mus['data']}</small></div>", unsafe_allow_html=True)
        if e_admin:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🗑️ Excluir", key=f"del_mus_{i}"):
                    deletar_item("musicas", i)
            with c2:
                key_edit = f"musicas_{i}"
                if st.button("✏️ Alterar", key=f"btn_edit_mus_{i}"):
                    st.session_state.editando = key_edit if st.session_state.editando != key_edit else None
                    st.rerun()

            if st.session_state.editando == f"musicas_{i}":
                novo_nome = st.text_input("Nome:", value=mus['nome'], key=f"edit_mus_nome_{i}")
                novo_link = st.text_input("Link:", value=mus.get('link', ''), key=f"edit_mus_link_{i}")
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    if st.button("Salvar Alteração", key=f"save_mus_{i}"):
                        st.session_state.dados["musicas"][i]['nome'] = novo_nome
                        st.session_state.dados["musicas"][i]['link'] = novo_link
                        salvar_dados(st.session_state.dados)
                        st.session_state.editando = None
                        st.rerun()
                with c_s2:
                    if st.button("Cancelar", key=f"canc_mus_{i}"):
                        st.session_state.editando = None
                        st.rerun()

# --- ABA 4: FOTOS ---
with t4:
    st.header("📸 Nosso Mural de Fotos")
    foto_mural = st.file_uploader("Escolha uma foto da galeria", type=["png", "jpg", "jpeg", "webp"], key="foto_mural")
    legenda = st.text_input("Legenda da foto:")
    
    if st.button("Adicionar ao Mural"):
        if foto_mural:
            img_b64 = processar_imagem(foto_mural)
            st.session_state.dados["fotos"].insert(0, {
                "autor": st.session_state.usuario_atual,
                "legenda": legenda,
                "foto": img_b64,
                "data": obter_data_hora()
            })
            if salvar_dados(st.session_state.dados):
                st.success("Foto adicionada!")
                st.rerun()

    st.divider()
    st.subheader("📜 Álbum")
    for i, ft in enumerate(st.session_state.dados["fotos"]):
        st.markdown(f"<div class='historico-card'><b>{ft['legenda']}</b><br><small>Por {ft['autor']} em {ft['data']}</small></div>", unsafe_allow_html=True)
        if ft.get('foto'):
            exibir_foto_nitida(ft['foto'])
        if e_admin:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🗑️ Excluir", key=f"del_fot_{i}"):
                    deletar_item("fotos", i)
            with c2:
                key_edit = f"fotos_{i}"
                if st.button("✏️ Alterar Legenda", key=f"btn_edit_fot_{i}"):
                    st.session_state.editando = key_edit if st.session_state.editando != key_edit else None
                    st.rerun()

            if st.session_state.editando == f"fotos_{i}":
                nova_legenda = st.text_input("Legenda:", value=ft['legenda'], key=f"edit_fot_txt_{i}")
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    if st.button("Salvar Alteração", key=f"save_fot_{i}"):
                        st.session_state.dados["fotos"][i]['legenda'] = nova_legenda
                        salvar_dados(st.session_state.dados)
                        st.session_state.editando = None
                        st.rerun()
                with c_s2:
                    if st.button("Cancelar", key=f"canc_fot_{i}"):
                        st.session_state.editando = None
                        st.rerun()

# --- ABA 5: DATAS ---
with t5:
    st.header("📅 Datas Importantes")
    nome_data = st.text_input("O que vamos comemorar/lembrar?")
    dia_data = st.date_input("Escolha o dia:")
    
    if st.button("Salvar Data"):
        if nome_data:
            st.session_state.dados["datas"].insert(0, {
                "autor": st.session_state.usuario_atual,
                "titulo": nome_data,
                "dia": dia_data.strftime("%d/%m/%Y"),
                "data": obter_data_hora()
            })
            if salvar_dados(st.session_state.dados):
                st.success("Data salva!")
                st.rerun()

    st.divider()
    st.subheader("📜 Datas Salvas")
    for i, dt in enumerate(st.session_state.dados["datas"]):
        st.markdown(f"<div class='historico-card'>📅 <b>{dt['titulo']}</b> no dia <b>{dt['dia']}</b><br><small>Adicionado por {dt['autor']} em {dt['data']}</small></div>", unsafe_allow_html=True)
        if e_admin:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🗑️ Excluir", key=f"del_dat_{i}"):
                    deletar_item("datas", i)
            with c2:
                key_edit = f"datas_{i}"
                if st.button("✏️ Alterar", key=f"btn_edit_dat_{i}"):
                    st.session_state.editando = key_edit if st.session_state.editando != key_edit else None
                    st.rerun()

            if st.session_state.editando == f"datas_{i}":
                novo_tit = st.text_input("Título:", value=dt['titulo'], key=f"edit_dat_txt_{i}")
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    if st.button("Salvar Alteração", key=f"save_dat_{i}"):
                        st.session_state.dados["datas"][i]['titulo'] = novo_tit
                        salvar_dados(st.session_state.dados)
                        st.session_state.editando = None
                        st.rerun()
                with c_s2:
                    if st.button("Cancelar", key=f"canc_dat_{i}"):
                        st.session_state.editando = None
                        st.rerun()

# --- ABA 6: COMIDAS ---
with t6:
    st.header("🍕 O que gostamos de comer")
    nome_comida = st.text_input("Nome da comida ou Restaurante:")
    tipo_comida = st.radio("Onde?", ["Fazer em Casa", "Comer Fora / Pedir"])
    
    if st.button("Salvar Comida"):
        if nome_comida:
            st.session_state.dados["comidas"].insert(0, {
                "autor": st.session_state.usuario_atual,
                "nome": nome_comida,
                "tipo": tipo_comida,
                "data": obter_data_hora()
            })
            if salvar_dados(st.session_state.dados):
                st.success("Comida salva!")
                st.rerun()

    st.divider()
    st.subheader("📜 Lista de Comidas")
    for i, cm in enumerate(st.session_state.dados["comidas"]):
        st.markdown(f"<div class='historico-card'><b>{cm['nome']}</b> ({cm['tipo']})<br><small>Adicionado por {cm['autor']} em {cm['data']}</small></div>", unsafe_allow_html=True)
        if e_admin:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🗑️ Excluir", key=f"del_com_{i}"):
                    deletar_item("comidas", i)
            with c2:
                key_edit = f"comidas_{i}"
                if st.button("✏️ Alterar", key=f"btn_edit_com_{i}"):
                    st.session_state.editando = key_edit if st.session_state.editando != key_edit else None
                    st.rerun()

            if st.session_state.editando == f"comidas_{i}":
                novo_nome = st.text_input("Nome:", value=cm['nome'], key=f"edit_com_nome_{i}")
                novo_tipo = st.text_input("Tipo (Casa/Fora):", value=cm['tipo'], key=f"edit_com_tipo_{i}")
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    if st.button("Salvar Alteração", key=f"save_com_{i}"):
                        st.session_state.dados["comidas"][i]['nome'] = novo_nome
                        st.session_state.dados["comidas"][i]['tipo'] = novo_tipo
                        salvar_dados(st.session_state.dados)
                        st.session_state.editando = None
                        st.rerun()
                with c_s2:
                    if st.button("Cancelar", key=f"canc_com_{i}"):
                        st.session_state.editando = None
                        st.rerun()

# --- ABA 7: DATES ---
with t7:
    st.header("🥂 Nossos Dates")
    ideia_date = st.text_input("Ideia de lugar ou date:")
    status_date = st.radio("Status:", ["Queremos ir/fazer", "Já fomos/fizemos e amamos!"])
    
    if st.button("Salvar Date"):
        if ideia_date:
            st.session_state.dados["dates"].insert(0, {
                "autor": st.session_state.usuario_atual,
                "ideia": ideia_date,
                "status": status_date,
                "data": obter_data_hora()
            })
            if salvar_dados(st.session_state.dados):
                st.success("Date salvo!")
                st.rerun()

    st.divider()
    st.subheader("📜 Nossa Lista de Dates")
    for i, dts in enumerate(st.session_state.dados["dates"]):
        st.markdown(f"<div class='historico-card'><b>{dts['ideia']}</b> - {dts['status']}<br><small>Adicionado por {dts['autor']} em {dts['data']}</small></div>", unsafe_allow_html=True)
        if e_admin:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🗑️ Excluir", key=f"del_date_{i}"):
                    deletar_item("dates", i)
            with c2:
                key_edit = f"dates_{i}"
                if st.button("✏️ Alterar", key=f"btn_edit_date_{i}"):
                    st.session_state.editando = key_edit if st.session_state.editando != key_edit else None
                    st.rerun()

            if st.session_state.editando == f"dates_{i}":
                nova_ideia = st.text_input("Ideia:", value=dts['ideia'], key=f"edit_date_ideia_{i}")
                novo_status = st.text_input("Status:", value=dts['status'], key=f"edit_date_status_{i}")
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    if st.button("Salvar Alteração", key=f"save_date_{i}"):
                        st.session_state.dados["dates"][i]['ideia'] = nova_ideia
                        st.session_state.dados["dates"][i]['status'] = novo_status
                        salvar_dados(st.session_state.dados)
                        st.session_state.editando = None
                        st.rerun()
                with c_s2:
                    if st.button("Cancelar", key=f"canc_date_{i}"):
                        st.session_state.editando = None
                        st.rerun()
