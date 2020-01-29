function corrmat = flip_and_average_corrmat(X)
%FLIP_AND_AVERAGE_CORRMAT flips across diagonal and averages

	dims = size(X);
	corrmat = zeros(dims);

	for i = 1:dims(1)
		for j = i:dims(2)
			if i==j
				corrmat(i,j) = X(i,j);
			else
				corrmat(j,i) = mean([X(i,j),X(j,i)]);
			end
		end
	end

end
