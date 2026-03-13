import os
import hashlib


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

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                file_hash = get_file_hash(file_path)

                if file_hash in hashes:
                    duplicates.append((file_path, hashes[file_hash]))
                else:
                    hashes[file_hash] = file_path

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return duplicates


def main():
    folder = input("Enter folder path to scan: ")

    if not os.path.exists(folder):
        print("Folder does not exist.")
        return

    duplicates = find_duplicate_files(folder)

    if duplicates:
        print("\nDuplicate files found:")
        for file1, file2 in duplicates:
            print(f"{file1} == {file2}")
    else:
        print("\nNo duplicate files found.")


if __name__ == "__main__":
    main()