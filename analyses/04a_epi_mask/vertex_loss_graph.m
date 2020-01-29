function vertex_loss_graph(datasets, FSIDs, mask_threshes, mask_base, outdir)

    outpath = sprintf('%s/vertex_loss.png', outdir);

    n_datasets = numel(datasets);
    n_threshes = length(mask_threshes);

    retentions = zeros(n_datasets,n_threshes);

    for i = 1:n_datasets
        fprintf('---Computing loss for %s\n', FSIDs{i});
        for j = 1:n_threshes
            retentions(i,j) = count_vertex_retained(datasets{i},...
                            FSIDs{i},...
                            mask_threshes(j),...
                            mask_base);
    	end
    end

    losses = 1 - retentions;
    plot_losses(losses, mask_threshes);
    export_fig(outpath);
    close all;

end

function retained = count_vertex_retained(dataset, FSID, thresh, mask_base);

	hemis = {'lh','rh'};

	preproc_base = sprintf('/home/stone-ext1/fmridata/%s/%s%s',...
	    dataset,...
	    mask_base,...
	    FSID);

	bias_struct = matfile(sprintf('%s/meanbiascorrected04.mat',preproc_base));
	bias_data = permute(bias_struct.data,[3 1 2]);

	n_vertices = size(bias_data, 1);

	mask = ones(n_vertices, 1);
	nan_mask = ones(n_vertices,1);

	for layer = 1:6
	    mb = bias_data(:,1,layer);

	    nan_passing = (isnan(mb));
	    nan_mask = nan_mask .* nan_passing;

	    passing = (mb >= thresh);
	    mask = mask .* (mb >= thresh);
	end

	retained = sum(mask)/(n_vertices-sum(nan_mask));
end

function plot_losses(losses, threshes)


    X = mean(losses,1);
    stds = std(losses, [], 1);
    err = stds./sqrt(size(losses,1));

    for i=1:length(threshes)
	fprintf('%.2f +/- %.2f%% of vertices lost at threshold %.2f\n', X(i), err(i), threshes(i));
    end

    figure();

    hb = bar(X);

    set(hb(1), 'FaceColor', 'w');
    set(hb(1), 'EdgeColor', 'k');
    set(hb(1), 'LineWidth', 2);

    % error bar plotting
    hold on;
    errorbar(1:length(X), X, err, 'k.',...
		    'LineWidth',2);

    ylim([0,1]);
    ylabel('Proportion of Vertices Remaining');
    xlabel('Mean EPI Threshold');
    set(gca,'XTickLabel', threshes);
    set(gcf, 'Color','w');

end
