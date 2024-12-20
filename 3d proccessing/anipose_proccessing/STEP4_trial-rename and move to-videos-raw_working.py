import os
import shutil

# This is to be executed after step3 (intervals to trials.py), it essentially renames the trials into an anipose friendly format and then moves them to a videos-raw file

# Define the root folder and other details
# define name and session
root_folder = r"D:\anipose_working_folder\individual sessions\anipose_marm3d_session1\oscar"
subject_name = "oscar"#
session_name = "session1"

def rename_and_move_videos(root_folder, subject_name, session_name):
    if not os.path.exists(root_folder):
        print(f"Root folder does not exist: {root_folder}")
        return

    # Iterate through trial folders
    for trial_folder in sorted(os.listdir(root_folder)):
        trial_path = os.path.join(root_folder, trial_folder)
        if not os.path.isdir(trial_path):
            continue

        # Create the videos-raw folder inside the trial folder
        videos_raw_folder = os.path.join(trial_path, "videos-raw")
        os.makedirs(videos_raw_folder, exist_ok=True)

        # Process all video files in the trial folder
        for file_name in os.listdir(trial_path):
            file_path = os.path.join(trial_path, file_name)

            if file_name.endswith(".mp4"):
                # Extract camera name (e.g., A, B, C) from the file name
                camera = file_name.split("_")[0]
                if camera not in ["A", "B", "C"]:
                    print(f"Skipping invalid file: {file_name}")
                    continue

                # Generate the new file name
                trial_number = trial_folder.split("_")[1]  # Extract trial number
                new_file_name = f"{subject_name}-{session_name}_trial_{trial_number}_cam{camera}.mp4"
                new_file_path = os.path.join(videos_raw_folder, new_file_name)

                # Move and rename the file
                try:
                    shutil.move(file_path, new_file_path)
                    print(f"Moved and renamed file: {file_path} -> {new_file_path}")
                except Exception as e:
                    print(f"Error moving file {file_path}: {e}")

# Run the function
rename_and_move_videos(root_folder, subject_name, session_name)
