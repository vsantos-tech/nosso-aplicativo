# =============================================================
# ABA 1: RECADO (COM UPLOAD DA GALERIA + GOOGLE SHEETS)
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
        ultimo_recado = df_recados.iloc[-1]
        autor_rec = ultimo_recado.get("Autor", "Nós")
        st.info(f"### {ultimo_recado.get('Mensagem', '')}")
        st.caption(f"🕒 **Enviado por {autor_rec} em:** {ultimo_recado.get('Data_Hora', '')}")
        
        url_ou_base64 = ultimo_recado.get("Imagem_URL")
        if pd.notna(url_ou_base64) and str(url_ou_base64).strip():
            img_obj = carregar_imagem_correta(url_ou_base64)
            if img_obj:
                st.image(img_obj, width=280)

        if pd.notna(ultimo_recado.get("Resposta")) and str(ultimo_recado.get("Resposta")).strip():
            st.success(f"💬 **Resposta:** {ultimo_recado.get('Resposta')}")
            st.caption(f"🕒 **Respondido em:** {ultimo_recado.get('Data_Resposta', '')}")

    st.markdown("---")

    st.subheader("✍️ Publicar Novo Lembrete")
    quem_manda = "Vitória" if st.session_state.usuario_atual == "vitoria" else "Larissa"
    novo_recado_txt = st.text_area(f"Escreva seu lembrete ({quem_manda}):", key="input_lembrete_geral")
    
    # OPÇÃO DE ANEXAR IMAGEM DA GALERIA OU POR LINK
    tab_img1, tab_img2 = st.tabs(["📁 Anexar da Galeria / Dispositivo", "🔗 Link da Imagem"])
    up_img_direto, url_img_direto = None, ""
    
    with tab_img1:
        up_img_direto = st.file_uploader("Escolha uma imagem da sua galeria:", type=["png", "jpg", "jpeg", "webp"], key="up_img_direto")
    with tab_img2:
        url_img_direto = st.text_input("Cole a URL/Link da imagem:", key="url_img_direto")

    if st.button("💌 Publicar Lembrete", key="btn_pub_lembrete_geral"):
        imagem_para_salvar = ""

        # Se enviou arquivo da galeria, converte para salvar na planilha
        if up_img_direto is not None:
            bytes_data = up_img_direto.getvalue()
            b64_str = base64.b64encode(bytes_data).decode()
            mime_type = up_img_direto.type
            imagem_para_salvar = f"data:{mime_type};base64,{b64_str}"
        elif url_img_direto.strip():
            imagem_para_salvar = url_img_direto.strip()

        if novo_recado_txt.strip() or imagem_para_salvar:
            novo_dado = pd.DataFrame([{
                "Autor": quem_manda,
                "Mensagem": novo_recado_txt,
                "Imagem_URL": imagem_para_salvar,
                "Data_Hora": formatar_data_hora(),
                "Resposta": "",
                "Data_Resposta": ""
            }])
            df_atualizado = pd.concat([df_recados, novo_dado], ignore_index=True)
            conn.update(worksheet="Recados", data=df_atualizado)
            st.cache_data.clear()
            st.toast("Lembrete publicado e foto salva para sempre! 💖")
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
                
                # Exibe a foto no histórico se houver
                url_hist = row.get("Imagem_URL")
                if pd.notna(url_hist) and str(url_hist).strip():
                    img_h = carregar_imagem_correta(url_hist)
                    if img_h:
                        st.image(img_h, width=180)

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
