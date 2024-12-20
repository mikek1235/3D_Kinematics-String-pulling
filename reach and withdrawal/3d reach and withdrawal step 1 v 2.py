import pandas as pd
import glob
import os
import numpy as np
import shutil

def find_increasing_decreasing_segments(y_data, x_data, merge_threshold=25, min_segment_duration=20, min_velocity=0.5):
    """
    Find continuous increasing/decreasing segments in y-coordinate data with enhanced filtering.
    """
    increasing_segments = []
    decreasing_segments = []
    
    if len(y_data) < min_segment_duration:
        return increasing_segments, decreasing_segments
    
    velocities = y_data.diff()
    
    current_segment = [(x_data[0], y_data.iloc[0])]
    current_velocity_sum = 0
    
    for i in range(1, len(y_data)):
        if y_data.iloc[i] > y_data.iloc[i - 1]:
            current_segment.append((x_data[i], y_data.iloc[i]))
            current_velocity_sum += abs(velocities.iloc[i]) if not pd.isna(velocities.iloc[i]) else 0
        else:
            if len(current_segment) >= min_segment_duration:
                avg_velocity = current_velocity_sum / len(current_segment)
                if avg_velocity >= min_velocity:
                    increasing_segments.append(current_segment)
            current_segment = [(x_data[i], y_data.iloc[i])]
            current_velocity_sum = 0
            
    if len(current_segment) >= min_segment_duration:
        avg_velocity = current_velocity_sum / len(current_segment)
        if avg_velocity >= min_velocity:
            increasing_segments.append(current_segment)
    
    current_segment = [(x_data[0], y_data.iloc[0])]
    current_velocity_sum = 0
    
    for i in range(1, len(y_data)):
        if y_data.iloc[i] < y_data.iloc[i - 1]:
            current_segment.append((x_data[i], y_data.iloc[i]))
            current_velocity_sum += abs(velocities.iloc[i]) if not pd.isna(velocities.iloc[i]) else 0
        else:
            if len(current_segment) >= min_segment_duration:
                avg_velocity = current_velocity_sum / len(current_segment)
                if avg_velocity >= min_velocity:
                    decreasing_segments.append(current_segment)
            current_segment = [(x_data[i], y_data.iloc[i])]
            current_velocity_sum = 0
            
    if len(current_segment) >= min_segment_duration:
        avg_velocity = current_velocity_sum / len(current_segment)
        if avg_velocity >= min_velocity:
            decreasing_segments.append(current_segment)
    
    increasing_segments = merge_segments(increasing_segments, merge_threshold)
    decreasing_segments = merge_segments(decreasing_segments, merge_threshold)
    
    return increasing_segments, decreasing_segments

def merge_segments(segments, merge_threshold):
    merged_segments = []
    if len(segments) > 0:
        current_segment = [segments[0]]
        for i in range(1, len(segments)):
            if segments[i][0][0] - current_segment[-1][-1][0] <= merge_threshold:
                current_segment.append(segments[i])
            else:
                merged_segments.append([item for sublist in current_segment for item in sublist])
                current_segment = [segments[i]]
        merged_segments.append([item for sublist in current_segment for item in sublist])
    return merged_segments

def plot_paw_coordinates(file_path, output_data):
    df = pd.read_csv(file_path)

    left_paw_y_col = 'l_hand_y'
    right_paw_y_col = 'r_hand_y'

    left_paw_y = pd.to_numeric(df[left_paw_y_col], errors='coerce')
    right_paw_y = pd.to_numeric(df[right_paw_y_col], errors='coerce')
    time_coords = df.index

    left_paw_y = left_paw_y.reset_index(drop=True)
    right_paw_y = right_paw_y.reset_index(drop=True)

    increasing_segments_left, decreasing_segments_left = find_increasing_decreasing_segments(left_paw_y, time_coords)
    increasing_segments_right, decreasing_segments_right = find_increasing_decreasing_segments(right_paw_y, time_coords)

    for segment in increasing_segments_left:
        for i, (x, y) in enumerate(segment):
            output_data.setdefault(x, {'frames': x, 'left hand increasing': '', 'left hand decreasing': '', 'right hand increasing': '', 'right hand decreasing': ''})
            output_data[x]['left hand increasing'] = y

    for segment in decreasing_segments_left:
        for i, (x, y) in enumerate(segment):
            output_data.setdefault(x, {'frames': x, 'left hand increasing': '', 'left hand decreasing': '', 'right hand increasing': '', 'right hand decreasing': ''})
            output_data[x]['left hand decreasing'] = y

    for segment in increasing_segments_right:
        for i, (x, y) in enumerate(segment):
            output_data.setdefault(x, {'frames': x, 'left hand increasing': '', 'left hand decreasing': '', 'right hand increasing': '', 'right hand decreasing': ''})
            output_data[x]['right hand increasing'] = y

    for segment in decreasing_segments_right:
        for i, (x, y) in enumerate(segment):
            output_data.setdefault(x, {'frames': x, 'left hand increasing': '', 'left hand decreasing': '', 'right hand increasing': '', 'right hand decreasing': ''})
            output_data[x]['right hand decreasing'] = y

