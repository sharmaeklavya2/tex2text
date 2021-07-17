#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convert TeX to plaintext or markdown"""

from __future__ import print_function
import sys
import re
import argparse


retcode = 0

SYMBOLS = {
    'Th': ('th', 'th'),
    'infty': ('∞', 'infinity'),
    'because': ('∵', 'because'),
    'therefore': ('∴', 'therefore'),
    'ldots': ('…', '...'),
    'cdots': ('⋯', '...'),
    'vdots': ('⋮', '...'),
    'ddots': ('⋱', '...'),
    'emptyset': ('∅', '{}'),
    'varnothing': ('∅', '{}'),
    'degree': ('°', 'deg'),
    'textdegree': ('°', 'deg'),
    'N': ('ℕ', 'N'),
    'R': ('ℝ', 'R'),
    'exists': ('∃', 'exists'),
    'forall': ('∀', 'for all'),
    'top': ('⊤', 'top'),
    'bot': ('⊥', 'bot'),
    'partial': ('∂', 'del'),
    'ell': ('ℓ', 'l'),
    'nabla': ('∇', 'nabla'),
    'grad': ('∇', 'grad'),
    'Box': ('□', 'box'),

    # lowercase greek symbols
    'alpha': ('α', 'alpha'),
    'beta': ('β', 'beta'),
    'gamma': ('γ', 'gamma'),
    'delta': ('δ', 'delta'),
    'eps': ('ε', 'epsilon'),
    'epsilon': ('ε', 'epsilon'),
    'varepsilon': ('ε', 'epsilon'),
    'zeta': ('ζ', 'zeta'),
    'eta': ('η', 'eta'),
    'theta': ('θ', 'theta'),
    'vartheta': ('ϑ', 'theta'),
    'iota': ('ι', 'iota'),
    'kappa': ('κ', 'kappa'),
    'varkappa': ('ϰ', 'kappa'),
    'lambda': ('λ', 'lambda'),
    'mu': ('μ', 'mu'),
    'nu': ('ν', 'nu'),
    'xi': ('ξ', 'xi'),
    'omicron': ('ο', 'omicron'),
    'pi': ('π', 'pi'),
    'varpi': ('ϖ', 'pi'),
    'rho': ('ρ', 'rho'),
    'varrho': ('ϱ', 'rho'),
    'sigma': ('σ', 'sigma'),
    'varsigma': ('ς', 'sigma'),
    'tau': ('τ', 'tau'),
    'upsilon': ('υ', 'upsilon'),
    'phi': ('ϕ', 'phi'),
    'varphi': ('φ', 'phi'),
    'chi': ('χ', 'chi'),
    'psi': ('ψ', 'psi'),
    'omega': ('ω', 'omega'),

    # uppercase greek symbols
    'Gamma': ('Γ', 'Gamma'),
    'Delta': ('Δ', 'Delta'),
    'Theta': ('Θ', 'Theta'),
    'Lambda': ('Λ', 'Lambda'),
    'Xi': ('Ξ', 'Xi'),
    'Pi': ('Π', 'Pi'),
    'Sigma': ('Σ', 'Sigma'),
    'Upsilon': ('Υ', 'Upsilon'),
    'Phi': ('Φ', 'Phi'),
    'Psi': ('Ψ', 'Psi'),
    'Omega': ('Ω', 'Omega'),

    # relational operators
    'neg': ('¬', '!'),
    'equiv': ('≡', '='),
    'approx': ('≈', '~'),
    'cong': ('≅', '='),
    'simeq': ('≃', '~'),
    'sim': ('∼', '~'),
    'propto': ('∝', 'prop'),
    'ne': ('≠', '!='),
    'neq': ('≠', '!='),
    'lt': ('<', '<'),
    'gt': ('>', '>'),
    'le': ('≤', '<='),
    'leq': ('≤', '<='),
    'leqslant': ('≤', '<='),
    'ge': ('≥', '>='),
    'geq': ('≥', '>='),
    'geqslant': ('≥', '>='),
    'prec': ('≺', '<'),
    'succ': ('≻', '>'),
    'nprec': ('⊀', '!<'),
    'nsucc': ('⊁', '!>'),
    'preceq': ('⪯', '<='),
    'succeq': ('⪰', '>='),
    'npreceq': ('⋠', '!<='),
    'nsucceq': ('⋡', '!>='),
    'll': ('≪', '<<'),
    'gg': ('≫', '>>'),
    'lll': ('⋘', '<<<'),
    'ggg': ('⋙', '<<<'),
    'subset': ('⊂', 'subset'),
    'supset': ('⊃', 'supset'),
    'subseteq': ('⊆', 'subseteq'),
    'supseteq': ('⊇', 'supseteq'),
    'nsubseteq': ('⊈', 'nsubseteq'),
    'nsupseteq': ('⊉', 'nsupseteq'),
    'subsetneq': ('⊊', 'subsetneq'),
    'supsetneq': ('⊋', 'supsetneq'),
    'vdash': ('⊢', '|-'),
    'dashv': ('⊣', '-|'),
    'models': ('⊨', '|='),
    'in': ('∈', 'in'),
    'ni': ('∋', 'contains'),
    'notin': ('∉', 'not in'),
    'notni': ('∌', 'does not contain'),
    'mid': ('∣', '|'),
    'nmid': ('∤', '!|'),
    'perp': ('⊥', 'perp'),
    'parallel': ('∥', '||'),

    # binary operators
    'pm': ('±', '+-'),
    'mp': ('∓', '-+'),
    'times': ('×', '*'),
    'divides': ('÷', '/'),
    'cap': ('∩', 'intersection'),
    'cup': ('∪', 'union'),
    'vee': ('∨', 'V'),
    'lor': ('∨', 'V'),
    'wedge': ('∧', '&'),
    'land': ('∧', '&'),
    'cdot': ('·', '.'),
    'bullet': ('•', '.'),
    'oplus': ('⊕', '+'),
    'ominus': ('⊖', '-'),
    'otimes': ('⊗', '*'),
    'oslash': ('⊘', '/'),
    'odot': ('⊙', '.'),
    'circ': ('∘', 'o'),
    'setminus': ('∖', '-'),
    'implies': ('⟹', '=>'),
    'Rightarrow': ('⇒', '=>'),
    'iff': ('⟺', 'iff'),
    'Leftrightarrow': ('⇔', '<=>'),
    'to': ('→', '->'),
    'rightarrow': ('→', '->'),
    'mapsto': ('↦', '->'),

    # delimiters
    'lceil': ('⌈', 'ceil('),
    'rceil': ('⌉', ')'),
    'lfloor': ('⌊', 'floor('),
    'rfloor': ('⌋', ')'),
    'langle': ('⟨', '<'),
    'rangle': ('⟩', '>'),
    'lvert': ('|', '|'),
    'rvert': ('|', '|'),
    '|': ('∥', '||'),
    'lVert': ('∥', '||'),
    'rVert': ('∥', '||'),

    # big operators
    'sum': ('∑', 'sum'),
    'prod': ('∏', 'prod'),
    'int': ('∫', 'integral'),

    # spacing
    '\\': ('\n', '\n'),
    ',': (' ', ' '),
    ';': (' ', ' '),
    ':': (' ', ' '),
}

