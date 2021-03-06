#include "HHTo4BNtupler.h"
#include "JetTree.h"

//C++ includes

//ROOT includes
#include "TH1F.h"

using namespace std;

double HHTo4BNtupler::getTriggerEff( TH2F *trigEffHist , double pt, double mass ) {
  double result = 0.0;
  double tmpMass = 0;
  double tmpPt = 0;

  if (trigEffHist) {
      // constrain to histogram bounds
      if( mass > trigEffHist->GetXaxis()->GetXmax() * 0.999 ) {
	tmpMass = trigEffHist->GetXaxis()->GetXmax() * 0.999;
      } else if ( mass < 0 ) {
	tmpMass = 0.001;
	//cout << "Warning: mass=" << mass << " is negative and unphysical\n";
      } else {
	tmpMass = mass;
      }

      if( pt > trigEffHist->GetYaxis()->GetXmax() * 0.999 ) {
	tmpPt = trigEffHist->GetYaxis()->GetXmax() * 0.999;
      } else if (pt < 0) {
	tmpPt = 0.001;
	cout << "Warning: pt=" << pt << " is negative and unphysical\n";
      } else {
	tmpPt = pt;
      }

      result = trigEffHist->GetBinContent(
				 trigEffHist->GetXaxis()->FindFixBin( tmpMass ),
				 trigEffHist->GetYaxis()->FindFixBin( tmpPt )
				 );  
         
  } else {
    std::cout << "Error: expected a histogram, got a null pointer" << std::endl;
    return 0;
  }
  
  //cout << "mass = " << mass << " , pt = " << pt << " : trigEff = " << result << "\n";

  return result; 
}