def ensure_merged_directory(session_folder):
    """Create merged directory if it doesn't exist, clear if it does"""
    merged_dir = os.path.join(session_folder, 'merged')
    if os.path.exists(merged_dir):
        for file in os.listdir(merged_dir):
            file_path = os.path.join(merged_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        os.makedirs(merged_dir)
    return merged_dir

# Define the session folders
session_folders = [
    "/Users/mkarkus/Desktop/hugee new/hugee session 6",
    "/Users/mkarkus/Desktop/hugee new/hugee session 5",
    "/Users/mkarkus/Desktop/hugee new/hugee session 4"
]

# Process each session folder
for folder_path in session_folders:
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue
        
    print(f"\nProcessing folder: {folder_path}")
    
    merged_dir = ensure_merged_directory(folder_path)
    
    file_paths = glob.glob(os.path.join(folder_path, '*.csv'))
    
    if not file_paths:
        print(f"No CSV files found in: {folder_path}")
        continue
        
    print(f"Found {len(file_paths)} CSV files")

    for file in file_paths:
        print(f"Processing file: {file}")
        output_data = {}
        plot_paw_coordinates(file, output_data)

        output_df = pd.DataFrame.from_dict(output_data, orient='index').sort_index()

        file_name = os.path.basename(file).replace('.csv', '')
        output_csv_path = os.path.join(folder_path, f'reach_withdraw_segments_{file_name}.csv')
        output_df.to_csv(output_csv_path, index=False)

        print(f"Reach and withdraw segment data saved to {output_csv_path}")

        reach_withdraw_path = output_csv_path

        fragment_df = pd.read_csv(file)
        reach_withdraw_df = pd.read_csv(reach_withdraw_path)

        merged_df = reach_withdraw_df.merge(fragment_df[['fnum', 'l_hand_x', 'r_hand_x']], left_on='frames', right_on='fnum', how='left')
        merged_df.drop(columns=['fnum'], inplace=True)

        merged_df['left hand increasing x'] = merged_df.apply(lambda row: row['l_hand_x'] if pd.notna(row['left hand increasing']) else None, axis=1)
        merged_df['left hand decreasing x'] = merged_df.apply(lambda row: row['l_hand_x'] if pd.notna(row['left hand decreasing']) else None, axis=1)
        merged_df['right hand increasing x'] = merged_df.apply(lambda row: row['r_hand_x'] if pd.notna(row['right hand increasing']) else None, axis=1)
        merged_df['right hand decreasing x'] = merged_df.apply(lambda row: row['r_hand_x'] if pd.notna(row['right hand decreasing']) else None, axis=1)

        desired_order = [
            'frames',
            'left hand increasing', 'left hand increasing x',
            'left hand decreasing', 'left hand decreasing x',
            'right hand increasing', 'right hand increasing x',
            'right hand decreasing', 'right hand decreasing x'
        ]

        ordered_df = merged_df[desired_order]

        outputfilename = f'reach_withdraw_segments_with_lx_rx_merged_{file_name}.csv'
        output_path = os.path.join(merged_dir, outputfilename)
        ordered_df.to_csv(output_path, index=False)

        if os.path.exists(output_csv_path):
            os.remove(output_csv_path)

        print(f"Merged data saved to {output_path}")