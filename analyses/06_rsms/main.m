% unpack constants
addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

mask_threshes = [0, .75];

% script-specific options
glm_dirs = {constants.glm_dir, constants.glm_dir_sim2pt4};

% load data
fprintf('Loading GLM data...\n');
data_struct = load(sprintf('%s/glm_metrics.mat', constants.output_dir));
data_struct = data_struct.data_struct;
fprintf('Loaded.\n');

fprintf('Loading mask data...\n');
mask_struct = load(sprintf('%s/masks.mat', constants.output_dir));
mask_struct = mask_struct.mask_struct;
fprintf('Loaded.\n');

outpath = sprintf('%s/corrmats.mat', constants.output_dir);

corrmats = struct();
for metric_idx = 1:length(constants.metrics)
    metric_struct = constants.metrics{metric_idx};
    fprintf('Metric: %s\n', metric_struct.name);

    for glm_dir_idx = 1:length(glm_dirs)
        glm_dir = glm_dirs{glm_dir_idx};
        fprintf('\tGLM Dir: %s\n', glm_dir);

        for noise_type_idx = 1:length(constants.noise_types)
            noise_struct = constants.noise_types{noise_type_idx};
            fprintf('\t\tNoise type: %s\n', noise_struct.type);

            if strcmp(noise_struct.type, 'gaussian')
                if strcmp(glm_dir, 'GLM_vanilla')
                    fprintf('Skipping Gaussian noise for hi-res case\n');
                    continue;
                end
                if ~metric_struct.primary
                    fprintf('Not adding noise for non-primary case\n');
                    continue;
                end
            end


            for partition_idx = 1:length(constants.partitions)
                partition = constants.partitions{partition_idx};
                fprintf('\t\t\tPartition: %s\n', partition);

                for session_idx = 1:length(constants.sessions)
                    session = constants.sessions{session_idx};
					session_date = session(1:8);
                    FSID = constants.FSIDs{session_idx};
					FSID_session_str = sprintf('%s_%s', FSID, session_date);
                    fprintf('\t\t\t\tFSID_Session: %s\n', FSID_session_str);

					if strcmp('20161006-CVNS001_floc3t', session) && strcmp(glm_dir, 'GLM_vanilla_sim2pt4')
						fprintf('Skipping sim2pt4 for 3t session\n');
						continue;
					end


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

                        odd_data_by_contrast = cell(length(constants.contrasts), 1);
                        even_data_by_contrast = cell(length(constants.contrasts), 1);

                        for contrast_idx = 1:length(constants.contrasts)
                            contrast = constants.contrasts{contrast_idx};

                            odd_data = data_struct.(FSID_session_str).(glm_dir).odd.(metric_struct.name).(noise_struct.type).(partition).(contrast);
                            even_data = data_struct.(FSID_session_str).(glm_dir).even.(metric_struct.name).(noise_struct.type).(partition).(contrast);

                            masked_odd_data = odd_data(~VTC_partition_mask, :);
                            masked_even_data = even_data(~VTC_partition_mask, :);

                            odd_data_by_contrast{contrast_idx} = masked_odd_data';
                            even_data_by_contrast{contrast_idx} = masked_even_data';
                        end

                        features_odd = vertcat(odd_data_by_contrast{:, :}); % units x 30
                        features_even = vertcat(even_data_by_contrast{:, :}); % units x 30

                        corrmat = corr(features_odd', features_even');
                        corrmat = flip_and_average_corrmat(corrmat);
                        corrmat = mirror_corrmat(corrmat);

                        corrmats.(FSID_session_str).(glm_dir).(metric_struct.name).(noise_struct.type).(partition).(mask_thresh_str) = corrmat;
                    end
                end
            end
        end
    end
end

save(outpath, 'corrmats');
