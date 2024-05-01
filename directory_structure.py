import os

# Function to list the directory structure
def list_directory_structure(startpath):
    structure = []
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Exclude .venv and .git or other specific directories
        dirs[:] = [d for d in dirs if d not in ['.venv', '.git', '.idea']]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{subindent}{f}")
    return structure

# Main function to write the structure to a file
def main():
    startpath = '.'  # starting directory
    output_file = 'directory_structure.txt'  # output file name
    structure = list_directory_structure(startpath)
    with open(output_file, 'w') as f:
        for item in structure:
            f.write(f"{item}\n")

    print(f"Directory structure written to {output_file}")

if __name__ == "__main__":
    main()
