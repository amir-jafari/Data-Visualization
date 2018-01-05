%%
% This is an example of how to create a simple stem plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/stem.html |stem|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load amplitude data
load amplitudeData sample amplitude

% Create a stem plot using the stem function
figure
stem(sample, amplitude, 'filled', 'b')

% Adjust the axis limits
axis([0 53 -1.2 1.2])

% Add title and axis labels
title('FIR Polyphase Interpolator')
xlabel('Samples')
ylabel('Amplitude')
