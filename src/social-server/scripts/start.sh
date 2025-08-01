@echo off

REM Create virtual environment if it doesn't exist
IF NOT EXIST .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Run the FastAPI app
echo Starting FastAPI server...
uvicorn server:app --host 0.0.0.0 --port 8000 --reload