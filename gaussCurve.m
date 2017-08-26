function curve = gaussCurve(In,ctr,sd)

curve = exp(-(In-ctr).^2 ./(2*sd^2));