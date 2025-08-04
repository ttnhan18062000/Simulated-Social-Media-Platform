import os
from pathlib import Path
import fnmatch

# Try to parse .gitignore if available
def parse_gitignore(gitignore_path):
    ignore_patterns = []
    if gitignore_path.exists():
        with gitignore_path.open() as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                ignore_patterns.append(line)
    return ignore_patterns


def is_ignored(path, ignore_patterns, base_dir):
    rel_path = path.relative_to(base_dir)
    rel_path_str = str(rel_path)

    for pattern in ignore_patterns:
        # Normalize trailing slashes
        if pattern.endswith("/"):
            pattern = pattern.rstrip("/")
        # Check exact matches and directory matches
        if fnmatch.fnmatch(rel_path_str, pattern) or any(
            part in pattern for part in rel_path.parts
        ):
            return True
    return False


def scan_repo(root, ignore_patterns):
    structure = []
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if path.name.startswith(".") or path.name in ["__pycache__", ".DS_Store"]:
            continue
        if is_ignored(path, ignore_patterns, root):
            continue
        if path.suffix.lower() in [".py", ".ts", ".tsx", ".js", ".jsx"]:
            rel_path = path.relative_to(root)
            structure.append(str(rel_path))
    return structure


def generate_repo_structure(root):
    gitignore_path = root.parent / ".gitignore"
    ignore_patterns = parse_gitignore(gitignore_path)

    files = scan_repo(root, ignore_patterns)
    lines = "\n".join(f"- {file}" for file in sorted(files))
    return "# Repo Structure\n\n" + lines


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent  # repo/src/
    output = generate_repo_structure(repo_root)
    output_path = repo_root / "repo_structure.md"
    with output_path.open("w") as f:
        f.write(output)
    print(f"Generated: {output_path}")
