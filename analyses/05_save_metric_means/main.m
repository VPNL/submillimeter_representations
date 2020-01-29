% unpack constants
addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

mask_threshes = [0, .75];

% script-specific options
glm_dir = constants.glm_dir;

% load data
fprintf('Loading GLM data...\n');
data_struct = load(sprintf('%s/glm_metrics.mat', constants.output_dir));
data_struct = data_struct.data_struct;
fprintf('Loaded.\n');

fprintf('Loading mask data...\n');
mask_struct = load(sprintf('%s/masks.mat', constants.output_dir));
mask_struct = mask_struct.mask_struct;
fprintf('Loaded.\n');

outpath = sprintf('%s/metric_means.mat', constants.output_dir);

corrmats = struct();
noise_struct = constants.noise_types{2}; % no noise


means = struct();
for metric_idx = 1:length(constants.metrics)
    metric_struct = constants.metrics{metric_idx};
    fprintf('Metric: %s\n', metric_struct.name);

	for partition_idx = 1:length(constants.partitions)
		partition = constants.partitions{partition_idx};
		fprintf('\t\t\tPartition: %s\n', partition);

		for session_idx = 1:length(constants.sessions)
			session = constants.sessions{session_idx};
			session_date = session(1:8);
			FSID = constants.FSIDs{session_idx};
			FSID_session_str = sprintf('%s_%s', FSID, session_date);
			fprintf('\t\t\t\tFSID_Session: %s\n', FSID_session_str);

			for thresh_idx = 1:length(mask_threshes)
				mask_thresh = mask_threshes(thresh_idx);
				mask_thresh_str = sprintf('thr_%d', ...
					ceil(mask_thresh * 100));
				fprintf('\t\t\t\t\tThreshold: %s\n', mask_thresh_str);
				mask = mask_struct.(FSID).(mask_thresh_str);

				% create a new mask that is restricted to partition
				VTC_partition_mask = restrict_EPI_mask(...
					FSID, ...
					partition, ...
					mask...
				);

				for contrast_idx = 1:length(constants.contrasts)
					contrast = constants.contrasts{contrast_idx};

					data = data_struct.(FSID_session_str).(glm_dir).all.(metric_struct.name).(noise_struct.type).(partition).(contrast);

					masked_data = data(~VTC_partition_mask, :); % V x 3
					abs_masked_data = abs(masked_data);

					means.(FSID_session_str).(glm_dir).(metric_struct.name).(partition).(contrast).noabs = mean(masked_data);
					means.(FSID_session_str).(glm_dir).(metric_struct.name).(partition).(contrast).abs = mean(abs_masked_data);
				end
			end
		end
	end
end

save(outpath, 'means');
