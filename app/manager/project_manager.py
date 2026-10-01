from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile, BadZipFile


WORKSPACE_DIR = Path("workspace")


def create_workspace() -> tuple[str, Path]:
    """
    Creates a unique workspace for one uploaded project.

    Returns:
        project_id: unique identifier
        project_path: path of the project's workspace
    """

    project_id = str(uuid4())
    project_path = WORKSPACE_DIR / project_id

    project_path.mkdir(parents=True, exist_ok=False)

    return project_id, project_path


def is_safe_path(base_path: Path, target_path: Path) -> bool:
    """
    Prevents ZIP path traversal attacks.

    Example of a dangerous path:
        ../../malicious_file
    """

    try:
        target_path.resolve().relative_to(base_path.resolve())
        return True
    except ValueError:
        return False


def extract_zip(zip_path: Path, destination: Path) -> None:
    """
    Safely extracts a ZIP file into the destination directory.
    """

    try:
        with ZipFile(zip_path, "r") as zip_file:

            for member in zip_file.infolist():

                target_path = destination / member.filename

                if not is_safe_path(destination, target_path):
                    raise ValueError(
                        f"Unsafe ZIP path detected: {member.filename}"
                    )

            zip_file.extractall(destination)

    except BadZipFile:
        raise ValueError("The uploaded file is not a valid ZIP archive.")


def prepare_project(zip_path: Path) -> tuple[str, Path]:
    """
    Main Project Manager function.

    Takes a ZIP file and prepares an isolated workspace.
    """

    if not zip_path.exists():
        raise FileNotFoundError("ZIP file not found.")

    if zip_path.suffix.lower() != ".zip":
        raise ValueError("Only ZIP files are supported.")

    project_id, project_path = create_workspace()

    try:
        extract_zip(zip_path, project_path)

    except Exception:
        # Cleanup workspace if extraction fails
        import shutil

        shutil.rmtree(project_path, ignore_errors=True)
        raise

    return project_id, project_path