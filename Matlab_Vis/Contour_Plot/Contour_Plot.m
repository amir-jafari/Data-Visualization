%%
% This is an example of how to create a contour plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/contour.html |contour|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load position and elevation data for Mount Bruno
load mtBruno Longitude Latitude Elevation

% Create a contour plot with 8 contour levels
figure
contour(Longitude, Latitude, Elevation, 8)

% Add title and exis labels
title('Mount Bruno Elevation')
xlabel('Longitude')
ylabel('Latitude')
