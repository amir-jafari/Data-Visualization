%%
% This is an example of how to create a stem plot with multiple data in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/stem.html |stem|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load the filter data
load filterData time signal filter1 filter2

% Create a stem plot using the stem function
figure
stem(time, signal, 'filled')
hold on

% Add the second and third data sets to the plot
stem(time - 0.2, filter1, 'c', 'filled')
stem(time - 0.4, filter2, 'm', 'filled')

% Add a legend
legend('Input Signal', 'Input Delayed by 0.2', ...
    'Input Delayed by 0.4', 'Location', 'SouthWest')
