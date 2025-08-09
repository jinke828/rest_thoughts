% Monica Rosenberg 5-6-18
% Jin Ke 1st use 9-16-22; 2nd use 7-19-23
% condition = 'aNT', 'vNT', 'avCake', 'avNW'

% aNT -- sub1 TR = 1039, all others TR = 1023
% vNT -- all TR = 1023
% avCake -- sub1 TR = 964, all others TR = 948
% avNorth -- all TR = 948
% rest -- sub3,4 TR = 581, all others TR = 597
% aCPT -- sub1 TR = 600, sub2,3 TR = 608, all others TR = 603
% vCPT -- sub1 TR = 624, sub2-5 TR = 608, all others TR = 603

cd '/Users/jinke/Desktop/spontaneous_thoughts';
condition = 'rest';
TRs = 597;

datadir_netts = './data/brain/netts/';
savedir_netts = './data/brain/';
    
datadir_netcc = './data/brain/netcc/';
savedir_netcc = './data/brain/';
    
all_file1 = dir(fullfile(datadir_netcc,'*netcc'));
all_file2 = dir(fullfile(datadir_netts,'*netts'));
ts = NaN(268,TRs,length(all_file1));
fc = NaN(268,268,length(all_file1));
badnodes = zeros(268,1);
badsubs  = zeros(length(all_file1),1);
nnode    = zeros(length(all_file1),1);
rois     = cell(length(all_file1),1);
for s = 1:length(all_file1)
    rois{s} = [];
end

% load FC matrices
for s = 1:length(all_file1)
    filepath = [datadir_netcc all_file1(s).name];
    try
        fileID     = fopen(filepath);
        tmpfile    = textscan(fileID,'%s');
    
        % Get # of nodes and load Fisher z matrix
        nnode(s,1) = str2num(tmpfile{1}{2});
        for i = 1:nnode(s)
            rois{s,1}(i,1) = str2num(tmpfile{1}{16+i});
        end
        tmpmat = dlmread(filepath,'\t',7+nnode(s),0);
    
        % Read in available rows/columns of matrix
        for i = 1:nnode(s)
            for j = 1:nnode(s)
                fc(rois{s}(i),rois{s}(j),s) = tmpmat(i,j);
            end
            if fc(i,i,s) ~= 4
               badnodes(i) = 1;
            end
        end
        clear fileID tmpfile i tmpmat
    catch
        badsubs(s) = 1;
    end

    % save([savedir_netcc condition '.mat'],'fc');
    clear filepath
end

% Load time series
for s = 1:length(all_file2)
    filepath = [datadir_netts all_file2(s).name];
        
    tmpmat = dlmread(filepath,'\t',0,0);
        
    fprintf('Sub %d\t', s);
    tc = size(tmpmat,2);
    fprintf('Total TR = %d\n', tc);
        
    if TRs == size(tmpmat,2)
        % Read in available rows/columns of matrix
        for i = 1:nnode(s)
            ts(rois{s}(i),:,s) = tmpmat(i,:);
        end
    else
        dif = size(tmpmat,2)-TRs;
        if dif < 0
            for i = 1:nnode(s)
                for t = 1:TRs+dif
                    ts(rois{s}(i),t,s) = tmpmat(i,t);
                end
            end
        else
            for i = 1:nnode(s)
                for t = 1:TRs
                    ts(rois{s}(i),t,s) = tmpmat(i,t);
                end
            end
        end
    end
    save([savedir_netts condition '_ts.mat'],'ts');
    clear filepath tmpmat i
end