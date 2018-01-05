%%
% This is an example of how to create an exploded pie chart in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/pie.html |pie|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load the data for South American populations
load SouthAmericaPopulations populations countries

% Calculate the total populations and percentage by country
total = sum(populations);
percent = populations/total;

% Create a pie chart with sections 3 and 6 exploded
figure
explode = [0 0 1 0 0 1 0 0];
pie(percent, explode, countries)

% Add title
title('South American Population by Country')
