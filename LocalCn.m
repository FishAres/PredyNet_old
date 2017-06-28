function mask = LocalCn(In,winSize)

M = size(In,1);
x = 1:M;
for ind = 1:M
    mask(ind,:) = gaussCurve(x,ind,winSize) -  gaussCurve(x,ind,1.2*winSize);
end

