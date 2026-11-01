import sys
from pathlib import Path

# Let the tests import the package from src/ without installing it.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
