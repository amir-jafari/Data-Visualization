%%
% This is an example of how to create a surface plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/surf.html |surf|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Create a grid of x and y points
points = linspace(-2, 2, 40);
[X, Y] = meshgrid(points, points);

% Define the function Z = f(X,Y)
Z = 2./exp((X-.5).^2+Y.^2)-2./exp((X+.5).^2+Y.^2);

% Create the surface plot using the surf command
figure
surf(X, Y, Z)
