from pathlib import Path


def scan_repo(root):
    structure = []
    for path in Path(root).rglob("*"):
        if (
            path.is_file()
            and not path.name.startswith(".")
            and path.suffix in [".ts", ".js", ".tsx", ".py"]
        ):
            rel_path = path.relative_to(root)
            structure.append(str(rel_path))
    return structure


def generate_repo_structure(root):
    lines = scan_repo(root)
    return "\n".join(f"- {line}" for line in lines)


if __name__ == "__main__":
    repo_path = "./"  # Point to your repo
    output = generate_repo_structure(repo_path)
    with open("repo_structure.md", "w") as f:
        f.write("# Repo Structure\n\n" + output)
