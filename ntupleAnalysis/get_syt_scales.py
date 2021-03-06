from __future__ import print_function
import numpy as np
import ROOT

hf = ROOT.TFile("Fits/Bkgfits_flat_regionlimit.root","READ")
#print(hf.ls())
hnames = list(hf.GetListOfKeys())
hnames = [h.GetName() for h in hnames]
print(hnames)

bg = 'bkg'

hbg = {}
for k in hnames:
    if bg in k:
        hbg[k] = hf.Get(k)
        #print(k, hbg[k].GetNbinsX())
# bg
nbg = {}
systbg = [k.split('_')[-1] for k in hbg.keys() if bg != k]
systbg = np.unique([syst.replace('Up','').replace('Down','') for syst in systbg])
#print(systbg)

for k in hbg:
    #if k != bg: continue
    #print(k)
    nbg[k] = np.zeros(hbg[k].GetNbinsX())
    count = 0
    for ib in range(1, hbg[k].GetNbinsX()+1):
        nbg[k][ib-1] = hbg[k].GetBinContent(ib)
        #print(ib-1, nbg[k][ib-1])
        count += 1
    #print(k, count)
    #break

for syst in systbg:
    #continue
    #rup = np.abs(nbg[bg])
    rup = np.abs(nbg[bg+'_'+syst+'Up']/nbg[bg] - 1.)
    rdn = np.abs(nbg[bg+'_'+syst+'Down']/nbg[bg] - 1.)
    rmax = [up if up > dn else dn for up,dn in zip(rup, rdn)]
    rmin = [dn if up > dn else up for up,dn in zip(rup, rdn)]
    for i,r in enumerate(rmax):
        pass
        #print(i, r)
    print(syst, np.min(rmin), np.max(rmax))
    #break

errbg = np.zeros(hbg[bg].GetNbinsX())
for ib in range(1, hbg[bg].GetNbinsX()+1):
    errbg[ib-1] = hbg[bg].GetBinError(ib)/hbg[bg].GetBinContent(ib)
print('stat', errbg.min(), errbg.max())

# sg

#sg = 'h4g_100MeV'
#sg = 'h4g_400MeV'
#sg = 'h4g_1GeV'
sgs = ['h4g_100MeV', 'h4g_400MeV', 'h4g_1GeV']

for sg in sgs:

    hsg = {}

    for k in hnames:
        if sg in k:
            hsg[k] = hf.Get(k)
            #print(k, hsg[k].GetNbinsX())

    nsg = {}
    systsg = [k.split('_')[-1] for k in hsg.keys() if sg != k]
    systsg = np.unique([syst.replace('Up','').replace('Down','') for syst in systsg])
    #print(systsg)

    halfmax = hsg[sg].GetMaximum()/2.
    print(sg,'halfmax:',halfmax)
    for k in hsg:
        #if k != sg: continue
        #if k != 'h4g_100MeV_scaleUp': continue
        #if k != 'h4g_100MeV_smearUp': continue
        #print(k)
        nsg[k] = np.zeros(hsg[k].GetNbinsX())
        count = 0
        for ib in range(1, hsg[k].GetNbinsX()+1):
            binc = hsg[k].GetBinContent(ib)
            if binc >= halfmax:
                nsg[k][ib-1] = binc
            #print(ib-1, nsg[k][ib-1])
            count += 1
        #print(k, count)
        #break

    #print(nsg.keys())
    for syst in systsg:
        #continue
        #rup = np.abs(nsg[sg])
        rup = np.nan_to_num(np.abs(nsg[sg+'_'+syst+'Up']/nsg[sg] - 1.))
        rdn = np.nan_to_num(np.abs(nsg[sg+'_'+syst+'Down']/nsg[sg] - 1.))
        rmax = np.array([up if up > dn else dn for up,dn in zip(rup, rdn)])
        rmin = np.array([dn if (up > dn and dn > 0.) else up for up,dn in zip(rup, rdn)])
        for i,r in enumerate(rmin):
            pass
            #print(i, r)
        print(syst, np.min(rmin[rmin>0.]), np.max(rmax))
        #break

    errsg = np.zeros(hsg[sg].GetNbinsX())
    for ib in range(1, hsg[sg].GetNbinsX()+1):
        binc = hsg[sg].GetBinContent(ib)
        if binc >= halfmax:
            errsg[ib-1] = hsg[sg].GetBinError(ib)/binc
    print('stat', errsg[errsg>0.].min(), errsg.max())
