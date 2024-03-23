# DirDive

**Simplify Your Code Sharing with LLMs by Exporting Directory Structure and File Contents**

DirDive is a command-line tool that simplifies the process of sharing of your project's directory structure and file contents, making it ideal for collaboration with LLMs (like ChatGPT, Claude, etc.). By allowing you to effortlessly share your codebase with LLMs, DirDive enhances their ability to assist you in debugging and building your projects by providing a comprehensive context.

## Features

- **Comprehensive Directory Tree:** Get a visual tree representation of your project's directory structure.
- **File Contents Display:** Easily view the contents of each file within the directory tree, enclosed in markdown code blocks for easy copying.
- **Customizable Ignoring:** Skip over files or directories you don't need with simple ignore patterns.
- **Output to File:** Option to save the directory structure and contents to a file for easy sharing or future reference.

## Usage

To use DirDive, simply navigate to your project directory and run:

```bash
dir_dive [options] <directory_path>
```

#### Options

- `-I`, `--ignore` : Patterns to ignore (e.g., `__pycache__`, `.git`, `node_modules`)
- `-o`, `--output` : Specify an output file for saving the directory structure and contents.

#### Example

To print the structure and content of the `src` directory while ignoring `.git` directories and saving the output to `output.txt`, run:

```bash
dir_dive src -o output.txt -I .json node_modules
```

## Installation

You can install DirDive directly from the source. Clone this repository and run the installation script:

```bash
git clone https://github.com/zebangeth/DirDive.git
cd DirDive
python setup.py install
```

Alternatively, you can install it using pip:

```bash
pip install dir_dive
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Inspired by the simplicity and utility of the `tree` command in Unix-like operating systems.
- Built with GitHub Copilot and GPT-4-0125-preview.

## About the Author

DirDive was created by `zebang.eth`, a developer passionate about making development and debugging processes smoother and more intuitive. 
