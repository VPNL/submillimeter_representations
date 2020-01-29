addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

sessions = constants.sessions;
FSIDs = constants.FSIDs;

%% load fsaverage label for hOc1 (V1)
cyto_dir = '/home/stone/eshed/beta_bricks/cyto_atlas';
fsaverage_label_lh = sprintf('%s/MPM_lh.hOc1.label', cyto_dir);
fsaverage_label_rh = sprintf('%s/MPM_rh.hOc1.label', cyto_dir);

lh_V1_vertices = fs_read_label(fsaverage_label_lh);
rh_V1_vertices = fs_read_label(fsaverage_label_rh);

% get number of vertices in lh and rh
numlh = cvnreadsurface('fsaverage', 'lh', 'sphere', 'orig', 'justcount', 'True');
numrh = cvnreadsurface('fsaverage', 'rh', 'sphere', 'orig', 'justcount', 'True');

lh_fsaverage_mask = zeros(numlh, 1);
rh_fsaverage_mask = zeros(numrh, 1);

% surfaces are 1-indexed, 
lh_fsaverage_mask(lh_V1_vertices) = 1;
rh_fsaverage_mask(rh_V1_vertices) = 1;

surfsuffix = 'DENSETRUNCpt';

for session_idx = 1:length(FSIDs)
	FSID = FSIDs{session_idx};
	session = sessions{session_idx};

	% transferred_lh = cvntransfertosubject('fsaverage', FSID, lh_fsaverage_mask, 'lh', 'nearest', 'orig', surfsuffix);
	% transferred_rh = cvntransfertosubject('fsaverage', FSID, rh_fsaverage_mask, 'rh', 'nearest', 'orig', surfsuffix);

	% outdir = sprintf('%s/%s/label', cvnpath('freesurfer'), FSID);
	% cvnwritemgz(FSID, 'hOc1', transferred_lh, 'lh', outdir, surfsuffix);
	% cvnwritemgz(FSID, 'hOc1', transferred_rh, 'rh', outdir, surfsuffix);

	% mask = [transferred_lh; transferred_rh];

	% show the user what we made
	surftype = 'inflated';
	viewname = 'ventral';

	[numlh, numrh] = cvnreadsurface(FSID,{'lh','rh'}, 'sphere', surfsuffix, 'justcount', true);
	valstruct = struct('data', ones(numlh + numrh, 1), 'numlh', numlh, 'numrh', numrh);
	[viewpt, ~, viewhemis] = cvnlookupviewpoint(FSID, {'lh','rh'}, viewname, surfsuffix);

	L = [];
	[rawimg, L, rgbimg] = cvnlookupimages(FSID, valstruct, viewhemis, ...
		viewpt, L, 'xyextent', [1 1], 'surftype', surftype, ...
		'surfsuffix', surfsuffix, 'absthreshold', 2, ...
		'roiname', 'hOc1');

	figure();
	img_handle = imshow(rgbimg);
	waitforbuttonpress;
	close all;
end

