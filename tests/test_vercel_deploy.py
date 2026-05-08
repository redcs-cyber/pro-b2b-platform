import json
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree


def test_vercel_config_routes_all_traffic_to_python_entrypoint() -> None:
    config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))

    assert config["builds"][0]["src"] == "api/vercel_app.py"
    assert config["builds"][0]["use"] == "@vercel/python"
    assert config["routes"][0] == {"src": "/(.*)", "dest": "api/vercel_app.py"}
    assert config["env"]["PROB2B_MODE"] == "vercel"


def test_vercel_deploy_check_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/vercel_deploy_check.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Vercel deploy check passed" in result.stdout


def test_vercel_visual_asset_is_valid_svg() -> None:
    root = ElementTree.parse("api/static/assets/3d/vercel-deploy-pipeline.svg").getroot()
    assert root.tag.endswith("svg")
