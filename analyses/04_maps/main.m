% unpack constants
addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

sessions = constants.sessions;
FSIDs = constants.FSIDs;
fmridata_dir = constants.fmridata_dir;
output_dir = constants.output_dir;
figure_dir = constants.figure_dir;
contrasts = constants.contrasts;
preproc_str_hires = constants.preproc_str_hires;
metrics = constants.metrics;
noise_types = constants.noise_types;
glm_dir = constants.glm_dir;
glm_dir_sim2pt4 = constants.glm_dir_sim2pt4;

% set mask_thresh to be 0 so we see the whole map
mask_thresh = 0;

% script-specific options
glm_dirs = {glm_dir, glm_dir_sim2pt4};

% set params that are universal to all maps
params = struct(...
	'split', 'all', ...
	'mask_thresh', mask_thresh, ...
	'mask_base', preproc_str_hires, ...
	'viewname', 'vInf', ...
	'viewnumber', 1 ...
);

fprintf('Loading data...\n');
data_struct = load(sprintf('%s/glm_metrics.mat', output_dir));
data_struct = data_struct.data_struct;
fprintf('Loaded.\n');

for metric_idx = 1:length(metrics)
	metric_struct = metrics{metric_idx};

	if ~metric_struct.primary
		continue
	end
	params.metric_name = metric_struct.name;
	params.clim = metric_struct.clim;
	params.cmap = metric_struct.cmap;

	for glm_dir_idx = 1:length(glm_dirs)
		glm_dir = glm_dirs{glm_dir_idx};

		params.glm_dir = glm_dir;

		for noise_type_idx = 1:length(noise_types)
			noise_struct = noise_types{noise_type_idx};

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

			params.noise_type = noise_struct.type;
			params.noise_magnitude = noise_struct.magnitude;

			for session_idx = 1:length(sessions)
				session = sessions{session_idx};
				FSID = FSIDs{session_idx};
				session_date = session(1:8);
				FSID_session_str = sprintf('%s_%s', FSID, session_date);

				if strcmp('20161006-CVNS001_floc3t', session) && strcmp(glm_dir, 'GLM_vanilla_sim2pt4')
					fprintf('Skipping sim2pt4 for 3t session\n');
					continue;
				end

				params.session = session;
				params.FSID = FSID;
				params.FSID_session_str = FSID_session_str;

				for contrast_idx = 1:length(contrasts)
					contrast = contrasts{contrast_idx};

					params.contrast = contrast;

					% construct output path
					outdir = sprintf('%s/04_maps/%s/%s/%s', ...
						figure_dir, ...
						noise_struct.type, ...
						glm_dir, ...
						metric_struct.name ...
					);
						
					% create output directory, recursively
					mkdirsquiet(outdir);

					data = data_struct.(FSID_session_str).(glm_dir).all.(metric_struct.name).(noise_struct.type).VTC_anat.(contrast);
					save_maps_at_each_depth(data, params, outdir);
				end
			end
		end
	end
end
