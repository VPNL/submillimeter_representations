mask_threshes = [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9];

%%%% MASTER PARAMS %%%%
fig_dir = '/home/stone/eshed/beta_bricks/figures/epi_mask'; mkdirquiet(fig_dir);

% if mask_thresh > 0, which mask to use (hires or lowres)
mask_base = 'preprocessVER1SURF'; 
data_base = '/home/stone-ext1/fmridata';

datasets = {                                                                    
	'20160212-ST001-E002'                                                   
	'20160623-CVNS004-fLoc_ph'                                              
	'20160628-CVNS003-fLoc_ph'                                              
	'20160630-CVNS005-fLoc_ph'                                              
	'20161014-ST001-CVNS009Floc'                                            
	'20170316-ST001-CVNS011Floc'
	'20170316-ST001-CVNS012Floc'
	%'20160428-ST001-S001_ph'  % retest                                      
};                                                                              

FSIDs = {
	'C1051'
	'CVNS104'
	'CVNS103'
	'CVNS105'
	'CVNS109'
	'CVNS011'
	'CVNS012'
	%'C1051'
};

contrasts = {
	'numberVSall'
	'wordVSall'
	'limbVSall'
	'bodyVSall'
	'adultVSall'
	'childVSall'
	'carVSall'
	'instrumentVSall'
	'houseVSall'
	'corridorVSall'
};

%% Plot vertex loss graph
vertex_loss_graph(datasets, FSIDs, mask_threshes, mask_base, fig_dir);

%% Plot maps of mean EPI
for i = 1:length(datasets)
	dataset = datasets{i};
	FSID = FSIDs{i};
	
	draw_mean_epis(dataset, FSID, 'vInf', 1, [0, 2], fig_dir);
end
