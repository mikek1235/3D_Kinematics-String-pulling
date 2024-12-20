import os
import glob
import pandas as pd

def calculate_correlations(file_path):
    """
    Calculate correlations between left and right hand coordinates (X, Y, Z).
    """
    data = pd.read_csv(file_path)
    correlations = {
        "file_name": os.path.basename(file_path),
        "x_correlation": data["r_hand_x"].corr(data["l_hand_x"]),
        "y_correlation": data["r_hand_y"].corr(data["l_hand_y"]),
        "z_correlation": data["r_hand_z"].corr(data["l_hand_z"]),
    }
    return correlations

def process_folder(folder_path, output_file):
    """
    Process all CSV files in the folder and calculate correlations.
    """
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    results = []
    
    # Process each file
    for file_path in csv_files:
        correlations = calculate_correlations(file_path)
        results.append(correlations)
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Calculate averages
    averages = {
        "file_name": "AVERAGE",
        "x_correlation": results_df["x_correlation"].mean(),
        "y_correlation": results_df["y_correlation"].mean(),
        "z_correlation": results_df["z_correlation"].mean(),
    }
    results_df = pd.concat([results_df, pd.DataFrame([averages])], ignore_index=True)
    
    # Save to CSV
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

# List of folders and corresponding output file paths
folders = [
    "/Users/mkarkus/Desktop/3d poses/owen/session8owen"
]



output_folder = "/Users/mkarkus/Desktop/3d poses/owen/session8owen"
os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

# Process each folder
for folder_path in folders:
    folder_name = os.path.basename(folder_path)  # Extract folder name
    output_file = os.path.join(output_folder, f"{folder_name}_correlations.csv")
    process_folder(folder_path, output_file)

print("All folders have been processed.")
