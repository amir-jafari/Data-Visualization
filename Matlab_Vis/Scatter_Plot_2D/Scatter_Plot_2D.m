%%
% This is an example of how to create a 2D scatter plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/scatter.html |scatter|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load undersea elevation data
load seamount x y z

% Create a scatter plot using the scatter function
figure
scatter(x, y, 10, z)

% Add title and axis labels
title('Undersea Elevation')
xlabel('Longitude')
ylabel('Latitude')
