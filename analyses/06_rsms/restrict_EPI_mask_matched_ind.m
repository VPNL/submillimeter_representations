function VTC_partition_mask = restrict_EPI_mask_matched_ind(FSID, partition, full_mask, matched_indices)
    [lh_mask, ~, ~] = cvnroimask(FSID, 'lh', partition, [], 'DENSETRUNCpt');
    [rh_mask, ~, ~] = cvnroimask(FSID, 'rh', partition, [], 'DENSETRUNCpt');
    partition_mask = [lh_mask{1}; rh_mask{1}];

	roi_indices = find(partition_mask);

	if isempty(matched_indices)
		VTC_partition_mask = full_mask(partition_mask);
	else
		matched_roi_indices = roi_indices(matched_indices);
		full_binary_matched_roi_mask = zeros(size(partition_mask));
		full_binary_matched_roi_mask(matched_roi_indices) = 1;

		VTC_partition_mask = full_mask(matched_roi_indices);
	end
end
