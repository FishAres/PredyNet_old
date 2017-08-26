function view_stack(In)

figure;
for ind = 1:size(In,1)
    imagesc(squeeze(In(ind,:,:)));
    title([num2str(ind)]);
    drawnow;
    pause(0.01);
end