CONSTANTS = set(['&', '_', '{', '}', 'OPT', 'opt',
    'sin', 'cos', 'tan', 'csc', 'sec', 'cot',
    'Pr', 'E', 'Var', 'lg', 'ln', 'log', 'exp',
    'gcd', 'min', 'max', 'argmin', 'argmax',
    'lim', 'limsup', 'deg', 'det', 'dim'])


INVISIBLE_SYMBOLS = set([
    'displaystyle', '!',
    'tiny', 'scriptsize', 'footnotesize', 'small', 'normalsize',
    'large', 'Large', 'LARGE', 'huge', 'Huge',
    'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
])


def identity_func(x):
    return x


def delim_func(d1, d2):
    def func(x):
        return d1 + x + d2
    return func


def paren_if_needed(x):
    return x if x.isalnum() else '(' + x + ')'


PLAIN_MACROS = {
    'emph': identity_func,
    'textit': identity_func,
    'textsl': identity_func,
    'textbf': identity_func,
    'textup': identity_func,
    'textsc': identity_func,
    'textrm': identity_func,
    'textsf': identity_func,
    'texttt': identity_func,
    'mathrm': identity_func,
    'mathbf': identity_func,
    'mathsf': identity_func,
    'mathtt': identity_func,
    'underline': identity_func,
    'operatorname': identity_func,
    'sqrt': delim_func('sqrt(', ')'),
    'frac': (lambda x, y: paren_if_needed(x) + '/' + paren_if_needed(y)),
}

MARKDOWN_MACROS = {
    'emph': delim_func('*', '*'),
    'textit': delim_func('*', '*'),
    'textsl': delim_func('*', '*'),
    'textbf': delim_func('**', '**'),
}

MATH_SYMBOLS = {
    'eps': '\\epsilon',
    'Th': '^{\\textrm{th}}',
}

MATH_MACROS = {}

MACROS = {
    'plain': PLAIN_MACROS,
    'markdown': PLAIN_MACROS.copy(),
}
MACROS['markdown'].update(MARKDOWN_MACROS)


def unknown_macro_warn(name):
    print('WARNING: unknown macro: \\' + name, file=sys.stderr)
    global retcode
    retcode = 1


def reconstruct_macro(name, x):
    return '\\' + name + ''.join(['{' + y + '}' for y in x])


