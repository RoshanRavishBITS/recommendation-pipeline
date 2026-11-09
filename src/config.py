from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
FEATURES = DATA / "features"
ERRORS = DATA / "errors"
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"
SCREENSHOTS = REPORTS / "screenshots"

for path in (RAW, PROCESSED, FEATURES, ERRORS, MODELS, REPORTS, SCREENSHOTS):
    path.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
K = 5
TEST_FRACTION = 0.20
