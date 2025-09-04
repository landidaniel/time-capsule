import streamlit as st
import requests
from datetime import datetime

st.title("Cápsula do Tempo ⏳")

name = st.text_input("Seu nome")
email = st.text_input("Seu email")
send_date = st.date_input("Data para receber a mensagem")
message = st.text_area("Mensagem para o futuro")

if st.button("Enviar cápsula"):
    if not name or not email or not message:
        st.warning("Preencha todos os campos!")
    else:
        payload = {
            "name": name,
            "email": email,
            "send_date": datetime.combine(send_date, datetime.min.time()).isoformat(),
            "message": message
        }
        try:
            response = requests.post("http://time-capsule-backend:8000/capsule/", json=payload)
            if response.status_code == 200:
                st.success("Cápsula criada com sucesso!")
            else:
                st.error("Erro ao criar cápsula.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")