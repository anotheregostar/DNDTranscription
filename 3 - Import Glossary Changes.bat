@echo off
setlocal
chcp 65001 >nul

:: =============================================
:: 📥 IMPORT GLOSSARY FROM EXCEL
:: ---------------------------------------------
:: Drag and drop your edited glossary_config_wide.xlsx
:: onto this script to rebuild:
::
::   ✅ glossary_config.json — with compact, campaign-aware structure
::
:: It will also reimport ignore_list.txt if present.
:: Output will overwrite the current glossary_config.json.
:: =============================================

set "SCRIPT_DIR=Transcription Scripts"
echo 🔄 Importing glossary_config_wide.xlsx into glossary_config.json...
python "%SCRIPT_DIR%\\import_glossary_from_excel.py" "%~1" ignore_list.txt
pause