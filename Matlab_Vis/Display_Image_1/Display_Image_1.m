%%
% This is an example of how to display a simple image in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/image.html |image|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Load the data for the North Atlantic image
load NAimage lng lat naimg

% Create the image display using the image command
figure
image(lng, lat, naimg)

% Turn the axes off
axis off

% Add title
title('North Atlantic')
