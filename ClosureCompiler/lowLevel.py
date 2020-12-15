import sys
import typing
from pathlib import Path, PurePosixPath

import JAbs

try:
	from psutil import cpu_count
except ImportError:

	def cpu_count(logical: bool = True) -> int:
		return ji.Runtime.getRuntime().availableProcessors()


__all__ = ("ji", "MyErrorHandler", "NativeSourcesMappingT", "SourcesMappingTU", "convertSourcesMapping", "sources2Chunks", "getBuiltInExterns", "createCompilerOptions", "Result")

from .enums import TypeInferMode
from .util import selectJar

SourcesMappingT = typing.Mapping[PurePosixPath, str]

goog = "com.google"
common = goog + ".common"
collect = common + ".collect"
googJs = goog + ".javascript"
jscomp = googJs + ".jscomp"
rhino = googJs + ".rhino"
parsing = jscomp + ".parsing"
compOpts = jscomp + ".CompilerOptions"
parsingCfg = parsing + ".Config"

jarsDir = Path(".")
ji = JAbs.SelectedJVMInitializer(
	classPaths=[selectJar(jarsDir)],
	classes2import=[
		"java.lang.Runtime",
		"java.util.HashSet",
		"java.util.ArrayList",
		"java.io.FileInputStream",
		# collect + ".Lists",
		collect + ".ImmutableList",
		jscomp + ".AbstractCommandLineRunner",
		jscomp + ".AbstractCommandLineRunner.JsChunkSpec",
		jscomp + ".AbstractCompiler",
		jscomp + ".CheckLevel",
		jscomp + ".ClosureCodingConvention",
		jscomp + ".CodingConvention",
		jscomp + ".CodingConventions",
		jscomp + ".CommandLineRunner",
		jscomp + ".CompilationLevel",
		jscomp + ".Compiler",
		jscomp + ".CompilerInput",
		jscomp + ".CompilerInput$ModuleType",
		jscomp + ".CompilerOptions",
		jscomp + ".CompilerOptions.Es6ModuleTranspilation",
		jscomp + ".CompilerOptions.ExtractPrototypeMemberDeclarationsMode",
		jscomp + ".CompilerOptions.TweakProcessing",
		jscomp + ".ConformanceConfig",
		(jscomp + ".ConformanceConfig$Builder", "ConformanceConfigBuilder"),
		jscomp + ".DependencyOptions$DependencyMode",
		jscomp + ".deps.ClosureBundler",
		jscomp + ".deps.ModuleLoader",
		(jscomp + ".deps.ModuleLoader$ResolutionMode", "ModuleResolutionMode"),
		jscomp + ".deps.ModuleLoader.PathEscaper",
		jscomp + ".DiagnosticGroup",
		jscomp + ".DiagnosticGroups",
		jscomp + ".EmptyMessageBundle",
		jscomp + ".ErrorHandler",
		jscomp + ".JsAst",
		jscomp + ".JSChunk",
		jscomp + ".JSError",
		jscomp + ".PropertyRenamingPolicy",
		jscomp + ".RecoverableJsAst",
		jscomp + ".resources.ResourceLoader",
		jscomp + ".RhinoErrorReporter",
		jscomp + ".SourceAst",
		jscomp + ".SourceFile",
		jscomp + ".SourceMap$LocationMapping",
		jscomp + ".transpile.BaseTranspiler",
		jscomp + ".transpile.BaseTranspiler$CompilerSupplier",
		jscomp + ".transpile.Transpiler",
		jscomp + ".VariableRenamingPolicy",
		jscomp + ".WarningLevel",
		jscomp + ".WarningsGuard",
		jscomp + ".XtbMessageBundle",
		compOpts + "$ChunkOutputType",
		compOpts + "$DevMode",
		compOpts + "$Environment",
		compOpts + "$ExtractPrototypeMemberDeclarationsMode",
		compOpts + "$IncrementalCheckMode",
		compOpts + "$InstrumentOption",
		compOpts + "$IsolationMode",
		compOpts + "$J2clPassMode",
		(compOpts + "$LanguageMode", "CompileLanguageMode"),
		compOpts + "$TracerMode",
		parsing + ".parser.FeatureSet",
		parsing + ".parser.FeatureSet$Feature",
		parsing + ".ParserRunner",
		parsing + ".ParserRunner$ParseResult",
		(parsingCfg, "ParsingConfig"),
		parsingCfg + "$JsDocParsing",
		(parsingCfg + "$LanguageMode", "ParsingLanguageMode"),
		parsingCfg + "$RunMode",
		parsingCfg + "$StrictMode",
		rhino + ".ErrorReporter",
		rhino + ".Node",
		rhino + ".SimpleSourceFile",
		rhino + ".StaticSourceFile",
		rhino + ".StaticSourceFile$SourceKind",
	],
)


