from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "express_delivery_model.joblib"
FEATURES_PATH = ARTIFACTS_DIR / "features.json"

# Configurations
MODEL_VERSION = "1.0.0"
