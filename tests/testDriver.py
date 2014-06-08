import numpy as np 
import matplotlib
matplotlib.use('Agg')
import unittest
import lsst.sims.maf.driver as driver
from lsst.sims.maf.driver.mafConfig import MafConfig
import glob
from subprocess import Popen
import os
import inspect
import shutil


#things to make sure I exercise

#multiple binners--with kwargs, params, setupkwrd, setupParams, constraints, stackCols, plotConfigs, metadata

# Need to test all the convienence functions


class TestDriver(unittest.TestCase):
    
    def setUp(self):
        # Files to loop over
        self.cfgFiles = ['mafconfigTest.cfg', 'mafconfigTest2.cfg']
        # Files that get created by those configs
        self.outputFiles= [['date_version_ran.dat','maf_config_asRan.py','OpsimTest_CoaddedM5__r_HEAL.npz','OpsimTest_CoaddedM5__r_HEAL_Histogram.png','OpsimTest_CoaddedM5__r_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__r_HEAL_SkyMap.png','OpsimTest_CoaddedM5__r_OPSI.npz','OpsimTest_CoaddedM5__r_OPSI_Histogram.png','OpsimTest_CoaddedM5__r_OPSI_SkyMap.png','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL.npz','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL_Histogram.png','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL_SkyMap.png','OpsimTest_CoaddedM5__r_and_night_<_730_OPSI.npz','OpsimTest_CoaddedM5__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_CoaddedM5__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL.npz','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL_Histogram.png','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL_SkyMap.png','OpsimTest_CoaddedM5__rdith_HEAL.npz','OpsimTest_CoaddedM5__rdith_HEAL_Histogram.png','OpsimTest_CoaddedM5__rdith_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__rdith_HEAL_SkyMap.png','OpsimTest_Count_expMJD__r_HEAL.npz','OpsimTest_Count_expMJD__r_HEAL_Histogram.png','OpsimTest_Count_expMJD__r_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__r_HEAL_SkyMap.png','OpsimTest_Count_expMJD__r_OPSI.npz','OpsimTest_Count_expMJD__r_OPSI_Histogram.png','OpsimTest_Count_expMJD__r_OPSI_SkyMap.png','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL.npz','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL_Histogram.png','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL_SkyMap.png','OpsimTest_Count_expMJD__r_and_night_<_730_OPSI.npz','OpsimTest_Count_expMJD__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_Count_expMJD__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL.npz','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL_Histogram.png','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL_SkyMap.png','OpsimTest_Count_expMJD__rdith_HEAL.npz','OpsimTest_Count_expMJD__rdith_HEAL_Histogram.png','OpsimTest_Count_expMJD__rdith_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__rdith_HEAL_SkyMap.png','OpsimTest_Count_normairmass__r_ONED.npz','OpsimTest_Count_normairmass__r_ONED_BinnedData.png','OpsimTest_Count_normairmass__r_and_night_<_730_ONED.npz','OpsimTest_Count_normairmass__r_and_night_<_730_ONED_BinnedData.png','OpsimTest_Count_slewDist__r_ONED.npz','OpsimTest_Count_slewDist__r_ONED_BinnedData.png','OpsimTest_Count_slewDist__r_and_night_<_730_ONED.npz','OpsimTest_Count_slewDist__r_and_night_<_730_ONED_BinnedData.png','OpsimTest_Mean_airmass_night_<_750_UNIB.npz','OpsimTest_Mean_normairmass__r_OPSI.npz','OpsimTest_Mean_normairmass__r_OPSI_Histogram.png','OpsimTest_Mean_normairmass__r_OPSI_SkyMap.png','OpsimTest_Mean_normairmass__r_and_night_<_730_OPSI.npz','OpsimTest_Mean_normairmass__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_Mean_normairmass__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_Min_airmass__r_OPSI.npz','OpsimTest_Min_airmass__r_OPSI_Histogram.png','OpsimTest_Min_airmass__r_OPSI_SkyMap.png','OpsimTest_Min_airmass__r_and_night_<_730_OPSI.npz','OpsimTest_Min_airmass__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_Min_airmass__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_hourglass_HOUR_hr.png','OpsimTest_hourglass_night_<_750_HOUR_hr.png','OpsimTest_normAir_hex__r_ONED.npz','OpsimTest_normAir_hex__r_ONED_BinnedData.png','OpsimTest_normAir_hex__r_and_night_<_730_ONED.npz','OpsimTest_normAir_hex__r_and_night_<_730_ONED_BinnedData.png','summaryStats.dat'],['date_version_ran.dat','maf_config_asRan.py','OpsimTest_CoaddedM5__r_HEAL.npz','OpsimTest_CoaddedM5__r_HEAL_Histogram.png','OpsimTest_CoaddedM5__r_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__r_HEAL_SkyMap.png','OpsimTest_CoaddedM5__r_OPSI.npz','OpsimTest_CoaddedM5__r_OPSI_Histogram.png','OpsimTest_CoaddedM5__r_OPSI_SkyMap.png','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL.npz','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL_Histogram.png','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__r_and_night_<_730_HEAL_SkyMap.png','OpsimTest_CoaddedM5__r_and_night_<_730_OPSI.npz','OpsimTest_CoaddedM5__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_CoaddedM5__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL.npz','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL_Histogram.png','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__r_and_night_<_730dith_HEAL_SkyMap.png','OpsimTest_CoaddedM5__rdith_HEAL.npz','OpsimTest_CoaddedM5__rdith_HEAL_Histogram.png','OpsimTest_CoaddedM5__rdith_HEAL_PowerSpectrum.png','OpsimTest_CoaddedM5__rdith_HEAL_SkyMap.png','OpsimTest_Count_expMJD__r_HEAL.npz','OpsimTest_Count_expMJD__r_HEAL_Histogram.png','OpsimTest_Count_expMJD__r_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__r_HEAL_SkyMap.png','OpsimTest_Count_expMJD__r_OPSI.npz','OpsimTest_Count_expMJD__r_OPSI_Histogram.png','OpsimTest_Count_expMJD__r_OPSI_SkyMap.png','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL.npz','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL_Histogram.png','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__r_and_night_<_730_HEAL_SkyMap.png','OpsimTest_Count_expMJD__r_and_night_<_730_OPSI.npz','OpsimTest_Count_expMJD__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_Count_expMJD__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL.npz','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL_Histogram.png','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__r_and_night_<_730dith_HEAL_SkyMap.png','OpsimTest_Count_expMJD__rdith_HEAL.npz','OpsimTest_Count_expMJD__rdith_HEAL_Histogram.png','OpsimTest_Count_expMJD__rdith_HEAL_PowerSpectrum.png','OpsimTest_Count_expMJD__rdith_HEAL_SkyMap.png','OpsimTest_Count_slewDist__r_ONED.npz','OpsimTest_Count_slewDist__r_ONED_BinnedData.png','OpsimTest_Count_slewDist__r_and_night_<_730_ONED.npz','OpsimTest_Count_slewDist__r_and_night_<_730_ONED_BinnedData.png','OpsimTest_Mean_airmass_night_<_750_UNIB.npz','OpsimTest_Mean_normairmass__r_OPSI.npz','OpsimTest_Mean_normairmass__r_OPSI_Histogram.png','OpsimTest_Mean_normairmass__r_OPSI_SkyMap.png','OpsimTest_Mean_normairmass__r_and_night_<_730_OPSI.npz','OpsimTest_Mean_normairmass__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_Mean_normairmass__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_Min_airmass__r_OPSI.npz','OpsimTest_Min_airmass__r_OPSI_Histogram.png','OpsimTest_Min_airmass__r_OPSI_SkyMap.png','OpsimTest_Min_airmass__r_and_night_<_730_OPSI.npz','OpsimTest_Min_airmass__r_and_night_<_730_OPSI_Histogram.png','OpsimTest_Min_airmass__r_and_night_<_730_OPSI_SkyMap.png','OpsimTest_hourglass_HOUR_hr.png','OpsimTest_hourglass_night_<_750_HOUR_hr.png','summaryStats.dat']]
        self.filepath = os.environ['SIMS_MAF_DIR']+'/tests/'
        #self.filepath=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+'/'
    def test_overwrite(self):
        filename = 'mafconfigTest3.cfg'
        configIn = MafConfig()
        configIn.load(self.filepath+filename)
        self.assertRaises(Exception, driver.MafDriver,**{'configvalues':configIn})
        filename = 'mafconfigTest5.cfg'
        configIn = MafConfig()
        configIn.load(self.filepath+filename)
        self.assertRaises(Exception, driver.MafDriver,**{'configvalues':configIn})

    def test_driver(self):
        
        for i,filename in enumerate(self.cfgFiles):
            configIn = MafConfig()
            configIn.load(self.filepath+filename)
            nnpz = glob.glob(configIn.outputDir+'/*.npz')
            if len(nnpz) > 0:
                ack = Popen('rm '+configIn.outputDir+'/*.npz', shell=True).wait()


            testDriver = driver.MafDriver(configIn)
            testDriver.run()

            configOut = MafConfig()
            configOut.load(configIn.outputDir+'/maf_config_asRan.py')
            assert(configIn == configOut)
            nout=0
            for j,binner in enumerate(configIn.binners):
                if configIn.binners[j].name != 'HourglassBinner':
                    nout += len(configIn.binners[j].constraints)*len(configIn.binners[j].metricDict)

            nnpz = glob.glob(configIn.outputDir+'/*.npz')
            assert(os.path.isfile(configIn.outputDir+'/date_version_ran.dat'))
            assert(os.path.isfile(configIn.outputDir+'/summaryStats.dat'))
            filelist = self.outputFiles[i]
            for filename in filelist:
                if not os.path.isfile(configIn.outputDir+'/'+filename):
                    print 'missing file %s'%filename
                assert(os.path.isfile(configIn.outputDir+'/'+filename))
            assert(nout == len(nnpz))

    def tearDown(self):
        if os.path.isdir('Output'):
            shutil.rmtree('Output')
        if os.path.isdir('Output_2'):
            shutil.rmtree('Output_2')
       
if __name__ == '__main__':
    unittest.main()



