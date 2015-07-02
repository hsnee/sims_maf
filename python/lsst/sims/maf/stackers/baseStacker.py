import inspect
import warnings
import numpy as np
import numpy.lib.recfunctions as rfn

__all__ = ['StackerRegistry', 'BaseStacker']

class StackerRegistry(type):
    """
    Meta class for Stackers, to build a registry of stacker classes.
    """
    def __init__(cls, name, bases, dict):
        super(StackerRegistry, cls).__init__(name, bases, dict)
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        modname = inspect.getmodule(cls).__name__
        if modname.startswith('lsst.sims.maf.stackers'):
            modname = ''
        else:
            if len(modname.split('.')) > 1:
                modname = '.'.join(modname.split('.')[:-1]) + '.'
            else:
                modname = modname + '.'
        stackername = modname + name
        if stackername in cls.registry:
            raise Exception('Redefining stacker %s! (there are >1 stackers with the same name)' %(stackername))
        if stackername != 'BaseStacker':
            cls.registry[stackername] = cls
    def getClass(cls, stackername):
        return cls.registry[stackername]
    def list(cls, doc=False):
        for stackername in sorted(cls.registry):
            if not doc:
                print stackername
            if doc:
                print '---- ', stackername, ' ----'
                print cls.registry[stackername].__doc__
                stacker = cls.registry[stackername]()
                print ' Columns added to SimData: ', ','.join(stacker.colsAdded)
                print ' Default columns required: ', ','.join(stacker.colsReq)


class BaseStacker(object):
    """Base MAF Stacker: add columns generated at run-time to the simdata array."""
    __metaclass__ = StackerRegistry

    def __init__(self):
        """
        Instantiate the stacker.
        This method should be overriden by the user. This serves as an example of
        the variables required by the framework.
        """
        # List of the names of the columns generated by the Stacker.
        self.colsAdded = [None]
        # List of the names of the columns required from the database (to generate the Stacker columns).
        self.colsReq = [None]
        # Optional: specify the new column types.
        self.colsAddedDtypes = None
        # Optional: provide a list of units for the columns defined in colsAdded.
        self.units = [None]

    def __eq__(self, otherStacker):
        """
        Evaluate if two stackers are equivalent.
        """
        # Are we comparing two classes before instantiation?
        if (self.__class__.__name__ == 'StackerRegistry' and
            otherStacker.__class__.__name__ == 'StackerRegistry'):
            if self.__name__ == otherStacker.__name__:
                return True
            else:
                return False
        # otherwise, we are not and these are instantiated stacker objects.
        # If the class names are different, they are not 'the same'.
        if self.__class__.__name__ != otherStacker.__class__.__name__:
            return False
        # Otherwise, this is the same stacker class, but may be instantiated differently.
        #  We have to delve a little further, and look at the kwargs for each stacker.
        # We assume that they are equal, unless they have specific attributes which are different.
        stateNow = dir(self)
        for key in stateNow:
            if not key.startswith('_') and key!='registry' and key!='run':
                if not hasattr(otherStacker, key):
                    return False
                # If the attribute is from numpy, assume it's an array and test it
                if type(getattr(self,key)).__module__ == np.__name__:
                    if not np.array_equal(getattr(self,key), getattr(otherStacker, key)):
                        return False
                else:
                    # If the attribute is from numpy, assume it's an array and test it
                    if type(getattr(self,key)).__module__ == np.__name__:
                        if not np.array_equal(getattr(self,key), getattr(otherStacker, key)):
                            return False
                    else:
                        if getattr(self, key) != getattr(otherStacker, key):
                            return False
        return True


    def __ne__(self, otherStacker):
        """
        Evaluate if two stackers are not equal.
        """
        if self == otherStacker:
            return False
        else:
            return True

    def _addStackers(self, simData):
        """
        Add the new Stacker columns to the simData array.
        If columns already present in simData, just allows 'run' method to overwrite.
        Returns simData array with these columns added (so 'run' method can set their values).
        """
        newcolList = [simData]
        if not hasattr(self, 'colsAddedDtypes') or self.colsAddedDtypes is None:
            self.colsAddedDtypes = [float for col in self.colsAdded]
        for col, dtype in zip(self.colsAdded, self.colsAddedDtypes):
            if col in simData:
                warnings.warn('Warning - column %s already present in simData, will be overwritten.'
                              %(col))
            else:
                newcol = np.empty(len(simData), dtype=[(col, dtype)])
                newcolList.append(newcol)
        return rfn.merge_arrays(newcolList, flatten=True, usemask=False)

    def run(self, simData):
        """
        Example: Generate the new stacker columns, given the simdata columns from the database.
        Returns the new simdata structured aray that includes the new stacker columns.
        """
        # Add new columns
        simData=self._addStackers(simData)
        # Populate the data in those columns.
        ## simData['newcol'] = XXXX
        return simData
