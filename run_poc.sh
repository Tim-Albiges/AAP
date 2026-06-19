#!/bin/bash

echo "=========================================================="
echo "    Initialising AAP Local Ecosystem Environment          "
echo "=========================================================="

if [ ! -d "venv" ]; then
    echo "[1/3] Creating Python Virtual Environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# THE FIX: Upgrade core packaging tools before installing requirements
echo "Updating pip and build tools..."
python3 -m pip install --upgrade pip setuptools wheel

echo "[2/3] Installing Enterprise dependencies..."
pip install -r Enterprise/Platform/requirements.txt

echo "[3/3] Launching FastAPI Enterprise Core..."
echo "----------------------------------------------------------"
echo "👉 1. Open Chrome/Edge extensions: chrome://extensions"
echo "👉 2. Enable 'Developer Mode'"
echo "👉 3. Click 'Load unpacked' -> select 'Open_Source_Engine'"
echo "👉 4. Navigate to: http://127.0.0.1:8000/demo/aap"
echo "=========================================================="

cd Enterprise/Platform
uvicorn main:app --reload --host 0.0.0.0 --port 8000