% unpack constants
addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

sessions = constants.sessions;
FSIDs = constants.FSIDs;
fmridata_dir = constants.fmridata_dir;
partitions = constants.partitions;
depth_sets = constants.depth_sets;
output_dir = constants.output_dir;
glm_dir = constants.glm_dir;

splits = {'all', 'odd', 'even'};

% prepare data structure that will store values
r2_struct = struct();
outpath = sprintf('%s/r_squared.mat', output_dir);

% loop over partitions (lateral/medial)
for split_idx = 1:length(splits)
	split = splits{split_idx};
	fprintf('Split: %s...\n', split);

	for partition_idx = 1:length(partitions)
		partition = partitions{partition_idx};
		r2_struct.(split).(partition) = zeros(length(sessions), numel(depth_sets));
		fprintf('\tPartition: %s...\n', partition);

		% loop over sessions 
		for session_idx = 1:length(sessions)
			session = sessions{session_idx};
			if strcmp(session, '20161006-CVNS001_floc3t')
				continue;
			end

			FSID = FSIDs{session_idx};
			fprintf('\t\tSession: %s...\n', session);

			% loop over depths
			for depth_set_idx = 1:numel(depth_sets)
				depths = depth_sets{depth_set_idx};
				fprintf('\t\t\tDepth Set: %d...\n', depth_set_idx);

				partition_r2 = get_r2(...
					session,...
					FSID,...
					fmridata_dir,...
					depths,...
					partition,...
					glm_dir,...
					split...
				);
				r2_struct.(split).(partition)(session_idx, depth_set_idx) = nanmean(partition_r2);
			end
		end
	end
end
save(outpath, 'r2_struct');
