function out = combine_pseudodepths(brick)

	[n_vert, n_layers] = size(brick);
	out = zeros(n_vert, 3);

	out(:,1) = mean(brick(:,1:2),2);
	out(:,2) = mean(brick(:,3:4),2);
	out(:,3) = mean(brick(:,5:6),2);

end
