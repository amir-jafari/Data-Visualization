%%
% This is an example of how to create a plot with two y axes in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/plotyy.html |plotyy|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Create some data for the two curves to be plotted
x  = 0:0.01:20;
y1 = 200*exp(-0.05*x).*sin(x);
y2 = 0.8*exp(-0.5*x).*sin(10*x);

% Create a plot with 2 y axes using the plotyy function
figure
[ax, h1, h2] = plotyy(x, y1, x, y2, 'plot');

% Add title and x axis label
xlabel('Time in \mu sec.')
title('Frequency Response')
% Use the axis handles to set the labels of the y axes
set(get(ax(1), 'YLabel'), 'String', 'Low Frequency')
set(get(ax(2), 'YLabel'), 'String', 'High Frequency')
