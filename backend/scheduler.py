from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import SessionLocal, Capsule
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz

# 🔔 Carrega variáveis do .env
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

tz = pytz.timezone("America/Sao_Paulo")  # Apenas para logs

def send_email(to_email: str, subject: str, body: str, html: bool = True) -> bool:
    """Envia email via SMTP"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html" if html else "plain"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email enviado para {to_email}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email para {to_email}: {e}")
        return False

def process_capsules():
    """Verifica cápsulas agendadas e envia emails"""
    db: Session = SessionLocal()
    now = datetime.now(pytz.UTC)

    # Janela de envio de ±30 segundos
    window_start = now - timedelta(seconds=30)
    window_end = now + timedelta(seconds=30)

    capsules = db.query(Capsule).filter(
        Capsule.send_date >= window_start,
        Capsule.send_date <= window_end,
        Capsule.sent_at.is_(None)
    ).all()

    if not capsules:
        print(f"⏱ Nenhuma cápsula para enviar em {now} UTC")
        db.close()
        return

    for capsule in capsules:
        email_body = f"""
        <p>Olá {capsule.recipient_name},</p>
        <p>{capsule.message}</p>
        <p>(Enviado por {capsule.email})</p>
        """
        if send_email(capsule.recipient_email,
                      f"Mensagem da Cápsula do Tempo de {capsule.name}",
                      email_body):
            # Atualiza sent_at para horário real de envio em UTC
            capsule.sent_at = datetime.now(pytz.UTC)
            db.add(capsule)
            db.commit()
            print(f"📬 Cápsula {capsule.id} enviada em {capsule.sent_at} UTC")

    db.close()

def start_scheduler():
    """Inicia o scheduler em background"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_capsules, "interval", seconds=30)  # roda a cada 30s para testes
    scheduler.start()
    print("⏰ Scheduler iniciado: verificando cápsulas a cada 30 segundos")
