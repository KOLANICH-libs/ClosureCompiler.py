ClosureCompiler.py
==================
~~[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/ClosureCompiler.py/workflows/CI/master/ClosureCompiler-0.CI-py3-none-any.whl)~~
~~[![GitHub Actions](https://github.com/KOLANICH-libs/ClosureCompiler.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/ClosureCompiler.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/ClosureCompiler.py.svg)](https://libraries.io/github/KOLANICH-libs/ClosureCompiler.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

Python bindings to [Google Closure Compiler](https://github.com/google/closure-compiler).

Contains sources derived from Closure Compiler source code. See [`./.reuse/dep5`](./.reuse/dep5) for more info.

## Usage

```python
from ClosureCompiler import *

c = Compiler(createCompilerOptions(level=CompilationLevel.ADVANCED_OPTIMIZATIONS))
res = c({
	"index.js": "const asdf = 'aaaa'; alert('1 ' + asdf);",
})
print(repr(res.js)) # '\'use strict\';\nalert("1 aaaa");\n'
```

WiP. Even the API is unstable and is subject to change.
