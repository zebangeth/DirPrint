# Directory Print - DirPrint

**Simplify Your Code Sharing with LLMs by Printing/Exporting Directory Structure and Within File Contents**

DirPrint is a command-line tool that simplifies the process of sharing of your project's directory structure and file contents, making it ideal for collaboration with LLMs (like ChatGPT, Claude, etc.). By allowing you to effortlessly share your codebase with LLMs, DirPrint enhances their ability to assist you in debugging and building your projects by providing them with comprehensive context.

## Features

- **Comprehensive Directory Tree:** Get a visual tree representation of your project's directory structure.
- **File Contents Display:** Easily view the contents of each file within the directory tree, enclosed in markdown code blocks for easy copying.
- **Customizable Ignoring:** Skip over files or directories you don't need with simple ignore patterns.
- **Output to File:** Option to save the directory structure and contents to a file for easy sharing or future reference.

## Usage

To use DirPrint, simply navigate to your project directory and run:

```bash
dir_print [options] <directory_path>
```

#### Options

- `-I`, `--ignore` : Patterns to ignore (e.g., `__pycache__`, `.git`, `node_modules`)
- `-o`, `--output` : Specify an output file for saving the directory structure and contents.

#### Example

Suppose you have a project directory structure like this:

```
my-project/
├── src/
│   ├── main.js
│   ├── utils.js
│   ├── vite-env.d.ts
│   └── views/
│       └── (other files in views directory)
├── tests/
│   └── test.js
└── README.md
```

To print the structure and content of the `src` directory while ignoring the `vite-env.d.ts` file and the `views` directory, and saving the output to `output.txt`, run:

```
dir_print src -o output.txt -I vite views
```

Note that partial matching is supported. In this case, for `vite-env.d.ts`, you can simply write `vite`.

The generated `output.txt` will contain:

```
src Directory Structure:
src/
├── main.js
└── utils.js

src/main.js:
```
console.log('Hello, world!');
```

src/utils.js:
```
export function greet(name) {
  return `Hello, ${name}!`;
}
```
```

Now you can easily share `output.txt` with an LLM, providing it with the necessary context about your project's structure and code.

## Installation

You can install DirPrint directly from the source. Clone this repository and run the installation script:

```bash
git clone https://github.com/zebangeth/DirPrint.git
cd DirPrint
python setup.py install
```

Alternatively, you can install it using pip:

```bash
pip install dir_print
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Inspired by the simplicity and utility of the `tree` command in Unix-like operating systems.
- Built with GitHub Copilot and GPT-4-0125-preview.

## About the Author

DirPrint was created by `zebang.eth`, a developer passionate about making development and debugging processes smoother and more intuitive. 
