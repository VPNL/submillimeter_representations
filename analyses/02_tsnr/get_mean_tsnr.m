function mean_tsnr = get_mean_tsnr(session, FSID, fmridata_dir, preproc_str, depths, partition)
% GET_MEAN_TSNR computes tsnr for a given partition and depth by averaging over vertices, then over runs

	data_dir = sprintf('%s/%s', fmridata_dir, session);
	[lh_mask, ~, ~] = cvnroimask(FSID, 'lh', partition, [], 'DENSETRUNCpt');
	[rh_mask, ~, ~] = cvnroimask(FSID, 'rh', partition, [], 'DENSETRUNCpt');
	mask = [lh_mask{1}; rh_mask{1}];

	tsnr_by_run = zeros(12,1);
	for run = 1:12
		raw_timecourse = sprintf('%s/%s%s/run%02d.mat', data_dir, preproc_str, FSID, run);
		assert(exist(raw_timecourse, 'file')==2);

		% load data
		load_struct = matfile(raw_timecourse);
		data = load_struct.data; % timepoints x depths x vertices
		% Of interest: cannot load only part of the data variable because indices from find(mask == 1)
		% do not increase in equal spacing, so I'll load everything and then mask 
		
		% mask out irrelevant vertices
		data = data(:, depths, mask);

		n_depths = size(data, 2);
		n_vert = size(data, 3);
		data = reshape(data, [size(data, 1), (n_depths * n_vert)]); % timepoints x all vertices
		data = single(data);

		% compute mean and std over timepoints
		tseries_means = mean(data);
		tseries_stds = std(data);
		tsnr = tseries_means ./ tseries_stds;

		% get the tsnr for this run as mean over all vertices
		tsnr_by_run(run) = nanmean(tsnr(:));
	end

	% finally, average tsnr across runs
	mean_tsnr = mean(tsnr_by_run);
end
