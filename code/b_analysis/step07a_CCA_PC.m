%%% additional matlab toolboxes required (will need to addpath for each of these)
% FSLNets     http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLNets
% PALM        http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/PALM
% nearestSPD  http://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd

cd ('/gpfs/milgram/project/chun/jk2992/rest_thoughts/code/b_analysis'); % change to your folder

% Add paths
addpath './z_CCA_helper/palm-alpha119'
addpath './z_CCA_helper/FSLNets';

% Load behavioral and confound variables
vars = load('./z_CCA_helper/vars.txt');
vars(:,sum(isnan(vars)==0)<130) = NaN;
varsQconf = load('./z_CCA_helper/varsQconf.txt');

%%% load netmats from HCP PTN release
% set NET to be the subjects X unwrapped network-matrices (partial correlations)
% Load predicted thought data
a_awake   = load('../../results/predicted/a_awake.mat').predicted(:);
b_external= load('../../results/predicted/b_external.mat').predicted(:);
c_future  = load('../../results/predicted/c_future.mat').predicted(:);
f_valence = load('../../results/predicted/f_valence.mat').predicted(:);
g_image   = load('../../results/predicted/g_image.mat').predicted(:);
d_past    = load('../../results/predicted/d_past.mat').predicted(:);
e_other   = load('../../results/predicted/e_other.mat').predicted(:);
h_word    = load('../../results/predicted/h_word.mat').predicted(:);
i_detail  = load('../../results/predicted/i_detail.mat').predicted(:);

NET = [a_awake b_external c_future d_past e_other f_valence g_image h_word i_detail];
topics = load('../../results/predicted/topics.mat').predicted;
NET = [NET topics];

% Setup confounds matrix
conf = palm_inormal([varsQconf vars(:,[7 14 15 22 23 25]) vars(:,[265 266]).^(1/3)]);
conf(isnan(conf)) = 0;
conf = nets_normalise([conf conf(:,2:end).^2]);

%% prepare permutation scheme using PALM - for more details see:
%% https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/PALM/ExchangeabilityBlocks#Generating_the_set_of_permutations_only
Nperm = 10000;
EB=hcp2blocks('../../data/beh/RESTRICTED_jinke_5_22_2024_13_45_6.csv', [ ], false, vars(:,1)); % change the filename to your version of the restricted file
PAPset=palm_quickperms([ ], EB, Nperm); 

%%% identify "bad" SMs - e.g. because of bad outliers or not enough distinct values
badvars=[];
for i=1:size(vars,2)
  Y=vars(:,i); grotKEEP=~isnan(Y);  
  grot=(Y(grotKEEP)-median(Y(grotKEEP))).^2; grot=max(grot/mean(grot));  % do we have extreme outliers?
  if (sum(grotKEEP)>300) & (std(Y(grotKEEP))>0) & (max(sum(nets_class_vectomat(Y(grotKEEP))))/length(Y(grotKEEP))<0.95) & (grot<100)
      % the 3rd thing above is:  is the size of the largest equal-values-group too large?
    i=i; % do nothing
  else
    [i sum(grotKEEP) std(Y(grotKEEP)) max(sum(nets_class_vectomat(Y(grotKEEP))))/length(Y(grotKEEP)) grot]
    badvars=[badvars i];
  end
end

%%% get list of which SMs to feed into CCA
varskeep=setdiff([1:size(vars,2)],[1 6 267:457 ...                            % SMs we generally ignore (ID, race, FreeSurfer)
 2 7 14 15 22 23 25 265 266  ...                                              % confound SMs
 11 12 13 17 19 27 29 31 34 40 204 205 212:223 229:233 236 238 242 477 ...    % some more SMs to ignore for the CCA
 3 4 5 8 9 10 16 18 20 21 24 26 28 30 32 33 35:39 458 459 460 463 464 ...     % some more SMs to ignore for the CCA
 103 193 470 ...                                                              % 3 extra variables that were not included in the paper 'Color_Vision', 'SSAGA_Mj_Age_1st_Use', 'Noise_Comp'
 badvars]);        

%%% "impute" missing vars data - actually this avoids any imputation
varsd=palm_inormal(vars(:,varskeep)); % Gaussianise
for i=1:size(varsd,2) % deconfound ignoring missing data
  grot=(isnan(varsd(:,i))==0); grotconf=nets_demean(conf(grot,:)); varsd(grot,i)=normalize(varsd(grot,i)-grotconf*(pinv(grotconf)*varsd(grot,i)));
end
varsdCOV=zeros(size(varsd,1));
for i=1:size(varsd,1) % estimate "pairwise" covariance, ignoring missing data
  for j=1:size(varsd,1)
    grot=varsd([i j],:); grot=cov(grot(:,sum(isnan(grot))==0)'); varsdCOV(i,j)=grot(1,2);
  end
end
varsdCOV2=nearestSPD(varsdCOV); % minor adjustment: project onto the nearest valid covariance matrix

%%% loop through the number of components to feed into CCA
for Nkeep = 2:16
    for Nkeep_beh = [10 15 20 25 30 35 40]

        fprintf('Running CCA with Nkeep=%d, Nkeep_beh=%d\n', Nkeep, Nkeep_beh);

        % Prepare NET
        NET1 = nets_demean(NET);  
        NET1 = NET1 / std(NET1(:)); 
        amNET = abs(mean(NET));
        NET3 = nets_demean(NET ./ repmat(amNET, size(NET,1), 1));  
        NET3(:,amNET < 0.1) = [];
        NET3 = NET3 / std(NET3(:)); 
        grot = [NET1 NET3];
        NETd = nets_demean(grot - conf * (pinv(conf) * grot));
        [uu1,ss1,vv1] = nets_svds(NETd, Nkeep);

        % Behavioral SVD
        [uu,dd] = eigs(varsdCOV2, Nkeep_beh);
        uu2 = uu - conf * (pinv(conf) * uu);

        % Run CCA
        [grotA,grotB,grotR,grotU,grotV,grotstats] = canoncorr(uu1, uu2);

        % Permutation testing
        grotRp = zeros(Nperm, min(Nkeep, Nkeep_beh));
        for j = 1:Nperm
            [~,~,grotRp(j,:),~,~,~] = canoncorr(uu1, uu2(PAPset(:,j),:));
        end
        for i = 1:min(Nkeep, Nkeep_beh)
            grotRpval(i) = (1 + sum(grotRp(2:end,1) >= grotR(i))) / Nperm;
        end
        Ncca = sum(grotRpval < 0.05);

        % CCA mode 1 weights
        grotAAd = corr(grotU(:,1), NETd(:,1:size(NET,2)))';
        varsgrot = palm_inormal(vars);
        for i = 1:size(varsgrot,2)
            grot = (isnan(varsgrot(:,i))==0);
            grotconf = nets_demean(conf(grot,:));
            varsgrot(grot,i) = nets_normalise(varsgrot(grot,i) - grotconf * (pinv(grotconf) * varsgrot(grot,i)));
        end
        grotBBd = corr(grotV(:,1), varsgrot, 'rows', 'pairwise')';

        % Save results
        save(sprintf('../../results/CCA/predicted-thoughts_behavior_HCP_%dthoughtPC_%dbehaviorPC.mat', ...
            Nkeep, Nkeep_beh), 'grotU', 'grotV', 'grotAAd', 'grotBBd', 'grotR', 'grotRpval');

    end
end