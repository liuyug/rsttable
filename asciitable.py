#!/usr/bin/env python
# -*- encoding:utf-8 -*-


class AsciiTable(object):
    header = None
    data = None
    widths = None
    justify = None
    nrow = 0
    ncol = 0

    def __repr__(self):
        return '<Ascii Table: %s rows, %s cols>' % (
            self.nrow, self.ncol
        )

    def __init__(self, data, header=True):
        if header:
            self.header = data[0]
            self.data = data[1:]
        else:
            self.data = data
        self.widths = self.calc_widths(data)
        self.data_justify = ['left'] * len(data[0])
        self.nrow = len(self.data)
        self.ncol = len(self.data[0])

    def calc_widths(self, data):
        max_widths = [0] * len(data[0])
        for row in data:
            for x in range(len(row)):
                w = self.text_length(row[x])
                max_widths[x] = max(w, max_widths[x])
        return max_widths

    def text_length(self, text):
        return len(text.encode('gbk'))

    def set_justify(self, x, align):
        """align: left, right, center
        """
        self.data_justify[x] = align

    def table(self):
        t = []
        tr_s = '+'
        for w in self.widths:
            tr_s = '%s%s%s' % (tr_s, '-' * (w + 2), '+')
        th_s = tr_s.replace('-', '=')
        # header
        if self.header:
            t.append(th_s)
            tr = '|'
            for x in range(len(self.header)):
                if self.header[x] is not None:
                    text = '%s' % self.header[x]
                else:
                    text = ''
                w = self.text_length(text)
                td = text.center(self.widths[x] - w)
                tr = '%s %s %s' % (tr, td, '|')
            t.append(tr)
            t.append(th_s)
        else:
            t.append(tr_s)
        # data
        if self.data:
            for row in self.data:
                tr = '|'
                for x in range(len(row)):
                    if row[x] is not None:
                        text = '%s' % row[x]
                    else:
                        text = ''
                    w = self.text_length(text)
                    if self.data_justify[x] == 'left':
                        td = text.ljust(self.widths[x] - w)
                    elif self.data_justify[x] == 'right':
                        td = text.rjust(self.widths[x] - w)
                    elif self.data_justify[x] == 'center':
                        td = text.center(self.widths[x] - w)
                    tr = '%s %s %s' % (tr, td, '|')
                for x in range(len(row), self.ncol):
                    td = ' ' * self.widths[x]
                    tr = '%s %s %s' % (tr, td, '|')
                t.append(tr)
                t.append(tr_s)
        return '\n'.join(t)
