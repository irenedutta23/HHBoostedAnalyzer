#!/usr/bin/python

import os
import datetime
import time
import subprocess
import glob
import sys
import json


datasets = {

# ####################################################################################################
# #2016 Datasets
# ####################################################################################################   
# 'SingleMuon_2016B-ver2':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2016B-17Jul2018_ver2-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'SingleMuon_2016C':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2016C-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'SingleMuon_2016D':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2016D-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'SingleMuon_2016E':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2016E-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'SingleMuon_2016F':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2016F-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'SingleMuon_2016G':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2016G-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'SingleMuon_2016H':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2016H-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'JetHT_2016B-ver2':'/JetHT/hqu-NanoTuples-30Apr2020_Run2016B-17Jul2018_ver2-v2-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'JetHT_2016C':'/JetHT/hqu-NanoTuples-30Apr2020_Run2016C-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'JetHT_2016D':'/JetHT/hqu-NanoTuples-30Apr2020_Run2016D-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'JetHT_2016E':'/JetHT/hqu-NanoTuples-30Apr2020_Run2016E-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'JetHT_2016F':'/JetHT/hqu-NanoTuples-30Apr2020_Run2016F-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'JetHT_2016G':'/JetHT/hqu-NanoTuples-30Apr2020_Run2016G-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'JetHT_2016H':'/JetHT/hqu-NanoTuples-30Apr2020_Run2016H-17Jul2018-v1-b0abb2002249db2b4f7fad7e7c1c0c68/USER',
# 'GluGluToHHTo4B_node_cHHH5_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH5_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'GluGluToHHTo4B_node_cHHH2p45_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH2p45_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'GluGluToHHTo4B_node_cHHH1_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH1_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'GluGluToHHTo4B_node_cHHH0_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH0_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'GluGluToHHTo4B_node_SM_13TeV-madgraph':'/GluGluToHHTo4B_node_SM_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_1_13TeV-madgraph':'/VBFHHTo4B_CV_1_C2V_1_C3_1_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHHTo4B_CV_1_C2V_2_C3_1_13TeV-madgraph':'/VBFHHTo4B_CV_1_C2V_2_C3_1_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_2_13TeV-madgraph':'/VBFHHTo4B_CV_1_C2V_1_C3_2_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_0_13TeV-madgraph':'/VBFHHTo4B_CV_1_C2V_1_C3_0_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHHTo4B_CV_1_5_C2V_1_C3_1_13TeV-madgraph':'/VBFHHTo4B_CV_1_5_C2V_1_C3_1_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHHTo4B_CV_0_5_C2V_1_C3_1_13TeV-madgraph':'/VBFHHTo4B_CV_0_5_C2V_1_C3_1_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-ext1':'/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-ext1':'/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-ext1':'/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-ext1':'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-ext1':'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-ext1':'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-ext1':'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8':'/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8':'/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8':'/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8':'/GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix':'/VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix-ext1':'/VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v1-44377faedc969dcf531f5eb3e501054b/USER',
#'WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8':'/WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-0185a8db413c92e1bf268f4636ab8496/USER',
#'WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8':'/WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-0185a8db413c92e1bf268f4636ab8496/USER',
# 'ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8':'/ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
# 'ttHTobb_M125_13TeV_powheg_pythia8':'/ttHTobb_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',
#'ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8':'/ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-0185a8db413c92e1bf268f4636ab8496/USER',
#'ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8':'/ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-0185a8db413c92e1bf268f4636ab8496/USER',
#'ZZ_TuneCUETP8M1_13TeV-pythia8':'/ZZ_TuneCUETP8M1_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'ZZ_TuneCUETP8M1_13TeV-pythia8-ext1':'/ZZ_TuneCUETP8M1_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8':'/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'WZ_TuneCUETP8M1_13TeV-pythia8':'/WZ_TuneCUETP8M1_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'WZ_TuneCUETP8M1_13TeV-pythia8-ext1':'/WZ_TuneCUETP8M1_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'WW_TuneCUETP8M1_13TeV-pythia8':'/WW_TuneCUETP8M1_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'WW_TuneCUETP8M1_13TeV-pythia8-ext1':'/WW_TuneCUETP8M1_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-ext1-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'WWTo4Q_13TeV-powheg':'/WWTo4Q_13TeV-powheg/sixie-NanoTuples-V2p0_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-0185a8db413c92e1bf268f4636ab8496/USER',
#'WJetsToQQ_HT400to600_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT400to600_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
#'WJetsToQQ_HT600to800_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT600to800_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
#'WJetsToQQ_HT-800toInf_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT-800toInf_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
#'ZJetsToQQ_HT400to600_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT400to600_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
#'ZJetsToQQ_HT600to800_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT600to800_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v1-44377faedc969dcf531f5eb3e501054b/USER',
#'ZJetsToQQ_HT-800toInf_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/bortigno-NanoTuples-30Apr2020_RunIISummer16MiniAODv3-PUMoriond17_94X_v3-v2-44377faedc969dcf531f5eb3e501054b/USER',


# ####################################################################################################
# #2017 Datasets
# ####################################################################################################   
#'SingleMuon_2017B':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2017B-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
#'SingleMuon_2017C':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2017C-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
#'SingleMuon_2017D':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2017D-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
#'SingleMuon_2017E':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2017E-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
#'SingleMuon_2017F':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2017F-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
# 'JetHT_2017B':'/JetHT/hqu-NanoTuples-30Apr2020_Run2017B-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
# 'JetHT_2017C':'/JetHT/hqu-NanoTuples-30Apr2020_Run2017C-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
# 'JetHT_2017D':'/JetHT/hqu-NanoTuples-30Apr2020_Run2017D-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
# 'JetHT_2017E':'/JetHT/hqu-NanoTuples-30Apr2020_Run2017E-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
# 'JetHT_2017F':'/JetHT/hqu-NanoTuples-30Apr2020_Run2017F-31Mar2018-v1-b2e5aecd7d318124ef1b7f48a4318be4/USER',
# 'GluGluToHHTo4B_node_SM':'/GluGluToHHTo4B_node_SM_13TeV-madgraph_correctedcfg/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
#'GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
#'GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
#'GluGluToHHTo4B_node_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
#'GluGluToHHTo4B_node_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_1':'/VBFHHTo4B_CV_1_C2V_1_C3_1_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v3-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'VBFHHTo4B_CV_1_C2V_2_C3_1_13TeV-madgraph':'/VBFHHTo4B_CV_1_C2V_2_C3_1_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_2_13TeV-madgraph':'/VBFHHTo4B_CV_1_C2V_1_C3_2_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_0_13TeV-madgraph':'/VBFHHTo4B_CV_1_C2V_1_C3_0_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'VBFHHTo4B_CV_1_5_C2V_1_C3_1_13TeV-madgraph':'/VBFHHTo4B_CV_1_5_C2V_1_C3_1_13TeV-madgraph/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v2-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-ext1-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-ext1-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8':'/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v2-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8':'/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8':'/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v2-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8':'/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v2-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8':'/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8':'/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v2-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8':'/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v2-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8':'/GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'VBFHToBB_M-125_13TeV_powheg_pythia8':'/VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8':'/WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8':'/WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8':'/ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8':'/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/slaurila-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
# 'ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8':'/ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
# 'ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8':'/ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
# 'ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8-ext1':'/ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-ext1-v1-11808738aa05d1901a77e0a4a3559b49/USER',
# 'ZZ_TuneCP5_13TeV-pythia8':'/ZZ_TuneCP5_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v2-11808738aa05d1901a77e0a4a3559b49/USER',
# 'WZ_TuneCP5_13TeV-pythia8':'/WZ_TuneCP5_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_PU2017_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
# 'WW_TuneCP5_13TeV-pythia8':'/WW_TuneCP5_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v2-11808738aa05d1901a77e0a4a3559b49/USER',
# 'WWTo4Q_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8':'/WWTo4Q_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-ext1-v1-11808738aa05d1901a77e0a4a3559b49/USER',
# 'WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8':'/WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_v14-v1-11808738aa05d1901a77e0a4a3559b49/USER',
#'WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
#'WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
#'WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
#'ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
#'ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',
#'ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/coli-NanoTuples-30Apr2020_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1-6f7c69ffdbb83072d4913e5f3cf0008f/USER',

####################################################################################################
#2018 Datasets
####################################################################################################   
#'SingleMuon_2018A':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2018A-17Sep2018-v2-51ac09360ac5a9839ebad8683652478b/USER',
#'SingleMuon_2018B':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2018B-17Sep2018-v1-51ac09360ac5a9839ebad8683652478b/USER',
#'SingleMuon_2018C':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2018C-17Sep2018-v1-51ac09360ac5a9839ebad8683652478b/USER',
#'SingleMuon_2018D':'/SingleMuon/hqu-NanoTuples-30Apr2020_Run2018D-22Jan2019-v2-99b92eeae6e347dd2619a79a606c4aaa/USER',
# 'JetHT_2018A':'/JetHT/hqu-NanoTuples-30Apr2020_Run2018A-17Sep2018-v1-51ac09360ac5a9839ebad8683652478b/USER',
# 'JetHT_2018B':'/JetHT/hqu-NanoTuples-30Apr2020_Run2018B-17Sep2018-v1-51ac09360ac5a9839ebad8683652478b/USER',
# 'JetHT_2018C':'/JetHT/hqu-NanoTuples-30Apr2020_Run2018C-17Sep2018-v1-51ac09360ac5a9839ebad8683652478b/USER',
# 'JetHT_2018D':'/JetHT/hqu-NanoTuples-30Apr2020_Run2018D-PromptReco-v2-99b92eeae6e347dd2619a79a606c4aaa/USER',
# 'GluGluToHHTo4B_node_SM_TuneCP5_PSWeights_13TeV-madgraph-pythia8':'/GluGluToHHTo4B_node_SM_TuneCP5_PSWeights_13TeV-madgraph-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
# 'GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
# 'GluGluToHHTo4B_node_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
# 'GluGluToHHTo4B_node_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8':'/GluGluToHHTo4B_node_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8':'/VBFHHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8':'/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_2_TuneCP5_PSWeights_13TeV-madgraph-pythia8':'/VBFHHTo4B_CV_1_C2V_1_C3_2_TuneCP5_PSWeights_13TeV-madgraph-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'VBFHHTo4B_CV_1_C2V_1_C3_0_TuneCP5_PSWeights_13TeV-madgraph-pythia8':'/VBFHHTo4B_CV_1_C2V_1_C3_0_TuneCP5_PSWeights_13TeV-madgraph-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'VBFHHTo4B_CV_1_5_C2V_1_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8':'/VBFHHTo4B_CV_1_5_C2V_1_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'VBFHHTo4B_CV_0_5_C2V_1_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8':'/VBFHHTo4B_CV_0_5_C2V_1_C3_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8':'/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8':'/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8':'/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8':'/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8':'/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8':'/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8':'/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8-ext2':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-ext2-v2-27c3bb388d728791ecf339ca1f755fce/USER',
# 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8-ext3':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-ext3-v2-27c3bb388d728791ecf339ca1f755fce/USER',
# 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8':'/GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix':'/VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8':'/WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8':'/WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8':'/ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
# 'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8':'/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/slaurila-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v2-27c3bb388d728791ecf339ca1f755fce/USER',
#'ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8':'/ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8':'/ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8-ext1':'/ggZH_HToBB_ZToBB_M125_TuneCP5_13TeV_powheg_pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-ext1-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'ZZ_TuneCP5_13TeV-pythia8':'/ZZ_TuneCP5_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v2-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'WZ_TuneCP5_PSweights_13TeV-pythia8':'/WZ_TuneCP5_PSweights_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'WZ_TuneCP5_13TeV-pythia8':'/WZ_TuneCP5_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v3-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'WW_TuneCP5_PSweights_13TeV-pythia8':'/WW_TuneCP5_PSweights_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'WW_TuneCP5_13TeV-pythia8':'/WW_TuneCP5_13TeV-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v2-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8':'/WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8/sixie-NanoTuples-V2p0_RunIIAutumn18MiniAOD-102X_v15-v1-cd471944433cef30a1e69a7cb38aa7e8/USER',
#'WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
#'WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
#'WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8':'/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
#'ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
#'ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',
#'ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8':'/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/gouskos-NanoTuples-30Apr2020_RunIIAutumn18MiniAOD-102X_v15-v1-27c3bb388d728791ecf339ca1f755fce/USER',

}

# if (len(sys.argv) -1 < 1):
#     print "Error. Not enough arguments provided.\n"
#     print "Usage: python printFilesInGivenBlocks.py\n"
#     exit()

#datasetName = sys.argv[1]


for processName in datasets.keys():

    outputFile = open(processName+".list","w")
    print processName
    command = "dasgoclient -query=\"file dataset=" + datasets[processName] + " instance=prod/phys03 \" -json > tmpOutput.json"
    os.system(command)

    jsonFile = open("tmpOutput.json","r")
    data = json.load(jsonFile)

    for p in data:
        blockName = p['file'][0]['block.name']
        fileName = p['file'][0]['name']
        outputFile.write("root://cmsxrootd.fnal.gov/"+fileName+"\n")
    

    

