#!/usr/bin/env python3

import os
import sys
import argparse
import pyperclip
import fnmatch

DEFAULT_IGNORE_CONTENT = """# Version control
.git/**
.gitignore

# Project concatenator
.pconcatignore

# Node.js
node_modules/**

# Python
__pycache__/**
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
.vscode/**
.idea/**
*.swp
*.swo

# Build directories
build/**

# Environment files
.env
.venv
env/**
venv/**
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
        if pattern.endswith('/**'):
            dir_pattern = pattern[:-3]
            if any(part == dir_pattern for part in path_parts):
                return True
        elif fnmatch.fnmatch(relative_path, pattern):
            return True
        elif any(fnmatch.fnmatch(part, pattern) for part in path_parts):
            return True
    return False


def generate_tree(root_dir, ignore_patterns, prefix="", is_last=True, max_depth=None):
    if max_depth is not None and max_depth < 0:
        return ""

    base_name = os.path.basename(root_dir)
    tree = prefix + ("└── " if is_last else "├── ") + base_name + "\n"

    entries = [e for e in os.scandir(root_dir) if not should_ignore(e.path, root_dir, ignore_patterns)]
    entries.sort(key=lambda e: e.name.lower())

    for i, entry in enumerate(entries):
        is_last_entry = i == len(entries) - 1
        new_prefix = prefix + ("    " if is_last else "│   ")

        if entry.is_dir():
            tree += generate_tree(entry.path, ignore_patterns, new_prefix, is_last_entry, max_depth - 1 if max_depth is not None else None)
        else:
            tree += new_prefix + ("└── " if is_last_entry else "├── ") + entry.name + "\n"

    return tree


def get_tree_structure(root_dir, ignore_patterns):
    return generate_tree(root_dir, ignore_patterns, max_depth=None)


def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False


def get_file_contents(root_dir, ignore_patterns, ignore_filename=False):
    contents = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), root_dir, ignore_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, root_dir, ignore_patterns) and is_text_file(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                relative_path = os.path.relpath(file_path, root_dir)
                contents.append(f"\nContents of {relative_path}:\n{content}" if not ignore_filename else content)
    return "\n".join(contents)


def pconcat(root_dir, output_file=None, print_to_shell=False, ignore_filename=False, ignore_tree=False, ignore_contents=False, is_dir=True):
    if is_dir:
        try:
            ignore_patterns = parse_ignore_file(root_dir)
            tree = get_tree_structure(root_dir, ignore_patterns) if not ignore_tree else ""
            contents = get_file_contents(root_dir, ignore_patterns, ignore_filename) if not ignore_contents else ""
            result = f"{tree}\n{contents}" if tree and contents else tree or contents

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
    else:
        try:
            with open(root_dir, 'r', encoding='utf-8') as f:
                content = f.read()
            if print_to_shell:
                print(content)
            elif output_file:
                with open(output_file, 'w', encoding='utf-8') as out:
                    out.write(content)
                print(f"File content has been written to {output_file}")
            else:
                pyperclip.copy(content)
                print("File content has been copied to clipboard")
            sys.exit(0)
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Project Concatenator")
    parser.add_argument("-t", "--target", help="Target directory to concatenate", default=os.getcwd())
    parser.add_argument("-f", "--file", help="Output to a file instead of clipboard")
    parser.add_argument("-s", "--shell", action="store_true", help="Print output to shell")
    parser.add_argument("-i", "--init", action="store_true", help="Create a standard .pconcatignore file")
    parser.add_argument("--no_filename", action="store_true", help="Do not include filename in output")
    parser.add_argument("--no_tree", action="store_true", help="Do not include directory tree in output")
    parser.add_argument("--no_contents", action="store_true", help="Do not include file contents in output")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.target)
    if os.path.isfile(root_dir):
        is_dir = False
    elif os.path.isdir(root_dir):
        is_dir = True
    else:
        print(f"Error: {root_dir} is not a valid file or directory")
        sys.exit(1)

    if args.init:
        create_ignore_file(root_dir)
    else:
        pconcat(root_dir, args.file, args.shell, args.no_filename, args.no_tree, args.no_contents, is_dir)


if __name__ == "__main__":
    main()
