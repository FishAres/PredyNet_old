
close all;
% rng(10);

% Network parameters

InSize = 25;
InputSize = InSize^2;
ySize =  60;
eSize = InputSize;

timelength = 2000;
or0 = randi(360,1);
Input = gaborPatch(InSize,or0,0.2,4);


W = 0.1 + 0.01*randn(InputSize,ySize);
V = 0.1 + 0.01*randn(ySize,InputSize);
H = 0 + 0.01*randn(ySize,ySize);
Hmask = -LocalCn(H,6);
H = Hmask.*H;

y = randn(1,ySize);
e = zeros(1,eSize);
yprev = y;
eprev = e;

eta = 0.01;
etaH = 0.015;
Y = zeros(timelength,ySize);
E = zeros(timelength,eSize);
Rec = zeros(timelength,eSize);
wStored = zeros(timelength,InputSize,ySize);
sgn = 1;
patchSign = zeros(1,timelength);
lmd = 0.01;
for t = 1:timelength
    if rand > 0.999
        sgn = -1*sgn;
    end
    
    In = gaborPatch(InSize,or0+sgn*4*t,0.2,4);
    In = In(:)';
    y = tanh(yprev*H + eprev*W);
    e = (In- yprev*V);
    
    eprev = e;
    yprev = y;
    
    Y(t,:) = y;
    E(t,:) = e;
    Rec(t,:) = y*V;
    
%     eta = etaH - 0.00001*t;
%     if eta <= 0
%         eta = 0;
%     end
    
    W = W + eta*(eprev'*yprev);
    V = V + eta*(yprev'*eprev);
%     H = H + etaH*Hmask.*(yprev'*yprev);
%     H = Hmask.*(H + etaH*((eprev*W)'*(e*W)));
    H = Hmask.*(H + etaH*(yprev'*yprev - lmd*H));
    H(H>0.2) = 0.2;
    H(H<-0.2) = -0.2;

    H(logical(eye(size(H)))) = 0;
    patchSign(t) = sgn;
    wStored(t,:,:) = W;
end

figure; 
subplot(2,2,1);
plot(In');
title('input')
subplot(2,2,2);
plot(Rec);
title('reconstruction')
subplot(2,2,3);
plot(E);
title('error')
subplot(2,2,4);
plot(Y);
title('y')


