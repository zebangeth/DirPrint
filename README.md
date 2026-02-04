# Directory Print - DirPrint

**Simplify Code Sharing with LLMs by Exporting Directory Structure and File Contents**

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/dirprint?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREEN&right_color=BLACK&left_text=PyPI+Downloads)](https://pepy.tech/projects/dirprint)

DirPrint is a command-line tool that streamlines sharing your project's directory structure and file contents with LLMs (like ChatGPT, Claude, etc.). By providing comprehensive context about your codebase, DirPrint enhances LLMs' ability to assist you in debugging and development tasks.

## Features

- **Visual Directory Tree:** Get a clear, hierarchical representation of your project's structure.
- **File Contents Display:** View file contents within the tree, formatted in markdown code blocks.
- **File Export:** Save the output to a file for easy sharing and reference.
- **Flexible Content Management:**
  - **Ignore Mode:** Completely hide specified files/directories from the output.
  - **Omit Mode:** Show files/directories in the directory structure but hide their contents for brevity.
  - **Glob Support:** Use standard globs (e.g., `*.pyc`, `test_*.js`) for flexible matching.
  - **GitIgnore Integration:** Automatically respects `.gitignore` rules (unless disabled).
  - **Strict Matching:** Enable exact matching for file/directory names by wrapping the pattern in carets (^).
- **Optional Line Count Analysis:** When enabled, DirPrint calculates and displays the number of lines for each file and directory.

## Installation

From source:

```bash
git clone https://github.com/zebangeth/DirPrint.git
cd DirPrint
python setup.py install
```

Via pip:

```bash
pip install DirPrint
```

or

```bash
pip install DirPrint==0.3.0
```

## Usage

Basic command structure:

```bash
dir_print [options] <directory_path>
```

### Options

- `--export`, `-E` : Save output to a specified file.
- `--ignore`, `-I` : Patterns to completely hide (e.g., `__pycache__`, `.git`, `node_modules`).
- `--omit`, `-O` : Patterns to show in the structure but hide their contents.
- `--no-gitignore` : Do not automatically load patterns from `.gitignore`.
- `--show-omitted-structure`, `--sos` : Show structure of omitted directories.
- `--line-count`, `-lc` : Enable display of line counts and percentages for files/directories.

### Strict Matching with Carets (^)

By default, patterns are matched partially (i.e., a pattern will match any file or directory that contains it). To enable strict (exact) matching, wrap the pattern in carets. This applies to both ignore and omit modes. For example:

- **Partial matching (default):**

  ```bash
  dir_print MindPlug -I doc .md build
  ```

  In this case, any file or directory name that _contains_ "build" (such as `build_check.py` or `build.py`) will be ignored.

- **Strict matching:**

  ```bash
  dir_print MindPlug -I doc .md ^build^
  ```

  With strict matching, only an entry whose name is exactly `build` will be ignored.  
  **Note:** Depending on your shell, you might need to escape carets (^) so that they are passed as part of the argument.

### Examples

Suppose you have a project directory structure like this:

```
my-project/
├── src/
│   ├── main.py              # 50 lines
│   ├── utils.py             # 30 lines
│   ├── config.json          # 20 lines
│   └── tests/
│       ├── test_main.py     # 20 lines
│       └── test_utils.py    # 30 lines
└── README.md                # 50 lines
```

1. **Basic usage** - Print everything:

   ```bash
   dir_print src
   ```

2. **Using ignore** - Hide files or directories containing "test":

   ```bash
   dir_print src -I test
   ```

   This will ignore any file or directory with "test" in its name.

3. **Using omit (partial matching)** - Show in the structure but hide contents:

   ```bash
   dir_print src -O config
   ```

   In this case, both the directory `config/` and the file `config.json` will be omitted because the pattern `config` matches any entry containing that substring:

   ```
   src/
   ├── main.js
   ├── utils.js
   ├── [omitted] config/
   ├── [omitted] config.json
   └── tests/
       ├── main.test.js
       └── utils.test.js

   [Contents of files shown except for entries matching "config"...]
   ```

4. **Using strict matching with carets** - Match only the exact name:

   ```bash
   dir_print src -O ^config^
   ```

   Here, only an entry whose name is exactly `config` (such as the `config/` directory) will be omitted. The file `config.json` will not be omitted because its name does not exactly equal `config`.
   **Note:** You may need to escape carets depending on your shell.

5. **Showing omitted structure** - View the internal structure of omitted items:

   ```bash
   dir_print src -O ^config^ --sos
   ```

6. **Enable line count analysis** - Print structure with line counts and percentages:

   ```bash
   dir_print src --line-count
   ```

   The output might look like this:

   ```plaintext
   src/ (150 lines, 100%)
   ├── main.py (50 lines, 33.3%)
   ├── utils.py (30 lines, 20.0%)
   ├── config.json (20 lines, 13.3%)
   └── tests/ (50 lines, 33.3%)
       ├── test_main.py (20 lines, 13.3%)
       └── test_utils.py (30 lines, 20.0%)
   ```

7. **Combined usage** - Multiple patterns, export, and line count analysis:

   ```bash
   dir_print src -I node_modules -O ^config^ test -E output.txt --sos --line-count
   ```

   In this example:

   - `node_modules` is ignored using partial matching.
   - `^config^` is strictly omitted (exact match only) so only an entry named exactly `config` is affected.
   - `test` is omitted using partial matching.
   - The `--line-count` flag enables line count statistics for non-ignored and non-omitted entries.

### Notes

- **Partial Matching:** By default, a pattern matches if it is a substring of the file or directory name (e.g., `test` matches `testing.js` or `tests/`).

- **Glob Matching:** Standard shell-style wildcards are supported (e.g., `*.log` matches `error.log`, `test_*.py` matches `test_main.py`).

- **Strict Matching:** Wrap a pattern in carets (e.g., `^build^`) to enable exact matching. This ensures the pattern only matches when the file or directory name is an exact match.

- Ignore patterns take precedence over omit patterns when they overlap.
- The `--sos` flag only affects directories marked for omission.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Inspired by the simplicity and utility of the `tree` command in Unix-like operating systems.
- Built with GitHub Copilot, GPT-4-0125-preview, and Claude 3.5 Sonnet.

## About the Author

DirPrint was created by `zebang.eth`, a developer passionate about making development and debugging processes smoother and more intuitive.
