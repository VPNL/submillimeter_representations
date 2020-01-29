function out = add_noise(in, noise_type, noise_magnitude)
%add_noise - Adds noise to inputs
	noise_type = lower(noise_type);
    if strcmp(noise_type, 'gaussian') || strcmp(noise_type, 'white') || strcmp(noise_type, 'normal')
        out = in + randn(size(in)) * noise_magnitude;
    elseif strcmp(noise_type, 'uniform')
        out = in + (rand(size(in)) - 0.5) * noise_magnitude;
    elseif strcmp(noise_type, 'none')
        out = in;
    else
        error('Sorry, cannot add noise of that type.')
    end
end
