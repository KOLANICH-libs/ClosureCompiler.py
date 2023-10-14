ClosureCompiler.py
==================
~~[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/ClosureCompiler.py/workflows/CI/master/ClosureCompiler-0.CI-py3-none-any.whl)~~
~~[![GitHub Actions](https://github.com/KOLANICH-libs/ClosureCompiler.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/ClosureCompiler.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/ClosureCompiler.py.svg)](https://libraries.io/github/KOLANICH-libs/ClosureCompiler.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/KOLANICH-libs/ClosureCompiler.py, grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success and wide adoption of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

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
