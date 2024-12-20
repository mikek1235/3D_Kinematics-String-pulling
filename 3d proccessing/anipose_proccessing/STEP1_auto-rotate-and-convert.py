import os
import subprocess

# List of folders containing videos
folders = [
    r"D:\anipose_working_folder\anipose_marm3d_v8_nov29calibration\OWEN\Owen-session9\videos-raw"
]

# Rotate and convert videos
def rotate_videos(folder):
    for file in os.listdir(folder):
        if file.endswith(".mp4") or file.endswith(".avi"):
            input_path = os.path.join(folder, file)
            output_path = os.path.join(folder, f"rotated_{os.path.splitext(file)[0]}.mp4")
            
            # ffmpeg command to rotate 180 degrees
            command = [
                "ffmpeg",
                "-i", input_path,  # Input file
                "-vf", "transpose=2,transpose=2",  # Rotate 180 degrees
                "-c:v", "libx264",  # H.264 codec for MP4
                "-crf", "18",  # High quality
                "-preset", "slow",  # Optimize compression
                "-c:a", "copy",  # Copy audio without re-encoding
                output_path
            ]
            
            print(f"Processing file: {input_path}")
            try:
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"Rotated and saved: {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_path}: {e.stderr.decode('utf-8')}")

# Iterate through all folders
for folder in folders:
    if os.path.exists(folder):
        print(f"\nProcessing folder: {folder}")
        rotate_videos(folder)
    else:
        print(f"Folder does not exist: {folder}")

print("\nAll videos processed!")
