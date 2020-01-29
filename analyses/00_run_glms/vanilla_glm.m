function vanilla_glm(data_dir, output_dir_name, FSID, runs, cutoffs, tr, stimdur, preproc_str)
% vanilla_glm runs standard GLM
% NOTES
% 	1. No condition splitting, a single beta is estimated per category per run
% 	2. Canonical HRF is assumed
% 	3. Expects that a designmatrix.mat file already exists in the data_dir or
%      the mat_files_from_scan dir. See `write_design_matrices.m` in this
%      directory for more details
% 	4. This script handles both the hi-res 0.8mm prep and the sim2pt4 prep, specify data
%		source with `preproc_str` input
%
% INPUTS
%	data_dir: name of session directory (e.g., 
%   	'/home/stone-ext1/fmridata/20160212-ST001-E002')
%	output_dir_name: where to write GLM outputs (e.g., 'GLMCS_floc_assume')
%	FSID: FreeSurfer ID for subject (e.g., 'C1051')
%	runs: array of scalar values indicating which runs to process (e.g.,
%   	1:12, [1:3, 5:12]);
%	cutoffs: how many TRs to use from each run (same size as runs) (e.g.,
%   	repmat(158,[1,12]))
%	tr: the preprocessed TR (e.g., 2.0)
%	stimdur: stimulus duration in seconds (e.g., 4.0)
%	preproc_str: where to find the actual data files, e.g., 'preprocessVER1SURF'

	%% Set draw function for GLMdenoisedata
	% Get viewpoint	
	hemis = {'lh','rh'};
	viewpt = cvnlookupviewpoint(FSID, hemis, 'occip', 'sphere');

	% Get number of vertices in left and right hemisphere
	[numlh, numrh] = cvnreadsurface(FSID, hemis, 'sphere', 'DENSETRUNCpt', ...
		'justcount', true);

	% Set empty value struct
	valstruct = struct('data', zeros(numlh+numrh, 1), 'numlh', numlh, ...
		'numrh', numrh);
	[~ , Lookup] = cvnlookupimages(FSID, valstruct, hemis, viewpt, [], ...
		'xyextent', [1 1]);
	cathemis = @(v)spherelookup_vert2image(struct('numlh', numlh, 'numrh', ...
		numrh, 'data', v(:, 1)), Lookup, nan);
	opt.drawfunction = @(vals)cathemis(vals(:));

	% Which runs go into each split in split_names?
	%     put all odd runs (that are present in the `runs` argument) in odd_runs, 
	%     repeat for evens
	[odd_runs, even_runs, odd_run_indices, even_run_indices] = get_odd_even_runs(runs);

	split_names           = {'all',          'odd',           'even'   };
	runs_per_split        = {runs,           odd_runs,        even_runs};
	run_indices_per_split = {1:length(runs), odd_run_indices, even_run_indices};

	%% loop over each split
	for split_num = 1:length(split_names) 
		split_name = split_names{split_num};
		fprintf('Beginning split: %s\n', split_name);

		runs_to_use = runs_per_split{split_num};
		run_indices_to_use = run_indices_per_split{split_num};
		fprintf('Using runs:\n');
		disp(runs_to_use);

		% loop over all layers
		for layer_num = 1:6
			fprintf('Processing layer: %d\n', layer_num);

			layer_result_fname = sprintf('%s/%s/results%s/layer%d.mat', ...
				data_dir, output_dir_name, split_names{split_num}, layer_num);
		
			if(exist(layer_result_fname))
				fprintf('GLM for layer %.0f already run, skipping layer\n', ...
					layer_num);
				continue;
			end

			% empty cell array to hold data from each run 
			data = {};

			% loop over each run
			for run_index = 1:length(runs_to_use) % for each run in the given split
				current_run = runs_to_use(run_index);
				fprintf('Loading data for run %d\n', current_run);

				% load the preprocessed surface data for that run
				a1 = matfile(sprintf([data_dir '/%s%s/run%02d.mat'],...
					preproc_str, FSID, current_run));

				% Permute data to be Vertices x TR x Layer
				data{run_index} = permute(single(a1.data(:, layer_num, :)),...
					[3 1 2]);

				% clear memory
				clear a1;
			end
			fprintf('All data loaded.\n\n');

			% load design matrix (from datadir or mat_files_from_scan)
			designmatfile = [data_dir '/designmatrix.mat'];
			if (exist(designmatfile) == 2)
				designmatrices = load(designmatfile);
			else
				designmatfile = [data_dir '/mat_files_from_scan/designmatrix.mat'];
				designmatrices = load(designmatfile);
			end
			
			% this is a cell array with an entry for each run that was used
			design = designmatrices.stimulus;
			fprintf('Loaded design matrix array with %d valid runs\n', length(design));

			% pick runs of design
			design = design(run_indices_to_use);
			fprintf('Using run indices:\n');
			disp(run_indices_to_use);
			fprintf('New design matrix array has %d runs\n', length(design));

			% truncate the end of the data
			for run_index=1:length(data)
				data{run_index} = data{run_index}(:, 1:cutoffs(run_index));
			end

			% define output path
			outpath = sprintf('%s/%s', data_dir, output_dir_name);
			mkdirquiet(sprintf('%s/figures%s', outpath, split_names{split_num}));
			mkdirquiet(sprintf('%s/results%s', outpath, split_names{split_num}));

			% no PCs (this is what makes it vanilla)
			opt.numpcstotry = 0;

			% call GLMdenoisedata
			figure_path = sprintf('%s/figures%s/layer%d', outpath, split_names{split_num}, layer_num);
			results = GLMdenoisedata(...
				design,...
				data,...
				stimdur,...
				tr, ...
			       'assume',...
			       [],...
			       opt,  ...
			       figure_path...
			);

			% save results after removing "models" field (very big) and modelse (which we won't use anyway)
			results = rmfield(results, {'models'});
			results.inputs.opt.drawfunction = [];

			% add FreeSurfer ID, and data_dir to results
			results.FSID = FSID;
			results.data_dir = data_dir;

			% convert modelmd and modelse to two separate fields, each (one for model and one for HRF)
			md = results.modelmd;
			results.modelmd = md{2};
			results.modelmd_hrf = md{1};

			se = results.modelse;
			results.modelse = se{2};
			results.modelse_hrf = se{1};
			
			% save results for that layer
			save_path = sprintf('%s/results%s/layer%d.mat', outpath, split_name, layer_num)
			save(save_path, '-struct', 'results', '-v7.3');
			clear results;
		end % layer loop
	end % split loop
end % fn

function [odd_runs, even_runs, odd_run_indices, even_run_indices] = get_odd_even_runs(runs)
	odds = 1:2:12;
	evens = 2:2:12;
	odd_runs = [];
	even_runs = [];

	odd_run_indices = [];
	even_run_indices = [];

	for i = 1:length(runs)
		if ismember(runs(i), odds)
			odd_runs = [odd_runs; runs(i)];
			odd_run_indices = [odd_run_indices; i];
		elseif ismember(runs(i), evens)
			even_runs = [even_runs; runs(i)];
			even_run_indices = [even_run_indices; i];
		end
	end
end
