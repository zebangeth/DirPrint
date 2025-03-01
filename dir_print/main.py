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

def calculate_line_counts(startpath, ignore=[], omit=[]):
    """
    Recursively calculates the number of lines for each file and aggregates them for directories.
    Files or directories matching any omit pattern are skipped (their count is 0 and not added to parents).
    Returns a dictionary mapping relative paths to line counts, and the total line count for startpath.
    """
    line_counts = {}
    def count_lines(current_path, rel_path):
        # For non-root entries, if the entry is omitted, skip counting.
        if rel_path != "." and any(pattern_matches(os.path.basename(current_path), o) for o in omit):
            line_counts[rel_path] = 0
            return 0

        if os.path.isfile(current_path):
            try:
                with open(current_path, 'r', encoding='utf-8') as f:
                    count = sum(1 for _ in f)
            except Exception:
                count = 0
            line_counts[rel_path] = count
            return count

        elif os.path.isdir(current_path):
            total = 0
            try:
                entries = os.listdir(current_path)
            except Exception:
                entries = []
            entries = sorted(entries)
            # Filter out ignored entries.
            entries = [e for e in entries if not any(pattern_matches(e, ig) for ig in ignore)]
            for entry in entries:
                child_path = os.path.join(current_path, entry)
                child_rel_path = os.path.join(rel_path, entry) if rel_path != "." else entry
                total += count_lines(child_path, child_rel_path)
            line_counts[rel_path] = total
            return total

        else:
            line_counts[rel_path] = 0
            return 0

    total_lines = count_lines(os.path.abspath(startpath), ".")
    return line_counts, total_lines

def print_dir_structure(startpath, ignore=[], omit=[], show_omitted_structure=False, line_counts=None, total_lines=None):
    """
    Prints the directory structure.
    If line_counts and total_lines are provided, it appends the line count and percentage
    information to each entry that is not omitted.
    """
    def print_tree(path, prefix="", rel_path="."):
        try:
            entries = os.listdir(path)
        except Exception:
            entries = []
        entries = sorted(entries)
        # Filter out ignored items.
        entries = [e for e in entries if not any(pattern_matches(e, ig) for ig in ignore)]
        # Separate directories and files.
        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]
        all_entries = dirs + files

        for i, entry in enumerate(all_entries):
            is_last = (i == len(all_entries) - 1)
            is_dir = entry in dirs

            if is_last:
                entry_prefix = prefix + "└── "
                new_prefix = prefix + "    "
            else:
                entry_prefix = prefix + "├── "
                new_prefix = prefix + "│   "

            entry_rel_path = os.path.join(rel_path, entry) if rel_path != "." else entry

            # Check if the entry is omitted.
            is_omitted = any(pattern_matches(entry, o) for o in omit)
            line_info = ""
            # Only add line count info if not omitted.
            if not is_omitted and line_counts is not None and total_lines is not None:
                count = line_counts.get(entry_rel_path, 0)
                percentage = (count / total_lines * 100) if total_lines > 0 else 0
                line_info = f" ({count} lines, {percentage:.1f}%)"

            if is_dir:
                if is_omitted:
                    print(f"{entry_prefix}[omitted] {entry}/{''}")
                    # If showing omitted structure, still print inner structure without line counts.
                    if show_omitted_structure:
                        print_tree(os.path.join(path, entry), new_prefix, entry_rel_path)
                else:
                    print(f"{entry_prefix}{entry}/{line_info}")
                    print_tree(os.path.join(path, entry), new_prefix, entry_rel_path)
            else:
                if is_omitted:
                    print(f"{entry_prefix}[omitted] {entry}")
                else:
                    print(f"{entry_prefix}{entry}{line_info}")

    # Start the recursive printing
    path = os.path.abspath(startpath)
    base = os.path.basename(path)
    root_line_info = ""
    # Always show root line count since root is not omitted.
    if line_counts is not None and total_lines is not None:
        root_count = line_counts.get(".", 0)
        root_line_info = f" ({root_count} lines, 100%)"
    print(f"{base}/" + root_line_info)
    print_tree(path, "", ".")
    print()

def print_file_contents(startpath, ignore=[], omit=[]):
    def process_directory(current_path):
        try:
            entries = os.listdir(current_path)
        except Exception:
            entries = []
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

def dir_print(path, ignore=[], omit=[], export=None, show_omitted_structure=False, line_count=False):
    """Main function to print directory structure and file contents."""
    original_stdout = sys.stdout
    line_counts = None
    total_lines = None
    if line_count:
        line_counts, total_lines = calculate_line_counts(path, ignore, omit)
    if export:
        with open(export, 'w', encoding='utf-8') as f:
            sys.stdout = f
            print(f'{os.path.basename(path)} Directory Structure and File Contents:\n')
            print(f'<{os.path.basename(path)}-Directory-Structure>\n')
            print_dir_structure(path, ignore, omit, show_omitted_structure, line_counts, total_lines)
            print(f'<{os.path.basename(path)}-Directory-Structure>\n')
            print(f'<{os.path.basename(path)}-File-Contents>\n')
            print_file_contents(path, ignore, omit)
            print(f'<{os.path.basename(path)}-File-Contents>\n')
            sys.stdout = original_stdout
    else:
        print(f'{os.path.basename(path)} Directory Structure:')
        print_dir_structure(path, ignore, omit, show_omitted_structure, line_counts, total_lines)
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
    parser.add_argument('-lc', '--line-count', action='store_true',
                        help='Display line counts and percentages next to each file/directory (omitted entries are skipped).')

    args = parser.parse_args()
    dir_print(args.path, args.ignore, args.omit, args.export, args.show_omitted_structure, args.line_count)

if __name__ == '__main__':
    main()
