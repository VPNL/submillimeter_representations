function VTC_partition_mask = restrict_EPI_mask(FSID, partition, full_mask)
    [lh_mask, ~, ~] = cvnroimask(FSID, 'lh', partition, [], 'DENSETRUNCpt');
    [rh_mask, ~, ~] = cvnroimask(FSID, 'rh', partition, [], 'DENSETRUNCpt');
    partition_mask = [lh_mask{1}; rh_mask{1}];

    VTC_partition_mask = full_mask(partition_mask);
end
