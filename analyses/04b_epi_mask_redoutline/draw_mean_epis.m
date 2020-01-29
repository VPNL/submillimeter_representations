function mask = draw_mean_epis(FSID, clim, depth_sets, outdir, preproc_base, mask_thresh)

	% constant, always use view number 1
	viewnumber = 1;

	for depth_set_idx = 1:length(depth_sets)
		savepath = sprintf('%s/depth_%d.png', outdir, depth_set_idx);
		depths = depth_sets{depth_set_idx};

		if exist(savepath, 'file') == 2
			fprintf('File already exists, skipping\n');
			% continue;
		end

		[rgbimg, mask] = plot_mean_epi(...
			FSID, ...
			preproc_base, ...
			depths, ...
			'gray', ...
			clim, ...
			viewnumber,...
			'VTC_anat', ...
			mask_thresh...
		);
		save_im(rgbimg, savepath, clim);
	end
end


function [rgbimg, under_threshold] = plot_mean_epi(sub, preproc_base, depths, cmap, clim, view_number, subsample, mask_thresh)

	% Set the colormap
	cmap = eval([cmap, '(', num2str(100), ')']);

	% set hemisphere and surface suffix
	hemis = {'lh', 'rh'};
	surfsuffix = 'DENSETRUNCpt';

	mean_bias_corrected_epi = get_mbc(preproc_base, depths);
	mean_bias_corrected_epi = squeeze(mean(mean_bias_corrected_epi, 3));

	% load views, specify correct params
	views = get_views();
	view = views{view_number};
	area = view{1};
	surftype = view{2};
	hemiflip = view{3};
	imageres = 2000;
	fsaverage0 = view{5};
	xyextent = view{6};

	% get number of vertices in inflated DENSETRUNCpt
	[numlh, numrh] = cvnreadsurface(...
		sub, ...
		hemis, ...
		'sphere', ...
		surfsuffix, ...
		'justcount', true ...
	);

	% get viewpoint
	if hemiflip 
		hemis = fliplr(hemis);
	end

	viewpt = cvnlookupviewpoint(sub, hemis, area, surftype);

	% setup image params
	dataStruct = struct('data', mean_bias_corrected_epi, 'numlh', numlh, 'numrh', numrh);
	under_threshold = (mean_bias_corrected_epi < mask_thresh);

	% get lateral/medial masks
	[lh_lateral,  ~,  ~] = cvnroimask(sub, 'lh', 'VTC_lateral', [], surfsuffix);
	[rh_lateral,  ~,  ~] = cvnroimask(sub, 'rh', 'VTC_lateral', [], surfsuffix);
	[lh_medial,  ~,  ~] = cvnroimask(sub, 'lh', 'VTC_medial', [], surfsuffix);
	[rh_medial,  ~,  ~] = cvnroimask(sub, 'rh', 'VTC_medial', [], surfsuffix);

	lateral_mask = cat(1, lh_lateral{1}, rh_lateral{1});
	medial_mask = cat(1, lh_medial{1}, rh_medial{1});

	% draw image and create RGB
	[img,  L,  rgbimg] = cvnlookupimages(...
		sub, ...
		dataStruct, ...
		hemis, ...
		viewpt, ...
		[], ...
		'xyextent', xyextent, ...
		'surftype', surftype, ...
		'imageres', imageres, ...
		'cmap', cmap, ...
		'clim', clim, ...
		'background', 'curv', ...
		'surfsuffix', surfsuffix, ...
		'roimask', {lateral_mask,  medial_mask,  under_threshold}, ...
		'roiwidth', {3,  3,  1}, ...
		'roicolor', {'w', 'w', 'r'}...
	);
end 

% from cvnvisualizeanatomicalresults.m
function allviews = get_views()
	allviews = { ...
	  {'ventral'        'inflated'                 1  500    0         [1 1]} ...
	  {'ventral'        'sphere'                   0 1000    0         [1 1]} ...
	  {'occip'          'sphere'                   0 1000    0         [1 1]} ...
	  {'occip'          'inflated'                 0  500    0         [1 1]} ...
	  {'parietal'       'inflated'                 0  500    0         [1 1]} ...
	  {'medial'         'inflated'                 0  500    0         [1 1]} ...
	  {'lateral'        'inflated'                 0  500    0         [1 1]} ...
	  {'medial-ventral' 'inflated'                 0  500    0         [1 1]} ...
	  {'ventral'        'gVTC.flat.patch.3d'       1 2000    0         [160 0]} ...   % 12.5 pixels per mm
	  {''               'gEVC.flat.patch.3d'       0 1500    0         [120 0]} ...   % 12.5 pixels per mm
	};
end

function [mbc] = get_mbc(preproc_base, layers)

	bias_struct = matfile(sprintf('%s/meanbiascorrected04.mat', preproc_base));
	bias_data = permute(bias_struct.data,  [3, 1, 2]);
	mbc = bias_data(:, 1, layers);

end

function save_im(rgbimg, outname, clim)

		figure;
		imshow(rgbimg);
		colormap(gray(100));
		h = colorbar;
		set(h,'Location','southoutside');
		set(h,'xlim',[1,100]);
		set(h,'xtick',linspace(1,100,11));
		set(h,'xticklabel',linspace(clim(1),clim(2),11));
		set(h,'FontSize',16);

		level = 0.75;
		loc = level / clim(2) * 100;
		line('parent',h,'ydata',[-5,5],'xdata',[loc, loc],'color','r','LineWidth',3);
		set(gcf,'Color','w');
		export_fig(outname);
		close all;

end

