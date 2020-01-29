function mkdirsquiet(path)
% MKDIRSQUIET recursively makes directories to the path, if not already there

	[fpath, fname, ext] = fileparts(path);

	% if no extension, last bit is also a directory
	if isempty(ext)
		fpath = sprintf('%s/%s', fpath, fname);
	end

	% split at '/'
	dirparts = strsplit(fpath, '/');

	% build path from bottom up
	path_so_far = '';

	for dirpart_idx = 1:length(dirparts)
		dirpart = dirparts{dirpart_idx};
		if strcmp(dirpart, '')
			continue;
		end
		path_so_far = sprintf('%s/%s', path_so_far, dirpart);
		mkdirquiet(path_so_far);
	end
end
