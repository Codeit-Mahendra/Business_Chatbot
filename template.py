

import os
from pathlib import Path

# Define folders and files
folders = ["src", "research"]
files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    "research/trials.ipynb",
    ".env",
    "setup.py",
    "app.py",
    "requirements.txt"
]

# Create folders
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Create files
for file in files:
    Path(file).touch()

print("Directory and files created successfully!")