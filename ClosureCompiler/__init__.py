import typing
from pathlib import Path

from .enums import TypeInferMode
from .lowLevel import *
from .lowLevel import _optionsComponentTypes, _otherEssentialClasses

__all__ = ("SourcesMappingTU", "Compiler", "createCompilerOptions") + _optionsComponentTypes + _otherEssentialClasses


class ClosureCompilerErrror(RuntimeError):
	__slots__ = ()


class Compiler:
	__slots__ = ("compiler", "options")

	def __init__(self, options: typing.Optional[CompilerOptions] = None) -> None:
		if options is None:
			options = createCompilerOptions()

		self.options = options
		self.compiler = None

	@property
	def _jsRoot(self):
		prop = ji.reflectClass(self.compiler.__class__).getDeclaredField("jsRoot")
		prop.setAccessible(True)
		return prop.get(self.compiler)

	def getBuiltInExterns(self):
		return getBuiltInExterns(self.options.getEnvironment())

	def __call__(self, sources: SourcesMappingTU, externs: typing.Optional[SourcesMappingTU] = None) -> Result:
		return self.compile(sources, externs)

	def compile(self, sources: SourcesMappingTU, externs: typing.Optional[SourcesMappingTU] = None) -> Result:
		sources = convertSourcesMapping(sources)

		builtinExterns = self.getBuiltInExterns()
		if externs:
			externs = convertSourcesMapping(externs)
		else:
			externs = []

		self.compiler = ji.Compiler()
		lowLevelRes = self.compiler.compile(
			ji.ArrayList(externs + builtinExterns),
			ji.ArrayList(sources),
			self.options,
		)

		return Result.fromNativeResult(str(self.compiler.toSource()), lowLevelRes)
