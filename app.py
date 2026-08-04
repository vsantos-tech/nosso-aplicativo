import streamlit as st
from github import Github
import json
from datetime import datetime, timedelta, timezone
import base64
from PIL import Image
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
        
        .stButton>button {{ 
            background: linear-gradient(90deg, #E65C83 0%, #F07865 100%); 
            color: white !important; 
            border-radius: 10px; 
            border: none; 
            font-weight: bold; 
        }}
        
        /* Estilo dos Cards (Destaque e Histórico) com texto escuro garantido */
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
            border-left: 5px solid #FFD700; /* Dourado para o destaque do dia */
        }}
        
        /* Garante que o texto dentro das caixas seja escuro */
        .historico-card b, .historico-card p, .historico-card small,
        .destaque-card b, .destaque-card p, .destaque-card small {{
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

# --- FUNÇÃO AUXILIAR PARA RENDERIZAR ITENS ---
def renderizar_itens(categoria, render_func):
    tem_hoje = False
    tem_historico = False
    
    # Renderiza Destaques de Hoje
    for i, item in enumerate(st.session_state.dados[categoria]):
        if item['data'].startswith(hoje):
            if not tem_hoje:
                st.subheader("🌟 Destaques de Hoje")
                tem_hoje = True
            render_func(item, "destaque-card")
            if e_admin:
                if st.button("🗑️ Excluir", key=f"del_{categoria}_hoje_{i}"):
                    deletar_item(categoria, i)
    
    st.divider()
    
    # Renderiza Histórico (Antes de Hoje)
    for i, item in enumerate(st.session_state.dados[categoria]):
        if not item['data'].startswith(hoje):
            if not tem_historico:
                st.subheader("📜 Histórico")
                tem_historico = True
            render_func(item, "historico-card")
            if e_admin:
                if st.button("🗑️ Excluir", key=f"del_{categoria}_hist_{i}"):
                    deletar_item(categoria, i)
                    
    if not tem_historico:
        st.write("O histórico está vazio.")


# --- ABA 1: RECADOS ---
with t1:
    st.header("💌 Mural de Recados")
    texto_recado = st.text_area("Escreva seu recado:")
    foto_recado = st.file_uploader("Anexar foto (opcional)", type=["png", "jpg", "jpeg"], key="up_recado")
    
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
    def render_recado(rec, css_class):
        st.markdown(f"""
        <div class="{css_class}">
            <b>{rec['autor']}</b> - <small>{rec['data']}</small><br>
            <p style="margin-top: 10px;">{rec['texto']}</p>
        </div>
        """, unsafe_allow_html=True)
        if rec.get('foto'):
            st.image(rec['foto'], use_container_width=True)
            
    renderizar_itens("recados", render_recado)


# --- ABA 2: SENTIMENTOS ---
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
    def render_sentimento(sen, css_class):
        st.markdown(f"<div class='{css_class}'><b>{sen['autor']}</b> se sentiu: <b>{sen['sentimentos']}</b> <br><small>{sen['data']}</small></div>", unsafe_allow_html=True)
        
    renderizar_itens("sentimentos", render_sentimento)


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
    def render_musica(mus, css_class):
        link_str = f" - <a href='{mus['link']}' target='_blank'>Ouvir no Spotify</a>" if mus.get('link') else ""
        st.markdown(f"<div class='{css_class}'>🎵 <b>{mus['nome']}</b>{link_str}<br><small>Adicionado por {mus['autor']} em {mus['data']}</small></div>", unsafe_allow_html=True)
        
    renderizar_itens("musicas", render_musica)


# --- ABA 4: FOTOS ---
with t4:
    st.header("📸 Nosso Mural de Fotos")
    foto_mural = st.file_uploader("Escolha uma foto da galeria", type=["png", "jpg", "jpeg"], key="foto_mural")
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
    def render_foto(ft, css_class):
        st.markdown(f"<div class='{css_class}'><b>{ft['legenda']}</b><br><small>Por {ft['autor']} em {ft['data']}</small></div>", unsafe_allow_html=True)
        st.image(ft['foto'], use_container_width=True)
        
    renderizar_itens("fotos", render_foto)


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
                "data": obter_data_hora() # Usando "data" para manter o padrão da função de renderizar
            })
            if salvar_dados(st.session_state.dados):
                st.success("Data salva!")
                st.rerun()

    st.divider()
    def render_data(dt, css_class):
        st.markdown(f"<div class='{css_class}'>📅 <b>{dt['titulo']}</b> no dia <b>{dt['dia']}</b><br><small>Adicionado por {dt['autor']} em {dt['data']}</small></div>", unsafe_allow_html=True)
        
    renderizar_itens("datas", render_data)


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
    def render_comida(cm, css_class):
        st.markdown(f"<div class='{css_class}'>🍕 <b>{cm['nome']}</b> ({cm['tipo']})<br><small>Adicionado por {cm['autor']} em {cm['data']}</small></div>", unsafe_allow_html=True)
        
    renderizar_itens("comidas", render_comida)


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
    def render_date(dts, css_class):
        st.markdown(f"<div class='{css_class}'>🥂 <b>{dts['ideia']}</b> - {dts['status']}<br><small>Adicionado por {dts['autor']} em {dts['data']}</small></div>", unsafe_allow_html=True)
        
    renderizar_itens("dates", render_date)
