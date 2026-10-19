# CyberBot Startup Guide

Use the commands below from the project root to set up the virtual environment, install dependencies, and run the app.

## 1) Open PowerShell in the project folder

```powershell
cd "c:\Users\Acer\Desktop\Dekstop\Imp\New folder (2)\CyberBot-main"
```

## 2) Create a virtual environment

```powershell
py -3 -m venv .venv
```

## 3) Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4) Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install scikit-learn Flask
```

## 5) Run the app

```powershell
python app.py
```

## 6) Open the app in your browser

Go to:

```text
http://127.0.0.1:5000/chat
```

## Optional: one-line setup command

```powershell
cd "c:\Users\Acer\Desktop\Dekstop\Imp\New folder (2)\CyberBot-main"; py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; python -m pip install scikit-learn Flask; python app.py
```

## Notes

- If `py` is not recognized, use `python` instead when available.
- If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again.
