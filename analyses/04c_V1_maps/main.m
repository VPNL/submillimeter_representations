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
glm_dir = constants.glm_dir_nesting_doll;

% nruns per subject
nruns = [12, 11, 12, 12, 12, 10, 12, 12];

% set mask_thresh to be 0 so we see the whole map
mask_thresh = 0;

% set params that are universal to all maps
params = struct(...
	'mask_thresh', mask_thresh, ...
	'mask_base', preproc_str_hires, ...
	'viewnumber', 4 ...
);

fprintf('Loading data...\n');
data_struct = load(sprintf('%s/glm_metrics_nesting_doll_with_hOc1.mat', output_dir));
data_struct = data_struct.data_struct;
fprintf('Loaded.\n');

for metric_idx = 1:length(metrics)
	metric_struct = metrics{metric_idx};

	params.metric_name = metric_struct.name;
	params.clim = metric_struct.clim;
	params.cmap = metric_struct.cmap;
	params.glm_dir = glm_dir;
	params.noise_type = 'none';
	params.noise_magnitude = 0.0;

	for session_idx = 1:length(sessions)
		session = sessions{session_idx};
		FSID = FSIDs{session_idx};
		session_date = session(1:8);
		FSID_session_str = sprintf('%s_%s', FSID, session_date);
		nruns_str = sprintf('nruns_%d', nruns(session_idx));

		params.session = session;
		params.FSID = FSID;

		for contrast_idx = 1:length(contrasts)
			contrast = contrasts{contrast_idx};

			params.contrast = contrast;

			% construct output path
			outdir = sprintf('%s/04c_V1_maps/none/%s/%s', ...
				figure_dir, ...
				glm_dir, ...
				metric_struct.name ...
			);

			% create output directory, recursively
			mkdirsquiet(outdir);

			data = data_struct.(FSID_session_str).GLM_nesting_doll.all.(nruns_str).(metric_struct.name).none.hOc1.(contrast);
			save_maps_at_each_depth(data, params, outdir);
		end
	end
end
