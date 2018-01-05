%%
% This is an example of how to create an area plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/area.html |area|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load population data
load PopulationAge years population groups

% Create the area plot using the area function
figure
area(years, population/1000000)
colormap winter

% Add a legend
legend(groups, 'Location', 'NorthWest')

% Add title and axis labels
title('US Population by Age (1860 - 2000)')
xlabel('Years')
ylabel('Population in Millions')
