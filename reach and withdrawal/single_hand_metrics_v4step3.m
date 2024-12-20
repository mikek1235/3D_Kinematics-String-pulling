% List of folders to process
folders = {
    '/Users/mkarkus/Desktop/3d poses/hazel/session1hazel/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/heidi/session2heidi/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/tikka/session2tikka/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/hazel/session2hazel/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/owen/session2owen/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/hugee/hugee-session3/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/hugee/session2hugee/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/hugee/hugee-session10/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/tikka/session1tikka/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/oscar/session1oscar/merged/subfolders';
    '/Users/mkarkus/Desktop/3d poses/oscar/session2oscar/merged/subfolders'
};

% Loop through each folder
for folderIdx = 1:length(folders)
    folderPath = folders{folderIdx};
    
    % Ensure the folder exists
    if ~isfolder(folderPath)
        error('Folder does not exist: %s', folderPath);
    end
    
    % Get a list of all CSV files in the folder
    csvFiles = dir(fullfile(folderPath, '*.csv'));
    
    % Initialize summary table
    summaryTable = table();
    
    % Process each CSV file
    for k = 1:length(csvFiles)
        if strcmp(csvFiles(k).name, 'summary.csv')
            continue;
        end
        
        % Load data
        filePath = fullfile(folderPath, csvFiles(k).name);
        data = readtable(filePath, 'VariableNamingRule', 'preserve');
        
        % Extract columns
        time = data{:, 1};
        position_y = data{:, 2};
        position_x = data{:, 3};
        
        % Handle missing data gracefully
        time(isnan(time)) = [];
        position_y(isnan(position_y)) = [];
        position_x(isnan(position_x)) = [];
        
        % Ensure sufficient data for calculations
        if length(time) < 4, continue; end
        
        % Calculate speed, acceleration, and jerk
        dt = diff(time);
        dp_y = diff(position_y);
        dp_x = diff(position_x);
        speed = sqrt(dp_y.^2 + dp_x.^2) ./ dt;
        acceleration = diff(speed) ./ dt(1:end-1);
        jerk = diff(acceleration) ./ dt(1:end-2);
        
        average_speed = mean(speed, 'omitnan');
        peak_speed = max(speed, [], 'omitnan');
        average_acceleration = mean(acceleration, 'omitnan');
        peak_acceleration = max(acceleration, [], 'omitnan');
        average_jerk = mean(jerk, 'omitnan');
        peak_jerk = max(jerk, [], 'omitnan');
        
        actual_distance = sum(sqrt(dp_x.^2 + dp_y.^2), 'omitnan');
        euclidean_distance = sqrt((position_x(end) - position_x(1))^2 + (position_y(end) - position_y(1))^2);
        
        % Calculate path circuitry ratio
        path_circuitry = euclidean_distance / max(actual_distance, 1e-6);
        
        % Circular statistics
        angles = atan2(dp_y, dp_x);
        mean_direction = circ_mean(angles);
        if mean_direction < 0, mean_direction = mean_direction + 2*pi; end
        mean_direction_deg = mean_direction * (180 / pi);
        R = circ_r(angles);
        circular_variance = 1 - R;
        
        % Check validity of mean direction and circular variance
        if isnan(mean_direction) || isnan(circular_variance)
            warning('Invalid mean direction or circular variance for file: %s', csvFiles(k).name);
            mean_direction_deg = NaN;
            circular_variance = NaN;
        end
        
        % Append to summary table
        summaryTable = [summaryTable; table({csvFiles(k).name}, average_speed, peak_speed, average_acceleration, peak_acceleration, average_jerk, peak_jerk, ...
            actual_distance, euclidean_distance, path_circuitry, mean_direction_deg, circular_variance, ...
            'VariableNames', {'FileName', 'AverageSpeed', 'PeakSpeed', 'AverageAcceleration', 'PeakAcceleration', 'AverageJerk', 'PeakJerk', ...
            'ActualDistance', 'EuclideanDistance', 'PathCircuitry', 'MeanDirection(degrees)', 'CircularVariance'})];
    end
    
    % Save the summary table
    summaryFilePath = fullfile(folderPath, 'summary.csv');
    writetable(summaryTable, summaryFilePath, 'WriteVariableNames', true);
    disp(['Summary saved: ', summaryFilePath]);
end

% Circular statistics functions
function mean_dir = circ_mean(angles)
    mean_dir = atan2(sum(sin(angles)), sum(cos(angles)));
end

function R = circ_r(angles)
    R = sqrt(sum(cos(angles))^2 + sum(sin(angles))^2) / length(angles);
end