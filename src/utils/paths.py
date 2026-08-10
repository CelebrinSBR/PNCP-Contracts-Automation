import sys
from pathlib import Path

# Verifica se o código está rodando compilado (PyInstaller) ou em desenvolvimento (.py)
if getattr(sys, 'frozen', False):
    # Se for .exe, a raiz do projeto é a pasta onde o .exe está salvo
    PROJECT_ROOT = Path(sys.executable).parent
else:
    # Se for código fonte, usa a lógica original do __file__
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

SRC_PATH = PROJECT_ROOT / "src"

DATA_PATH = PROJECT_ROOT / "data"
DATABASE_DIR = DATA_PATH / "database"
DATABASE_PATH = DATABASE_DIR / "controle_notificacoes.db"

DRIVERS_PATH = PROJECT_ROOT / "drivers"
DRIVER_PATH = DRIVERS_PATH / "chromedriver.exe"

WHATSAPP_SESSION_PATH = DATABASE_DIR / "whatsapp_profile"