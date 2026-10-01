from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.manager.project_manager import prepare_project

project_id, project_path = prepare_project(
    Path("C:\\Users\\pc\\Desktop\\zipdetest2222.zip")
)

print(project_id)
print(project_path)