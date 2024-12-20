import os

# Converts intervals from the auto-segment output to trials (e.g. trial 1,2,3,4, etc)
# Need to run "trial-rename and move to videos-raw_working.py" in order to rename the actual cameras to the proper anipose format 

# Define the root folder containing interval directories
root_folder = r"D:\anipose_working_folder\individual sessions\anipose_marm3d_session1\oscar"

def rename_interval_folders(root_folder):
    if os.path.exists(root_folder):
        # List all directories and sort them numerically by the interval
        interval_folders = sorted(
            [folder for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))],
            key=lambda x: float(x.split('_')[0])  # Sort based on the first part of the interval
        )
        
        trial_index = 1  # Start trial numbering
        for folder_name in interval_folders:
            old_path = os.path.join(root_folder, folder_name)
            new_folder_name = f"trial_{trial_index}"
            new_path = os.path.join(root_folder, new_folder_name)
            
            # Rename the folder
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")
                trial_index += 1
            except Exception as e:
                print(f"Error renaming folder {old_path}: {e}")
    else:
        print(f"Root folder does not exist: {root_folder}")

# Run the function
rename_interval_folders(root_folder)
