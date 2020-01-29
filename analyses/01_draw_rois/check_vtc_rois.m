function check_vtc_rois(FSID)

	surfsuffix = 'DENSETRUNCpt';
	surftype = 'inflated';
	viewname = 'ventral';

	% get number of vertices in inflated DENSETRUNCpt
	[numlh, numrh] = cvnreadsurface(FSID,{'lh','rh'},'sphere',surfsuffix,...
		'justcount',true);

	valstruct = struct('data',ones(numlh+numrh,1),...
		'numlh',numlh,'numrh',numrh);

	[viewpt, ~, viewhemis] = cvnlookupviewpoint(FSID, {'lh','rh'},...
		viewname, surftype);

	L = [];


	roi_args = {'roiname','VTC*al','roicolor',[0 0 0],'drawroinames',false,...
	    'roiwidth', 0};
	[rawimg, L, rgbimg] = cvnlookupimages(FSID, valstruct, viewhemis, ...
		viewpt, L, 'xyextent', [1 1], 'surftype', surftype, ...
		'surfsuffix', surfsuffix, 'absthreshold', 2, ...
		roi_args{:});

	figure();
	img_handle = imshow(rgbimg);

end
