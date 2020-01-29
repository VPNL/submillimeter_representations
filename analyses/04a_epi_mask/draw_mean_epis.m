function draw_mean_epis(dataset, FSID, viewname, viewnumber, clim, outdir)

	layer_sets = {[1,2],[3,4],[5,6]};
	n_layer_sets = numel(layer_sets);

	data_dir = sprintf('/home/stone-ext1/fmridata/%s',...
		dataset);

	base = sprintf('%s/%s', outdir, FSID);
	mkdirquiet(base);

	for i = 1:n_layer_sets
		outname_low = sprintf('%s/lowres_%d.png', base, i);
		outname_high = sprintf('%s/highres_%d.png', base, i);

		if exist(outname_low, 'file') == 2
		    continue;
		end

		layers = layer_sets{i};

		preproc_base = sprintf('%s/preprocessVER1SURF%s',...
			data_dir,FSID);
		[rgbimg, L] = plot_mean_epi(FSID, preproc_base, layers, ...
			'gray', clim, viewnumber,...
			'VTC_anat');

		preproc_base = sprintf('%s/preprocess_sim2pt4_VER1SURF%s',...
			data_dir,FSID);

		[rgbimg2, L2] = plot_mean_epi(FSID, preproc_base, layers, ...
			'gray', clim, viewnumber,...
			'VTC_anat');

		save_im(rgbimg, outname_high, clim);
		save_im(rgbimg2, outname_low, clim);
		
	end

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

function [rgbimg, L] = plot_mean_epi(sub, preproc_base, layers, cmap, clim, view_number, subsample)

	% Set the colormap
	cmap = eval([cmap, '(', num2str(100), ')']);

	hemis = {'lh', 'rh'};
	surfsuffix = 'DENSETRUNCpt';

	mbc = get_mbc(preproc_base, layers);
	mbc = squeeze(mean(mbc,3));

	% load views, specify correct params
	views = get_views();
	view = views{view_number};
	area = view{1};
	surftype = view{2};
	hemiflip = view{3};
	%imageres = view{4};
	imageres = 2000;
	fsaverage0 = view{5};
	xyextent = view{6};

	% get number of vertices in inflated DENSETRUNCpt
	[numlh, numrh] = cvnreadsurface(sub,hemis,'sphere',surfsuffix,...
		'justcount',true);

	% get viewpoint
	if hemiflip 
		hemis = fliplr(hemis);
	end

	viewpt = cvnlookupviewpoint(sub,hemis,area,surftype);

	% setup image params
	dataStruct = struct('data',mbc,'numlh',numlh,'numrh',numrh);

	% draw image and create RGB
	[img, L, rgbimg] = cvnlookupimages(sub,dataStruct,hemis,viewpt,[],'xyextent',xyextent,...
		'surftype',surftype,'imageres',imageres,'cmap',cmap,'clim',clim, 'background',...
		'curv','surfsuffix',surfsuffix,...
		'roiname',{'VTC_lateral','VTC_medial'},'roiwidth',3,'roicolor','w');

end %end fx

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

	bias_struct = matfile(sprintf('%s/meanbiascorrected04.mat',preproc_base));
	bias_data = permute(bias_struct.data, [3,1,2]);
	mbc = bias_data(:,1,layers);

end
