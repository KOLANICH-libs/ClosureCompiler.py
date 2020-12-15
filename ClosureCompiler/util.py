import re
import typing
from pathlib import Path

compilerNameRx = re.compile("closure-compiler-(?:1\.0-SNAPSHOT|v202\\d{5})\.jar")


def getJarCandidates(baseDir: Path) -> typing.Iterable[Path]:
	baseDir = Path(".")
	cands = [baseDir / "compiler_uberjar_deploy.jar"]
	cands.extend(sorted((el for el in baseDir.glob("closure-compiler-*.jar") if compilerNameRx.match(el.name)), reverse=True))
	return [el for el in cands if el.is_file()]


def selectJar(baseDir: Path) -> Path:
	return next(iter(getJarCandidates(baseDir)))
