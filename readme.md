# Tex2Text

The program `tex2text.py` converts TeX to plain text or markdown.
I wrote this program to obtain plain text versions of abstracts of my
research papers because conferences (and ArXiv) ask for them.

Example invocations:

* `python tex2text.py example.tex --fix-spacing`
* `python tex2text.py example.tex --fmt=markdown --keep-math`

Here is how it roughly works:

* Remove all comments
* Replace occurrences of `\texorpdfstring{X}{Y}` by `Y`.
* Remove inline math delimiting characters `$`
(use the `--keep-math` option to prevent this.
This is useful if math is handled separately, e.g.,
using [MathJax](https://www.mathjax.org/)).
* Replace all known macros by symbols (see source code for list of known macros). So
`\alpha` becomes `α`, `\infty` becomes `∞`, etc.
Macros `\emph` and `\textbf` are ignored in plain text mode,
but processed appropriately in markdown mode.
* Throw an error if an unknown macro is encountered.

The default output format is plain text, but markdown can be obtained using
the `--fmt=markdown` option.

Run `python tex2text.py --help` to learn about other command-line options.
