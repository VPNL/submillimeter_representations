function [matched_A_indices, matched_B_indices] = get_matching_indices(sorted_A, sorted_B, n_keep)
% GET_MATCHING_INDICES 
% For two distributions, gets n_keep values from each distribution that
% are as closely matched in value as possible. Keeps highest values possible!
%
% Not perfect, but algorithm goes like this:
% 	1. Pull the top n_keep from each vector and figure out which is larger
% 	2. From the smaller of the two, take the first n_keep elements
% 	3. For the larger of the two, iteratively shift the starting index,
% 		and check against desired value. Stop when we get as close
% 		as possible


    top_n_A = mean(sorted_A(1:(n_keep + 1)));
    top_n_B = mean(sorted_B(1:(n_keep + 1)));


    if top_n_A > top_n_B
		matched_B_indices = 1:(n_keep + 1);
		matched_A_indices = iterative_match(sorted_A, top_n_B, n_keep);
    else
		matched_A_indices = 1:(n_keep + 1);
		matched_B_indices = iterative_match(sorted_B, top_n_A, n_keep);
    end


end

function matched_ind = iterative_match(sorted, target, n_keep)
% ITERATIVE_MATCH
% Iterates over starting indices for sorted, choosing the starting index that
% brings us closest to the target value


    best_distance_to_target = 9999999;
    best_idx = -1;
    for starting_ind = 1:length(sorted) - n_keep
		mn = mean(sorted(starting_ind:(starting_ind + n_keep)));
		distance_to_target = abs(mn - target);
		if distance_to_target < best_distance_to_target
			best_distance_to_target = distance_to_target;
			best_idx = starting_ind;
		end
    end

    matched_ind = best_idx:(best_idx + n_keep);

end
