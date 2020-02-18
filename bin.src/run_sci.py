#!/usr/bin/env python

"""
Run the SRD metrics.
"""

from __future__ import print_function

import matplotlib
matplotlib.use('Agg')
import lsst.sims.maf.batches as batches
from run_generic import *


def setBatches(opsdb, colmap, args):
    propids, proptags, sqls, metadata = setSQL(opsdb, sqlConstraint=args.sqlConstraint,
                                               extraMeta=None)

    bdict = {}
    sciR = batches.scienceRadarBatch(colmap=colmap, runName=args.runName,
                                    extraSql=sqls['All'], extraMetadata=metadata['All'], DDF=True)
    bdict.update(sciR)


    return bdict


if __name__ == '__main__':
    args = parseArgs(subdir='srd')
    opsdb, colmap = connectDb(args.dbfile)
    bdict = setBatches(opsdb, colmap, args)
    if args.plotOnly:
        replot(bdict, opsdb, colmap, args)
    else:
        run(bdict, opsdb, colmap, args)
    opsdb.close()
