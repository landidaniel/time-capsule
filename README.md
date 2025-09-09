# Time Capsule

Este projeto é uma cápsula do tempo que permite que usuários programem o envio de emails para si mesmos em uma data futura.

Baseado no vídeo da Codecon: [Um sênior contra um júnior com IA para criar uma API de cápsula do tempo em apenas 1 hora](https://www.youtube.com/watch?v=ad046g56LZk&ab_channel=Codecon)

## Estrutura do projeto

- `backend/` → Código Python da API (FastAPI, SQLAlchemy)
- `frontend/` → Interface em Streamlit
- `database/` → Scripts e dados do banco PostgreSQL

## Tecnologias

- Python 3.11  
- FastAPI  
- Streamlit  
- PostgreSQL  
- Docker / Docker Compose

## Como Rodar o Projeto

### 1. Clonar o repositório
git clone git@github.com:landidaniel/time-capsule.git  
cd time-capsule

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` baseado no exemplo `.env.example` e edite com suas credenciais do banco e email:

cp .env.example .env  
# depois abra o .env e coloque suas credenciais de banco e email

### 3. Subir os containers com Docker
docker-compose up --build

Isso vai criar containers para o backend, frontend e banco de dados.

### 4. Acessar as aplicações
- Frontend Streamlit: http://localhost:8501  
- Backend FastAPI (Swagger): http://localhost:8000/docs

### 5. Comandos úteis
- Rodar apenas backend: docker-compose up backend  
- Rodar apenas frontend: docker-compose up frontend  
- Parar todos os containers: docker-compose down  
- Reiniciar containers: docker-compose restart