def apply_macro(name, x, args, math_mode):
    if math_mode:
        if not x and name in MATH_SYMBOLS:
            return MATH_SYMBOLS[name]
        elif not x and name in MATH_MACROS:
            return MATH_MACROS[name](x)
        else:
            return reconstruct_macro(name, x)
    else:
        if not x:
            if name in CONSTANTS:
                return name
            elif name in SYMBOLS:
                return SYMBOLS[name][1 - args.unicode]
            elif name in INVISIBLE_SYMBOLS:
                return ''
            else:
                unknown_macro_warn(name)
                return reconstruct_macro(name, x)
        else:
            macros = MACROS[args.fmt]
            if name in macros:
                return macros[name](*x)
            else:
                unknown_macro_warn(name)
                return reconstruct_macro(name, x)


def find_matching_paren(s, start, ch1, ch2):
    depth = 1
    for i in range(start, len(s)):
        if s[i] == ch1:
            depth += 1
        elif s[i] == ch2:
            depth -= 1
        if depth == 0:
            return i
    raise ValueError('unmatched parens')


def find_chars(s, start, t):
    pos = -1
    chosen = None
    for ch in t:
        i = s.find(ch, start)
        if i != -1 and (pos == -1 or pos > i):
            pos = i
            chosen = ch
    return (chosen, pos)


def clean_alt_text(s, args):
    if args.fmt == 'markdown':
        return s
    else:
        return s.replace('\\_', '_')


def replace_alt_text(texs, args):
    output = []
    for tex in texs:
        head = 0
        tpdf = '\\texorpdfstring{'
        n_tpdf = len(tpdf)
        while True:
            pos = tex.find(tpdf, head)
            if pos == -1:
                output.append(tex[head:])
                break
            elif pos > head:
                output.append(tex[head: pos])
            head = pos + n_tpdf

            pos = find_matching_paren(tex, head, '{', '}') + 1
            if tex[pos] != '{':
                raise ValueError("second '{' not found for \\texorpdfstring")
            head = pos + 1
            pos = find_matching_paren(tex, head, '{', '}')
            output.append(clean_alt_text(tex[head: pos], args))
            head = pos + 1
    return output


def replace_macros(texs, args, orig_math_mode=False):
    output = []
    for tex in texs:
        head = 0
        math_mode = orig_math_mode
        while True:
            ch, pos = find_chars(tex, head, '$\\{}')
            if pos == -1:
                output.append(tex[head:])
                break
            elif pos > head:
                output.append(tex[head: pos])
            head = pos + 1

            if ch == '$':
                math_mode = not math_mode
                if args.keep_math:
                    output.append('$')
            elif ch == '{':
                if math_mode:
                    if args.keep_math:
                        output.append('{')
                    else:
                        output.append('(')
            elif ch == '}':
                if math_mode:
                    if args.keep_math:
                        output.append('}')
                    else:
                        output.append(')')
            else:
                # read macro name
                if tex[head].isalpha():
                    for pos in range(head, len(tex)):
                        if not tex[pos].isalpha():
                            break
                    macro_name = tex[head: pos]
                    head = pos
                else:
                    macro_name = tex[head]
                    head += 1

                # read macro arg
                raw_args = []
                while tex[head] == '{':
                    head += 1
                    pos = find_matching_paren(tex, head, '{', '}')
                    raw_args.append(''.join(replace_macros([tex[head: pos]], args, math_mode)))
                    head = pos + 1
                output.append(apply_macro(macro_name, raw_args, args,
                    args.keep_math and math_mode))
    return output


def remove_tex_comments(texs):
    output = []
    for tex in texs:
        head = 0
        # invariant: tex[:head] has been processed and added to output
        while True:
            perc_index = tex.find('%', head)
            if perc_index == -1:
                output.append(tex[head:])
                break
            else:
                if perc_index > head:
                    output.append(tex[head: perc_index])
                newline_index = tex.find('\n', perc_index + 1)
                if newline_index == -1:
                    break
                else:
                    head = newline_index + 1
    return output


def tex2text(texs, args):
    return replace_macros(replace_alt_text(remove_tex_comments(texs), args), args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fpath', help='path to TeX file')
    parser.add_argument('-o', '--output', help='path to output file')
    parser.add_argument('--fmt', choices=['plain', 'markdown'], default='plain',
        help='output format (default: plain)')
    parser.add_argument('--ascii', action='store_false', dest='unicode', default=True,
        help='only output ascii text')
    parser.add_argument('--keep-math', action='store_true', default=False,
        help="do not convert math (perhaps we're using MathJax)")
    parser.add_argument('--fix-spacing', action='store_true', default=False,
        help="convert lone newlines to space and coalesce multiple spaces.")
    args = parser.parse_args()

    with open(args.fpath) as fp:
        tex = fp.read()
    s = ''.join(tex2text([tex], args))
    if args.fix_spacing:
        s = re.sub(r'([^\n])\n([^\n])', r'\1 \2', s)
        s = re.sub(r' +', r' ', s)
    if args.output:
        with open(args.output, 'w') as fp:
            fp.write(s)
    else:
        print(s)


if __name__ == '__main__':
    main()
    sys.exit(retcode)
