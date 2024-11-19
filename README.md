# Directory Print - DirPrint

**Simplify Code Sharing with LLMs by Exporting Directory Structure and File Contents**

DirPrint is a command-line tool that streamlines sharing your project's directory structure and file contents with LLMs (like ChatGPT, Claude, etc.). By providing comprehensive context about your codebase, DirPrint enhances LLMs' ability to assist you in debugging and development tasks.

## Features

- **Visual Directory Tree:** Get a clear, hierarchical representation of your project's structure
- **File Contents Display:** View file contents within the tree, formatted in markdown code blocks
- **File Export:** Save the output to a file for easy sharing and reference
- **Flexible Content Management:**
  - **Ignore Mode:** Completely hide specified files/directories from the output
  - **Omit Mode:** Show files/directories in the directory structure but hide their contents for brevity

## Installation

From source:
```bash
git clone https://github.com/zebangeth/DirPrint.git
cd DirPrint
python setup.py install
```

Via pip:
```bash
pip install DirPrint==0.2.1
```

## Usage

Basic command structure:
```bash
dir_print [options] <directory_path>
```

### Options

- `-E`, `--export` : Save output to specified file
- `-I`, `--ignore` : Patterns to completely hide (e.g., `__pycache__`, `.git`)
- `-O`, `--omit` : Patterns to show in structure but hide contents
- `--sos`, `--show-omitted-structure` : Show structure of omitted directories

### Examples

Suppose you have a project directory structure like this:

```
my-project/
├── src/
│   ├── main.js
│   ├── utils.js
│   ├── vite-env.d.ts
│   ├── config/
│   │   ├── dev.js
│   │   └── prod.js
│   └── tests/
│       ├── main.test.js
│       └── utils.test.js
└── README.md
```
To print the structure and content of the src directory while ignoring the vite-env.d.ts file and the views directory, and saving the output to output.txt, run:

```bash
dir_print src -E output.txt -I vite views
```

Note that partial matching is supported. In this case, for vite-env.d.ts, you can simply write vite.


1. **Basic usage** - Print everything:
```bash
dir_print src
```

2. **Using ignore** - Hide test files:
```bash
dir_print src -I test
```
Output will not show any files/directories containing "test"

3. **Using omit** - Show but hide contents:
```bash
dir_print src -O config
```
Output:
```
src/
├── main.js
├── utils.js
├── [omitted] config/
└── tests/
    ├── main.test.js
    └── utils.test.js

[Contents of files shown except for config directory...]
```

4. **Showing omitted structure** - View internal structure of omitted items:
```bash
dir_print src -O config --sos
```
Output shows config directory's structure but still omits its contents.

5. **Combined usage** - Multiple patterns and export:
```bash
dir_print src -I node_modules -O "config" "test" -E output.txt --sos
```

### Notes
- Patterns support partial matching (e.g., 'test' matches 'testing.js', 'tests/')
- Ignore takes precedence over omit when patterns overlap
- The `--sos` flag only affects directories marked for omission

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Inspired by the simplicity and utility of the `tree` command in Unix-like operating systems.
- Built with GitHub Copilot, GPT-4-0125-preview, and Claude 3.5 Sonnet.

## About the Author

DirPrint was created by `zebang.eth`, a developer passionate about making development and debugging processes smoother and more intuitive. 
