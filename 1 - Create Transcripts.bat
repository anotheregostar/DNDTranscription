@echo off
setlocal enabledelayedexpansion
set HF_HUB_DISABLE_SYMLINKS_WARNING=1
chcp 65001 >nul
:: Makes emoji appear in cmd
:: Activate WhisperX Conda environment
call conda activate whisperx

:: ================================================
:: WHISPERX D&D TRANSCRIPTION WORKFLOW
:: --------------------------------
:: 📂 Drag & Drop a folder onto this batch file.
:: It will:
:: 
:: 1. Detect the campaign name from the folder name
:: 2. Rename audio files using campaign/player mappings (config.json)
:: 3. Transcribe all .flac audio files using WhisperX
:: 4. Save output into /Transcripts/CharacterName/ folders
:: 5. Skip transcription if /Transcripts folder already exists
:: 6. Convert all WhisperX .json files into timestamped .tsv files
:: 7. Combine all TSVs into:
::     - ✅ Color-coded XLSX transcript
::     - ✅ Plain TXT + Obsidian-friendly Markdown
:: 8. Apply glossary corrections from glossary_config.json:
::     - Uses both global and campaign-specific terms
:: 9. Detect likely mistranscriptions and log anomalies
:: 10. Suggest new glossary terms with fuzzy matching
:: 11. Add YAML metadata headers to the final .txt and .md
:: 
:: 📁 Final files will appear inside the Transcripts folder.
:: ================================================

REM === INIT MESSAGE ===
echo.
echo ================================
echo   WhisperX DnD Transcription
echo   Initializing environment...
echo ================================
echo.

:: ================================
:: CONFIGURATION AND SETUP
:: ================================

:: Set config file path
set "CONFIG_FILE=config.json"
set "SCRIPT_DIR=Transcription Scripts"


:: Check if config.json exists, otherwise prompt user to create one
if not exist "%CONFIG_FILE%" (
    echo config.json not found. Creating a new one.
    echo "{\"campaigns\": {\"Campaign\": {\"discord_handle\": \"charactername\"}}, \"whisperx_model\": \"whisper-large\"}" > "%CONFIG_FILE%"
)

:: Load the model setting from config.json
for /f "tokens=2 delims=:," %%A in ('findstr /i "whisperx_model" "%CONFIG_FILE%"') do set "WHISPERX_MODEL=%%~A"
set "WHISPERX_MODEL=%WHISPERX_MODEL:~1,-1%"  :: Trim quotes

:: HuggingFace token (if needed) - Put your token (hf_xxxxxxx) after the = sign below
set HUGGING_FACE_HUB_TOKEN=

:: ================================
:: CHECKING FOLDER AND CAMPAIGN
:: ================================

:: ✅ Check if a folder was dragged
if "%~1"=="" (
    echo ❌ ERROR: No folder provided.
    echo Please drag and drop a folder containing audio files onto this script.
    pause
    exit /b
)

:: ✅ Strip trailing backslash if present
set "input_folder=%~1"
if "%input_folder:~-1%"=="\\" set "input_folder=%input_folder:~0,-1%"

:: ✅ Confirm folder exists
if not exist "%input_folder%" (
    echo ❌ ERROR: Folder does not exist: "%input_folder%"
    pause
    exit /b
)

:: ✅ Extract folder name and split into campaign/session
for %%A in ("%input_folder%") do set "folder_name=%%~nxA"
for /f "tokens=1,* delims= " %%a in ("!folder_name!") do (
    set "CAMPAIGN=%%a"
    set "SESSION_DATE=%%b"
)

:: ✅ Define output folder for final YAML and transcripts
set "output_root=%input_folder%\Transcripts"
set "FINAL_NAME=!CAMPAIGN! !SESSION_DATE! Final Transcript"

if not exist "!output_root!" mkdir "!output_root!"

:: ================================
:: CAMPAIGN SETUP (ADDED BASED ON config.json)
:: ================================

:: Detect campaign
for /f "delims=" %%C in ('python "%SCRIPT_DIR%\\detect_campaign.py" "%input_folder%"') do set "campaign_name=%%C"

if "%campaign_name%"=="NO_MATCH" (
    echo ❌ ERROR: Could not detect campaign name in folder name.
    pause
    exit /b
)

echo 📘 Campaign detected: %campaign_name%

:: 🔁 Rename audio files using campaign/player mapping
python "%SCRIPT_DIR%\\rename_files.py" "%input_folder%" "%campaign_name%"

