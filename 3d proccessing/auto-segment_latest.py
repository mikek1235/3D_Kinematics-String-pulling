import os
from moviepy.editor import VideoFileClip

# Define video paths
video_paths = {
    "A": r"D:\anipose_working_folder\anipose_marm3d_v8_nov29calibration\Oscar-session2\rotated_oscar_CamA_2024-12-04-12042024174612-0000.mp4",
    "B": r"D:\anipose_working_folder\anipose_marm3d_v8_nov29calibration\Oscar-session2\rotated_oscar_CamB_2024-12-04-12042024174614-0000.mp4",
    "C": r"D:\anipose_working_folder\anipose_marm3d_v8_nov29calibration\Oscar-session2\rotated_oscar_CamC_2024-12-04-12042024174614-0000.mp4"
}

# Define intervals in seconds (adjusted)
intervals = [
    (28.5, 32),
    (31.5, 34),
    (33.5, 38),
    (37.5, 42),
    (43.5, 47),
    (49.5, 53),
    (54.5, 58),
    (57.5, 61),
    (60.5, 64),
    (63.5, 68),
    (71.5, 75),
    (84.5, 87),
    (89.5, 93),
    (112.5, 116),
    (127.5, 130),
    (144.5, 148),
    (147.5, 151),
    (150.5, 154),
    (165.5, 168),
    (171.5, 174),
    (176.5, 180),
    (185.5, 189),
    (207.5, 212),
    (212.5, 215),
    (229.5, 233),
    (237.5, 240),
    (290.5, 293),
    (319.5, 322)
]

# Define output folder
output_base_folder = r"D:\anipose_working_folder\anipose_marm3d_v8_nov29calibration\Oscar-session2\fragments"
os.makedirs(output_base_folder, exist_ok=True)

# Process videos
for camera, path in video_paths.items():
    print(f"\nProcessing camera: {camera}")
    try:
        clip = VideoFileClip(path)
        video_duration = clip.duration
        print(f"Loaded {camera} successfully. Duration: {video_duration:.2f} seconds.")
    except Exception as e:
        print(f"Error loading video for {camera}: {e}")
        continue

    for idx, (start, end) in enumerate(intervals):
        if start < video_duration and end <= video_duration:
            try:
                print(f"Processing interval {start}-{end} for {camera}...")
                subclip = clip.subclip(start, end)
                
                # Create a folder for this segment
                segment_folder = os.path.join(output_base_folder, f"{start}_{end}")
                os.makedirs(segment_folder, exist_ok=True)
                
                # Save the segment in its corresponding folder
                output_path = os.path.join(segment_folder, f"{camera}_clip_{idx + 1}.mp4")
                subclip.write_videofile(
                    output_path,
                    codec="libx264",
                    preset="slow",
                    ffmpeg_params=["-crf", "18"]
                )
            except Exception as e:
                print(f"Error processing interval {start}-{end} for {camera}: {e}")
        else:
            print(f"Skipping interval {start}-{end} for {camera}, as it exceeds the video duration.")
    
    try:
        clip.close()
    except Exception as e:
        print(f"Error closing video for {camera}: {e}")

print("\nProcessing complete!")
