# pconcat (Project Concatenator)

pconcat is a command-line tool designed to concatenate the contents of an entire project into a single output. Its primary purpose is to provide a comprehensive project overview to AI assistants, giving them all the context they need to help you with development tasks. Note that this project was mostly made using Claude 3.5 Sonnet.

## Main Features

- Generates a tree structure of your project directory
- Concatenates the contents of text files
- Outputs the entire project structure and contents in a format suitable for AI assistants
- Supports ignoring files and directories using .pconcatignore
- Flexible output options: clipboard, file, or shell
- Can generate a standard .pconcatignore file

## Why pconcat?

When working with AI assistants on development tasks, providing context is crucial. pconcat allows you to easily share your entire project structure and contents in a single, organized format. This gives AI assistants a comprehensive view of your project, enabling them to provide more accurate and context-aware assistance.

## Installation

1. Ensure you have Python 3.6 or later installed.
2. Clone this repository or download the `pconcat` script.
3. Make the script executable:
   ```
   chmod +x /path/to/pconcat
   ```
4. Move the script to a directory in your PATH, e.g.:
   ```
   sudo mv /path/to/pconcat /usr/local/bin/
   ```
5. Install the required Python libraries:
   ```
   pip install pyperclip
   ```

## Usage

Run `pconcat` in your project directory:

```
pconcat [options]
```

### Options

- `-f FILE`, `--file FILE`: Output to a file instead of clipboard
- `-s`, `--shell`: Print output to shell
- `-i`, `--init`: Create a standard .pconcatignore file

### Examples

1. Copy project contents to clipboard (default behavior):
   ```
   pconcat
   ```

2. Output to a file:
   ```
   pconcat -f project_overview.txt
   ```

3. Print to shell:
   ```
   pconcat -s
   ```

4. Create a standard .pconcatignore file:
   ```
   pconcat -i
   ```

## .pconcatignore

pconcat supports ignoring files and directories using a `.pconcatignore` file. This file works similarly to `.gitignore`. You can create a standard .pconcatignore file using the `-i` option.

Example .pconcatignore contents:

```
.git/**
node_modules/
*.log
build/
```

## Dependencies

- Python 3.6+
- pyperclip

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/Scezaquer/pconcat/issues) if you want to contribute.

## Author

Scezaquer - [@Scezaquer](https://github.com/Scezaquer)

Project Link: [https://github.com/Scezaquer/pconcat](https://github.com/Scezaquer/pconcat)
