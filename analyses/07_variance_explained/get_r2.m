function partition_R2 = get_r2(session, FSID, fmridata_dir, depths, partition, glm_dir, split)
% GET_R2 computes variance explained by the GLM for each depth provided, then averages across depths

	data_dir = sprintf('%s/%s', fmridata_dir, session);
	results_dir = sprintf('%s/%s/results%s', data_dir, glm_dir, split);
	[lh_mask, ~, ~] = cvnroimask(FSID, 'lh', partition, [], 'DENSETRUNCpt');
	[rh_mask, ~, ~] = cvnroimask(FSID, 'rh', partition, [], 'DENSETRUNCpt');
	mask = [lh_mask{1}; rh_mask{1}];

	n_depths = length(depths);
	
	for i = 1:n_depths
	    a = matfile(sprintf('%s/layer%d.mat', results_dir, depths(i)));
	    depth_r2s(:, i) = a.R2;
	    clear a;
	end

	depth_mean = nanmean(depth_r2s, 2);
	partition_R2 = depth_mean(mask);
end
