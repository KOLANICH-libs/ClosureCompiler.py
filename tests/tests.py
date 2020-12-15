#!/usr/bin/env python3
import itertools
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from collections import OrderedDict

dict = OrderedDict

import ClosureCompiler
from ClosureCompiler import CompilationLevel, Compiler, createCompilerOptions


def _enumValueName(v):
	return v.__class__.__name__.split(".")[-1] + "." + str(v)


class Tests(unittest.TestCase):
	def testSuccess(self):
		challenge = "const m = 'aaaa'; function a(){alert(m);} a();"
		matrix = {
			CompilationLevel.ADVANCED_OPTIMIZATIONS: "'use strict';\nalert(\"aaaa\");\n",
			CompilationLevel.SIMPLE_OPTIMIZATIONS: "'use strict';\nconst m = \"aaaa\";\nfunction a() {\n  alert(m);\n}\na();\n",
			CompilationLevel.WHITESPACE_ONLY: "'use strict';\nconst m = \"aaaa\";\nfunction a() {\n  alert(m);\n}\na();\n",
		}

		for level, etalon in matrix.items():
			with self.subTest(level=_enumValueName(level), etalon=etalon):
				c = Compiler(createCompilerOptions(level=level))
				res = c({"source.jsm": challenge})
				self.assertTrue(res.isSuccess)
				self.assertEqual(res.js, etalon)

	def testError(self):
		c = Compiler()
		res = c({"source.jsm": "const asdf = 'aaaa';asdf = 'bbbb';"})
		self.assertFalse(res.isSuccess)
		self.assertEqual(len(res.errors), 1)
		self.assertEqual(res.errors.__class__, tuple)
		self.assertEqual(str(res.errors[0]), "JSC_REASSIGNED_CONSTANT. Constant reassigned: asdf at source.jsm line 1 : 20")


if __name__ == "__main__":
	unittest.main()
