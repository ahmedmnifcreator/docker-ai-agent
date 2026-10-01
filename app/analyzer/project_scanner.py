from pathlib import Path


# Fichiers qui nous intéressent particulièrement
IMPORTANT_FILES = {
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",

    "requirements.txt",
    "pyproject.toml",
    "Pipfile",

    "pom.xml",
    "build.gradle",
    "build.gradle.kts",

    "go.mod",

    "composer.json",

    "angular.json",

    "vite.config.js",
    "vite.config.ts",

    "next.config.js",
    "next.config.mjs",
    "next.config.ts",

    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",

    "README.md",
}


# Dossiers qu'on ne veut généralement pas scanner
IGNORED_DIRECTORIES = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "target",
    "dist",
    "build",
}


def scan_project(project_path: Path) -> dict:
    """
    Scans the project directory and collects
    structural information.
    """

    if not project_path.exists():
        raise FileNotFoundError(
            f"Project not found: {project_path}"
        )

    if not project_path.is_dir():
        raise ValueError(
            f"Project path is not a directory: {project_path}"
        )

    files = []
    directories = []
    important_files = []

    for path in project_path.rglob("*"):

        # Ignore unwanted directories
        if any(
            ignored in path.parts
            for ignored in IGNORED_DIRECTORIES
        ):
            continue

        relative_path = path.relative_to(project_path)

        if path.is_dir():

            directories.append(str(relative_path))

        elif path.is_file():

            files.append(str(relative_path))

            if path.name in IMPORTANT_FILES:
                important_files.append(str(relative_path))

    return {
        "project_path": str(project_path),
        "files": files,
        "directories": directories,
        "important_files": important_files,
        "total_files": len(files),
        "total_directories": len(directories),
    }