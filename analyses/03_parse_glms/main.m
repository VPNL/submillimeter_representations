% set RNG seed
rng(0, 'twister');

% unpack constants
addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

sessions = constants.sessions;
FSIDs = constants.FSIDs;
fmridata_dir = constants.fmridata_dir;
partitions = constants.partitions;
output_dir = constants.output_dir;
contrasts = constants.contrasts;
depth_sets = constants.depth_sets;
metrics = constants.metrics;
noise_types = constants.noise_types;
glm_dir = constants.glm_dir;
glm_dir_sim2pt4 = constants.glm_dir_sim2pt4;

% script specific options
mask_thresh = 0.75;
glm_dirs = {glm_dir, glm_dir_sim2pt4};
splits = {'all', 'odd', 'even'};

outpath = sprintf('%s/glm_metrics.mat', output_dir);

data_struct = struct();
for session_idx = 1:length(sessions)
    session = sessions{session_idx};
	session_date = session(1:8);
    FSID = FSIDs{session_idx};
	FSID_session_str = sprintf('%s_%s', FSID, session_date);

    masks = struct();
    for partition_idx = 1:length(partitions)
        partition = partitions{partition_idx};
        masks.(partition) = get_roi_mask(FSID, partition);
    end

    for glm_dir_idx = 1:length(glm_dirs)
        glm_dir = glm_dirs{glm_dir_idx};

		if strcmp('20161006-CVNS001_floc3t', session) && strcmp(glm_dir, 'GLM_vanilla_sim2pt4')
			fprintf('Skipping sim2pt4 for 3t session\n');
			continue;
		end

		for split_idx = 1:length(splits)
			split = splits{split_idx};

			% load glm results
			glm_session_dir = sprintf('%s/%s/%s/results%s', fmridata_dir, session, glm_dir, split);
			[betas, se] = get_betas_se(glm_session_dir);

			for metric_idx = 1:length(metrics)
				metric_struct = metrics{metric_idx};
				metric = metric_struct.name;

				for noise_type_idx = 1:length(noise_types)
					noise_struct = noise_types{noise_type_idx};

					if strcmp(noise_struct.type, 'gaussian')
						if strcmp(glm_dir, 'GLM_vanilla')
							fprintf('Skipping Gaussian noise for hi-res case\n');
							continue;
						end

						if ~metric_struct.primary
							fprintf('Not adding noise for non-primary metric\n');
							continue;
						end
					end

					noise_type = noise_struct.type;
					noise_magnitude = noise_struct.magnitude;

					for partition_idx = 1:length(partitions)
						partition = partitions{partition_idx};

						mask = masks.(partition);
						partition_betas = betas(mask, :, :);
						partition_se = se(mask, :, :);

						for contrast_idx = 1:length(contrasts)
							contrast = contrasts{contrast_idx};
							[con1, con2] = get_con1_con2('floc', contrast);

							for depth = 1:6
								% this result is for a given combo of:
								% session x glm_dir x metric x noise_type x partition x contrast x depth
								fprintf('%s (%s: %s). %s, noise type: %s, %s, %s, depth %d\n',...
									FSID, ...
									glm_dir, ...
									split, ...
									metric, ...
									noise_type, ...
									partition, ...
									contrast, ...
									depth ...
								);

								glm_metric = compute_glm_metric(...
									partition_betas(:, :, depth), ...
									partition_se(:, :, depth), ...
									con1, ...
									con2, ...
									metric ...
								);

								% add noise to metric values
								metric_values{depth} = add_noise(...
									glm_metric, ...
									noise_type, ...
									noise_magnitude ...
								);
							end

							% combine across pseudodepths here
							for depth_set_idx = 1:length(depth_sets)
								depth_set = depth_sets{depth_set_idx};

								depth_set_values = [];
								for d = 1:length(depth_set)
									depth_set_values(:, d) = metric_values{depth_set(d)};
								end

								mean_depth_set_values = mean(depth_set_values, 2);
								data_struct.(FSID_session_str).(glm_dir).(split).(metric).(noise_type).(partition).(contrast)(:, depth_set_idx) = mean_depth_set_values;
							end % depth_set_idx
						end % contrast
					end % partition
				end % noise_type
			end % metric
        end %  split
    end % glm_dir
end % session

save(outpath, 'data_struct');
