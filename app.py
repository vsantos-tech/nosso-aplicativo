import streamlit as st
from github import Github
import json
from datetime import datetime, timedelta, timezone
import base64
from PIL import Image
import io
import os

# 1. CONFIGURAÇÃO DA PÁGINA E IMAGEM DE FUNDO
st.set_page_config(page_title="Nosso Aplicativo 💗", page_icon="💗", layout="centered")

def carregar_estilo_fundo():
    bg_image_path = None
    # Procura se você tem a imagem de fundo salva no seu GitHub
    for ext in ["fundo.png", "fundo.jpg", "fundo.jpeg"]:
        if os.path.exists(ext):
            bg_image_path = ext
            break

    if bg_image_path:
        with open(bg_image_path, "rb") as f:
            bin_str = base64.b64encode(f.read()).decode()
        bg_style = f'background-image: url("data:image/png;base64,{bin_str}");'
    else:
        # Fundo rosa gradiente padrão caso não ache a imagem
        bg_style = "background: linear-gradient(135deg, #FFD1DC 0%, #FFB07C 50%, #E65C83 100%);"

    css = f"""
        <style>
        .stApp {{
            {bg_style}
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        h1, h2, h3, p {{ 
            color: #4A1228 !important; 
            font-weight: bold; 
            text-shadow: 1px 1px 3px rgba(255,255,255,0.7); 
        }}
        .stButton>button {{ 
            background: linear-gradient(90deg, #E65C83 0%, #F07865 100%); 
            color: white !important; 
            border-radius: 10px; 
            border: none; 
            font-weight: bold; 
        }}
        div[data-testid="stExpander"] {{ 
            background-color: rgba(255, 255, 255, 0.85); 
            border-radius: 10px; 
        }}
        .historico-card {{ 
            background-color: rgba(255, 255, 255, 0.9); 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 10px; 
            border-left: 5px solid #FF69B4; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

carregar_estilo_fundo()

# 2. FUNÇÕES DE DATA E IMAGEM
def obter_data_hora():
    fuso = timezone(timedelta(hours=-3))
    return datetime.now(fuso).strftime("%d/%m/%Y às %H:%M")

def processar_imagem(uploaded_file):
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img.thumbnail((600, 600)) # Reduz o tamanho para o app não travar
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    return None

# 3. CONEXÃO COM O GITHUB (SALVAMENTO PERMANENTE)
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

# 5. CABEÇALHO DO APP
col_topo1, col_topo2 = st.columns([3, 1])
with col_topo1:
    st.title("Nosso Aplicativo 💗")
    st.write(f"Logada como: **{st.session_state.usuario_atual}**")
with col_topo2:
    if st.button("Sair / Trocar", use_container_width=True):
        st.session_state.usuario_atual = None
        st.rerun()

# 6. AS 7 ABAS
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["💌 Recados", "💭 Sentimentos", "🎵 Músicas", "📸 Fotos", "📅 Datas", "🍕 Comidas", "🥂 Dates"])

# --- ABA 1: RECADOS ---
with t1:
    st.header("💌 Mural de Recados")
    texto_recado = st.text_area("Escreva seu recado:")
    foto_recado = st.file_uploader("Anexar foto da galeria (opcional)", type=["png", "jpg", "jpeg"])
    
    if st.button("Publicar Recado"):
        if texto_recado or foto_recado:
            img_b64 = processar_imagem(foto_recado)
            novo_recado = {
                "autor": st.session_state.usuario_atual,
                "texto": texto_recado,
                "foto": img_b64,
                "data": obter_data_hora()
            }
            st.session_state.dados["recados"].insert(0, novo_recado)
            if salvar_dados(st.session_state.dados):
                st.success("Recado salvo para sempre!")
                st.rerun()
    
    st.divider()
    st.subheader("📜 Histórico de Recados")
    for rec in st.session_state.dados["recados"]:
        st.markdown(f"""
        <div class="historico-card">
            <b>{rec['autor']}</b> - <small>{rec['data']}</small><br>
            <p style="margin-top: 10px;">{rec['texto']}</p>
        </div>
        """, unsafe_allow_html=True)
        if rec.get('foto'):
            st.image(rec['foto'], use_container_width=True)

# --- ABA 2: SENTIMENTOS ---
with t2:
    st.header("💭 Como estamos hoje?")
    opcoes_sentimentos = ["Feliz 😊", "Ansiosa 😰", "Cansada 🥱", "Empolgada ✨", "Triste 😢", "Com Saudade ❤️", "Estressada 🤯"]
    sentimento_escolhido = st.multiselect("Selecione seus sentimentos:", opcoes_sentimentos)
    
    if st.button("Salvar Sentimento"):
        if sentimento_escolhido:
            novo_sentimento = {
                "autor": st.session_state.usuario_atual,
                "sentimentos": ", ".join(sentimento_escolhido),
                "data": obter_data_hora()
            }
            st.session_state.dados["sentimentos"].insert(0, novo_sentimento)
            if salvar_dados(st.session_state.dados):
                st.success("Sentimento registrado!")
                st.rerun()

    st.divider()
    st.subheader("📜 Histórico de Sentimentos")
    for sen in st.session_state.dados["sentimentos"]:
        st.markdown(f"<div class='historico-card'><b>{sen['autor']}</b> se sentiu: <b>{sen['sentimentos']}</b> <br><small>{sen['data']}</small></div>", unsafe_allow_html=True)

# --- ABA 3: MÚSICAS ---
with t3:
    st.header("🎵 Nossas Músicas")
    nome_musica = st.text_input("Nome da Música e Artista:")
    link_musica = st.text_input("Link do Spotify (opcional):")
    
    if st.button("Adicionar Música"):
        if nome_musica:
            nova_musica = {
                "autor": st.session_state.usuario_atual,
                "nome": nome_musica,
                "link": link_musica,
                "data": obter_data_hora()
            }
            st.session_state.dados["musicas"].insert(0, nova_musica)
            if salvar_dados(st.session_state.dados):
                st.success("Música salva!")
                st.rerun()

    st.divider()
    st.subheader("📜 Histórico de Músicas")
    for mus in st.session_state.dados["musicas"]:
        link_str = f" - <a href='{mus['link']}' target='_blank'>Ouvir no Spotify</a>" if mus.get('link') else ""
        st.markdown(f"<div class='historico-card'>🎵 <b>{mus['nome']}</b>{link_str}<br><small>Adicionado por {mus['autor']} em {mus['data']}</small></div>", unsafe_allow_html=True)

# --- ABA 4: FOTOS ---
with t4:
    st.header("📸 Nosso Mural de Fotos")
    foto_mural = st.file_uploader("Escolha uma foto da galeria", type=["png", "jpg", "jpeg"], key="foto_mural")
    legenda = st.text_input("Legenda da foto:")
    
    if st.button("Adicionar ao Mural"):
        if foto_mural:
            img_b64 = processar_imagem(foto_mural)
            nova_foto = {
                "autor": st.session_state.usuario_atual,
                "legenda": legenda,
                "foto": img_b64,
                "data": obter_data_hora()
            }
            st.session_state.dados["fotos"].insert(0, nova_foto)
            if salvar_dados(st.session_state.dados):
                st.success("Foto adicionada ao mural!")
                st.rerun()

    st.divider()
    st.subheader("📜 Histórico de Fotos")
    for ft in st.session_state.dados["fotos"]:
        st.markdown(f"**{ft['legenda']}** (Por {ft['autor']} em {ft['data']})")
        st.image(ft['foto'], use_container_width=True)
        st.markdown("---")

# --- ABA 5: DATAS ---
with t5:
    st.header("📅 Datas Importantes")
    nome_data = st.text_input("O que vamos comemorar/lembrar?")
    dia_data = st.date_input("Escolha o dia:")
    
    if st.button("Salvar Data"):
        if nome_data:
            nova_data = {
                "autor": st.session_state.usuario_atual,
                "titulo": nome_data,
                "dia": dia_data.strftime("%d/%m/%Y"),
                "data_registro": obter_data_hora()
            }
            st.session_state.dados["datas"].insert(0, nova_data)
            if salvar_dados(st.session_state.dados):
                st.success("Data salva!")
                st.rerun()

    st.divider()
    st.subheader("📜 Histórico de Datas")
    for dt in st.session_state.dados["datas"]:
        st.markdown(f"<div class='historico-card'>📅 <b>{dt['titulo']}</b> no dia <b>{dt['dia']}</b><br><small>Adicionado por {dt['autor']} em {dt['data_registro']}</small></div>", unsafe_allow_html=True)

# --- ABA 6: COMIDAS ---
with t6:
    st.header("🍕 O que gostamos de comer")
    nome_comida = st.text_input("Nome da comida ou Restaurante:")
    tipo_comida = st.radio("Onde?", ["Fazer em Casa", "Comer Fora / Pedir"])
    
    if st.button("Salvar Comida"):
        if nome_comida:
            nova_comida = {
                "autor": st.session_state.usuario_atual,
                "nome": nome_comida,
                "tipo": tipo_comida,
                "data": obter_data_hora()
            }
            st.session_state.dados["comidas"].insert(0, nova_comida)
            if salvar_dados(st.session_state.dados):
                st.success("Comida salva!")
                st.rerun()

    st.divider()
    st.subheader("📜 Histórico de Comidas")
    for cm in st.session_state.dados["comidas"]:
        st.markdown(f"<div class='historico-card'>🍕 <b>{cm['nome']}</b> ({cm['tipo']})<br><small>Adicionado por {cm['autor']} em {cm['data']}</small></div>", unsafe_allow_html=True)

# --- ABA 7: DATES ---
with t7:
    st.header("🥂 Nossos Dates")
    ideia_date = st.text_input("Ideia de lugar ou date:")
    status_date = st.radio("Status:", ["Queremos ir/fazer", "Já fomos/fizemos e amamos!"])
    
    if st.button("Salvar Date"):
        if ideia_date:
            novo_date = {
                "autor": st.session_state.usuario_atual,
                "ideia": ideia_date,
                "status": status_date,
                "data": obter_data_hora()
            }
            st.session_state.dados["dates"].insert(0, novo_date)
            if salvar_dados(st.session_state.dados):
                st.success("Date salvo!")
                st.rerun()

    st.divider()
    st.subheader("📜 Histórico de Dates")
    for dts in st.session_state.dados["dates"]:
        st.markdown(f"<div class='historico-card'>🥂 <b>{dts['ideia']}</b> - {dts['status']}<br><small>Adicionado por {dts['autor']} em {dts['data']}</small></div>", unsafe_allow_html=True)
