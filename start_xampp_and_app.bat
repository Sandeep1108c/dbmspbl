@echo off
title Library DBMS PBL - XAMPP MySQL and App Launcher
echo =====================================================================
echo Starting XAMPP MySQL and Apache Services...
echo =====================================================================
start "" "D:\xampp\mysql\bin\mysqld.exe" --defaults-file="D:\xampp\mysql\bin\my.ini" --standalone
start "" "D:\xampp\apache\bin\httpd.exe"
timeout /t 2 /nobreak >nul
echo =====================================================================
echo Launching Streamlit Web Application on http://localhost:8501...
echo phpMyAdmin available at: http://localhost/phpmyadmin/
echo =====================================================================
python -m streamlit run app.py
pause
