function draw_vtc_roi(dataset, FSID, roiname)

	surfsuffix = 'orig'; % DENSTRUNCpt
	surfsuffix = 'DENSETRUNCpt';
	surftype='sphere'; % inflated
	viewname='occip';

	% get valid vertices
	valid = loadmulti(sprintf(['/home/stone-ext1/fmridata/%s/preprocessVER1SURF%s/valid.mat'],...
	    dataset, FSID),'data');
	n_layers = size(valid,2);
	valid_mask = ones(size(valid,3),1);
	for i = 1:n_layers
	    valid_mask = valid_mask.*squeeze(valid(1,i,:));
	end

	% get the viewpoint
	[viewpt, ~, viewhemis] = cvnlookupviewpoint(FSID,...
		{'lh','rh'}, viewname, surftype);

	L = [];

	% get number of vertices in inflated DENSETRUNCpt
	[numlh, numrh] = cvnreadsurface(FSID,{'lh','rh'},'sphere',surfsuffix,...
		'justcount',true);

	valstruct = struct('data',ones(numlh+numrh,1).*valid_mask,...
		'numlh',numlh,'numrh',numrh);


	[rawimg, L, rgbimg] = cvnlookupimages(FSID, valstruct, viewhemis, ...
		viewpt, L, 'xyextent', [1 1], 'surftype', surftype, ...
		'surfsuffix', surfsuffix, 'absthreshold', 0, 'overlayalpha', ones(numlh+numrh,1)*.5);

	% plot image
	figure();
	img_handle = imshow(rgbimg);

	% draw ROI
	[mask, ~, roihemi] = drawroipoly(img_handle, L);
	roistruct = setfield(valstruct,'data',mask);

	% save ROI
	subdir = sprintf('%s/../new_rois/%s',pwd,FSID);
	mkdirquiet(subdir);
	cvnwritemgz(FSID, roiname, valstruct_getdata(roistruct,roihemi),...
		roihemi, subdir);

	% show the user what we made
	surftype = 'inflated';
	viewname = 'ventral';

	[viewpt, ~, viewhemis] = cvnlookupviewpoint(FSID, {'lh','rh'},...
		viewname, surftype);

	L = [];

	[rawimg, L, rgbimg] = cvnlookupimages(FSID, valstruct, viewhemis, ...
		viewpt, L, 'xyextent', [1 1], 'surftype', surftype, ...
		'surfsuffix', surfsuffix, 'absthreshold', 2, ...
		'roimask', mask);

	figure();
	img_handle = imshow(rgbimg);

end
