import streamlit as st
from github import Github
import json
from datetime import datetime, timedelta, timezone
import base64
from PIL import Image, ImageOps
import io
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Nosso Aplicativo 💗", page_icon="💗", layout="centered")

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
        .stApp {{
            {bg_style}
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        
        /* Força a cor do texto geral para escuro */
        h1, h2, h3, p, span, div {{ 
            color: #4A1228 !important; 
        }}
        
        /* Correção para não misturar a cor da fonte nas caixas de digitação */
        .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] {{
            color: #4A1228 !important;
            background-color: #FFFFFF !important;
            -webkit-text-fill-color: #4A1228 !important;
            border-radius: 8px !important;
        }}
        
        .stButton>button {{ 
            background: linear-gradient(90deg, #E65C83 0%, #F07865 100%); 
            color: white !important; 
            border-radius: 10px; 
            border: none; 
            font-weight: bold; 
        }}
        
        /* Estilo dos Cards (Destaque e Histórico) */
        .historico-card, .destaque-card {{ 
            background-color: rgba(255, 255, 255, 0.95); 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 10px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }}
        .historico-card {{
            border-left: 5px solid #E65C83; 
        }}
        .destaque-card {{
            border-left: 5px solid #FFD700; /* Dourado apenas para o destaque de hoje */
        }}
        
        /* Garante que o texto dentro das caixas seja escuro */
        .historico-card b, .historico-card p, .historico-card small, .historico-card a,
        .destaque-card b, .destaque-card p, .destaque-card small, .destaque-card a {{
            color: #4A1228 !important;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

carregar_estilo_fundo()

# 2. FUNÇÕES DE DATA E IMAGEM
def obter_fuso_horario():
    return timezone(timedelta(hours=-3))

def obter_data_hora():
    return datetime.now(obter_fuso_horario()).strftime("%d/%m/%Y às %H:%M")

def obter_data_hoje():
    return datetime.now(obter_fuso_horario()).strftime("%d/%m/%Y")

def processar_imagem(uploaded_file):
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        # Corrige a foto de cabeça para baixo puxada da galeria (iPhone/Android)
        img = ImageOps.exif_transpose(img) 
        img.thumbnail((600, 600))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    return None

# 3. CONEXÃO COM O GITHUB
@st.cache_resource
def conectar_github():
    return Github(st.secrets["GITHUB_TOKEN"])

def ler_dados():
    try:
        g = conectar_github()
        repo = g.get_repo(st.secrets["GITHUB_REPO"])
        file_content = repo.get_contents("dados_app.json")
        return json.loads(file_content.decoded_content.decode())
    except Exception:
        return {"recados": [], "sentimentos": [], "musicas": [], "fotos": [], "datas": [], "comidas": [], "dates": []}

def salvar_dados(dados):
    try:
        g = conectar_github()
        repo = g.get_repo(st.secrets["GITHUB_REPO"])
        content_str = json.dumps(dados, indent=4)
        try:
            contents = repo.get_contents("dados_app.json")
            repo.update_file(contents.path, "Atualizando dados", content_str, contents.sha)
        except:
            repo.create_file("dados_app.json", "Criando banco de dados", content_str)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def deletar_item(categoria, index):
    st.session_state.dados[categoria].pop(index)
    salvar_dados(st.session_state.dados)
    st.rerun()

if "dados" not in st.session_state:
    st.session_state.dados = ler_dados()

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

# --- ABA 1: RECADOS (Com divisão de Destaques de Hoje e Histórico) ---
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
    tem_hoje = False
    tem_historico = False
    
    # Renderiza Destaques de Hoje
    for i, item in enumerate(st.session_state.dados["recados"]):
        if item['data'].startswith(hoje):
            if not tem_hoje:
                st.subheader("🌟 Destaques de Hoje")
                tem_hoje = True
            st.markdown(f"""
            <div class="destaque-card">
                <b>{item['autor']}</b> - <small>{item['data']}</small><br>
                <p style="margin-top: 10px;">{item['texto']}</p>
            </div>
            """, unsafe_allow_html=True)
            if item.get('foto'):
                st.image(item['foto'], use_container_width=True)
            if e_admin and st.button("🗑️ Excluir", key=f"del_recados_hoje_{i}"):
                deletar_item("recados", i)
    
    if tem_hoje:
        st.divider()
    
    # Renderiza Histórico
    for i, item in enumerate(st.session_state.dados["recados"]):
        if not item['data'].startswith(hoje):
            if not tem_historico:
                st.subheader("📜 Histórico")
                tem_historico = True
            st.markdown(f"""
            <div class="historico-card">
                <b>{item['autor']}</b> - <small>{item['data']}</small><br>
                <p style="margin-top: 10px;">{item['texto']}</p>
            </div>
            """, unsafe_allow_html=True)
            if item.get('foto'):
                st.image(item['foto'], use_container_width=True)
            if e_admin and st.button("🗑️ Excluir", key=f"del_recados_hist_{i}"):
                deletar_item("recados", i)
                
    if not tem_historico and not tem_hoje:
        st.write("Ainda não há recados.")

# --- ABA 2: SENTIMENTOS (Visual Feed Limpo) ---
with t2:
    st.header("💭 Como estamos hoje?")
    opcoes_sentimentos = ["Feliz 😊", "Ansiosa 😰", "Cansada 🥱", "Empolgada ✨", "Triste 😢", "Com Saudade ❤️", "Estressada 🤯"]
    sentimento_escolhido = st.multiselect("Selecione seus sentimentos:", opcoes_sentimentos)
    
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
        if e_admin and st.button("🗑️ Excluir", key=f"del_sentimentos_{i}"):
            deletar_item("sentimentos", i)

# --- ABA 3: MÚSICAS (Visual Feed Limpo) ---
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
        if e_admin and st.button("🗑️ Excluir", key=f"del_musicas_{i}"):
            deletar_item("musicas", i)

# --- ABA 4: FOTOS (Visual Feed Limpo) ---
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
        st.image(ft['foto'], use_container_width=True)
        if e_admin and st.button("🗑️ Excluir", key=f"del_fotos_{i}"):
            deletar_item("fotos", i)

# --- ABA 5: DATAS (Visual Feed Limpo) ---
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
        if e_admin and st.button("🗑️ Excluir", key=f"del_datas_{i}"):
            deletar_item("datas", i)

# --- ABA 6: COMIDAS (Visual Feed Limpo) ---
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
        st.markdown(f"<div class='historico-card'>🍕 <b>{cm['nome']}</b> ({cm['tipo']})<br><small>Adicionado por {cm['autor']} em {cm['data']}</small></div>", unsafe_allow_html=True)
        if e_admin and st.button("🗑️ Excluir", key=f"del_comidas_{i}"):
            deletar_item("comidas", i)

# --- ABA 7: DATES (Visual Feed Limpo) ---
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
        st.markdown(f"<div class='historico-card'>🥂 <b>{dts['ideia']}</b> - {dts['status']}<br><small>Adicionado por {dts['autor']} em {dts['data']}</small></div>", unsafe_allow_html=True)
        if e_admin and st.button("🗑️ Excluir", key=f"del_dates_{i}"):
            deletar_item("dates", i)
