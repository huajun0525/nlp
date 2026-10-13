from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent

# 动态将 src 目录加入 Python 模块搜索路径，确保任何工作目录下均能无缝运行
src_dir = str(ROOT_DIR / "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
LOGS_DIR = ROOT_DIR / "logs"
MODELS_DIR = ROOT_DIR / "models"
PRE_TRAINED_DIR = ROOT_DIR / "pretrained"

SEQ_LEN = 128
BATCH_SIZE = 16
EMBEDDING_DIM = 128
HIDDEN_SIZE = 256
LEARNING_RATE = 1e-5
EPOCHS = 20