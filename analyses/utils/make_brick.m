function brick = make_brick(FSID, preproc_base, results_dir, contrast_str, metric, subsample, biasmask, beta_arr, se_arr, hemi, matched_indices)
% MAKE_BRICK generates m x n x 6 brick for given contrast and metric
%
% Inputs
%	FSID (str): FreeSurfer ID
%	results_dir (str) : directory with GLM outputs to use 
%	contrast_str (str) : like 'facesVSall'. 
%	metric (str) : method for computing the glm metric 
%	subsample (str): if not '', indicates the ROI to subsample to 
%	biasmask (float): cutoff for biasmask (if 0, does not mask) 
%	matched_indices (struct): optional, if not empty, fields 'lateral'
%		and 'medial' further restrict anatomical rois
%	
%
% Notes
%	Workhorse function call is of the form:
%		layer_values = compute_glm_metric(layer_betas, layer_SEs, con1, con2, metric, 2);
% Eshed Margalit
% August 2017

	%% Create full brick
	layers = 1:6;

	[con1, con2] = get_con1_con2('floc', contrast_str);
	[numlh, numrh] = cvnreadsurface(FSID, {'lh','rh'}, 'sphere', 'DENSETRUNCpt','justcount',true);

	n_vertices = numlh + numrh;
	brick = zeros(n_vertices,length(layers));

	for layer = layers
		brick(:, layer) = em_compute_glm_metric(beta_arr{layer}, se_arr{layer},...
			con1, con2, metric);
	end
	
	if ~strcmp(subsample,'none')
		%fprintf('\nSubsampling to %s\n', subsample);
		div = sprintf('VTC_%s', subsample);
		[lh_mask, ~, ~] = cvnroimask(FSID, 'lh', div, [], 'DENSETRUNCpt');
		[rh_mask, ~, ~] = cvnroimask(FSID, 'rh', div, [], 'DENSETRUNCpt');
		lh_roimask = lh_mask{1};
		rh_roimask = rh_mask{1};

		switch hemi
		case 'both'
			mask = [lh_roimask; rh_roimask];
		case 'lh'
			mask = [lh_roimask; rh_roimask.*0];
		case 'rh'
			mask = [lh_roimask.*0; rh_roimask];
		otherwise
			error('Choose ''lh'' or ''rh'' or ''both''');
		end
	end
	n_anat = sum(mask);

	% if matched indices are provided, use those instead
	if ~isempty(fieldnames(matched_indices))
		roi_indices = find(mask);
		matched_ind = matched_indices.(subsample);
		matched_roi_ind = roi_indices(matched_ind);

		% reset mask to zeros
		mask = zeros(size(mask));
		mask(matched_roi_ind) = 1;
	end
	fprintf('%s %s %d\n', FSID, subsample, sum(mask));


	n_masked = 0;
	if biasmask
		bmask = get_biasmask(preproc_base, {'lh','rh'}, biasmask);
		mask = mask & bmask;
	end
	n_masked = sum(mask);

	% apply the mask
	sampled = brick(mask,:);
	brick = denan(sampled);

	%fprintf('Masked out %.2f%% of vertices\n', 100-(n_masked/n_anat)*100);

end

function mask = get_biasmask(preproc_base, hemis, thresh)
	bias_struct = matfile(sprintf('%s/meanbiascorrected04.mat',preproc_base));
	bias_data = permute(bias_struct.data,[3 1 2]);

	n_vertices = size(bias_data, 1);
	mask = ones(n_vertices, 1);

	mean_bias_corrected = cell(1,6);

	for layer = 1:6
	    mb = bias_data(:,1,layer);
	    mean_bias_corrected{layer} = mb; 
	    mask = mask .* (mb > thresh);
	end
end

function brick = denan(sampled)

	n_nan = sum(sum(isnan(sampled)));

	if n_nan > 10
		warning('Found %d NaNs. Watch out!', n_nan);
	end

	sampled(isnan(sampled))=0;
	brick = sampled;
end

