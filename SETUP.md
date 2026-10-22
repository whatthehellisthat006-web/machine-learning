# Project setup

This repository contains the Guichet ML application and the completed Atelier 2 model-comparison practical work.

## Python environment

From the project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The Atelier 2 scripts and outputs are in `atelier2/`. Run its scripts from the `atelier2` folder, for example:

```powershell
cd .\atelier2
..\.venv\Scripts\Activate.ps1
python .\code\explorer.py
```

## Groq API key

The Atelier 2 classifier reads `GROQ_API_KEY` from the current PowerShell session. Do not put the key in source code, `.env`, or any file committed to Git. Set it for a session with:

```powershell
$secureKey = Read-Host "Groq API key" -AsSecureString
$env:GROQ_API_KEY = [System.Net.NetworkCredential]::new("", $secureKey).Password
Remove-Variable secureKey
```

The key is not included in this repository. Close the terminal when finished to clear the session variable.

## Files excluded from Git

`.gitignore` excludes the virtual environment, Python/test caches, and `.env` files (except the blank `.env.example` template).
