# pconcat (Project Concatenator)

A command-line tool to concatenate project contents into a single output, made for sharing context with AI assistants.

## Features

- Directory tree structure generation
- Text file content concatenation
- Flexible output: clipboard, file, or shell
- `.pconcatignore` file support
- Command to generate standard `.pconcatignore`
- Single file reading support

## Installation

1. Install Python 3.6+
2. Clone repository
3. Make executable:
   ```bash
   chmod +x /path/to/pconcat
   ```
4. Add to PATH:
   ```bash
   sudo mv /path/to/pconcat /usr/local/bin/
   ```
5. Install dependencies:
   ```bash
   pip install pyperclip
   ```

## Usage

```bash
pconcat [options] [-t TARGET]
```

### Options

- `-t`, `--target`: Target directory/file (default: current directory)
- `-f`, `--file`: Output to file
- `-s`, `--shell`: Print to shell
- `-i`, `--init`: Create `.pconcatignore`
- `--no_filename`: Exclude filenames
- `--no_tree`: Exclude directory tree
- `--no_contents`: Exclude file contents

### Examples

```bash
# Copy to clipboard
pconcat

# Output to file
pconcat -f output.txt

# Print to shell
pconcat -s

# Create .pconcatignore
pconcat -i
```

## Dependencies

- Python 3.6+
- pyperclip

## License

MIT License

## Links

- [GitHub Repository](https://github.com/Scezaquer/pconcat)
- [Issues](https://github.com/Scezaquer/pconcat/issues)

## Author

Scezaquer - [@Scezaquer](https://github.com/Scezaquer)
