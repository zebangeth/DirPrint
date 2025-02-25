import os
import sys
import argparse

# Mapping of file extensions to markdown language identifiers.
EXTENSION_LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.json': 'json',
    '.md': 'markdown',
    '.html': 'html',
    '.css': 'css',
    '.sh': 'shell',
    '.swift': 'swift',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.ini': 'ini',
    '.xml': 'xml',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.rb': 'ruby',
}

def pattern_matches(name, pattern):
    """
    Check if a given name matches a pattern.

    - If the pattern is surrounded by carets (^), perform a strict match (exact equality).
    - Otherwise, perform a partial match (substring check).
    """
    if pattern.startswith('^') and pattern.endswith('^'):
        return name == pattern[1:-1]
    else:
        return pattern in name

def print_dir_structure(startpath, ignore=[], omit=[], show_omitted_structure=False):
    def print_tree(path, prefix=""):
        # Get the contents of the directory
        entries = os.listdir(path)
        entries = sorted(entries)  # Sort entries alphabetically

        # Filter out ignored items
        entries = [e for e in entries if not any(pattern_matches(e, ig) for ig in ignore)]

        # Separate directories and files
        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

        # Process all entries
        for i, entry in enumerate(dirs + files):
            is_last = (i == len(dirs + files) - 1)
            is_dir = entry in dirs

            # Prepare the prefix for this entry
            if is_last:
                entry_prefix = prefix + "└── "
                new_prefix = prefix + "    "
            else:
                entry_prefix = prefix + "├── "
                new_prefix = prefix + "│   "

            # Check if entry should be omitted using strict/partial matching
            is_omitted = any(pattern_matches(entry, o) for o in omit)

            # Print the entry
            if is_dir:
                if is_omitted:
                    print(f"{entry_prefix}[omitted] {entry}/")
                    if show_omitted_structure:
                        print_tree(os.path.join(path, entry), new_prefix)
                else:
                    print(f"{entry_prefix}{entry}/")
                    print_tree(os.path.join(path, entry), new_prefix)
            else:
                if is_omitted:
                    print(f"{entry_prefix}[omitted] {entry}")
                else:
                    print(f"{entry_prefix}{entry}")

    # Start the recursive printing
    path = os.path.abspath(startpath)
    base = os.path.basename(path)
    print(f"{base}/")
    print_tree(path)
    print()

def print_file_contents(startpath, ignore=[], omit=[]):
    def process_directory(current_path):
        entries = os.listdir(current_path)
        entries = sorted(entries)
        entries = [e for e in entries if not any(pattern_matches(e, ig) for ig in ignore)]

        # Separate directories and files
        dirs = [e for e in entries if os.path.isdir(os.path.join(current_path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(current_path, e))]

        # Process directories first
        for d in dirs:
            dir_path = os.path.join(current_path, d)
            rel_path = os.path.relpath(dir_path, startpath)
            if any(pattern_matches(d, o) for o in omit):
                print(f'{rel_path}/:')
                print('[Directory contents omitted for brevity...]')
                print()
            else:
                process_directory(dir_path)

        # Process files after directories
        for f in files:
            if any(pattern_matches(f, ig) for ig in ignore):
                continue
            rel_path = os.path.relpath(os.path.join(current_path, f), startpath)
            if any(pattern_matches(f, o) for o in omit):
                print(f'{rel_path}:')
                print('[Content omitted for brevity...]')
                print()
            else:
                print(f'{rel_path}:')
                # Determine file type based on extension.
                _, ext = os.path.splitext(f)
                language = EXTENSION_LANGUAGE_MAP.get(ext.lower(), '')
                print(f'```{language}')
                try:
                    with open(os.path.join(current_path, f), 'r', encoding='utf-8') as file:
                        print(file.read())
                    print('```')
                except Exception as e:
                    print(f"Error reading file: {e}")
                print()

    process_directory(startpath)

def dir_print(path, ignore=[], omit=[], export=None, show_omitted_structure=False):
    """Main function to print directory structure and contents"""
    original_stdout = sys.stdout

    if export:
        with open(export, 'w', encoding='utf-8') as f:
            sys.stdout = f
            print(f'{os.path.basename(path)} Directory Structure and File Contents:\n')
            print(f'<{os.path.basename(path)}-Directory-Structure>\n')
            print_dir_structure(path, ignore, omit, show_omitted_structure)
            print(f'<{os.path.basename(path)}-Directory-Structure>\n')
            print(f'<{os.path.basename(path)}-File-Contents>\n')
            print_file_contents(path, ignore, omit)
            print(f'<{os.path.basename(path)}-File-Contents>\n')
            sys.stdout = original_stdout
    else:
        print(f'{os.path.basename(path)} Directory Structure:')
        print_dir_structure(path, ignore, omit, show_omitted_structure)
        print_file_contents(path, ignore, omit)

def main():
    parser = argparse.ArgumentParser(
        description='DirPrint: Print your directory structure and file contents. '
                    'The default behavior is partial matching (substring check). '
                    'Wrap a pattern in carets(^) (e.g., ^build^) to enable strict matching.'
    )
    parser.add_argument('path', type=str, help='Directory path to print')
    parser.add_argument('-I', '--ignore', type=str, nargs='*', default=[],
                        help='Patterns to completely hide (e.g., __pycache__, .git, node_modules)')
    parser.add_argument('-O', '--omit', type=str, nargs='*', default=[],
                        help='Patterns to show in structure but hide contents')
    parser.add_argument('-E', '--export', type=str,
                        help='Export output to file')
    parser.add_argument('--sos', '--show-omitted-structure',
                        dest='show_omitted_structure',
                        action='store_true',
                        help='Show structure of omitted directories')

    args = parser.parse_args()
    dir_print(args.path, args.ignore, args.omit, args.export, args.show_omitted_structure)

if __name__ == '__main__':
    main()
