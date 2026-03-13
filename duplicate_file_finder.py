import os
import hashlib
import argparse


def get_file_hash(file_path):
    """Return SHA256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicate_files(folder_path):
    """Find duplicate files in a folder."""
    hashes = {}
    duplicates = []
    total_wasted_space = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                print(f"Scanning: {file_path}")

                file_hash = get_file_hash(file_path)

                if file_hash in hashes:
                    duplicates.append((file_path, hashes[file_hash]))
                    total_wasted_space += os.path.getsize(file_path)
                else:
                    hashes[file_hash] = file_path

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return duplicates, total_wasted_space


def save_report(duplicates):
    """Save duplicate report to a file."""
    with open("duplicate_report.txt", "w") as report:
        for file1, file2 in duplicates:
            report.write(f"{file1} == {file2}\n")

    print("\nReport saved as duplicate_report.txt")


def delete_duplicates(duplicates):
    """Delete duplicate files."""
    for file1, file2 in duplicates:
        try:
            os.remove(file1)
            print(f"Deleted: {file1}")
        except Exception as e:
            print(f"Could not delete {file1}: {e}")


def main():

    parser = argparse.ArgumentParser(description="Duplicate File Finder")
    parser.add_argument("folder", help="Folder path to scan")

    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print("Folder does not exist.")
        return

    duplicates, wasted_space = find_duplicate_files(args.folder)

    if duplicates:
        print("\nDuplicate files found:\n")

        for file1, file2 in duplicates:
            size = os.path.getsize(file1) / (1024 * 1024)
            print(f"{file1} == {file2} | Size: {size:.2f} MB")

        print(f"\nTotal duplicate space: {wasted_space/(1024*1024):.2f} MB")

        save_report(duplicates)

        choice = input("\nDo you want to delete duplicate files? (y/n): ")
        if choice.lower() == "y":
            delete_duplicates(duplicates)

    else:
        print("\nNo duplicate files found.")


if __name__ == "__main__":
    main()