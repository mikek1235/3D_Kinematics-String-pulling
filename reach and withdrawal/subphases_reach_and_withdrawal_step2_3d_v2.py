import pandas as pd
import glob
import os

# Define a function to save segments to CSV files
def save_segments_to_csv(df, y_col, x_col, prefix, output_folder, session, trial, file):
    if y_col not in df.columns or x_col not in df.columns:
        print(f"Error: Columns '{y_col}' or '{x_col}' not found in the dataframe.")
        return
    
    segments = []
    current_segment = []

    for i in range(len(df)):
        if pd.notna(df[y_col].iloc[i]) and pd.notna(df[x_col].iloc[i]):
            current_segment.append((df['frames'].iloc[i], df[y_col].iloc[i], df[x_col].iloc[i]))
        else:
            if len(current_segment) > 0:
                segments.append(current_segment)
                current_segment = []

    if len(current_segment) > 0:
        segments.append(current_segment)

    subfolder_path = os.path.join(output_folder, "subfolders")
    os.makedirs(subfolder_path, exist_ok=True)

    for idx, segment in enumerate(segments):
        segment_df = pd.DataFrame(segment, columns=['frames', y_col, x_col])
        output_file_path = os.path.join(subfolder_path, f"{session}_{trial}_{file}_{prefix}_{idx+1}.csv")
        segment_df.to_csv(output_file_path, index=False)
        print(f"Saved: {output_file_path}")

# List of folder paths to process
folders = [
    "/Users/mkarkus/Desktop/hugee new/hugee session 4/merged",
    "/Users/mkarkus/Desktop/hugee new/hugee session 6/merged",
    "/Users/mkarkus/Desktop/hugee new/hugee session 5/merged"
]

# Process each folder
for folder in folders:
    print(f"Processing folder: {folder}")
    
    # Extract session and trial information from the folder path
    parts = folder.split('/')
    subject = parts[-3]
    session = parts[-2].split(subject)[0].rstrip('-')
    trial = parts[-1]
    
    # Finding all CSV files in the folder
    file_paths = glob.glob(os.path.join(folder, '*.csv'))

    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        
        # Extract file name from the file path
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Generate segmented files for each pair of x and y values
        save_segments_to_csv(df, 'left hand increasing', 'left hand increasing x', 'Ly_Lx_increasing', folder, session, trial, file_name)
        save_segments_to_csv(df, 'left hand decreasing', 'left hand decreasing x', 'Ly_Lx_decreasing', folder, session, trial, file_name)
        save_segments_to_csv(df, 'right hand increasing', 'right hand increasing x', 'Ry_Rx_increasing', folder, session, trial, file_name)
        save_segments_to_csv(df, 'right hand decreasing', 'right hand decreasing x', 'Ry_Rx_decreasing', folder, session, trial, file_name)