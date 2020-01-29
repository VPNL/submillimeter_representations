% unpack constants
addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

sessions = constants.sessions;
FSIDs = constants.FSIDs;
preproc_str_hires = constants.preproc_str_hires;
preproc_str_sim2pt4 = constants.preproc_str_sim2pt4;
fmridata_dir = constants.fmridata_dir;
partitions = constants.partitions;
depth_sets = constants.depth_sets;
output_dir = constants.output_dir;

% prepare data structure that will store values
tsnr_struct = struct();
outpath = sprintf('%s/tsnr.mat', output_dir);

% loop over partitions (lateral/medial)
for p = 1:length(partitions)
    partition = partitions{p};
    tsnr_struct.(partition) = zeros(length(sessions), numel(depth_sets));
	fprintf('Partition: %s...\n', partition);

	% loop over sessions 
    for sess_idx = 1:length(sessions)
		session = sessions{sess_idx};
		FSID = FSIDs{sess_idx};
		fprintf('\tSession: %s...\n', session);

		% loop over depths
		for depth_set_idx = 1:numel(depth_sets)
			depths = depth_sets{depth_set_idx};
			fprintf('\t\tDepth Set: %d...\n', depth_set_idx);

			tsnr_struct.(partition)(sess_idx, depth_set_idx) = get_mean_tsnr(...
				session,...
				FSID,...
				fmridata_dir,...
				preproc_str_hires,...
				depths,...
				partition...
			);
		end
    end
end

save(outpath, 'tsnr_struct');
