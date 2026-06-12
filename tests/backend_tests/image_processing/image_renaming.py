file_location = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_07_08_34_26\0.png"

import os

def rename_files_remove_undist(directory_path):
    """
    Renames image files in a directory by removing "_undist" from filenames ending with ".png".

    Args:
        directory_path (str): The path to the directory containing the image files.
    """
    try:
        # Check if the directory exists
        if not os.path.isdir(directory_path):
            print(f"Error: Directory '{directory_path}' not found.")
            return

        # Iterate through files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".png") and "_undist" in filename:
                old_filepath = os.path.join(directory_path, filename)

                # Construct the new filename by removing "_undist"
                new_filename_base = filename.replace("_undist", "")
                new_filepath = os.path.join(directory_path, new_filename_base)

                try:
                    # Rename the file
                    os.rename(old_filepath, new_filepath)
                    print(f"Renamed '{filename}' to '{new_filename_base}'")
                except OSError as e:
                    print(f"Error renaming '{filename}': {e}")

        print("Renaming process completed.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    file_location = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_07_08_34_26\0.png"

    # Extract the directory path from the given file location
    directory_to_process = os.path.dirname(file_location)

    rename_files_remove_undist(directory_to_process)