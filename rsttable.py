#!/usr/bin/env python
# -*- encoding:utf-8 -*-

AlignSymbol = {
    'left': '<',
    'center': '^',
    'right': '>',
}

CjkRange = (
    (0x2E80, 0x9FC3),
    (0xAC00, 0xD7A3),
    (0xF900, 0xFAFF),
    (0xFE30, 0xFE4F),
    (0xFF01, 0xFF60),
    (0xFFE0, 0xFFE6),
)


class RstTable(object):
    _header = None
    _data = None
    _header_show = True
    _widths = None
    _left_padding = ' '
    _right_padding = ' '
    _encoding = None
    _null_char = ''

    def __init__(self, data, header=True, encoding=None):
        self._encoding = encoding
        self._header_show = header
        self._header = []
        self._data = []
        fmt = '%s'
        if self._header_show:
            for item in data[0]:
                self._header.append({
                    'data': item,
                    'format': fmt,
                    'width': 0,
                    'align': 'center',
                    'MB': 0,
                })
            data = data[1:]
        else:
            for item in data[0]:
                self._header.append({
                    'data': None,
                    'format': fmt,
                    'width': 0,
                    'align': 'left',
                    'MB': 0,
                })

        for record in data:
            row = []
            for item in record:
                row.append({
                    'data': item,
                    'format': fmt,
                    'align': 'left',
                    'MB': 0,
                })
            self._data.append(row)

    def __repr__(self):
        return '<reStructedText Table: %s rows, %s cols>' % (
            self.row_count(), self.column_count()
        )

    def row_count(self):
        return len(self._data)

    def column_count(self):
        return len(self._header)

    def calc_widths(self, columns=None):
        if columns is None:
            columns = range(self.column_count())
        elif isinstance(columns, int):
            columns = [columns]
        for column in columns:
            item = self._header[column]
            mb = self.cjk_count(item)
            w = self.get_text_length(item) + mb
            self._header[column]['width'] = max(
                w, self._header[column]['width'])
            item['MB'] = mb
        for column in columns:
            for row in range(self.row_count()):
                item = self._data[row][column]
                mb = self.cjk_count(item)
                w = self.get_text_length(item) + mb
                self._header[column]['width'] = max(
                    w, self._header[column]['width'])
                item['MB'] = mb

    def cjk_count(self, item):
        count = 0
        text = self.get_text(item)
        for ch in text:
            for b, e in CjkRange:
                if b <= ord(ch) <= e:
                    count += 1
                    break
        return count

    def get_text(self, item):
        data = item['data']
        if data is None:
            text = self._null_char
        else:
            text = item['format'] % data
        if self._encoding:
            text = text.encode(self._encoding)
        return text

    def get_text_length(self, item):
        text = self.get_text(item)
        return len(text)

    def set_align(self, align, rows=None, columns=None):
        """align: left, right, center
        """
        rows = rows or self.row_count()
        if isinstance(rows, int):
            rows = [rows]
        columns = columns or self.column_count()
        if isinstance(columns, int):
            columns = [columns]
        for row in rows:
            for column in columns:
                self._data[row][columns]['align'] = align

    def set_format(self, fmt, rows=None, columns=None):
        rows = rows or self.row_count()
        if isinstance(rows, int):
            rows = [rows]
        columns = columns or self.column_count()
        if isinstance(columns, int):
            columns = [columns]

        for row in rows:
            for column in columns:
                self._data[row][columns]['format'] = fmt

    def get_view_header_item(self, column):
        item = self._header[column]
        width = item['width'] - item['MB']
        align = AlignSymbol.get(item['align'])
        text = self.get_text(item)
        view = u'{:{align}{width}}'.format(text, align=align, width=width)
        return view

    def get_view_data_item(self, row, column):
        item = self._data[row][column]
        width = self._header[column]['width'] - item['MB']
        align = AlignSymbol.get(item['align'])
        text = self.get_text(item)
        view = u'{:{align}{width}}'.format(text, align=align, width=width)
        return view

    def table(self, style=None):
        """style:
        nosep: no separater
        """
        self.calc_widths()
        widths = [h['width'] for h in self._header]
        t = []
        th_s = ['+']
        tr_s = ['+']
        for w in widths:
            tr_s.append('-' * (
                len(self._left_padding) + w + len(self._right_padding)))
            tr_s.append('+')
            th_s.append('=' * (
                len(self._left_padding) + w + len(self._right_padding)))
            th_s.append('+')
        # header
        if self._header_show:
            if style == 'nosep':
                pass
            else:
                t.append(''.join(th_s))
            tr = ['|']
            for col in range(self.column_count()):
                tr.append(self._left_padding)
                tr.append(self.get_view_header_item(col))
                tr.append(self._right_padding)
                tr.append('|')
            t.append(''.join(tr))
            if style == 'nosep':
                pass
            else:
                t.append(''.join(th_s))
        else:
            if style == 'nosep':
                pass
            else:
                t.append(''.join(tr_s))
        # data
        for row in range(self.row_count()):
            tr = ['|']
            for column in range(self.column_count()):
                tr.append(self._left_padding)
                tr.append(self.get_view_data_item(row, column))
                tr.append(self._right_padding)
                tr.append('|')
            t.append(''.join(tr))
            if style == 'nosep':
                pass
            else:
                t.append(''.join(tr_s))
        return '\n'.join(t)


if __name__ == '__main__':
    chars = [chr(x + ord('a')) for x in range(0, 26)]
    a = RstTable(chars)
    print(a.table())
    b = RstTable([chars])
    print(b.table())
