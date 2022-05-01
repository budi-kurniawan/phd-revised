import glob
from unittest import TestCase, TestSuite, TextTestResult
import unittest

test_files = glob.glob('*test_case.py') + glob.glob('rlagents/rl_agent/*test_case.py')
print('\nTesting', test_files)
module_strings = [test_file[0:len(test_file)-3] for test_file in test_files]
suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
test_suite = TestSuite(suites)
test_runner = unittest.TextTestRunner().run(test_suite)