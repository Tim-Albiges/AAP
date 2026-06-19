# Agentic Accessibility Protocol (AAP) - Proof of Concept

This repository contains the Minimum Viable Product (MVP) for the **Agentic Accessibility Protocol (AAP)**. 

The AAP is a foundational internet infrastructure project designed to bridge the communication gap between human intent, machine interfaces, and autonomous AI. It shifts digital accessibility from a reactive compliance checklist into a deterministic, universally understood machine-readable standard.

## 🏛️ The Three Pillars of the Ecosystem

This project is separated into three distinct, interconnected layers:

## 📂 Project Structure

app/
│
├── Open_Standard/
│   └── Vocabulary/
│       └── V1.jsonld                 # The globally hosted standard dictionary
│
├── Open_Source_Engine/               # The browser extension (Client Bridge)
│   ├── manifest.json
│   ├── content.js                    # Intercepts clicks, fetches patches, updates UI
│   └── test-harness/
│       └── app.html                  # Standard-compliant local test page
│
├── Enterprise/
│   └── Platform/                     # The FastAPI Backend
│       ├── main.py                   # Ingests telemetry, serves patches
│       ├── requirements.txt
│       └── fine-tune.py              # Compiles datasets for model alignment
│
├── run_poc.sh                        # Master automation script
└── README.md                         # This file

🚀 Getting Started (Windows 11 & WSL)
Prerequisites
Ensure your WSL environment is fully updated and contains the necessary Python build tools:

Bash
sudo apt update && sudo apt install -y python3-pip python3-venv build-essential
1. Initialise the Environment
Navigate to the root of the project in your WSL terminal and execute the master setup script. This script creates an isolated Python environment, installs the latest Enterprise dependencies, and boots the FastAPI server.

Bash
chmod +x run_poc.sh
./run_poc.sh
You should see the server successfully boot on http://0.0.0.0:8000.

2. Load the Open-Source Engine (Chrome/Edge)
Because this project runs inside WSL, you must explicitly point your Windows browser to the hidden Linux file path to load the extension.

Open Google Chrome or Microsoft Edge.

Navigate to chrome://extensions/ (or edge://extensions/).

Toggle Developer mode ON (top right corner).

Click Load unpacked (top left corner).

In the Windows file explorer pop-up, click the address bar, paste your direct WSL path, and hit Enter. It will look something like this:
\\wsl$\Ubuntu\home\your_username\app\Open_Source_Engine
(Ensure you replace your_username and Ubuntu with your specific WSL details).

Click Select Folder. The AAP Open-Source Engine card will appear.

3. Run the Demonstration
Open a new browser tab and navigate to the local test harness:
👉 http://localhost:8000/demo/aap

Refresh the page to ensure the extension is injected.

Open your browser's Developer Tools (F12) and look at the Console. You should see:
[AAP Engine] Content script successfully injected into the page.

Click the green "Process Secure Transaction" button.

🎯 Expected Outcomes
When the button is clicked, the following sequence occurs instantly:

Visual UI: A green success message (✅ Processed & Accessibility Patched!) dynamically appears next to the button.

Under the Hood (DOM): The extension intercepts the click, queries the Enterprise backend, and dynamically injects role="button" and aria-label="Submit Payment Confirmation" into the raw HTML <div>.

Under the Hood (Server): The FastAPI server logs the telemetry trace to a local mock_feature_store.json file, materialising the feature for future LLM training pipelines.

🛠️ Data Export for Model Alignment
To demonstrate how this ecosystem supports AI development (like Vibe Coding or Agentic AI guardrails), you can export the captured telemetry as "Golden Pairs" for LLM fine-tuning.

With the server running, navigate to:
http://localhost:8000/api/v1/export/golden-pairs

This returns a dataset mapping the raw, inaccessible HTML to the verified, AAP-compliant standard, ready to be fed into a machine learning pipeline.

That is an excellent question regarding the lifecycle management of a local development project. You want to make sure you know how to safely spin this down and bring it back up without breaking the ecosystem.

Here is exactly how to handle shutting down, restarting, and cleaning up your environment.

🛑 Shutting Down the Project
When you are finished testing or developing for the day, you need to stop the FastAPI backend from running in the background.

Open the VS Code terminal where your server is running.

Press Ctrl + C.

This sends an interrupt signal, gracefully shutting down the Uvicorn server and freeing up port 8000.

Note: You do not need to do anything to the Chrome extension. It will just sit dormant in your browser until the next time you boot the server.

Restarting the Project Later
Because we designed your run_poc.sh script to be intelligent, restarting the project after a reboot or a break is incredibly simple. You do not need to rebuild the environment.

Open your WSL terminal in the root app folder.

Run the master script again:

Bash
./run_poc.sh
The script will check for the venv folder, see that it already exists, skip the creation step, activate the environment, and instantly launch the server.

3. Deleting the venv (When and Why)
You do not need to delete the venv folder after every session. It is simply a local folder containing the specific Python packages required for the AAP project. Leaving it there means your project will boot up instantly the next time you need it.

However, there are two specific scenarios where you should delete it:

The "Nuke and Pave" Reset: If you accidentally install a broken package, or if Python gets confused (like the pydantic versioning clash), deleting the venv is the fastest way to fix it. It forces the system to build a fresh, clean environment from scratch.

Archiving for Space: If you are done with the project for a few months and want to reclaim some disk space (~100MB+), deleting the environment keeps your file system clean.

How to delete it safely:
Make sure the server is stopped (Ctrl + C), ensure your terminal is in the root app folder, and run:

Bash
rm -rf venv
If you ever want to run the project again after deleting the environment, simply execute ./run_poc.sh. The script will notice the folder is missing, automatically create a new one, download all the fresh packages from your requirements.txt, and start the server.

Chrome Browser extension
go to chrome extensions and add the extension from the manifest.json path.