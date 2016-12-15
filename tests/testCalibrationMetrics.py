import matplotlib
matplotlib.use("Agg")
import numpy as np
import unittest
import lsst.sims.maf.metrics as metrics
import lsst.sims.maf.stackers as stackers
import lsst.utils.tests


class TestCalibrationMetrics(unittest.TestCase):

    def testParallaxMetric(self):
        """
        Test the parallax metric.
        """
        names = ['observationStartMJD', 'finSeeing', 'fiveSigmaDepth', 'ra_rad', 'dec_rad', 'filter']
        types = [float, float, float, float, float, '|S1']
        data = np.zeros(700, dtype=zip(names, types))
        slicePoint = {'sid': 0}
        data['observationStartMJD'] = np.arange(700)+56762
        data['finSeeing'] = 0.7
        data['filter'][0:100] = 'r'
        data['filter'][100:200] = 'u'
        data['filter'][200:] = 'g'
        data['fiveSigmaDepth'] = 24.
        stacker = stackers.ParallaxFactorStacker()
        data = stacker.run(data)
        normFlags = [False, True]
        for flag in normFlags:
            data['finSeeing'] = 0.7
            data['fiveSigmaDepth'] = 24.
            baseline = metrics.ParallaxMetric(normalize=flag, seeingCol='finSeeing').run(data, slicePoint)
            data['finSeeing'] = data['finSeeing']+.3
            worse1 = metrics.ParallaxMetric(normalize=flag, seeingCol='finSeeing').run(data, slicePoint)
            worse2 = metrics.ParallaxMetric(normalize=flag, rmag=22.,
                                            seeingCol='finSeeing').run(data, slicePoint)
            worse3 = metrics.ParallaxMetric(normalize=flag, rmag=22.,
                                            seeingCol='finSeeing').run(data[0:300], slicePoint)
            data['fiveSigmaDepth'] = data['fiveSigmaDepth']-1.
            worse4 = metrics.ParallaxMetric(normalize=flag, rmag=22.,
                                            seeingCol='finSeeing').run(data[0:300], slicePoint)
            # Make sure the RMS increases as seeing increases, the star gets fainter,
            #    the background gets brighter, or the baseline decreases.
            if flag:
                pass
            else:
                assert(worse1 > baseline)
                assert(worse2 > worse1)
                assert(worse3 > worse2)
                assert(worse4 > worse3)

    def testProperMotionMetric(self):
        """
        Test the ProperMotion metric.
        """
        names = ['observationStartMJD', 'finSeeing', 'fiveSigmaDepth', 'ra_rad', 'dec_rad', 'filter']
        types = [float, float, float, float, float, '|S1']
        data = np.zeros(700, dtype=zip(names, types))
        slicePoint = [0]
        stacker = stackers.ParallaxFactorStacker()
        normFlags = [False, True]
        data['observationStartMJD'] = np.arange(700)+56762
        data['finSeeing'] = 0.7
        data['filter'][0:100] = 'r'
        data['filter'][100:200] = 'u'
        data['filter'][200:] = 'g'
        data['fiveSigmaDepth'] = 24.
        data = stacker.run(data)
        for flag in normFlags:
            data['finSeeing'] = 0.7
            data['fiveSigmaDepth'] = 24
            baseline = metrics.ProperMotionMetric(normalize=flag, seeingCol='finSeeing').run(data, slicePoint)
            data['finSeeing'] = data['finSeeing']+.3
            worse1 = metrics.ProperMotionMetric(normalize=flag, seeingCol='finSeeing').run(data, slicePoint)
            worse2 = metrics.ProperMotionMetric(normalize=flag, rmag=22.,
                                                seeingCol='finSeeing').run(data, slicePoint)
            worse3 = metrics.ProperMotionMetric(normalize=flag, rmag=22.,
                                                seeingCol='finSeeing').run(data[0:300], slicePoint)
            data['fiveSigmaDepth'] = data['fiveSigmaDepth']-1.
            worse4 = metrics.ProperMotionMetric(normalize=flag, rmag=22.,
                                                seeingCol='finSeeing').run(data[0:300], slicePoint)
            # Make sure the RMS increases as seeing increases, the star gets fainter,
            # the background gets brighter, or the baseline decreases.
            if flag:
                # When normalized, mag of star and m5 don't matter (just scheduling).
                self.assertAlmostEqual(worse2, worse1)
                self.assertAlmostEqual(worse4, worse3)
                # But using fewer points should make proper motion worse.
                # survey assumed to have same seeing and limiting mags.
                assert(worse3 < worse2)
            else:
                assert(worse1 > baseline)
                assert(worse2 > worse1)
                assert(worse3 > worse2)
                assert(worse4 > worse3)

    def testParallaxCoverageMetric(self):
        """
        Test the parallax coverage
        """
        names = ['observationStartMJD', 'finSeeing', 'fiveSigmaDepth', 'ra_rad', 'dec_rad',
                 'filter', 'ra_pi_amp', 'dec_pi_amp']
        types = [float, float, float, float, float, '|S1', float, float]
        data = np.zeros(100, dtype=zip(names, types))
        data['filter'] = 'r'
        data['fiveSigmaDepth'] = 25.
        data['ra_pi_amp'] = 1.
        data['dec_pi_amp'] = 1.

        # All the parallax amplitudes are the same, should return zero
        metric = metrics.ParallaxCoverageMetric(seeingCol='finSeeing')
        val = metric.run(data)
        assert(val == 0)

        # Half at (1,1), half at (0.5,0.5)
        data['ra_pi_amp'][0:50] = 1
        data['dec_pi_amp'][0:50] = 1
        data['ra_pi_amp'][50:] = -1
        data['dec_pi_amp'][50:] = -1
        val = metric.run(data)
        self.assertAlmostEqual(val, 2.**0.5)

        data['ra_pi_amp'][0:50] = 0.5
        data['dec_pi_amp'][0:50] = 0.5
        data['ra_pi_amp'][50:] = -0.5
        data['dec_pi_amp'][50:] = -0.5
        val = metric.run(data)
        self.assertAlmostEqual(val, 0.5*2**0.5)

        data['ra_pi_amp'][0:50] = 1
        data['dec_pi_amp'][0:50] = 0
        data['ra_pi_amp'][50:] = -1
        data['dec_pi_amp'][50:] = 0
        val = metric.run(data)
        assert(val == 1)

    def testParallaxDcrDegenMetric(self):
        """
        Test the parallax-DCR degeneracy metric
        """
        names = ['observationStartMJD', 'finSeeing', 'fiveSigmaDepth', 'ra_rad', 'dec_rad',
                 'filter', 'ra_pi_amp', 'dec_pi_amp', 'ra_dcr_amp', 'dec_dcr_amp']
        types = [float, float, float, float, float, '|S1', float,
                 float, float, float]
        data = np.zeros(100, dtype=zip(names, types))
        data['filter'] = 'r'
        data['fiveSigmaDepth'] = 25.

        # Set so ra is perfecly correlated
        data['ra_pi_amp'] = 1.
        data['dec_pi_amp'] = 0.01
        data['ra_dcr_amp'] = 0.2

        metric = metrics.ParallaxDcrDegenMetric(seeingCol='finSeeing')
        val = metric.run(data)
        np.testing.assert_almost_equal(np.abs(val), 1., decimal=2)

        # set so the offsets are always nearly perpendicular
        data['ra_pi_amp'] = 0.001
        data['dec_pi_amp'] = 1.
        data['ra_dcr_amp'] = 0.2

        metric = metrics.ParallaxDcrDegenMetric(seeingCol='finSeeing')
        val = metric.run(data)
        np.testing.assert_almost_equal(val, 0., decimal=2)

        # Generate a random distribution that should have little or no correlation
        np.random.seed(42)

        data['ra_pi_amp'] = np.random.rand(100)*2-1.
        data['dec_pi_amp'] = np.random.rand(100)*2-1.
        data['ra_dcr_amp'] = np.random.rand(100)*2-1.
        data['dec_dcr_amp'] = np.random.rand(100)*2-1.

        val = metric.run(data)
        assert(np.abs(val) < 0.2)

    def testRadiusObsMetric(self):
        """
        Test the RadiusObsMetric
        """

        names = ['ra_rad', 'dec_rad']
        dt = ['float']*2
        data = np.zeros(3, dtype=zip(names, dt))
        data['dec_rad'] = [-.1, 0, .1]
        slicePoint = {'ra': 0., 'dec': 0.}
        metric = metrics.RadiusObsMetric()
        result = metric.run(data, slicePoint)
        for i, r in enumerate(result):
            np.testing.assert_almost_equal(r, abs(data['dec_rad'][i]))
        assert(metric.reduceMean(result) == np.mean(result))
        assert(metric.reduceRMS(result) == np.std(result))
        np.testing.assert_almost_equal(metric.reduceFullRange(result),
                                       np.max(np.abs(data['dec_rad']))-np.min(np.abs(data['dec_rad'])))


class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
