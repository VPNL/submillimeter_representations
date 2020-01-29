% checks percent difference in R2 in matched index sets across partitions
base = '/home/stone-ext3/eshed/beta_bricks/outputs/r_squared_matched_indices';
mean_val_outpath = sprintf('%s/mean_vals.mat', base);

l = load(mean_val_outpath);
mean_vals = l.mean_vals;

% get difference between lateral and medial in percentages
% partition_diffs_pct = 100 * ((mean_vals(:, :, 1) - mean_vals(:, :, 2))./(mean_vals(:, :, 1)));
partition_diffs = mean_vals(:, :, 1) - mean_vals(:, :, 2);

subject_means = mean(partition_diffs);
subject_sems = std(partition_diffs) ./ sqrt(size(partition_diffs, 1));

depths = {'deep', 'middle', 'superficial'};
for depth = 1:3
	fprintf('Difference in %s: %.6f +/- %.6f\n', depths{depth}, subject_means(depth), subject_sems(depth));
	[h, p, ci, stats] = ttest(partition_diffs(:, depth));
	fprintf('One-sample t-test against 0: t(%d) = %.2f, p = %.4f\n', stats.df, stats.tstat, p);

end
	