void HHTo4BNtupler::Analyze(bool isData, int Option, string outputfilename, string year, string pileupWeightName)
{
 
    cout << "Initializing..." << endl;

    //----------------------------------------
    //Load auxiliary information
    //----------------------------------------  
    TH2F *triggerEffHist = 0;    
    TH1F *pileupWeightHist = 0;
    
    if (!isData) {
      string CMSSWDir = std::getenv("CMSSW_BASE");
      string triggerEffFilename = "";
      if (year == "2016") {
	triggerEffFilename = CMSSWDir + "/src/HHBoostedAnalyzer/data/JetHTTriggerEfficiency_2016.root";
      } else if (year == "2017") {
	triggerEffFilename = CMSSWDir + "/src/HHBoostedAnalyzer/data/JetHTTriggerEfficiency_2017.root";
      } else if (year == "2018") {
	triggerEffFilename = CMSSWDir + "/src/HHBoostedAnalyzer/data/JetHTTriggerEfficiency_2018.root";
      } else {
	cout << "[HHTo4BNtupler] Warning: year " << year << " is not supported. \n";
      }
      TFile *triggerEffFile = new TFile(triggerEffFilename.c_str(),"READ");

      if (!triggerEffFile) {
	cout << "Warning : triggerEffFile " << triggerEffFilename << " could not be opened.\n";
      } else {
	cout << "Opened triggerEffFile " << triggerEffFilename << "\n";
      }
      if (triggerEffFile) {
	triggerEffHist = (TH2F*)triggerEffFile->Get("efficiency_ptmass");    
      } else {
	cout << "Warning : could not find triggerEffHist named efficiency_ptmass in file " << triggerEffFilename << "\n";
      }
      if (triggerEffHist) {
	cout << "Found triggerEffHist in file " << triggerEffFilename << "\n";
      }

      string pileupWeightFilename = CMSSWDir + "/src/HHBoostedAnalyzer/data/PileupWeights/PileupWeights.root";
      TFile *pileupWeightFile = new TFile(pileupWeightFilename.c_str(),"READ");
      if (!pileupWeightFile) {
	cout << "Warning : pileupWeightFile " << pileupWeightFile << " could not be opened.\n";  
      } else {
	cout << "Opened pileupWeightFile " << pileupWeightFilename << "\n"; 
      }
      string pileupWeightHistname = "PUWeight_" + pileupWeightName + "_" + year;
      if (pileupWeightFile) {
	pileupWeightHist = (TH1F*)pileupWeightFile->Get(pileupWeightHistname.c_str());
      } 
      if (pileupWeightHist) {
	cout << "Found pileupWeightHist " << pileupWeightHistname << "in file " << pileupWeightFilename << "\n";
      } else {
	cout << "Warning :  could not find pileupWeightHist named " 
	     << pileupWeightHistname 
	     << " in file " << pileupWeightFilename << "\n";
      }
    }

    //----------------------------------------
    //Output file
    //----------------------------------------  
    string outfilename = outputfilename;
    if (outfilename == "") outfilename = "HHTo4BNtuple.root";
    TFile *outFile = new TFile(outfilename.c_str(), "RECREATE");    
 
    //histogram containing total number of processed events (for normalization)
    TH1F *NEvents = new TH1F("NEvents", "NEvents", 1, 1, 2);

    //output TTree
    TTree *outputTree = new TTree("tree", "");
 
    //------------------------
    //declare branch variables
    //------------------------  
    float weight = 0;
    float triggerEffWeight = 0;
    float pileupWeight = 0;
    float totalWeight = 0;

    float genHiggs1Pt = -1;
    float genHiggs1Eta = -1;
    float genHiggs1Phi = -1;
    float genHiggs2Pt = -1;
    float genHiggs2Eta = -1;
    float genHiggs2Phi = -1;
    float genHH_pt = -99;
    float genHH_eta = -99;
    float genHH_phi = -99;
    float genHH_mass = -99;
    float genLeptonPt = -1;
    float genLeptonEta = -1;
    float genLeptonPhi = -1;
    int   genLeptonId = 0;
    int   genLeptonMotherId = 0;
 
    int NJets = 0;
    float MET = -1;
    float fatJet1Pt = -99;
    float fatJet1Eta = -99;
    float fatJet1Phi = -99;
    float fatJet1Mass = -99;
    float fatJet1MassSD = -99;
    float fatJet1DDBTagger = -99;
    float fatJet1PNetXbb = -99;
    float fatJet1PNetQCDb = -99;
    float fatJet1PNetQCDbb = -99;
    float fatJet1PNetQCDc = -99;
    float fatJet1PNetQCDcc = -99;
    float fatJet1PNetQCDothers = -99;
    int   fatJet1GenMatchIndex = -99;
    float fatJet1Tau3OverTau2 = -99;
    bool fatJet1HasMuon = 0;
    bool fatJet1HasElectron = 0;
    bool fatJet1HasBJetCSVLoose = 0;
    bool fatJet1HasBJetCSVMedium = 0;
    bool fatJet1HasBJetCSVTight = 0;
    float fatJet2Pt = -99;
    float fatJet2Eta = -99;
    float fatJet2Phi = -99;
    float fatJet2Mass = -99;
    float fatJet2MassSD = -99;
    float fatJet2DDBTagger = -99;
    float fatJet2PNetXbb = -99;
    float fatJet2PNetQCDb = -99;
    float fatJet2PNetQCDbb = -99;
    float fatJet2PNetQCDc = -99;
    float fatJet2PNetQCDcc = -99;
    float fatJet2PNetQCDothers = -99;
    int   fatJet2GenMatchIndex = -99;
    float fatJet2Tau3OverTau2 = -99;
    bool fatJet2HasMuon = 0;
    bool fatJet2HasElectron = 0;
    bool fatJet2HasBJetCSVLoose = 0;
    bool fatJet2HasBJetCSVMedium = 0;
    bool fatJet2HasBJetCSVTight = 0;
    float fatJet3Pt = -99;
    float fatJet3Eta = -99;
    float fatJet3Phi = -99;
    float fatJet3Mass = -99;
    float fatJet3MassSD = -99;
    float fatJet3DDBTagger = -99;
    float fatJet3PNetXbb = -99;
    float fatJet3PNetQCDb = -99;
    float fatJet3PNetQCDbb = -99;
    float fatJet3PNetQCDc = -99;
    float fatJet3PNetQCDcc = -99;
    float fatJet3PNetQCDothers = -99;
    float fatJet3Tau3OverTau2 = -99;
    bool fatJet3HasMuon = 0;
    bool fatJet3HasElectron = 0;
    bool fatJet3HasBJetCSVLoose = 0;
    bool fatJet3HasBJetCSVMedium = 0;
    bool fatJet3HasBJetCSVTight = 0;
    float hh_pt = -99;
    float hh_eta = -99;
    float hh_phi = -99;
    float hh_mass = -99;        
    float fatJet1PtOverMHH = -99;
    float fatJet1PtOverMSD = -99;
    float fatJet2PtOverMHH = -99;
    float fatJet2PtOverMSD = -99;
    float deltaEta_j1j2 = -99;
    float deltaPhi_j1j2 = -99;
    float deltaR_j1j2 = -99;    
    float ptj2_over_ptj1 = -99;
    float mj2_over_mj1 = -99;
   

    //------------------------
    //set branches on big tree
    //------------------------
    outputTree->Branch("weight", &weight, "weight/F");
    outputTree->Branch("triggerEffWeight", &triggerEffWeight, "triggerEffWeight/F");
    outputTree->Branch("pileupWeight", &pileupWeight, "pileupWeight/F");
    outputTree->Branch("totalWeight", &totalWeight, "totalWeight/F");
    outputTree->Branch("run", &run, "run/i");
    outputTree->Branch("lumi", &luminosityBlock, "lumi/i");
    outputTree->Branch("event", &event, "event/l");
    outputTree->Branch("npu", &Pileup_nTrueInt, "npu/F");
    outputTree->Branch("rho", &fixedGridRhoFastjetAll, "rho/F");
 

    outputTree->Branch("genHiggs1Pt", &genHiggs1Pt, "genHiggs1Pt/F");
    outputTree->Branch("genHiggs1Eta", &genHiggs1Eta, "genHiggs1Eta/F");
    outputTree->Branch("genHiggs1Phi", &genHiggs1Phi, "genHiggs1Phi/F");
    outputTree->Branch("genHiggs2Pt", &genHiggs2Pt, "genHiggs2Pt/F");
    outputTree->Branch("genHiggs2Eta", &genHiggs2Eta, "genHiggs2Eta/F");
    outputTree->Branch("genHiggs2Phi", &genHiggs2Phi, "genHiggs2Phi/F");
    outputTree->Branch("genHH_pt",      &genHH_pt,     "genHH_pt/F");
    outputTree->Branch("genHH_eta",     &genHH_eta,    "genHH_eta/F");
    outputTree->Branch("genHH_phi",     &genHH_phi,    "genHH_phi/F");
    outputTree->Branch("genHH_mass",    &genHH_mass,   "genHH_mass/F");
    outputTree->Branch("genLeptonId", &genLeptonId, "genLeptonId/I");
    outputTree->Branch("genLeptonMotherId", &genLeptonMotherId, "genLeptonMotherId/I");
    outputTree->Branch("genLeptonPt", &genLeptonPt, "genLeptonPt/F");
    outputTree->Branch("genLeptonEta", &genLeptonEta, "genLeptonEta/F");
    outputTree->Branch("genLeptonPhi", &genLeptonPhi, "genLeptonPhi/F");
    
    outputTree->Branch("NJets", &NJets, "NJets/I");
    outputTree->Branch("MET", &MET, "MET/F");
    outputTree->Branch("fatJet1Pt", &fatJet1Pt, "fatJet1Pt/F");
    outputTree->Branch("fatJet1Eta", &fatJet1Eta, "fatJet1Eta/F");
    outputTree->Branch("fatJet1Phi", &fatJet1Phi, "fatJet1Phi/F");
    outputTree->Branch("fatJet1Mass", &fatJet1Mass, "fatJet1Mass/F");
    outputTree->Branch("fatJet1MassSD", &fatJet1MassSD, "fatJet1MassSD/F");
    outputTree->Branch("fatJet1DDBTagger", &fatJet1DDBTagger, "fatJet1DDBTagger/F");
    outputTree->Branch("fatJet1PNetXbb", &fatJet1PNetXbb, "fatJet1PNetXbb/F");
    outputTree->Branch("fatJet1PNetQCDb", &fatJet1PNetQCDb, "fatJet1PNetQCDb/F");
    outputTree->Branch("fatJet1PNetQCDbb", &fatJet1PNetQCDbb, "fatJet1PNetQCDbb/F");
    outputTree->Branch("fatJet1PNetQCDc", &fatJet1PNetQCDc, "fatJet1PNetQCDc/F");
    outputTree->Branch("fatJet1PNetQCDcc", &fatJet1PNetQCDcc, "fatJet1PNetQCDcc/F");
    outputTree->Branch("fatJet1PNetQCDothers", &fatJet1PNetQCDothers, "fatJet1PNetQCDothers/F");
    outputTree->Branch("fatJet1GenMatchIndex", &fatJet1GenMatchIndex, "fatJet1GenMatchIndex/I");
    outputTree->Branch("fatJet1Tau3OverTau2", &fatJet1Tau3OverTau2, "fatJet1Tau3OverTau2/F");
    outputTree->Branch("fatJet1HasMuon", &fatJet1HasMuon, "fatJet1HasMuon/O");
    outputTree->Branch("fatJet1HasElectron", &fatJet1HasElectron, "fatJet1HasElectron/O");
    outputTree->Branch("fatJet1HasBJetCSVLoose", &fatJet1HasBJetCSVLoose, "fatJet1HasBJetCSVLoose/O");
    outputTree->Branch("fatJet1HasBJetCSVMedium", &fatJet1HasBJetCSVMedium, "fatJet1HasBJetCSVMedium/O");
    outputTree->Branch("fatJet1HasBJetCSVTight", &fatJet1HasBJetCSVTight, "fatJet1HasBJetCSVTight/O");
    outputTree->Branch("fatJet2Pt", &fatJet2Pt, "fatJet2Pt/F");
    outputTree->Branch("fatJet2Eta", &fatJet2Eta, "fatJet2Eta/F");
    outputTree->Branch("fatJet2Phi", &fatJet2Phi, "fatJet2Phi/F");
    outputTree->Branch("fatJet2Mass", &fatJet2Mass, "fatJet2Mass/F");
    outputTree->Branch("fatJet2MassSD", &fatJet2MassSD, "fatJet2MassSD/F");
    outputTree->Branch("fatJet2DDBTagger", &fatJet2DDBTagger, "fatJet2DDBTagger/F");
    outputTree->Branch("fatJet2PNetXbb", &fatJet2PNetXbb, "fatJet2PNetXbb/F");
    outputTree->Branch("fatJet2PNetQCDb", &fatJet2PNetQCDb, "fatJet2PNetQCDb/F");
    outputTree->Branch("fatJet2PNetQCDbb", &fatJet2PNetQCDbb, "fatJet2PNetQCDbb/F");
    outputTree->Branch("fatJet2PNetQCDc", &fatJet2PNetQCDc, "fatJet2PNetQCDc/F");
    outputTree->Branch("fatJet2PNetQCDcc", &fatJet2PNetQCDcc, "fatJet2PNetQCDcc/F");
    outputTree->Branch("fatJet2PNetQCDothers", &fatJet2PNetQCDothers, "fatJet2PNetQCDothers/F");
    outputTree->Branch("fatJet2GenMatchIndex", &fatJet2GenMatchIndex, "fatJet2GenMatchIndex/I");
    outputTree->Branch("fatJet2Tau3OverTau2", &fatJet2Tau3OverTau2, "fatJet2Tau3OverTau2/F");
    outputTree->Branch("fatJet2HasMuon", &fatJet2HasMuon, "fatJet2HasMuon/O");
    outputTree->Branch("fatJet2HasElectron", &fatJet2HasElectron, "fatJet2HasElectron/O");
    outputTree->Branch("fatJet2HasBJetCSVLoose", &fatJet2HasBJetCSVLoose, "fatJet2HasBJetCSVLoose/O");
    outputTree->Branch("fatJet2HasBJetCSVMedium", &fatJet2HasBJetCSVMedium, "fatJet2HasBJetCSVMedium/O");
    outputTree->Branch("fatJet2HasBJetCSVTight", &fatJet2HasBJetCSVTight, "fatJet2HasBJetCSVTight/O");
    outputTree->Branch("fatJet3Pt", &fatJet3Pt, "fatJet3Pt/F");
    outputTree->Branch("fatJet3Eta", &fatJet3Eta, "fatJet3Eta/F");
    outputTree->Branch("fatJet3Phi", &fatJet3Phi, "fatJet3Phi/F");
    outputTree->Branch("fatJet3Mass", &fatJet3Mass, "fatJet3Mass/F");
    outputTree->Branch("fatJet3MassSD", &fatJet3MassSD, "fatJet3MassSD/F");
    outputTree->Branch("fatJet3DDBTagger", &fatJet3DDBTagger, "fatJet3DDBTagger/F");
    outputTree->Branch("fatJet3PNetXbb", &fatJet3PNetXbb, "fatJet3PNetXbb/F");
    outputTree->Branch("fatJet3PNetQCDb", &fatJet3PNetQCDb, "fatJet3PNetQCDb/F");
    outputTree->Branch("fatJet3PNetQCDbb", &fatJet3PNetQCDbb, "fatJet3PNetQCDbb/F");
    outputTree->Branch("fatJet3PNetQCDc", &fatJet3PNetQCDc, "fatJet3PNetQCDc/F");
    outputTree->Branch("fatJet3PNetQCDcc", &fatJet3PNetQCDcc, "fatJet3PNetQCDcc/F");
    outputTree->Branch("fatJet3PNetQCDothers", &fatJet3PNetQCDothers, "fatJet3PNetQCDothers/F");
    outputTree->Branch("fatJet3Tau3OverTau2", &fatJet3Tau3OverTau2, "fatJet3Tau3OverTau2/F");
    outputTree->Branch("fatJet3HasMuon", &fatJet3HasMuon, "fatJet3HasMuon/O");
    outputTree->Branch("fatJet3HasElectron", &fatJet3HasElectron, "fatJet3HasElectron/O");
    outputTree->Branch("fatJet3HasBJetCSVLoose", &fatJet3HasBJetCSVLoose, "fatJet3HasBJetCSVLoose/O");
    outputTree->Branch("fatJet3HasBJetCSVMedium", &fatJet3HasBJetCSVMedium, "fatJet3HasBJetCSVMedium/O");
    outputTree->Branch("fatJet3HasBJetCSVTight", &fatJet3HasBJetCSVTight, "fatJet3HasBJetCSVTight/O");
    outputTree->Branch("hh_pt",      &hh_pt,     "hh_pt/F");
    outputTree->Branch("hh_eta",     &hh_eta,    "hh_eta/F");
    outputTree->Branch("hh_phi",     &hh_phi,    "hh_phi/F");
    outputTree->Branch("hh_mass",    &hh_mass,   "hh_mass/F");
    outputTree->Branch("fatJet1PtOverMHH",    &fatJet1PtOverMHH,   "fatJet1PtOverMHH/F");
    outputTree->Branch("fatJet1PtOverMSD",    &fatJet1PtOverMSD,   "fatJet1PtOverMSD/F");
    outputTree->Branch("fatJet2PtOverMHH",    &fatJet2PtOverMHH,   "fatJet2PtOverMHH/F");
    outputTree->Branch("fatJet2PtOverMSD",    &fatJet2PtOverMSD,   "fatJet2PtOverMSD/F");
    outputTree->Branch("deltaEta_j1j2",    &deltaEta_j1j2,   "deltaEta_j1j2/F");
    outputTree->Branch("deltaPhi_j1j2",    &deltaPhi_j1j2,   "deltaPhi_j1j2/F");
    outputTree->Branch("deltaR_j1j2",    &deltaR_j1j2,   "deltaR_j1j2/F");
    outputTree->Branch("ptj2_over_ptj1",    &ptj2_over_ptj1,   "ptj2_over_ptj1/F");
    outputTree->Branch("mj2_over_mj1",    &mj2_over_mj1,   "mj2_over_mj1/F");
  
    //PFHT800 and PFHT900 only exists in 2016 data
    // outputTree->Branch("HLT_PFHT800",                                        &HLT_PFHT800,                                       "HLT_PFHT800/O");
    // outputTree->Branch("HLT_PFHT900",                                        &HLT_PFHT900,                                       "HLT_PFHT900/O");
    outputTree->Branch("HLT_PFHT1050",                                        &HLT_PFHT1050,                                       "HLT_PFHT1050/O");
    outputTree->Branch("HLT_AK8PFJet360_TrimMass30",                          &HLT_AK8PFJet360_TrimMass30,                         "HLT_AK8PFJet360_TrimMass30/O");
    outputTree->Branch("HLT_AK8PFJet380_TrimMass30",                          &HLT_AK8PFJet380_TrimMass30,                         "HLT_AK8PFJet380_TrimMass30/O");
    outputTree->Branch("HLT_AK8PFJet400_TrimMass30",                          &HLT_AK8PFJet400_TrimMass30,                         "HLT_AK8PFJet400_TrimMass30/O");
    outputTree->Branch("HLT_AK8PFJet420_TrimMass30",                          &HLT_AK8PFJet420_TrimMass30,                         "HLT_AK8PFJet420_TrimMass30/O");
    outputTree->Branch("HLT_AK8PFHT750_TrimMass50",                           &HLT_AK8PFHT750_TrimMass50,                          "HLT_AK8PFHT750_TrimMass50/O");
    outputTree->Branch("HLT_AK8PFHT800_TrimMass50",                           &HLT_AK8PFHT800_TrimMass50,                          "HLT_AK8PFHT800_TrimMass50/O");
    outputTree->Branch("HLT_AK8PFHT850_TrimMass50",                           &HLT_AK8PFHT850_TrimMass50,                          "HLT_AK8PFHT850_TrimMass50/O");
    outputTree->Branch("HLT_AK8PFHT900_TrimMass50",                           &HLT_AK8PFHT900_TrimMass50,                          "HLT_AK8PFHT900_TrimMass50/O");
    outputTree->Branch("HLT_PFJet450",                                        &HLT_PFJet450,                                       "HLT_PFJet450/O");
    outputTree->Branch("HLT_PFJet500",                                        &HLT_PFJet500,                                       "HLT_PFJet500/O");
    outputTree->Branch("HLT_PFJet550",                                        &HLT_PFJet550,                                       "HLT_PFJet550/O");
    outputTree->Branch("HLT_AK8PFJet450",                                     &HLT_AK8PFJet450,                                    "HLT_AK8PFJet450/O");
    outputTree->Branch("HLT_AK8PFJet500",                                     &HLT_AK8PFJet500,                                    "HLT_AK8PFJet500/O");
    outputTree->Branch("HLT_AK8PFJet550",                                     &HLT_AK8PFJet550,                                    "HLT_AK8PFJet550/O");
    outputTree->Branch("HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17",     &HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17,    "HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17/O");
    outputTree->Branch("HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1",      &HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1,     "HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1/O");
    outputTree->Branch("HLT_AK8PFJet330_PFAK8BTagCSV_p17",                    &HLT_AK8PFJet330_PFAK8BTagCSV_p17,                   "HLT_AK8PFJet330_PFAK8BTagCSV_p17/O");
    outputTree->Branch("HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02",  &HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02, "HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02/O");
    outputTree->Branch("HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2",  &HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2, "HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2/O");
    outputTree->Branch("HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4",  &HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4, "HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4/O"); 
    outputTree->Branch("HLT_AK8DiPFJet300_200_TrimMass30_BTagCSV_p20",        &HLT_AK8DiPFJet300_200_TrimMass30_BTagCSV_p20,       "HLT_AK8DiPFJet300_200_TrimMass30_BTagCSV_p20/O");
    outputTree->Branch("HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p087",       &HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p087,      "HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p087/O");
    outputTree->Branch("HLT_AK8DiPFJet300_200_TrimMass30_BTagCSV_p087",       &HLT_AK8DiPFJet300_200_TrimMass30_BTagCSV_p087,      "HLT_AK8DiPFJet300_200_TrimMass30_BTagCSV_p087/O");
    outputTree->Branch("HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20",     &HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20,    "HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20/O");
    outputTree->Branch("HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20",        &HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20,       "HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20/O");
    outputTree->Branch("HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20",        &HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20,       "HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20/O");	


    cout << "Run With Option = " << Option << "\n";
    
    if (Option == 2) cout << "Option = 2 : Select FatJets with pT > 200 GeV and PNetXbb > 0.8 only\n";
    if (Option == 5) cout << "Option = 5 : Select Events with FatJet1 pT > 200 GeV and PNetXbb > 0.8 only\n";
    if (Option == 10) cout << "Option = 10 : Select FatJets with pT > 200 GeV and tau3/tau2 < 0.54 only\n";

    UInt_t NEventsFilled = 0;
 
    //begin loop
    if (fChain == 0) return;
    UInt_t nentries = fChain->GetEntries();
    Long64_t nbytes = 0, nb = 0;

    cout << "nentries = " << nentries << "\n";
    for (UInt_t jentry=0; jentry<nentries;jentry++) {
      //begin event
      if(jentry % 1000 == 0) cout << "Processing entry " << jentry << endl;
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;


      //fill normalization histogram
      weight = genWeight / fabs(genWeight);
      NEvents->SetBinContent( 1, NEvents->GetBinContent(1) + weight);


      //reset tree variables
      genHiggs1Pt = -99.0;
      genHiggs1Eta = -99.0;
      genHiggs1Phi = -99.0;
      genHiggs2Pt = -99.0;
      genHiggs2Eta = -99.0;
      genHiggs2Phi = -99.0;
      genHH_pt = -99;
      genHH_eta = -99;
      genHH_phi = -99;
      genHH_mass = -99;   
      genLeptonId = 0;
      genLeptonMotherId = 0;
      genLeptonPt = -99.0;
      genLeptonEta = -99.0;
      genLeptonPhi = -99.0;
      NJets = -1;
      MET = -99.0;

      fatJet1Pt = -99.0;
      fatJet1Eta = -99.0;
      fatJet1Phi = -99.0;
      fatJet1Mass = -99.0;
      fatJet1MassSD = -99.0;
      fatJet1DDBTagger = -99.0;
      fatJet1PNetXbb = -99;
      fatJet1PNetQCDb = -99;
      fatJet1PNetQCDbb = -99;
      fatJet1PNetQCDc = -99;
      fatJet1PNetQCDcc = -99;
      fatJet1PNetQCDothers = -99;
      fatJet1GenMatchIndex = -99.0;
      fatJet1Tau3OverTau2 = -99;
      fatJet1HasMuon = 0;
      fatJet1HasElectron = 0;
      fatJet1HasBJetCSVLoose = 0;
      fatJet1HasBJetCSVMedium = 0;
      fatJet1HasBJetCSVTight = 0;
      fatJet2Pt = -99.0;
      fatJet2Eta = -99.0;
      fatJet2Phi = -99.0;
      fatJet2Mass = -99.0;
      fatJet2MassSD = -99.0;
      fatJet2DDBTagger = -99.0;
      fatJet2PNetXbb = -99;
      fatJet2PNetQCDb = -99;
      fatJet2PNetQCDbb = -99;
      fatJet2PNetQCDc = -99;
      fatJet2PNetQCDcc = -99;
      fatJet2PNetQCDothers = -99;
      fatJet2GenMatchIndex = -99.0;
      fatJet2Tau3OverTau2 = -99;
      fatJet2HasMuon = 0;
      fatJet2HasElectron = 0;
      fatJet2HasBJetCSVLoose = 0;
      fatJet2HasBJetCSVMedium = 0;
      fatJet2HasBJetCSVTight = 0;
      fatJet3Pt = -99.0;
      fatJet3Eta = -99.0;
      fatJet3Phi = -99.0;
      fatJet3Mass = -99.0;
      fatJet3MassSD = -99.0;
      fatJet3DDBTagger = -99.0;
      fatJet3PNetXbb = -99;
      fatJet3PNetQCDb = -99;
      fatJet3PNetQCDbb = -99;
      fatJet3PNetQCDc = -99;
      fatJet3PNetQCDcc = -99;
      fatJet3PNetQCDothers = -99;
      fatJet3Tau3OverTau2 = -99;
      fatJet3HasMuon = 0;
      fatJet3HasElectron = 0;
      fatJet3HasBJetCSVLoose = 0;
      fatJet3HasBJetCSVMedium = 0;
      fatJet3HasBJetCSVTight = 0;
      hh_pt = -99;
      hh_eta = -99;
      hh_phi = -99;
      hh_mass = -99;
      fatJet1PtOverMHH = -99;
      fatJet1PtOverMSD = -99;
      fatJet2PtOverMHH = -99;
      fatJet2PtOverMSD = -99;
      deltaEta_j1j2 = -99;
      deltaPhi_j1j2 = -99;
      deltaR_j1j2 = -99;    
      ptj2_over_ptj1 = -99;
      mj2_over_mj1 = -99;
              

      //------------------------------
      //----Event variables------------
      //------------------------------
      MET = MET_pt;

      //------------------------------
      //----find gen-higgs------------
      //------------------------------
      int current_mIndex = -1;
      std::vector< TLorentzVector > genHiggsVector;
      if (!isData) {

	for(int i = 0; i < nGenPart; i++) {
	  if( abs(GenPart_pdgId[i]) == 5  && GenPart_pdgId[GenPart_genPartIdxMother[i]] == 25 && current_mIndex != GenPart_genPartIdxMother[i] ) {
	    //std::cout << GenPart_genPartIdxMother[i] << std::endl;
	    // std::cout << "mother: " << GenPart_pdgId[GenPart_genPartIdxMother[i]]
	    // << " PT: " << GenPart_pt[GenPart_genPartIdxMother[i]]
	    // << " eta: " << GenPart_eta[GenPart_genPartIdxMother[i]]
	    // << " phi: " << GenPart_phi[GenPart_genPartIdxMother[i]] << std::endl;
	    TLorentzVector h;
	    h.SetPtEtaPhiM( GenPart_pt[GenPart_genPartIdxMother[i]], GenPart_eta[GenPart_genPartIdxMother[i]], GenPart_phi[GenPart_genPartIdxMother[i]], GenPart_mass[GenPart_genPartIdxMother[i]] );
	    genHiggsVector.push_back(h);
	    current_mIndex = GenPart_genPartIdxMother[i];
	  }

	  if ( (abs(GenPart_pdgId[i]) == 11 || abs(GenPart_pdgId[i]) == 13)
	       && GenPart_pt[i] > 10
	       && (abs(GenPart_pdgId[GenPart_genPartIdxMother[i]]) == 23 || abs(GenPart_pdgId[GenPart_genPartIdxMother[i]]) == 24 || abs(GenPart_pdgId[GenPart_genPartIdxMother[i]]) == 15)
	       && GenPart_pt[i] > genLeptonPt 
	       ) {
	    genLeptonId = GenPart_pdgId[i];
	    genLeptonMotherId = GenPart_pdgId[GenPart_genPartIdxMother[i]];
	    genLeptonPt = GenPart_pt[i];
	    genLeptonEta = GenPart_eta[i];
	    genLeptonPhi = GenPart_phi[i];	    
	  }	       

	}

	if(genHiggsVector.size() >= 1) {
	  //filling tree_out variables
	  genHiggs1Pt = genHiggsVector[0].Pt();
	  genHiggs1Eta = genHiggsVector[0].Eta();
	  genHiggs1Phi = genHiggsVector[0].Phi();
	  //
	  if(genHiggsVector.size() >= 2) {
	    genHiggs2Pt = genHiggsVector[1].Pt();
	    genHiggs2Eta = genHiggsVector[1].Eta();
	    genHiggs2Phi = genHiggsVector[1].Phi();	
	  }
	}

	//gen level
	if(genHiggsVector.size() > 1) { 
	  genHH_pt = (genHiggsVector[0]+genHiggsVector[1]).Pt();
	  genHH_eta = (genHiggsVector[0]+genHiggsVector[1]).Eta();
	  genHH_phi = (genHiggsVector[0]+genHiggsVector[1]).Phi();
	  genHH_mass= (genHiggsVector[0]+genHiggsVector[1]).M();
	}
      
      } //end if !data

      //------------------------------
      //-------find fatJet------------
      //------------------------------
      vector<int> selectedFatJetIndices;

      for(unsigned int i = 0; i < nFatJet; i++ ) {       
	//Hbb fat jet pre-selection
	if (FatJet_pt[i] < 200) continue;

	//Select signal region with jets having DDB > 0.8
	if (Option == 1) {
	  if (!(FatJet_btagDDBvL[i] > 0.80)) continue;
	} 
	if (Option == 2) {
	  if (!(FatJet_ParticleNetMD_probXbb[i]/(1.0 - FatJet_ParticleNetMD_probXcc[i] - FatJet_ParticleNetMD_probXqq[i]) > 0.80)) continue;
	} 
	
	//Select ttbar control region with jets 
	if (Option == 10) {
	  if (!(FatJet_tau3[i] / FatJet_tau2[i] < 0.54 )) continue;
	} 
	selectedFatJetIndices.push_back(i);
      }

      //------------------------------------------------------
      //----------select the two H candidates with largest pT
      //------------------------------------------------------
      int fatJet1Index = -1;
      int fatJet2Index = -1;
      double tmpfatJet1Pt = -999;
      double tmpfatJet2Pt = -999;
      double tmpfatJet1Tagger = -999;
      double tmpfatJet2Tagger = -999;
      for(unsigned int i = 0; i < selectedFatJetIndices.size(); i++ ) {
	double fatJetTagger = FatJet_ParticleNetMD_probXbb[i]/(1.0 - FatJet_ParticleNetMD_probXcc[i] - FatJet_ParticleNetMD_probXqq[i]);
	if (fatJetTagger > tmpfatJet1Tagger) {
	  tmpfatJet2Pt = fatJet1Pt;
	  tmpfatJet2Tagger = tmpfatJet1Tagger;
	  fatJet2Index = fatJet1Index;	  
	  tmpfatJet1Pt = FatJet_pt[selectedFatJetIndices[i]];
	  tmpfatJet1Tagger = fatJetTagger;
	  fatJet1Index = selectedFatJetIndices[i];
	} else if (fatJetTagger > tmpfatJet2Tagger) {
	  tmpfatJet2Pt = FatJet_pt[selectedFatJetIndices[i]];
	  tmpfatJet2Tagger = fatJetTagger;
	  fatJet2Index = selectedFatJetIndices[i];
	}
      }

      //------------------------------------------------------
      //----------look for presence of a third AK8 jet
      //------------------------------------------------------
      int fatJet3Index = -1;
      double tmpfatJet3Pt = -999;
      double tmpfatJet3Tagger = -999;
      for(unsigned int i = 0; i < nFatJet; i++ ) {  
	double fatJetTagger = FatJet_ParticleNetMD_probXbb[i]/(1.0 - FatJet_ParticleNetMD_probXcc[i] - FatJet_ParticleNetMD_probXqq[i]);
	//Hbb fat jet pre-selection
	if (FatJet_pt[i] < 100) continue;
	if (i == fatJet1Index || i == fatJet2Index) continue;
	if (fatJetTagger > tmpfatJet3Tagger) {
	  fatJet3Index = i;
	  tmpfatJet3Pt = FatJet_pt[i];
	  tmpfatJet3Tagger = fatJetTagger;
	}
      }

      //------------------------------------------------------
      //----------Fill higgs candidate information
      //------------------------------------------------------
   
      TLorentzVector Higgs1Jet;
      Higgs1Jet.SetPtEtaPhiM(FatJet_pt[fatJet1Index],FatJet_eta[fatJet1Index],FatJet_phi[fatJet1Index],FatJet_msoftdrop[fatJet1Index]);
      float Higgs1MinDR = 999.;
      int Higgs1_match_idx = -1;
      for( int j = 0; j < genHiggsVector.size(); j++) {
	if(Higgs1Jet.DeltaR(genHiggsVector[j]) < Higgs1MinDR) {
	  Higgs1MinDR = Higgs1Jet.DeltaR(genHiggsVector[j]);
	  Higgs1_match_idx = j;
	}
      }
      fatJet1Pt = FatJet_pt[fatJet1Index];
      fatJet1Eta = FatJet_eta[fatJet1Index];
      fatJet1Phi = FatJet_phi[fatJet1Index];
      fatJet1Mass = FatJet_mass[fatJet1Index];
      fatJet1MassSD = FatJet_msoftdrop[fatJet1Index];
      fatJet1DDBTagger = FatJet_btagDDBvL[fatJet1Index];
      fatJet1PNetXbb = FatJet_ParticleNetMD_probXbb[fatJet1Index]/(1.0 - FatJet_ParticleNetMD_probXcc[fatJet1Index] - FatJet_ParticleNetMD_probXqq[fatJet1Index]);
      fatJet1PNetQCDb = FatJet_ParticleNetMD_probQCDb[fatJet1Index];
      fatJet1PNetQCDbb = FatJet_ParticleNetMD_probQCDbb[fatJet1Index];
      fatJet1PNetQCDc = FatJet_ParticleNetMD_probQCDc[fatJet1Index];
      fatJet1PNetQCDcc = FatJet_ParticleNetMD_probQCDcc[fatJet1Index];
      fatJet1PNetQCDothers = FatJet_ParticleNetMD_probQCDothers[fatJet1Index];

      if(Higgs1MinDR < 0.4) {
	fatJet1GenMatchIndex = Higgs1_match_idx;
      }
      fatJet1Tau3OverTau2 = FatJet_tau3[fatJet1Index] /  FatJet_tau2[fatJet1Index];
      //find muon inside jet
      for(unsigned int q = 0; q < nMuon; q++ ) {       
	if (Muon_pt[q] > 30 && Muon_looseId[q] && 
	    deltaR(fatJet1Eta , fatJet1Phi, Muon_eta[q], Muon_phi[q]) < 1.0
	    ) {
	  fatJet1HasMuon = true;
	  break;
	}
      }
      //find electron inside jet
      for(unsigned int q = 0; q < nElectron; q++ ) {       
	if (Electron_pt[q] > 30 && Electron_mvaFall17V2noIso_WP90[q] && 
	    deltaR(fatJet1Eta , fatJet1Phi, Electron_eta[q], Electron_phi[q]) < 1.0
	    ) {
	  fatJet1HasElectron = true;
	  break;
	}
      }
      //find loose b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.0521 && 
	    deltaR(fatJet1Eta , fatJet1Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet1HasBJetCSVLoose = true;
	  break;
	}
      }
     //find medium b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.3033 && 
	    deltaR(fatJet1Eta , fatJet1Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet1HasBJetCSVMedium = true;
	  break;
	}
      }
      //find tight b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.7489 && 
	    deltaR(fatJet1Eta , fatJet1Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet1HasBJetCSVTight = true;
	  break;
	}
      }



      TLorentzVector Higgs2Jet;
      Higgs2Jet.SetPtEtaPhiM(FatJet_pt[fatJet2Index],FatJet_eta[fatJet2Index],FatJet_phi[fatJet2Index],FatJet_msoftdrop[fatJet2Index]);
      float Higgs2MinDR = 999.;
      int Higgs2_match_idx = -1;
      for( int j = 0; j < genHiggsVector.size(); j++) {
	if(Higgs2Jet.DeltaR(genHiggsVector[j]) < Higgs2MinDR) {
	  Higgs2MinDR = Higgs2Jet.DeltaR(genHiggsVector[j]);
	  Higgs2_match_idx = j;
	}
      }
     
      fatJet2Pt = FatJet_pt[fatJet2Index];
      fatJet2Eta = FatJet_eta[fatJet2Index];
      fatJet2Phi = FatJet_phi[fatJet2Index];
      fatJet2Mass = FatJet_mass[fatJet2Index];
      fatJet2MassSD = FatJet_msoftdrop[fatJet2Index];
      fatJet2DDBTagger = FatJet_btagDDBvL[fatJet2Index];
      fatJet2PNetXbb = FatJet_ParticleNetMD_probXbb[fatJet2Index]/(1.0 - FatJet_ParticleNetMD_probXcc[fatJet2Index] - FatJet_ParticleNetMD_probXqq[fatJet2Index]);
      fatJet2PNetQCDb = FatJet_ParticleNetMD_probQCDb[fatJet2Index];
      fatJet2PNetQCDbb = FatJet_ParticleNetMD_probQCDbb[fatJet2Index];
      fatJet2PNetQCDc = FatJet_ParticleNetMD_probQCDc[fatJet2Index];
      fatJet2PNetQCDcc = FatJet_ParticleNetMD_probQCDcc[fatJet2Index];
      fatJet2PNetQCDothers = FatJet_ParticleNetMD_probQCDothers[fatJet2Index];

      if(Higgs2MinDR < 0.4) {
	fatJet2GenMatchIndex = Higgs2_match_idx;
      }
      fatJet2Tau3OverTau2 = FatJet_tau3[fatJet2Index] /  FatJet_tau2[fatJet2Index];
      
      //find muon inside jet
      for(unsigned int q = 0; q < nMuon; q++ ) {       
	if (Muon_pt[q] > 30 && Muon_looseId[q] && 
	    deltaR(fatJet2Eta , fatJet2Phi, Muon_eta[q], Muon_phi[q]) < 1.0
	    ) {
	  fatJet2HasMuon = true;
	  break;
	}
      }
      //find electron inside jet
      for(unsigned int q = 0; q < nElectron; q++ ) {       
	if (Electron_pt[q] > 30 && Electron_mvaFall17V2noIso_WP90[q] && 
	    deltaR(fatJet2Eta , fatJet2Phi, Electron_eta[q], Electron_phi[q]) < 1.0
	    ) {
	  fatJet2HasElectron = true;
	  break;
	}
      }
      //find loose b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.0521 && 
	    deltaR(fatJet2Eta , fatJet2Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet2HasBJetCSVLoose = true;
	  break;
	}
      }
      //find medium b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.3033 && 
	    deltaR(fatJet2Eta , fatJet2Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet2HasBJetCSVMedium = true;
	  break;
	}
      }
      //find tight b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.7489 && 
	    deltaR(fatJet2Eta , fatJet2Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet2HasBJetCSVTight = true;
	  break;
	}
      }


      //------------------------------------------------------
      //----------Fill Jet 3 information
      //------------------------------------------------------
      fatJet3Pt = FatJet_pt[fatJet3Index];
      fatJet3Eta = FatJet_eta[fatJet3Index];
      fatJet3Phi = FatJet_phi[fatJet3Index];
      fatJet3Mass = FatJet_mass[fatJet3Index];
      fatJet3MassSD = FatJet_msoftdrop[fatJet3Index];
      fatJet3DDBTagger = FatJet_btagDDBvL[fatJet3Index];
      fatJet3PNetXbb = FatJet_ParticleNetMD_probXbb[fatJet3Index]/(1.0 - FatJet_ParticleNetMD_probXcc[fatJet3Index] - FatJet_ParticleNetMD_probXqq[fatJet3Index]);
      fatJet3PNetQCDb = FatJet_ParticleNetMD_probQCDb[fatJet3Index];
      fatJet3PNetQCDbb = FatJet_ParticleNetMD_probQCDbb[fatJet3Index];
      fatJet3PNetQCDc = FatJet_ParticleNetMD_probQCDc[fatJet3Index];
      fatJet3PNetQCDcc = FatJet_ParticleNetMD_probQCDcc[fatJet3Index];
      fatJet3PNetQCDothers = FatJet_ParticleNetMD_probQCDothers[fatJet3Index];

      fatJet3Tau3OverTau2 = FatJet_tau3[fatJet3Index] /  FatJet_tau2[fatJet3Index];
      //find muon inside jet
      for(unsigned int q = 0; q < nMuon; q++ ) {       
	if (Muon_pt[q] > 30 && Muon_looseId[q] && 
	    deltaR(fatJet3Eta , fatJet3Phi, Muon_eta[q], Muon_phi[q]) < 1.0
	    ) {
	  fatJet3HasMuon = true;
	  break;
	}
      }
      //find electron inside jet
      for(unsigned int q = 0; q < nElectron; q++ ) {       
	if (Electron_pt[q] > 30 && Electron_mvaFall17V2noIso_WP90[q] && 
	    deltaR(fatJet3Eta , fatJet3Phi, Electron_eta[q], Electron_phi[q]) < 1.0
	    ) {
	  fatJet3HasElectron = true;
	  break;
	}
      }
      //find loose b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.0521 && 
	    deltaR(fatJet3Eta , fatJet3Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet3HasBJetCSVLoose = true;
	  break;
	}
      }
     //find medium b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.3033 && 
	    deltaR(fatJet3Eta , fatJet3Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet3HasBJetCSVMedium = true;
	  break;
	}
      }
      //find tight b-tagged jet inside jet
      for(unsigned int q = 0; q < nJet; q++ ) {       
	if (Jet_btagDeepB[q] > 0.7489 && 
	    deltaR(fatJet3Eta , fatJet3Phi, Jet_eta[q], Jet_phi[q]) < 1.0
	    ) {
	  fatJet3HasBJetCSVTight = true;
	  break;
	}
      }


      //------------------------------------------------------
      //----------Fill hh candidate information
      //------------------------------------------------------
      hh_pt = (Higgs1Jet+Higgs2Jet).Pt();
      hh_eta = (Higgs1Jet+Higgs2Jet).Eta();
      hh_phi = (Higgs1Jet+Higgs2Jet).Phi();
      hh_mass = (Higgs1Jet+Higgs2Jet).M();      
    
      fatJet1PtOverMHH = fatJet1Pt / hh_mass;
      fatJet1PtOverMSD = fatJet1Pt / fatJet1MassSD;
      fatJet2PtOverMHH = fatJet2Pt / hh_mass;
      fatJet2PtOverMSD = fatJet2Pt / fatJet1MassSD;
      deltaEta_j1j2 = fabs(fatJet1Eta - fatJet2Eta);
      deltaPhi_j1j2 = deltaPhi(fatJet1Phi, fatJet2Phi);
      deltaR_j1j2 = deltaR(fatJet1Eta, fatJet1Phi, fatJet2Eta, fatJet2Phi);
      ptj2_over_ptj1 = fatJet2Pt / fatJet1Pt;
      mj2_over_mj1 = fatJet2MassSD / fatJet1MassSD;             


      //*******************************
      //Count additional AK4 jets 
      //*******************************
      for(int i = 0; i < nJet; i++) {
	if (Jet_pt[i] > 30 && fabs(Jet_eta[i]) < 2.5
	    && deltaR(Jet_eta[i] , Jet_phi[i], fatJet1Eta, fatJet1Phi) > 0.8
	    && deltaR(Jet_eta[i] , Jet_phi[i], fatJet2Eta, fatJet2Phi) > 0.8
	    ) {
	  NJets++;
	}
      }
      
       
      //****************************************************
      //Fill Event - skim for events with two jets found
      //****************************************************
      if (Option == 0 || 
	  (fatJet1Pt > 250 && fatJet2Pt > 250)
	  ) {
	
	//****************************************************
	//Compute trigger efficiency weight
	//****************************************************      
	if (triggerEffHist) {
	  triggerEffWeight = 1.0 - 
	    (1 - getTriggerEff( triggerEffHist , fatJet1Pt, fatJet1MassSD )) * 
	    (1 - getTriggerEff( triggerEffHist , fatJet2Pt, fatJet2MassSD ))
	    ;	
	}
	
	//****************************************************
	//Compute pileupWeight
	//****************************************************      
	if (pileupWeightHist) {
	  pileupWeight = pileupWeightHist->GetBinContent( pileupWeightHist->GetXaxis()->FindFixBin(Pileup_nTrueInt));
	}

	//****************************************************
	//Compute totalWeight
	//****************************************************      
	totalWeight = weight * triggerEffWeight * pileupWeight;

	if (Option==5) {
	  if (!(fatJet1PNetXbb > 0.8)) continue;
	  if (!(fatJet1MassSD > 50 && fatJet2MassSD > 50)) continue;
	}
	NEventsFilled++;            
	outputTree->Fill();      
      }
    }//end of event loop

    cout << "Filled Total of " << NEventsFilled << " Events\n";
    cout << "Writing output trees..." << endl;
    outFile->Write();
    outFile->Close();

}



