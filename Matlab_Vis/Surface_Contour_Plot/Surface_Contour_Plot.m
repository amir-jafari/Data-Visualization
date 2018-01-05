%%
% This is an example of how to create a surface contour plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/surfc.html |surfc|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Create a grid of x and y data
y = -10:0.5:10;
x = -10:0.5:10;
[X, Y] = meshgrid(x, y);

% Create the function values for Z = f(X,Y)
Z = sin(sqrt(X.^2+Y.^2)) ./ sqrt(X.^2+Y.^2);

% Create a surface contour plor using the surfc function
figure
surfc(X, Y, Z)

% Adjust the view angle
view(-38, 18)

% Add title and axis labels
title('Normal Response')
xlabel('x')
ylabel('y')
zlabel('z')
