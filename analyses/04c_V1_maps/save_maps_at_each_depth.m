function save_maps_at_each_depth(data, params, outdir)
% SAVE_MAPS_AT_EACH_DEPTH draws and saves inflated ventral contrast maps for a given dataset at each cortical depth 
% INPUTS
%   data (V x n_depths)
%	params (struct)
% 		example: 
%			mask_thresh: 0
%			mask_base: 'preprocessVER1SURF'
%			viewnumber: 1
%			data_path: '/home/stone/eshed/beta_bricks/outputs/glm_metrics.mat'
%			metric_name: 'tstat'
%			clim: [-7 7]
%			cmap: 'cmapsign4'
%			glm_dir: 'GLM_vanilla'
%			noise_type: 'gaussian'
%			noise_magnitude: 3.5
%			session: '20160212-ST001-E002'
%			FSID: 'C1051'
%			contrast: 'numberVSall'
%
%	outdir (str) - where to save the images
%
% RETURNS
%	none
%
% EM 04/2018
% EM 09/2019 - reworked to take a single params dict and data vector. Better, simpler, faster!

	num_depths = size(data, 2);

    for depth_idx = 1:num_depths
		depth_data = data(:, depth_idx);

		savepath = sprintf('%s/%s_%s_depth_%d.png', ...
			outdir, ...
			params.FSID, ...
			params.contrast, ...
			depth_idx ...
		);

		if exist(savepath, 'file') == 2
			fprintf('File exists, skipping!\n');
			continue;
		end

		% generate image
		[img, L] = plot_vals_with_mask(...
			params.session, ...
			params.FSID, ...
			depth_data, ...
			params.cmap, ...
			params.clim, ...
			params.viewnumber, ...
			'hOc1',...
			params.mask_thresh, ...
			params.mask_base ...
		);

		% save image
		save_im(img, params.cmap, params.clim, params.metric_name, savepath);
    end
end

function save_im(im, cmap, clim, metric, savepath)
% SAVE_IM saves the cortical map image to the indicated path
    figure;
    imshow(im);
	cmap = eval([cmap, '(', num2str(100), ')']);
    colormap(cmap);

    h = colorbar;
    set(h, 'FontSize', 15);
    set(h, 'Location', 'southoutside');
    set(h, 'xlim', [1, 100]);
    set(h, 'xtick', linspace(1, 100, 11));
    set(h, 'xticklabel', linspace(clim(1), clim(2), 11));

    set(gcf, 'Color', 'w');
    export_fig(savepath);
    close all;
end
