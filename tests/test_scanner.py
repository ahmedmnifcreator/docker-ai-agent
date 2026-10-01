from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.analyzer.project_scanner import scan_project


project_path = Path("workspace/159bb7a2-0d33-44ad-bf37-380e4e1dec73")

result = scan_project(project_path)

print(result)