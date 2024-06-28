#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import pyperclip
import fnmatch

DEFAULT_IGNORE_CONTENT = """# Version control
.git/**
.gitignore

# Project concatenator
.pconcatignore

# Node.js
node_modules/

# Python
__pycache__/
*.py[cod]
*.so

# Logs
*.log

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE specific files
.vscode/
.idea/
*.swp
*.swo

# Build directories
build/
dist/

# Environment files
.env
.venv
env/
venv/
"""

def create_ignore_file(root_dir):
    ignore_file_path = os.path.join(root_dir, '.pconcatignore')
    if os.path.exists(ignore_file_path):
        confirm = input(".pconcatignore already exists. Overwrite? (y/N): ").lower().strip()
        if confirm != 'y':
            print("Operation cancelled.")
            return

    with open(ignore_file_path, 'w') as f:
        f.write(DEFAULT_IGNORE_CONTENT)
    print(f".pconcatignore file created at {ignore_file_path}")

def parse_ignore_file(root_dir):
    ignore_patterns = []
    ignore_file = os.path.join(root_dir, '.pconcatignore')
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as f:
            ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ignore_patterns

def should_ignore(path, root_dir, ignore_patterns):
    relative_path = os.path.relpath(path, root_dir)
    path_parts = relative_path.split(os.sep)
    
    for pattern in ignore_patterns:
        if any(fnmatch.fnmatch(part, pattern) for part in path_parts):
            return True
        if fnmatch.fnmatch(relative_path, pattern):
            return True
    return False

def get_tree_structure(root_dir, ignore_patterns):
    ignore_arg = "|".join(ignore_patterns).replace("*", "")  # Remove asterisks for tree command
    tree = subprocess.check_output(["tree", "-L", "2", "-I", ignore_arg, root_dir]).decode("utf-8")
    return tree.strip()

def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False

def get_file_contents(root_dir, ignore_patterns):
    contents = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), root_dir, ignore_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, root_dir, ignore_patterns) and is_text_file(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                relative_path = os.path.relpath(file_path, root_dir)
                contents.append(f"\nContents of {relative_path}:\n{content}")
    return "\n".join(contents)

def pconcat(root_dir, output_file=None, print_to_shell=False):
    try:
        ignore_patterns = parse_ignore_file(root_dir)
        tree = get_tree_structure(root_dir, ignore_patterns)
        contents = get_file_contents(root_dir, ignore_patterns)
        result = f"{tree}\n{contents}"

        if print_to_shell:
            print(result)
        elif output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Project content has been written to {output_file}")
        else:
            pyperclip.copy(result)
            print("Project content has been copied to clipboard")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Project Concatenator")
    parser.add_argument("-f", "--file", help="Output to a file instead of clipboard")
    parser.add_argument("-s", "--shell", action="store_true", help="Print output to shell")
    parser.add_argument("-i", "--init", action="store_true", help="Create a standard .pconcatignore file")
    args = parser.parse_args()

    root_dir = os.getcwd()

    if args.init:
        create_ignore_file(root_dir)
    else:
        pconcat(root_dir, args.file, args.shell)

if __name__ == "__main__":
    main()