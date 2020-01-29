function corrmat = mirror_corrmat(X)
% MIRROR_CORRMAT partially undoes flip_and_average_corrmat by mirroring values across diagonal

	
	dims = size(X);
	corrmat = X; 

	for i = 1:dims(1)
		for j = i:dims(2)
			if i==j
				corrmat(i,j) = X(i,j);
			else
				corrmat(i,j) = X(j,i); 
			end
		end
	end

end