:: ================================
:: Begin Transcription (Skip Option)
:: ================================

:: Check if user wants to skip WhisperX
if exist "!output_root!" (
    echo 📂 Output folder "!output_root!" already exists.
    set /p userchoice="❓ Do you want to skip WhisperX transcription and go straight to processing? (y/n): "
    if /i "!userchoice!"=="y" goto PROCESS_ONLY
)

:: Loop through all audio files
for %%F in ("%input_folder%\*.flac") do (

    set "input_file=%%F"
    set "file_name=%%~nF"
    set "character_folder=!output_root!\!file_name!"

    if not exist "!character_folder!" mkdir "!character_folder!"

    echo Running WhisperX on "!input_file!" using model: !WHISPERX_MODEL!...
    whisperx "!input_file!" --output_dir "!character_folder!" --language en --task transcribe --compute_type float32 --model !WHISPERX_MODEL!

	:: Find the output JSON file (ignoring pretty_*.json)
	set "json_file="
	for %%f in ("!character_folder!\*.json") do (
		set "filename=%%~nxf"
		echo !filename! | findstr /B /C:"pretty_" >nul
		if errorlevel 1 (
			set "json_file=%%f"
		)
	)

	if defined json_file (
		echo Creating TSV from "!json_file!"...
		python "%SCRIPT_DIR%\\convert_json_to_tsv.py" "!json_file!"

		:: Extract folder name to create output like pretty_MyFolder.json
		for %%A in ("!character_folder!") do set "folder_name=%%~nxA"
		set "pretty_json_file=!character_folder!\pretty_!folder_name!.json"

		echo Pretty-printing to "!pretty_json_file!"...
		python -m json.tool "!json_file!" > "!pretty_json_file!"
	) else (
		echo ❌ ERROR: No JSON found for "!input_file!"!
	)
)

:PROCESS_ONLY
echo ✅ Skipping transcription. Beginning JSON-to-TSV conversion...
echo. 
echo 📂 Looking for JSONs in: !output_root!

set "tsv_count=0"

:: 🧠 Convert JSON to TSV (per character)
for /D %%d in ("!output_root!\*") do (
    for %%f in ("%%d\*.json") do (
        echo 📄 Found JSON: %%f
        python "%SCRIPT_DIR%\\convert_json_to_tsv.py" "%%f"
        if exist "%%~dpnf.tsv" (
            echo ✅ TSV created: %%~dpnf.tsv
			echo.
            set /a tsv_count+=1
        ) else (
            echo ⚠️  No TSV created for: %%f
        )
    )
)

echo ✅ Total TSV files created: !tsv_count!
if "!tsv_count!"=="0" (
    echo ❌ No TSVs were created — aborting merge.
    pause
    exit /b
)

:: ================================
:: Combine TSVs
:: ================================

echo 📋 Combining all TSVs...
for %%I in ("%input_folder%") do set "folder_name=%%~nxI"
set "final_transcript_xlsx=%output_root%\%folder_name%_transcript.xlsx"
set "final_transcript_txt=%output_root%\%folder_name%_transcript.txt"


:: 🧩 Combine all TSVs into one XLSX + TXT
python "%SCRIPT_DIR%\\combine_tsvs_with_colors.py" "!output_root!" "!final_transcript_xlsx!" "!final_transcript_txt!"

echo.
echo ✅ Combined transcripts created!

:: ================================
:: Final Transcript Processing
:: ================================

:: 🧹 Run glossary corrections and anomaly suggestions

if not exist "glossary_config.json" (
    echo ❌ glossary_config.json not found. Cannot run transcript processing.
    pause
    exit /b
)

echo.
echo 🧠 Running final transcript cleanup and anomaly detection...
python "%SCRIPT_DIR%\\process_transcript.py" "!final_transcript_xlsx!"


:: 📎 Add YAML metadata to .txt and .md
echo.
echo Adding YAML headers to final transcript files...
for %%f in ("!output_root!\*20??-??-??_transcript_corrected.txt") do (
    python "%SCRIPT_DIR%\\add_yaml_header.py" "%%f"
)

echo.
echo ✅ Final processing complete. Check the Transcripts folder for:
echo • Corrected XLSX
echo • Plain TXT and Markdown
echo • Glossary suggestions - For easy editing drag glossary_config.json onto "2 - Export Glossary.bat"

pause