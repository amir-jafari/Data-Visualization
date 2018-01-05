%%
% This is an example of how to display a simple image in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/image.html |image|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load the data for the mandrill image
load mandrill X map

% Create the image display using the image command
figure
image(X)

% Use the colormap specified in the image data file
colormap(map)

% Turn the axes off
axis off

% Add title
title('Mandrill')
