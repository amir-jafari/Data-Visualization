%%
% This is an example of how to create a surface plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/surf.html |surf|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Generate points for a cylinder with profile 2 + sin(t)
t = 0:pi/50:2*pi;
[x, y, z] = cylinder(2+sin(t));

% Create a surface plot using the surf function
figure
surf(x, y, z, 'LineStyle', 'none', 'FaceColor', 'interp')
colormap('summer')

% Turn off the axis and the grid
axis square
axis off
grid off
