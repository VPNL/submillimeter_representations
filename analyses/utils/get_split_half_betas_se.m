function [betas1, betas2, se1, se2, subject] = get_split_half_betas_se(resultsdir, layer)
% GET_BETAS_SE extracts betas and standard errors for specified GLM results at the given layer
%
% Inputs
%	resultsdir (str) : where to find GLM results
%	layer (int) : which layer to get results for
%
% Eshed Margalit
% August 2017

	a1 = matfile(sprintf([resultsdir '/layer%d.mat'],layer));
	betas = a1.modelmd;
	reps_per_run = a1.reps_per_run;
	subject = a1.FSID;

	[betas1, se1] = compress_condition_split_half(betas,reps_per_run,1:3);
	[betas2, se2] = compress_condition_split_half(betas,reps_per_run,4:6);

end

function [compressed_betas, se] = compress_condition_split_half(betas,reps_per_run,reps_to_use)
% COMPRESS_CONDITION_SPLIT_HALF compresses condition split results matrix
% INPUTS:
% 	betas - beta matrix of form V x (num_conds * reps_per_run), ...
%		where V is the number of vertices
%	reps_per_run - how many repetitions of each condition ...
%		occured in each run; i.e., the condition-split factor
%	reps_to_use - which repetitions to use in the averaging
% OUTPUTS:
%	compressed_betas - compressed betas, of form V x num_conds
%	se - standard error over repetitions, of form V x num_conds

	% get dimensions of input matrix
	[V, C_times_reps_per_run] = size(betas);
	
	% compute number of true (experimental) conditions
	C = C_times_reps_per_run / reps_per_run;

	% for each condition, collapse over repetitions
	for i=1:C
		% determine region of beta matrix pertaining to condition i
		start_idx = (i-1)*reps_per_run + 1;
		end_idx = start_idx + reps_per_run-1;
		subset = betas(:,start_idx:end_idx);
		subset = subset(:,reps_to_use);

		% compute betas and SEM for condition
		compressed_betas(:,i) = mean(subset,2);
		se(:,i) = std(subset,[],2)./sqrt(reps_per_run);
	end
end
