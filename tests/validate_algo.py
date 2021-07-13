from pyIFD.ADQ1 import detectDQ
from pyIFD.ADQ2 import getJmap
from pyIFD.ADQ3 import BenfordDQ
from pyIFD.BLK import GetBlockGrid
from pyIFD.CAGI import CAGI
from pyIFD.ELA import ELA
from pyIFD.GHOST import GHOST
from pyIFD.NOI1 import GetNoiseMap
from pyIFD.NOI2 import GetNoiseMaps 
from pyIFD.NOI4 import MedFiltForensics
from pyIFD.NOI5 import PCANoise
import numpy as np
import scipy.io as spio
from skimage.metrics import structural_similarity as comp
import sys

ADQ1_CRITERIA = 0.99
ADQ2_CRITERIA = 0.99
ADQ3_CRITERIA = 0.99
BLK_CRITERIA = 0.99
CAGI_CRITERIA = 0.90
ELA_CRITERIA = 0.99
GHOST_CRITERIA = 0.99
NOI1_CRITERIA = 0.99
NOI2_CRITERIA = 0.99
NOI4_CRITERIA = 0.99
NOI5_CRITERIA = 0.99

def main(argv):
    infilename = sys.argv[1]
    matfilename = sys.argv[2]
    algoname = sys.argv[3]

    if algoname == 'ADQ1':
        adq1test=detectDQ(infilename)
        adq1mat=spio.loadmat(matfilename)
        if(comp(adq1mat['OutputMap'],adq1test[0])<ADQ1_CRITERIA):
            print('ADQ1 JPEG: FAIL')
        else:
            print('ADQ1 JPEG: PASS')

    elif algoname == 'ADQ2':
        adq2test=getJmap(infilename)
        adq2mat=spio.loadmat(matfilename)
        if(comp(adq2mat['OutputMap'],adq2test[0])<ADQ2_CRITERIA):
            print('ADQ2: FAIL')
        else:
            print('ADQ2: PASS')            

    elif algoname == 'ADQ3':
        adq3test=BenfordDQ(infilename)
        adq3mat=spio.loadmat(matfilename)
        if(comp(adq3mat['OutputMap'],adq3test)<ADQ3_CRITERIA):
            print('ADQ3: FAIL')
        else:
            print('ADQ3: PASS')

    elif algoname == 'BLK':
        blktest=GetBlockGrid(infilename)
        blkmat=spio.loadmat(matfilename)
        if(comp(blkmat['OutputMap'],blktest[0])<BLK_CRITERIA):
            print('BLK: FAIL')
        else:
            print('BLK: PASS')

    elif algoname == 'CAGI':    
        cagitest=CAGI(infilename)
        cagimat=spio.loadmat(matfilename)
        sim = comp(cagimat['OutputMap'],cagitest[0])
        if(sim<CAGI_CRITERIA):
            print('CAGI: FAIL Similarity: ' + str(sim))
        else:
            print('CAGI: PASS')

        sim = comp(cagimat['OutputMap_Inverse'],cagitest[1])
        if(sim<CAGI_CRITERIA):
            print('CAGI INVERSE: FAIL Similarity: ' + str(sim))
        else:
            print('CAGI INVERSE: PASS')
    
    elif algoname == 'ELA':
        elatest=ELA(infilename)
        elamat=spio.loadmat(matfilename)
        sim=comp(elamat['OutputMap'],elatest.astype(np.uint8))
        if(sim<ELA_CRITERIA):
            print('ELA: FAIL Similarity: ' + str(sim))
        else:
            print('ELA: PASS')

    elif algoname == 'GHO':
        ghosttest=GHOST(infilename)
        ghostmat=spio.loadmat(matfilename)
        matDispImages = ghostmat['OutputMap'][0]
        pyDispImages = ghosttest[2]
        similarity=[]
        for i in range(len(matDispImages)):
            similarity.append(comp(matDispImages[i],pyDispImages[i]))
        sim = np.mean(similarity)
        if(sim<GHOST_CRITERIA):
            print('GHOST: FAIL Similarity: ' + str(sim))
        else:
            print('GHOST: PASS')

    elif algoname == 'NOI1':
        noi1test=GetNoiseMap(infilename)
        noi1mat=spio.loadmat(matfilename)
        sim = comp(noi1mat['OutputMap'],noi1test)
        if(sim<NOI1_CRITERIA):
            print('NOI1: FAIL Similarity: ' + str(sim))
        else:
            print('NOI1: PASS')

    elif algoname == 'NOI2':
        noi2test=GetNoiseMaps(infilename)
        noi2mat=spio.loadmat(matfilename)
        sim = comp(noi2mat['OutputMap'],noi2test)
        if(sim<NOI2_CRITERIA):
            print('NOI2: FAIL Similarity: ' + str(sim))
        else:
            print('NOI2: PASS')

    elif algoname == 'NOI4':
        noi4test=MedFiltForensics(infilename)
        noi4mat=spio.loadmat(matfilename)
        sim = comp(noi4mat['OutputMap'],noi4test)
        if(sim<NOI4_CRITERIA):
            print('NOI4: FAIL Similarity: ' + str(sim))
        else:
            print('NOI4: PASS')

    elif algoname == 'NOI5':
        noi5test=PCANoise(infilename)
        noi5mat=spio.loadmat(matfilename)
        sim = comp(noi5mat['OutputMap'],noi5test[0])
        if(sim<NOI5_CRITERIA):
            print('NOI5 OutputMap: FAIL Similarity: ' + str(sim))
        else:
            print('NOI5 OutputMap: PASS')
        sim = comp(noi5mat['OutputMap_Quant'],noi5test[1],multichannel=True)
        if(sim<NOI5_CRITERIA):
            print('NOI5 OutputMap_Quant: FAIL Similarity: ' + str(sim))
        else:
            print('NOI5 OutputMap_Quant: PASS')

    else:
        print('Unknown algorithm: ' + algoname)

if __name__ == "__main__":
    main(sys.argv[1:])
