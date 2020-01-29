function write_design_matrices(runs,data_dir,subject,nTRs,TR,onset_delay)

	nRuns = length(runs);
	stimulus = cell(1,nRuns);

	for run_idx = 1:nRuns
		run = runs(run_idx);

		data_file = sprintf('%s/preprocessVER1SURF%s/run%02d.mat', data_dir,subject, run);
		stim_file = matchfiles(sprintf('%s/mat_files_from_scan/data/*_run%d.mat', data_dir, run));
		stim_file = stim_file{1};		

		stimulus{run_idx} = sparse(double(make_design_matrix(stim_file, 314, 1, 12)));

	end

	%outname = sprintf('%s/mat_files_from_scan/designmatrix.mat',data_dir)
	outname = sprintf('%s/designmatrix.mat', data_dir)
	save(outname, 'stimulus');

end

function d_mat = make_design_matrix(run_str, num_TR, design_TR, stimulus_delay)
% MAKE_DESIGN_MATRIX makes design matrix out of run string


	tvol = [0:num_TR-1] * design_TR;

	P = load(run_str);
	T = P.theSubject.trials;

	D_stim = zeros(numel(T.block),11);
	D_stim(sub2ind(size(D_stim),1:size(D_stim,1),T.cond+1)) = 1;
	D_stim = D_stim(:,2:end);
	D_tr = interp1(T.onset+stimulus_delay,D_stim,tvol,'linear');
	D_tr(isnan(D_tr)) = 0;

	d_mat = diff([zeros(1,size(D_tr,2)); D_tr])>0;
	    
end
