@echo off
title Library Circulation and Digital Resource Management System - DBMS PBL
echo =====================================================================
echo Launching Library DBMS PBL Interactive Working Model...
echo =====================================================================
python -m streamlit run app.py --server.port=8501 --server.headless=false
pause
