
close all;
rng(10);

% Network parameters

InSize = 2;
ySize = 12;
eSize = InSize;

timelength = 600;

W = 0.1 + 0.01*randn(InSize,ySize);
V = 0.1 + 0.01*randn(ySize,InSize);
H = 0.1 + 0.01*randn(ySize,ySize);

Input = zeros(InSize,timelength);
inVec = 1:timelength;
inVec2 = zeros(1,timelength);
inVec2(80:end) = 1;
Input(1,:) = sin(0.1*inVec) + 0.5*cos(0.2*inVec) - 0.2*sin(0.5*inVec);
Input(2,:) = 1 - exp(-inVec2);
Input(2,300:400) = 0.5;

Input(1,:) = (Input(1,:) - mean(Input(1,:)))/max(abs(Input(1,:)));
y = randn(1,ySize);
e = zeros(1,eSize);
yprev = y;
eprev = e;

eta = 0.1;
Y = zeros(timelength,ySize);
E = zeros(timelength,eSize);
Rec = zeros(timelength,eSize);


for t = 1:timelength
    
    y = tanh(y + y*H + eprev*W);
    e = tanh(Input(:,t)'- yprev*V);
    
    eprev = e;
    yprev = y;
    
    Y(t,:) = y;
    E(t,:) = e;
    Rec(t,:) = y*V;
    
    W = W + eta*(eprev'*yprev);
    V = V + eta*(yprev'*eprev);
    H = H + eta*(yprev'*yprev);
    H(logical(eye(size(H)))) = 0;
    
end

figure; 
subplot(2,2,1);
plot(Input');
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


