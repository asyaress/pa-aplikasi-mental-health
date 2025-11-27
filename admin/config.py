import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

PASIEN_FILE = os.path.join(DATA_DIR, "pasien.json")
DOKTER_FILE = os.path.join(DATA_DIR, "dokter.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ITEM_FILE = os.path.join(DATA_DIR, "item_pertanyaan.json")
SET_FILE = os.path.join(DATA_DIR, "set_pertanyaan.json")
ROLE_FILE = os.path.join(DATA_DIR, "roles.json")

WINDOW_TITLE = "Dashboard"
WINDOW_SIZE = "1400x800"

SIDEBAR_WIDTH = 250
MAIN_BG = "#f5f5f5"
ROOT_BG = "#2d2d2d"
PRIMARY_COLOR = "#1e5a9e"