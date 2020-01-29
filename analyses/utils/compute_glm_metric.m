function metric = compute_glm_metric(betas, se, con1, con2, metric, varargin)
%COMPUTE_GLM_METRIC computes the specified metric for each vertex
%
% Inputs
%    betas (vertices x conditions)
%    se (vertices x conditions)
%    con1 : condition indices for first part of contrast
%    con2 : condition indices for second part of contrast
%    metric : metric to compute

  take_abs = 0;
  if ~isempty(varargin)
      take_abs = varargin{1};
  end
  switch metric
  case 'tstat'
    metric = compute_tstat(betas, se, con1, con2);
  case 'betanorm'
    metric = compute_betanorm(betas, se, con1);
  case 'tnorm'
    metric = compute_tnorm(betas, se, con1);
  case 'beta'
    metric = mean(betas(:,con1),2);
  case 'betasub'
    metric = compute_betasub(betas, con1);
  case 'dprime'
    metric = compute_dprime(betas, se, con1, con2);
  case 'zscore'
    metric = compute_zscore(betas, se, con1);
  case 'znorm'
    metric = compute_znorm(betas, se, con1);
  otherwise
    error('%s is not supported at this time. Bug Eshed about it.', metric);
  end

  if take_abs
      metric = abs(metric);
  end

end

function betasub = compute_betasub(betas, con1)
    meansub = betas - repmat(mean(betas, 2), [1, 10]);
    betasub = mean(meansub(:,con1),2);
end

function betanorm = compute_betanorm(betas, se, con1)

    [n_vertices, n_conditions] = size(betas);

    b1 = mean(betas(:,con1),2);
    squared_betas = betas.^2;
    sum_of_squares = sum(squared_betas,2); % sum along conditions
    betanorm = b1./sqrt(sum_of_squares);

end

function zscore = compute_zscore(betas, se, con1)

    [n_vertices, n_conditions] = size(betas);
	mean_across_conditions = mean(betas, 2);
	std_across_conditions = std(betas, [], 2);

	con1_response = mean(betas(:, con1), 2);
	zscore = (con1_response - mean_across_conditions) ./ std_across_conditions;
end

function znorm = compute_znorm(betas, se, con1)
    [n_vertices, n_conditions] = size(betas);
	mean_across_conditions = mean(betas, 2);
	se_across_conditions = mean(se, 2);

	con1_response = mean(betas(:, con1), 2);
	znorm = (con1_response - mean_across_conditions) ./ se_across_conditions;
end


function dp = compute_dprime(betas, se, con1, con2)

    b1 = betas(:,con1);
    b2 = betas(:,con2);

    se1 = mean(se(:,con1),2);
    se2 = mean(se(:,con2),2);

    b1_mean = mean(b1,2);
    b2_mean = mean(b2,2);

    dp = (b1_mean - b2_mean)./(sqrt(se1 + se2)/2);
end

function t = compute_tstat(betas, se, con1, con2)
    [n_vertices, n_conditions] = size(betas);

    b1 = betas(:,con1);
    b2 = betas(:,con2);

    se1 = mean(se(:,con1),2);
    se2 = mean(se(:,con2),2);

    n1 = length(con1);
    n2 = length(con2);

    b1_mean = mean(b1,2);
    b2_mean = mean(b2,2);

    t = (b1_mean - b2_mean)./sqrt((se1.^2 / n1) + (se2.^2 / n2));
end

function tn = compute_tnorm(betas, se, con1)
    [n_vertices, n_conditions] = size(betas);

    b1 = betas(:,con1);
    se1 = mean(se(:,con1),2);
    n1 = length(con1);
    b1_mean = mean(b1, 2);

    tn = b1_mean./sqrt(se1);
end
