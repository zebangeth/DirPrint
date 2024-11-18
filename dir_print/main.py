import os
import sys
import argparse

def print_dir_structure(startpath, ignore=[], omit=[], show_omitted_structure=False):
    """Print directory structure with support for ignore and omit patterns"""
    def print_tree(path, prefix=""):
        # Get the contents of the directory
        entries = os.listdir(path)
        entries = sorted(entries)  # Sort entries alphabetically
        
        # Filter out ignored items
        entries = [e for e in entries if not any(ig in e for ig in ignore)]
        
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
            
            # Check if entry should be omitted
            is_omitted = any(o in entry for o in omit)
            
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
    """Print file contents with support for ignore and omit patterns"""
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if not any(ig in d for ig in ignore)]
        
        # Check if current directory is omitted
        current_dir = os.path.basename(root)
        if any(o in current_dir for o in omit):
            print(f'{os.path.relpath(root, startpath)}/:')
            print('[Directory contents omitted for brevity...]')
            print()
            dirs[:] = []  # Skip processing this directory's contents
            continue
        
        # Process files
        for f in sorted(files):  # Sort files for consistent output
            if any(ig in f for ig in ignore):
                continue
                
            rel_path = os.path.relpath(os.path.join(root, f), startpath)
            print(f'{rel_path}:')
            
            if any(o in f for o in omit):
                print('[Content omitted for brevity...]')
                print()
            else:
                print('```')
                try:
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                        print(file.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
                print('```')
                print()

def dir_print(path, ignore=[], omit=[], export=None, show_omitted_structure=False):
    """Main function to print directory structure and contents"""
    original_stdout = sys.stdout
    
    if export:
        with open(export, 'w', encoding='utf-8') as f:
            sys.stdout = f
            print(f'{os.path.basename(path)} Directory Structure:')
            print_dir_structure(path, ignore, omit, show_omitted_structure)
            print_file_contents(path, ignore, omit)
            sys.stdout = original_stdout
    else:
        print(f'{os.path.basename(path)} Directory Structure:')
        print_dir_structure(path, ignore, omit, show_omitted_structure)
        print_file_contents(path, ignore, omit)

def main():
    parser = argparse.ArgumentParser(description='DirPrint: Print your directory structure and file contents.')
    parser.add_argument('path', type=str, help='Directory path to print')
    parser.add_argument('-I', '--ignore', type=str, nargs='*', default=[], 
                        help='Patterns to ignore (completely hide)')
    parser.add_argument('-O', '--omit', type=str, nargs='*', default=[],
                        help='Patterns to omit (show in structure but hide contents)')
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
