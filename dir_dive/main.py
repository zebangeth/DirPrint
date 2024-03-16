import os
import sys
import argparse

def print_dir_structure(startpath, ignore=[]):
    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if not any(ig in d for ig in ignore)]
        files = [f for f in files if not any(ig in f for ig in ignore)]
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        print(f'{indent}{os.path.basename(root)}/')
        subindent = '│   ' * level + '├── '
        for f in files:
            print(f'{subindent}{f}')
    print()

def print_file_contents(startpath, ignore=[]):
    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if not any(ig in d for ig in ignore)]
        files = [f for f in files if not any(ig in f for ig in ignore)]
        for f in files:
            filepath = os.path.join(root, f)
            print(f'{os.path.relpath(filepath, startpath)}:')
            print('```')
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    print(file.read())
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")
            print('```')
            print()

def dir_dive(path, ignore=[], output=None):
    original_stdout = sys.stdout

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            sys.stdout = f
            print(f'{path} Directory Structure:')
            print_dir_structure(path, ignore)
            print_file_contents(path, ignore)
            sys.stdout = original_stdout
    else:
        print(f'{path} Directory Structure:')
        print_dir_structure(path, ignore)
        print_file_contents(path, ignore)

def main():
    parser = argparse.ArgumentParser(description='DirDive: Dive into your directory structure and file contents.')
    parser.add_argument('path', type=str, help='Directory path to dive into')
    parser.add_argument('-I', '--ignore', type=str, nargs='*', default=[], help='Patterns to ignore separated by |')
    parser.add_argument('-o', '--output', type=str, help='Output file (optional)')
    args = parser.parse_args()
    dir_dive(args.path, args.ignore, args.output)

if __name__ == '__main__':
    main()