def _importFromJavaNamespace(names, locs) -> None:
	for name in names:
		locs[name] = getattr(ji, name)


_otherEssentialClasses = (
	"JSError",
	"SourceFile",
	"ErrorHandler",
	"CheckLevel",
	"ParsingLanguageMode",
	"JsDocParsing",
	"RunMode",
	"StrictMode",
	"ParsingConfig",
	"ParseResult",
	"SourceKind",
	"JSChunk",
	"CompilerOptions",
)
__all__ += _otherEssentialClasses

_importFromJavaNamespace(_otherEssentialClasses, locals())


class MyErrorHandler(ErrorHandler, metaclass=ji._Implements):
	@ji._Override
	def report(self, level: CheckLevel, error: JSError) -> None:
		"""
		level -  the reporting level
		error - the error to report
		"""
		print(level, error, file=sys.stderr)


_defaultErrorHandler = MyErrorHandler()

NativeSourcesMappingT = typing.List[SourceFile]


class Result:
	__slots__ = ("js", "errors", "warnings", "isSuccess")

	def __init__(self, js: typing.Optional[str], isSuccess: bool, errors: typing.Collection[JSError], warnings: typing.Collection[JSError]):
		self.js = js
		self.isSuccess = isSuccess
		self.errors = errors
		self.warnings = warnings

	def raiseOnError(self):
		if not self.isSuccess:
			raise ClosureCompilerErrror("JS compilation failed", self)

	def __str__(self) -> str:
		return self.js

	def __bool__(self):
		return self.js is not None and self.isSuccess

	@classmethod
	def fromNativeResult(cls, src: str, lowLevelRes) -> "Result":
		return cls(src, bool(lowLevelRes.success), tuple(lowLevelRes.errors), tuple(lowLevelRes.warnings))


def createParserConfig(
	languageMode: ParsingLanguageMode = ParsingLanguageMode.ES_NEXT,
	docStringParsing: JsDocParsing = JsDocParsing.INCLUDE_ALL_COMMENTS,
	runMode: RunMode = RunMode.KEEP_GOING,
	extraAnnotationNames: typing.Set[str] = set(),
	parseInlineSourceMaps: bool = False,
	strictMode: StrictMode = StrictMode.STRICT,
) -> ParsingConfig:
	return ji.ParserRunner.createConfig(languageMode, docStringParsing, runMode, ji.HashSet(extraAnnotationNames), parseInlineSourceMaps, strictMode)


def parseSource(sourceString: str, parserConfig, errorReporter, kind: SourceKind = SourceKind.STRONG, fileName: PurePosixPath = PurePosixPath("file.js")) -> ParseResult:
	sourceFile = ji.SimpleSourceFile(str(fileName), kind)
	parsedSource = ji.ParserRunner.parse(
		# StaticSourceFile
		sourceFile,
		sourceString,
		parserConfig,
		errorReporter,
	)
	parsedSource.ast.setStaticSourceFile(sourceFile)
	return parsedSource


def _convertSourcesMapping(sources: SourcesMappingT) -> NativeSourcesMappingT:
	res = []
	for fileName, sourceString in sources.items():
		sourceFile = ji.SourceFile.fromCode(str(fileName), sourceString, ji.SourceKind.STRONG)
		res.append(sourceFile)

	return res


SourcesMappingTU = typing.Union[SourcesMappingT, NativeSourcesMappingT]


def convertSourcesMapping(sources: SourcesMappingTU) -> NativeSourcesMappingT:
	if isinstance(sources, dict):
		sources = _convertSourcesMapping(sources)

	return sources


def sources2Chunks(sources: NativeSourcesMappingT) -> typing.Collection[JSChunk]:
	chunks = []
	for s in sources:
		c = JSChunk(s.getName())
		c.add(s)
		chunks.append(c)
	return chunks


_optionsComponentTypes = (
	"CompileLanguageMode",
	"CompilationLevel",
	"WarningLevel",
	"J2clPassMode",
	"CodingConvention",
	"Environment",
	"IncrementalCheckMode",
	"ChunkOutputType",
	"ConformanceConfig",
	"TracerMode",
	"ModuleResolutionMode",
	"VariableRenamingPolicy",
	"PropertyRenamingPolicy",
	"InstrumentOption",
	"ErrorHandler",
	"TweakProcessing",
	"Es6ModuleTranspilation",
	"WarningsGuard",
	"PathEscaper",
)
__all__ += _optionsComponentTypes

_importFromJavaNamespace(_optionsComponentTypes, locals())


def getBuiltInExterns(env: Environment) -> NativeSourcesMappingT:
	return list(ji.AbstractCommandLineRunner.getBuiltinExterns(env))


