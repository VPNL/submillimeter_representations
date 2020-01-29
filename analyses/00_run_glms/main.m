addpath(genpath('/home/stone/eshed/beta_bricks/analyses'));
constants = Constants;

sessions = constants.sessions;
FSIDs = constants.FSIDs;
preproc_str_hires = constants.preproc_str_hires;
preproc_str_sim2pt4 = constants.preproc_str_sim2pt4;
fmridata_dir = constants.fmridata_dir;
glm_dir = constants.glm_dir;
glm_dir_sim2pt4 = constants.glm_dir_sim2pt4;

runs = {
	1:12                 % C1051
	setdiff(1:12, [4])   % CVNS104 (excluding run 4)
	1:12                 % CVNS103
	1:12                 % CVNS105
	1:12                 % CVNS109
	setdiff(1:12, [4 6]) % CVNS011 (excluding runs 4 and 6)
	1:12                 % CVNS012
	1:12                 % C1051 3T
}; 

cutoffs = {
	[repmat([158], 1, 12)],    % C1051
	[repmat([158], 1, 12)],    % CVNS104
	[repmat([158], 1, 12)],    % CVNS103
	[repmat([158], 1, 12)],    % CVNS105
	[repmat([158], 1, 12)],    % CVNS109
	[repmat([158], 1, 12)],    % CVNS011
	[repmat([158], 1, 12)],    % CVNS012
	[repmat([314], 1, 12)],    % C1051 3T
};

TRs =      [2.00 2.00 2.00 2.00 2.00 2.00 2.00 2.00 1.00];
stimdurs = [4.00 4.00 4.00 4.00 4.00 4.00 4.00 4.00 4.00];

preproc_strs = {preproc_str_hires, preproc_str_sim2pt4}; 
for p = 1:length(preproc_strs)
	preproc_str = preproc_strs{p};
	
	for session_idx = 1:length(sessions)
		
		session = sessions{session_idx};
		fsid = FSIDs{session_idx};
		run = runs{session_idx}; 
		cutoff = cutoffs{session_idx};
		tr = TRs(session_idx);
		stimdur = stimdurs(session_idx);

		% skip sim2pt4 for 3T session
		if strcmp('20161006-CVNS001_floc3t', session) && strcmp(preproc_str, 'preprocess_sim2pt4_VER1SURF')
			fprintf('Skipping sim2pt4 for 3t session\n');
			continue;
		end
		fprintf('%s: %s', fsid, session);
		fprintf('\n\n');
		
		data_dir = sprintf('%s/%s', fmridata_dir, session);
		assert(isdir(data_dir));

		if strcmp(preproc_str, preproc_str_sim2pt4)
			outdir = glm_dir_sim2pt4;
		else
			outdir = glm_dir;
		end

		vanilla_glm(...
			data_dir,...
			outdir,...
			fsid,...
			run,...
			cutoff,...
			tr,...
			stimdur,...
			preproc_str...
		);
	end 
end
