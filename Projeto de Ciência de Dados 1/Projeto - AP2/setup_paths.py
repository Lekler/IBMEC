import sys
from pathlib import Path

# Define o diretório base e o diretório backend
BASE_DIR = Path(__file__).resolve().parent
FRONT_DIR = BASE_DIR / 'frontend'
BACK_DIR = BASE_DIR / 'backend'

# Adiciona os diretórios ao sys.path
sys.path.append(str(BASE_DIR))
sys.path.append(str(FRONT_DIR))
sys.path.append(str(BACK_DIR))