def createCompilerOptions(
	*,
	languageIn: CompileLanguageMode = CompileLanguageMode.ECMASCRIPT_NEXT,
	languageOut: CompileLanguageMode = CompileLanguageMode.ECMASCRIPT_NEXT,
	level=CompilationLevel.ADVANCED_OPTIMIZATIONS,
	prettyPrint: bool = True,
	environment: Environment = Environment.BROWSER,
	chunkOutputType: ChunkOutputType = ChunkOutputType.GLOBAL_NAMESPACE,
	typedAstOutputFile: Path = None,
	generateExports: bool = False,
	moduleResolutionMode: ModuleResolutionMode = ModuleResolutionMode.BROWSER,
	wLevel=WarningLevel.VERBOSE,
	codingConvertion: typing.Optional[CodingConvention] = None,
	allowDynamicImport: bool = True,
	angularPass: bool = False,
	applyInputSourceMaps: bool = False,
	assumeNoPrototypeMethodEnumeration: bool = False,
	assumeStaticInheritanceIsNotUsed: bool = True,
	browserResolverPrefixReplacements: typing.Mapping[str, str] = None,
	checkSuspiciousCode: bool = True,
	chromePass: bool = False,
	conformanceConfigs: typing.Tuple[ConformanceConfig] = (),
	continueAfterErrors: bool = False,
	devMode: ji.DevMode = ji.DevMode.OFF,
	dynamicImportAlias: typing.Optional[str] = None,
	emitUseStrict: bool = True,
	errorHandler: ErrorHandler = None,
	es6ModuleTranspilation: Es6ModuleTranspilation = Es6ModuleTranspilation.COMPILE,
	exportLocalPropertyDefinitions: bool = False,
	extraAnnotationName: typing.List[str] = (),
	forceInjectLibraries: typing.List[str] = [],
	incrementalCheckMode: IncrementalCheckMode = IncrementalCheckMode.OFF,
	injectLibraries: bool = True,
	instrumentCodeParsed: InstrumentOption = InstrumentOption.NONE,
	isolatePolyfills: bool = False,
	j2clPassMode=J2clPassMode.AUTO,
	modulePathEscaper: PathEscaper = PathEscaper.ESCAPE,
	moduleRoots: typing.Optional[typing.Collection[str]] = None,
	numParallelThreads: typing.Optional[int] = None,
	packageJsonEntryNames: typing.Iterable[str] = (),
	parseInlineSourceMaps: bool = True,
	polymerVersion: typing.Optional[int] = None,
	preserveClosurePrimitives: bool = True,
	preserveTypeAnnotations: bool = False,
	printSourceAfterEachPass: bool = False,
	processClosurePrimitives: bool = False,
	productionInstrumentationArrayName: str = "",
	propertyRenamingPolicy: typing.Optional[PropertyRenamingPolicy] = None,
	quoteKeywordProperties: bool = False,
	removeJ2cLAsserts: bool = False,
	renamePrefixNamespace: typing.Optional[str] = None,
	renamePrefix: typing.Optional[str] = None,
	rewritePolyfills: bool = False,
	sourceMapIncludeSourcesContent: bool = False,
	strictModeInput: bool = True,
	tracerMode: TracerMode = TracerMode.OFF,
	translationsFile: typing.Optional[Path] = None,
	translationsProject: typing.Optional[str] = None,
	tweakProcessing: TweakProcessing = TweakProcessing.OFF,
	typingMode: TypeInferMode = TypeInferMode.check,
	variableRenamingPolicy: typing.Optional[VariableRenamingPolicy] = None,
	warningGuards: typing.Iterable[WarningsGuard] = (),
) -> CompilerOptions:
	options = CompilerOptions()  # type: CompilerOptions

	# additional options not present in CommandLineRunner
	options.setInferTypes(bool(typingMode & TypeInferMode.infer))
	options.setCheckTypes(bool(typingMode & TypeInferMode.check))
	options.setDevMode(devMode)
	if errorHandler is None:
		errorHandler = _defaultErrorHandler
	options.setErrorHandler(errorHandler)
	options.setCheckSuspiciousCode(checkSuspiciousCode)
	options.setPreserveClosurePrimitives(preserveClosurePrimitives)
	options.setTweakProcessing(tweakProcessing)
	options.setEs6ModuleTranspilation(es6ModuleTranspilation)
	options.setQuoteKeywordProperties(quoteKeywordProperties)
	options.setPrettyPrint(prettyPrint)
	for wG in warningGuards:
		options.addWarningsGuard(wG)
	options.setParseInlineSourceMaps(parseInlineSourceMaps)
	options.setApplyInputSourceMaps(applyInputSourceMaps)
	if moduleRoots is not None:
		options.setModuleRoots(ji.ArrayList(moduleRoots))
	options.setPathEscaper(modulePathEscaper)

	# setting mirroring the structure of CommandLineRunner
	options.setLanguageIn(languageIn)
	options.setLanguageOut(languageOut)
	if codingConvertion is None:
		codingConvertion = ji.CodingConventions.getDefault()
	options.setCodingConvention(codingConvertion)
	options.setExtraAnnotationNames(extraAnnotationName)

	level.setOptionsForCompilationLevel(options)
	level.setDebugOptionsForCompilationLevel(options)

	if numParallelThreads is None:
		numParallelThreads = cpu_count(logical=True)

	options.setNumParallelThreads(numParallelThreads)
	options.setEnvironment(environment)
	options.setIncrementalChecks(incrementalCheckMode)
	options.setContinueAfterErrors(continueAfterErrors)

	# TODO(b/144593112): remove this flag.
	options.setBadRewriteModulesBeforeTypecheckingThatWeWantToGetRidOf(True)
	level.setTypeBasedOptimizationOptions(options)

	if chunkOutputType == ji.ChunkOutputType.ES_MODULES:
		level.setWrappedOutputOptimizations(options)

	if typedAstOutputFile is not None:
		options.setTypedAstOutputFile(ji.Path(str(typedAstOutputFile)))

	options.setGenerateExports(generateExports)
	options.setExportLocalPropertyDefinitions(exportLocalPropertyDefinitions)

	wLevel.setOptionsForWarningLevel(options)
	# for formattingOption in flags.formatting:  # FormattingOption
	# 	formattingOption.applyToOptions(options)

	options.closurePass = processClosurePrimitives
	options.angularPass = angularPass
	options.polymerVersion = polymerVersion
	# options.polymerExportPolicy =
	options.setChromePass(chromePass)

	options.setJ2clPass(j2clPassMode)

	options.removeJ2clAsserts = removeJ2cLAsserts
	options.renamePrefix = renamePrefix

	options.setPreserveTypeAnnotations(preserveTypeAnnotations)
	options.setPreventLibraryInjection(not injectLibraries)

	options.setForceLibraryInjection([str(el) for el in forceInjectLibraries])

	options.rewritePolyfills = rewritePolyfills and languageIn.toFeatureSet().contains(FeatureSet.ES2015)
	options.setIsolatePolyfills(isolatePolyfills)

	if translationsFile:
		options.messageBundle = ji.XtbMessageBundle(ji.FileInputStream(str(translationsFile)), translationsProject)
	elif ji.CompilationLevel.ADVANCED_OPTIMIZATIONS == level:
		options.messageBundle = ji.EmptyMessageBundle()
		options.setWarningLevel(ji.DiagnosticGroups.MSG_CONVENTIONS, ji.CheckLevel.OFF)

	# TypeError: Java class has no constructors
	# options.setConformanceConfigs(ji.ImmutableList(ji.ResourceLoader.loadGlobalConformance(ji.reflectClass(CompilerOptions))))

	options.setPrintSourceAfterEachPass(printSourceAfterEachPass)
	options.setTracerMode(tracerMode)
	options.setStrictModeInput(strictModeInput)
	options.setSourceMapIncludeSourcesContent(sourceMapIncludeSourcesContent)
	options.setModuleResolutionMode(moduleResolutionMode)

	if browserResolverPrefixReplacements is not None:
		options.setBrowserResolverPrefixReplacements(ji.ImmutableMap((k, v) for k, v in browserResolverPrefixReplacements.items()))

	if packageJsonEntryNames:
		options.setPackageJsonEntryNames(list(packageJsonEntryNames))

	if variableRenamingPolicy is not None:
		options.setVariableRenaming(variableRenamingPolicy)

	if propertyRenamingPolicy is not None:
		options.setPropertyRenaming(propertyRenamingPolicy)

	options.setInstrumentForCoverageOption(instrumentCodeParsed)
	options.setProductionInstrumentationArrayName(productionInstrumentationArrayName)
	options.setAllowDynamicImport(allowDynamicImport)
	options.setDynamicImportAlias(dynamicImportAlias)
	options.setAssumeStaticInheritanceIsNotUsed(assumeStaticInheritanceIsNotUsed)
	options.setCrossChunkCodeMotionNoStubMethods(assumeNoPrototypeMethodEnumeration)

	if chunkOutputType == ji.ChunkOutputType.ES_MODULES:
		renamePrefixNamespace = None
		emitUseStrict = False

		if level == ji.CompilationLevel.ADVANCED_OPTIMIZATIONS:
			options.setExtractPrototypeMemberDeclarations(ji.ExtractPrototypeMemberDeclarationsMode.USE_CHUNK_TEMP)

	options.setEmitUseStrict(emitUseStrict)
	options.renamePrefixNamespace = renamePrefixNamespace
	options.chunkOutputType = chunkOutputType
	return options
