# DirDive

![DirDive Logo](path/to/logo/if/any.png)

**DirDive: Unveil Your Code's Depths with Ease**

DirDive is a command-line tool that simplifies the process of understanding and sharing your project's directory structure and file contents. Perfect for debugging, collaboration, or simply getting a bird's-eye view of your codebase, DirDive presents your project's anatomy in a clear, navigable, and shareable format.

## Features

- **Comprehensive Directory Tree:** Get a visual tree representation of your project's directory structure.
- **File Contents Display:** Easily view the contents of each file within the directory tree, enclosed in markdown code blocks for easy copying.
- **Customizable Ignoring:** Skip over files or directories you don't need with simple ignore patterns.
- **Output to File:** Save the directory structure and contents to a file for easy sharing or future reference.

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
dir_dive src -I .git -o output.txt
```

## Contributing

Any contributions you make are **greatly appreciated**.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Inspired by the simplicity and utility of the `tree` command in Unix-like operating systems.

## About the Author

DirDive was created by `zebang.eth`, a developer passionate about making development and debugging processes smoother and more intuitive. 
