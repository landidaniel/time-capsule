import streamlit as st
import requests
from datetime import datetime
from pydantic import BaseModel, EmailStr, ValidationError
import time as t
import pytz

st.title("📩 Cápsula do Tempo ⏳")

# Campos do remetente
name = st.text_input("Seu nome")
email = st.text_input("Seu email")

# Campos do destinatário
recipient_name = st.text_input("Nome do destinatário")
recipient_email = st.text_input("Email do destinatário")

# Data e hora livres
send_date = st.date_input("Data para receber a mensagem")
send_time = st.time_input("Hora para receber a mensagem")  # ⬅️ Agora pode escolher exato, tipo 13:34

# Mensagem
message = st.text_area("Mensagem para o futuro")

# Função para validar e-mails
def is_valid_email(email: str) -> bool:
    try:
        class EmailModel(BaseModel):
            email: EmailStr
        EmailModel(email=email)
        return True
    except ValidationError:
        return False

# Função para esperar backend ficar pronto
def wait_for_backend(url: str, retries: int = 10, delay: float = 1.0):
    for _ in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            t.sleep(delay)
    return False

backend_url = "http://backend:8000"

if st.button("Enviar cápsula"):
    if not all([name, email, recipient_name, recipient_email, message]):
        st.warning("⚠️ Preencha todos os campos!")
    elif not is_valid_email(email) or not is_valid_email(recipient_email):
        st.warning("⚠️ Digite emails válidos!")
    else:
        if not wait_for_backend(f"{backend_url}/"):
            st.error("❌ Backend não está disponível. Tente novamente mais tarde.")
        else:
            # Converte hora local para UTC
            tz_sp = pytz.timezone("America/Sao_Paulo")
            send_datetime_sp = datetime.combine(send_date, send_time)
            send_datetime_sp = tz_sp.localize(send_datetime_sp)
            send_datetime_utc = send_datetime_sp.astimezone(pytz.UTC)

            payload = {
                "name": name,
                "email": email,
                "recipient_name": recipient_name,
                "recipient_email": recipient_email,
                "send_date": send_datetime_utc.isoformat(),
                "message": message
            }

            try:
                response = requests.post(f"{backend_url}/capsule/", json=payload)
                if response.status_code == 200:
                    st.success("✅ Cápsula criada com sucesso!")
                else:
                    st.error(f"❌ Erro ao criar cápsula: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erro de conexão: {e}")
