classdef Constants
	properties( Constant = true )
		%% data constants
		fmridata_dir = '/home/stone-ext1/fmridata';
		sessions = { 
			'20160212-ST001-E002'                                                   
			'20160623-CVNS004-fLoc_ph'                                              
			'20160628-CVNS003-fLoc_ph'                                              
			'20160630-CVNS005-fLoc_ph'                                              
			'20161014-ST001-CVNS009Floc'                                            
			'20170316-ST001-CVNS011Floc'
			'20170316-ST001-CVNS012Floc'
			'20161006-CVNS001_floc3t' % 3T
		};                                                                              

		FSIDs = {
			'C1051'
			'CVNS104'
			'CVNS103'
			'CVNS105'
			'CVNS109'
			'CVNS011'
			'CVNS012'
			'C1051'
		};

		preproc_str_hires = 'preprocessVER1SURF';
		preproc_str_sim2pt4 = 'preprocess_sim2pt4_VER1SURF';

		%% analysis constants
		output_dir = '/home/stone-ext3/eshed/beta_bricks/outputs';
		figure_dir = '/home/stone-ext3/eshed/beta_bricks/figures';
		partitions = {'VTC_anat', 'VTC_lateral', 'VTC_medial', 'hOc1'}; % ROI names
		depth_sets = {[1,2],[3,4],[5,6]};
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

		glm_dir = 'GLM_vanilla';
		glm_dir_sim2pt4 = 'GLM_vanilla_sim2pt4';

		metrics = {
			struct(...
				'name', 'zscore', ...
				'clim', [-3, 3], ...
				'cmap', 'cmapsign4', ...
				'primary', false ...
			);
			struct(...
				'name', 'tstat', ...
				'clim', [-7, 7], ...
				'cmap', 'cmapsign4', ...
				'primary', false ...
			);
			struct(...
				'name', 'tnorm', ...
				'clim', [-7, 7], ...
				'cmap', 'cmapsign4', ...
				'primary', false ...
			);
			struct(...
				'name', 'znorm', ...
				'clim', [-7, 7], ...
				'cmap', 'cmapsign4', ...
				'primary', true...
			);
		};

		noise_types = {
			struct(...
				'type', 'gaussian', ...
				'magnitude', 1.3 ...
			);
			struct(...
				'type', 'none', ...
				'magnitude', 0.0 ...
			);
		};
	end
end
