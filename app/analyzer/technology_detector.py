from pathlib import Path


SERVICE_MARKERS = {
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "Pipfile",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "go.mod",
}


def detect_services(project_path: Path) -> list[dict]:
    """
    Detects directories that probably represent
    independent application services.

    Example:

        project/
        ├── frontend/
        │   └── package.json
        ├── backend/
        │   └── package.json
        └── auth-service/
            └── pom.xml

    Returns:

        [
            {
                "name": "frontend",
                "path": "frontend",
                "marker": "package.json"
            },
            ...
        ]
    """

    services = []

    for directory in project_path.iterdir():

        # We only care about directories
        if not directory.is_dir():
            continue

        # Ignore common technical directories
        if directory.name in {
            "node_modules",
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "target",
            "dist",
            "build",
        }:
            continue

        # Look for a technology marker
        marker_found = None

        for marker in SERVICE_MARKERS:

            if (directory / marker).exists():
                marker_found = marker
                break

        # If the directory contains a known
        # project marker, consider it a service
        if marker_found:

            services.append({
                "name": directory.name,
                "path": str(
                    directory.relative_to(project_path)
                ),
                "marker": marker_found
            })

    return services