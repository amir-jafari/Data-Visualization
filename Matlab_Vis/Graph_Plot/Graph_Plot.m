%%
% This is an example of how to create a graph plot in MATLAB&#174;.
% 
% Read about the <http://www.mathworks.com/help/matlab/ref/gplot.html |gplot|> function in the MATLAB documentation.
%
% For more examples, go to <http://www.mathworks.com/discovery/gallery.html MATLAB Plot Gallery>
%
% Copyright 2012-2014 The MathWorks, Inc.

% Create the onnectivity graph of the Buckminster Fuller geodesic dome
[B, V] = bucky;
H = sparse(60, 60);
k = 31:60;
H(k, k) = B(k, k);

% Visualize the graph using the gplot function (blue)
figure
gplot(B - H, V, 'b-')
hold on

% Visualize a rotation of the graph (red)
gplot(H, V, 'r-')
axis off equal
