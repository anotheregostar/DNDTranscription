@echo off
setlocal
chcp 65001 >nul

:: =============================================
:: 📤 EXPORT GLOSSARY TO EXCEL + IGNORE LIST
:: ---------------------------------------------
:: Drag and drop your glossary_config.json file
:: onto this script to generate:
::
::   ✅ glossary_config_wide.xlsx — for easy editing
::   ✅ ignore_list.txt           — for review or reimport
::
:: Output will be saved in the same folder as this script.
:: =============================================

set "SCRIPT_DIR=Transcription Scripts"
echo 🔄 Exporting glossary_config.json to Excel and ignore list...
python "%SCRIPT_DIR%\\export_glossary_to_excel.py" "%~1"
pause