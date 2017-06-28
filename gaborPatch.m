function patch = gaborPatch(imSize,angle, sg,sf)

x = 1:imSize;
x0 = (x/imSize)-0.5;
[X,Y] = meshgrid(x0,x0);
angleRad = (angle/360)*pi;
Xt = X*cos(angleRad);
Yt = Y*sin(angleRad);
XYt = [Xt + Yt];

Xf = XYt*sf*2*pi;
grat = sin(Xf);

trim = 0.1;
mask = exp(-(((X.^2)+(Y.^2))./(2 * sg^2)));
mask(mask < trim) = 0;

patch = grat.*mask;



