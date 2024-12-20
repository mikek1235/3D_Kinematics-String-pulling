% Define the folder where your CSV files are stored
folderPath = '/Users/mkarkus/Desktop/dec 11 data/backup/correlation calculation';

% Get a list of all files in the folder with the desired file name pattern
filePattern = fullfile(folderPath, '*.csv'); 
csvFiles = dir(filePattern);

% Initialize a table to store results for all files
resultsTable = table();

for k = 1:length(csvFiles)
    baseFileName = csvFiles(k).name;
    fullFileName = fullfile(folderPath, baseFileName);
    fprintf('Now reading %s\n', fullFileName);
  
    % Extract the name identifier (e.g., owen, heidi, oscar)
    [~, namePart, ~] = fileparts(baseFileName);
    underscoreIndex = strfind(namePart, '_');
    if ~isempty(underscoreIndex)
        subjectName = namePart(1:underscoreIndex(1)-1);
    else
        subjectName = namePart; % Default to entire name if no underscore
    end
  
    % Read the CSV file
    data = readtable(fullFileName);

    % Select the columns for cross-correlation
    Lx = data.l_hand_x;
    Ly = data.l_hand_y;
    Lz = data.l_hand_z;
    Rx = data.r_hand_x;
    Ry = data.r_hand_y;
    Rz = data.r_hand_z;

    % Cross-correlation and phase shift calculations
    [c_Lx_Rx, lags_Lx_Rx] = xcorr(Lx, Rx, 'normalized');
    [c_max_Lx_Rx, max_ind_Lx_Rx] = max(c_Lx_Rx);
    t_lag_Lx_Rx = lags_Lx_Rx(max_ind_Lx_Rx);

    [c_Ly_Ry, lags_Ly_Ry] = xcorr(Ly, Ry, 'normalized');
    [c_max_Ly_Ry, max_ind_Ly_Ry] = max(c_Ly_Ry);
    t_lag_Ly_Ry = lags_Ly_Ry(max_ind_Ly_Ry);

    [c_Lz_Rz, lags_Lz_Rz] = xcorr(Lz, Rz, 'normalized');
    [c_max_Lz_Rz, max_ind_Lz_Rz] = max(c_Lz_Rz);
    t_lag_Lz_Rz = lags_Lz_Rz(max_ind_Lz_Rz);

    % Phase shift calculations
    % Find peaks for left and right signals to calculate cycle lengths
    [~, locs_Lx] = findpeaks(Lx, 'MinPeakDistance', 30);
    [~, locs_Rx] = findpeaks(Rx, 'MinPeakDistance', 30);
    cycle_Lx = diff(locs_Lx);
    cycle_Rx = diff(locs_Rx);
    avg_cycle_Lx_Rx = mean([mean(cycle_Lx, 'omitnan'), mean(cycle_Rx, 'omitnan')], 'omitnan');

    [~, locs_Ly] = findpeaks(Ly, 'MinPeakDistance', 30);
    [~, locs_Ry] = findpeaks(Ry, 'MinPeakDistance', 30);
    cycle_Ly = diff(locs_Ly);
    cycle_Ry = diff(locs_Ry);
    avg_cycle_Ly_Ry = mean([mean(cycle_Ly, 'omitnan'), mean(cycle_Ry, 'omitnan')], 'omitnan');

    [~, locs_Lz] = findpeaks(Lz, 'MinPeakDistance', 30);
    [~, locs_Rz] = findpeaks(Rz, 'MinPeakDistance', 30);
    cycle_Lz = diff(locs_Lz);
    cycle_Rz = diff(locs_Rz);
    avg_cycle_Lz_Rz = mean([mean(cycle_Lz, 'omitnan'), mean(cycle_Rz, 'omitnan')], 'omitnan');

    % Calculate phase delays and effective degree delays
    phase_Lx_Rx = 360 * (t_lag_Lx_Rx / avg_cycle_Lx_Rx);
    effective_phase_Lx_Rx = mod(phase_Lx_Rx, 360);

    phase_Ly_Ry = 360 * (t_lag_Ly_Ry / avg_cycle_Ly_Ry);
    effective_phase_Ly_Ry = mod(phase_Ly_Ry, 360);

    phase_Lz_Rz = 360 * (t_lag_Lz_Rz / avg_cycle_Lz_Rz);
    effective_phase_Lz_Rz = mod(phase_Lz_Rz, 360);

    % Append the results to the results table
    newRow = {subjectName, baseFileName, ...
        t_lag_Lx_Rx, c_max_Lx_Rx, phase_Lx_Rx, effective_phase_Lx_Rx, ...
        t_lag_Ly_Ry, c_max_Ly_Ry, phase_Ly_Ry, effective_phase_Ly_Ry, ...
        t_lag_Lz_Rz, c_max_Lz_Rz, phase_Lz_Rz, effective_phase_Lz_Rz};
    newRowTable = cell2table(newRow, 'VariableNames', ...
        {'SubjectName', 'FileName', ...
        'Lag_Lx_Rx', 'MaxCorr_Lx_Rx', 'Phase_Lx_Rx', 'EffectivePhase_Lx_Rx', ...
        'Lag_Ly_Ry', 'MaxCorr_Ly_Ry', 'Phase_Ly_Ry', 'EffectivePhase_Ly_Ry', ...
        'Lag_Lz_Rz', 'MaxCorr_Lz_Rz', 'Phase_Lz_Rz', 'EffectivePhase_Lz_Rz'});
    resultsTable = [resultsTable; newRowTable];
end

% Ensure the 'SubjectName' column exists and is recognized as a grouping variable
if ismember('SubjectName', resultsTable.Properties.VariableNames)
    % Calculate the averages grouped by SubjectName
    groupedResults = varfun(@mean, resultsTable, 'InputVariables', @isnumeric, 'GroupingVariables', 'SubjectName');
else
    error('SubjectName column is missing in resultsTable.');
end

% Save individual results and averages
uniqueSubjects = unique(resultsTable.SubjectName);
for i = 1:length(uniqueSubjects)
    subjectName = uniqueSubjects{i};
    subjectResults = resultsTable(strcmp(resultsTable.SubjectName, subjectName), :);
    subjectAverages = groupedResults(strcmp(groupedResults.SubjectName, subjectName), :);

    % Save individual results
    resultsFilename = fullfile(folderPath, [subjectName, '_CrossCorrelation_Phase_results.csv']);
    writetable(subjectResults, resultsFilename);
    fprintf('Individual results saved to %s\n', resultsFilename);

    % Save averages
    averagesFilename = fullfile(folderPath, [subjectName, '_CrossCorrelation_Phase_averages.csv']);
    writetable(subjectAverages, averagesFilename);
    fprintf('Averages saved to %s\n', averagesFilename);
end

% Save the complete results table for all subjects
overallResultsFilename = fullfile(folderPath, 'Overall_CrossCorrelation_Phase_results.csv');
writetable(resultsTable, overallResultsFilename);
fprintf('Overall results saved to %s\n', overallResultsFilename);
