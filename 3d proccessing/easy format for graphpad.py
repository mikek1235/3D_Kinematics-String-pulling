import pandas as pd
import os
import re

def determine_movement_type(filename):
    """
    Determine hand and movement type based on filename
    """
    # Check hand side
    if 'Ly_Lx' in filename:
        hand = 'Left'
    elif 'Ry_Rx' in filename:
        hand = 'Right'
    else:
        hand = 'Unknown'
    
    # Check movement type
    if 'increasing' in filename:
        movement = 'Reach'
    elif 'decreasing' in filename:
        movement = 'Withdrawal'
    else:
        movement = 'Unknown'
    
    return hand, movement

def convert_csv(file_path):
    """
    Convert a single CSV file to the desired format
    """
    # Read the input CSV file
    df = pd.read_csv(file_path)
    
    # Flexible column mapping with multiple possible variations
    column_mapping = {
        'AverageJerk': ['AverageJerk', 'Jerk', 'Average Jerk', 'AverageJerks'],
        'PathCircuitry': ['PathCircuitry', 'Path Circuitry', 'Circuitry', 'Path_Circuitry'],
        'MeanDirection': ['MeanDirection', 'Mean Direction', 'Direction', 'MeanDirection(degrees)', 'Mean_Direction'],
        'CircularVariance': ['CircularVariance', 'Circular Variance', 'Variance', 'Circular_Variance']
    }
    
    # Find matching columns
    columns_to_convert = []
    for target_col, possible_names in column_mapping.items():
        match = next((col for col in df.columns if col in possible_names), None)
        if match:
            columns_to_convert.append((target_col, match))
    
    # If no columns found, skip this file
    if not columns_to_convert:
        print(f"No matching columns found in {os.path.basename(file_path)}")
        return None
    
    # Extract subject name and session from filename
    filename = os.path.basename(file_path)
    
    # More robust subject extraction
    parts = filename.split('_')
    if len(parts) >= 2:
        subject = parts[0]
    else:
        subject = filename.split('.')[0]
    
    # Create a new dataframe with hand and movement information
    new_data = []
    
    for _, row in df.iterrows():
        # Determine hand and movement from the filename in each row
        hand, movement = determine_movement_type(row['FileName'])
        
        # Create a new row with all the required information
        new_row = {
            'Subject': subject,
            'Hand': hand,
            'Movement': movement
        }
        
        # Add the columns we want to convert
        for target, original in columns_to_convert:
            new_row[target] = row[original]
        
        new_data.append(new_row)
    
    return pd.DataFrame(new_data)

def process_csv_files(file_paths):
    """
    Process multiple CSV files and combine them
    """
    # List to store converted DataFrames
    converted_dataframes = []
    
    # Process each file
    for file_path in file_paths:
        try:
            converted_df = convert_csv(file_path)
            if converted_df is not None:
                converted_dataframes.append(converted_df)
                print(f"Processed: {file_path}")
                
                # Print unique hand and movement combinations
                print("Unique Hand and Movement combinations:")
                print(converted_df.groupby(['Hand', 'Movement']).size())
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Check if we have any DataFrames to combine
    if not converted_dataframes:
        raise ValueError("No valid DataFrames to combine. Check column names.")
    
    # Combine all DataFrames
    final_df = pd.concat(converted_dataframes, ignore_index=True)
    
    return final_df

# List of file paths
file_paths = [
    '/Users/mkarkus/Desktop/hugee new/hugee session 4/merged/subfolders/hugee new_hugee session 4_summary.csv',
    '/Users/mkarkus/Desktop/hugee new/hugee session 5/merged/subfolders/hugee new_hugee session 5_summary.csv',
    '/Users/mkarkus/Desktop/hugee new/hugee session 6/merged/subfolders/hugee new_hugee session 6_summary.csv',
]

# Process the files
final_dataset = process_csv_files(file_paths)

# Save the combined dataset
output_path = '/Users/mkarkus/Desktop/3d poses/combined_summary_dataset.csv'
final_dataset.to_csv(output_path, index=False)

print(f"\nCombined dataset saved to {output_path}")
print(f"Total rows: {len(final_dataset)}")
print("Columns:", list(final_dataset.columns))

# Print summary of the dataset
print("\nDataset Summary:")
print(final_dataset.groupby(['Subject', 'Hand', 'Movement']).size())