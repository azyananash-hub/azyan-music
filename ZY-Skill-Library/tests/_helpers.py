"""Helper untuk memuat script skill dari path file tanpa mengubah sys.path permanen."""

import importlib.util
import os
import sys

LIBRARY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(LIBRARY_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)


def load_module(name: str, relative_path: str):
    """Muat modul dari path relatif terhadap root library."""
    path = os.path.join(LIBRARY_ROOT, relative_path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # dataclass butuh modul terdaftar di sys.modules saat diproses
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SHORT_CIRCUIT = "skills/engineering/short-circuit-calculator/scripts/short_circuit.py"
FMEA = "skills/engineering/fmea-rpn-prioritizer/scripts/fmea_rpn.py"
TRADE_STATS = "skills/quantitative-trading/trade-statistics/scripts/trade_stats.py"
POSITION = "skills/quantitative-trading/position-size-calculator/scripts/position_size.py"
SM2 = "skills/japanese-education/srs-sm2-scheduler/scripts/sm2.py"
RENDER = "skills/clipacanvas/render-link-builder/scripts/build_render_link.py"
RISK_SCAN = "skills/governance/third-party-skill-audit/scripts/scan_skill_risk.py"
SECRET_SCAN = "skills/software-development/secret-leak-scan/scripts/scan_secrets.py"
