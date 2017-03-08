#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________
#
# Tests for Pyomo kernel examples
#

import os
import glob
from os.path import basename, dirname, abspath, join

import pyutilib.subprocess
import pyutilib.th as unittest

currdir = dirname(abspath(__file__))
topdir = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))
examplesdir = join(topdir, "examples", "kernel")

examples = glob.glob(join(examplesdir,"*.py"))

numpy_available = False
try:
    import numpy
    numpy_available = True
except:
    pass

scipy_available = False
try:
    import scipy
    scipy_available = True
except:
    pass

testing_solvers = {}
testing_solvers['ipopt','nl'] = False
testing_solvers['glpk','lp'] = False
def setUpModule():
    global testing_solvers
    import pyomo.environ
    from pyomo.solvers.tests.solvers import test_solver_cases
    for _solver, _io in test_solver_cases():
        if (_solver, _io) in testing_solvers and \
            test_solver_cases(_solver, _io).available:
            testing_solvers[_solver, _io] = True

@unittest.nottest
def create_test_method(example, skip=None):
    # It is important that this inner function has a name that
    # starts with 'test' in order for nose to discover it
    # after we assign it to the class. I have _no_ idea why
    # this is the case since we are returing the function object
    # and placing it on the class with a different name.
    def testmethod(self):
        if skip is not None:
            self.skipTest(skip)
        rc, log = pyutilib.subprocess.run(['python',example])
        self.assertEqual(rc, 0, msg=log)
    return testmethod

@unittest.category("smoke", "nightly", "expensive")
class TestKernelExamples(unittest.TestCase):
    pass
for filename in examples:
    skip = None
    testname = basename(filename)
    assert testname.endswith(".py")
    if testname == "piecewise_nd_functions.py":
        if (not numpy_available) or \
           (not scipy_available) or \
           (not testing_solvers['ipopt','nl']) or \
           (not testing_solvers['glpk','lp']):
            skip = "Numpy or Scipy or Ipopt or Glpk is not available"
    testname = "test_"+testname[:-3]+"_example"
    setattr(TestKernelExamples,
            testname,
            create_test_method(filename, skip=skip))

if __name__ == "__main__":
    unittest.main()