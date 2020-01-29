function [betas, se, subject] = get_betas_se(glm_session_dir)
% GET_BETAS_SE extracts betas and standard errors for specified GLM results at the given depth
%
% Inputs
%	glm_session_dir (str) : where to find GLM results
%
% Eshed Margalit
% September 2019

	
	for depth = 1:6
		a1 = matfile(sprintf('%s/layer%d.mat', glm_session_dir, depth));
		betas(:, :, depth) = a1.modelmd;
		se(:, :, depth) = a1.modelse;
		clear a1;
	end

end
