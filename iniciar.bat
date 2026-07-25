@echo off
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Iniciando YT Download...
streamlit run app.py
pause
