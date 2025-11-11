# 🌾 AgroPredict FDSW 2025

**Plataforma de predicción frutícola** desarrollada para la Feria de Software 2025 — USM Viña del Mar.  
Analiza rendimiento, ROI y eficiencia hídrica en cultivos agrícolas mediante modelos predictivos y paneles visuales.

---

## 🚀 Tecnologías
- **Django 4.2** (Backend principal)
- **HTML + CSS + JS** (Frontend)
- **WhiteNoise** (Static serving)
- **PostgreSQL / SQLite** (Base de datos)
- **Railway** (Hosting y despliegue)
- **OpenAI API** (Asistente IA)

---

## ⚙️ Instalación local

```bash
git clone https://github.com/tecnologyman/AgroPredictFDSW.git
cd AgroPredictFDSW
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
cp .env.sample .env
python manage.py migrate
python manage.py runserver
