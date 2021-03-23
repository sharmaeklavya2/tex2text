#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convert TeX to plaintext or markdown"""

from __future__ import print_function
import argparse


SYMBOLS = {
    'ldots': ('…', '...'),
    'in': ('∈', 'in'),
    'Th': ('th', 'th'),
    'infty': ('∞', 'infinity'),
    'approx': ('≈', 'approx'),

    'alpha': ('α', 'alpha'),
    'beta': ('β', 'beta'),
    'gamma': ('γ', 'gamma'),
    'delta': ('δ', 'delta'),
    'eps': ('ε', 'eps'),
    'epsilon': ('ε', 'epsilon'),
    'varepsilon': ('ε', 'epsilon'),
}

CONSTANTS = set(['ln', 'log', '&', '_', 'opt', 'OPT'])


class UnknownMacroError(ValueError):
    pass


def identity_func(x):
    return x


PLAIN_MACROS = {
    'emph': identity_func,
    'textbf': identity_func,
    'cite': (lambda x: '(' + x + ')'),
}

MARKDOWN_MACROS = PLAIN_MACROS

MACROS = {
    'plain': PLAIN_MACROS,
    'markdown': MARKDOWN_MACROS,
}


def apply_macro(name, x, args):
    if x is None:
        if name in CONSTANTS:
            return name
        elif name in SYMBOLS:
            return SYMBOLS[name][1 - args.unicode]
        else:
            raise UnknownMacroError('unknown macro ' + name)
    else:
        macros = MACROS[args.fmt]
        if name in macros:
            return macros[name](x)
        else:
            raise UnknownMacroError('unknown macro ' + name)


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


def replace_macros(texs, args):
    output = []
    for tex in texs:
        head = 0
        math_mode = False
        math_mode_pattern = '$' if args.keep_math else '$\\'
        while True:
            if math_mode:
                ch, pos = find_chars(tex, head, math_mode_pattern)
            else:
                ch, pos = find_chars(tex, head, '$\\')
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
                if tex[head] == '{':
                    head += 1
                    pos = find_matching_paren(tex, head, '{', '}')
                    raw_arg = tex[head: pos]
                    output.append(apply_macro(macro_name, raw_arg, args))
                    head = pos + 1
                else:
                    output.append(apply_macro(macro_name, None, args))
    return output


def tex2text(texs, args):
    return replace_macros(replace_alt_text(texs, args), args)


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
    args = parser.parse_args()

    with open(args.fpath) as fp:
        tex = fp.read()
    s = ''.join(tex2text([tex], args))
    if args.output:
        with open(args.output, 'w') as fp:
            fp.write(s)
    else:
        print(s)


if __name__ == '__main__':
    main()
