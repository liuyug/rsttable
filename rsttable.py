#!/usr/bin/env python
# -*- encoding:utf-8 -*-


class RstTable(object):
    header = None
    data = None
    widths = None
    justify = None
    nrow = 0
    ncol = 0

    def __init__(self, data, header=True, encoding='ascii'):
        self.encoding = encoding
        if header:
            self.header = data[0]
            self.data = data[1:]
        else:
            self.data = data
        self.nrow = len(self.data)
        self.ncol = len(data[0])
        self.widths = self.calc_widths(data)
        self.data_justify = ['left'] * len(data[0])

    def __repr__(self):
        return '<reStructedText Table: %s rows, %s cols>' % (
            self.nrow, self.ncol
        )

    def calc_widths(self, data):
        max_widths = [0] * self.ncol
        for row in data:
            for x in range(self.ncol):
                w = self.text_length(row[x])
                max_widths[x] = max(w, max_widths[x])
        return max_widths

    def text_length(self, text):
        if text:
            return len(text.encode(self.encoding))
        else:
            return 0

    def set_justify(self, x, align):
        """align: left, right, center
        """
        self.data_justify[x] = align

    def table(self, style=None):
        """style:
        nosep: no separater
        """
        t = []
        tr_s = '+'
        for w in self.widths:
            tr_s = '%s%s%s' % (tr_s, '-' * (w + 2), '+')
        th_s = tr_s.replace('-', '=')
        # header
        if self.header:
            if style == 'nosep':
                pass
            else:
                t.append(th_s)
            tr = '|'
            for x in range(self.ncol):
                if self.header[x] is not None:
                    text = '%s' % self.header[x]
                else:
                    text = ''
                fix = self.text_length(text) - len(text)
                td = text.center(self.widths[x] - fix)
                tr = '%s %s %s' % (tr, td, '|')
            t.append(tr)
            if style == 'nosep':
                pass
            else:
                t.append(th_s)
        else:
            if style == 'nosep':
                pass
            else:
                t.append(tr_s)
        # data
        if self.data:
            for row in self.data:
                tr = '|'
                for x in range(self.ncol):
                    if row[x] is not None:
                        text = '%s' % row[x]
                    else:
                        text = ''
                    fix = self.text_length(text) - len(text)
                    if self.data_justify[x] == 'left':
                        td = text.ljust(self.widths[x] - fix)
                    elif self.data_justify[x] == 'right':
                        td = text.rjust(self.widths[x] - fix)
                    elif self.data_justify[x] == 'center':
                        td = text.center(self.widths[x] - fix)
                    tr = '%s %s %s' % (tr, td, '|')
                t.append(tr)
                if style == 'nosep':
                    pass
                else:
                    t.append(tr_s)
        return '\n'.join(t)


if __name__ == '__main__':
    chars = [chr(x + ord('a')) for x in range(0, 26)]
    a = RstTable(chars)
    print(a.table())
    b = RstTable([chars])
    print(b.table())
