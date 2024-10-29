import os
import zlib
# Author: St1cky
# Github: https://github.com/St1ckyNew
# Date: 29.10.2024

# List of .sso files to replace
sso_files = [
    # "C:\\SSO\\heraldry_library.sso"
    "C:\\SSO\\heraldry_library.sso",
    "C:\\SSO\\cam_base.sso"
    # Add all other files here...
]

# Path to the target .pak file
pak_file_path = "C:\default_other.pak"

def calculate_crc32(file_data):
    """Calculate CRC32 checksum for the given file data."""
    return zlib.crc32(file_data) & 0xFFFFFFFF

def replace_in_pak(pak_file_path, sso_files):
    successful_replacements = 0
    failed_replacements = 0

    print("Starting the merge process...\n")

    with open(pak_file_path, 'r+b') as pak_file:
        pak_data = pak_file.read()

        for sso_path in sso_files:
            sso_filename = os.path.basename(sso_path)

            try:
                with open(sso_path, 'rb') as sso_file:
                    sso_data = sso_file.read()

                print(f"Processing {sso_filename}...")

                # Find the location of the .sso file in the .pak file
                pos = pak_data.find(sso_filename.encode())
                if pos == -1:
                    print(f"  [ERROR] {sso_filename} not found in the .pak file.\n")
                    failed_replacements += 1
                    continue

                # Assuming the raw data starts immediately after the filename
                start_pos = pos + len(sso_filename)

                # Verify file size and the 'PK' marker
                raw_data_length = len(sso_data)
                end_pos = start_pos + raw_data_length

                # Check that the data ends with 'PK'
                if pak_data[end_pos:end_pos + 2] != b'PK':
                    print(f"  [ERROR] No 'PK' marker found after raw data for {sso_filename}.\n")
                    failed_replacements += 1
                    continue

                # Calculate CRC32 of original and replacement data
                original_data = pak_data[start_pos:end_pos]
                original_crc = calculate_crc32(original_data)
                new_crc = calculate_crc32(sso_data)

                # Replace the data in the .pak file
                pak_file.seek(start_pos)
                pak_file.write(sso_data)

                # Output CRC information
                print(f"  Original CRC32: {hex(original_crc)}")
                print(f"  New CRC32:      {hex(new_crc)}")

                if original_crc != new_crc:
                    print(f"  [WARNING] CRC32 mismatch for {sso_filename}: original {hex(original_crc)}, new {hex(new_crc)}")
                else:
                    print(f"  {sso_filename} replaced successfully with matching CRC32.\n")

                successful_replacements += 1

            except Exception as e:
                print(f"  [ERROR] Failed to process {sso_filename}: {e}\n")
                failed_replacements += 1

    # Summary of results
    print("\nMerge process completed.")
    print(f"  Successful replacements: {successful_replacements}")
    print(f"  Failed replacements:     {failed_replacements}\n")

if __name__ == "__main__":
    replace_in_pak(pak_file_path, sso_files)
