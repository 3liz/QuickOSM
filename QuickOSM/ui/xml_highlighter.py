"""Query Highlighter class."""

from qgis.PyQt.QtCore import QRegExp, Qt
from qgis.PyQt.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class QueryHighlighter(QSyntaxHighlighter):
    """Query Highlighter class."""

    def __init__(self, parent=None):
        super().__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.darkMagenta)

        keyword_patterns = [
            "\\b?xml\\b", "/>", ">", "<",
            ";", r"\[", r"\]", r"\(", r"\)"
        ]

        self.highlightingRules = [
            (QRegExp(pattern), keyword_format)
            for pattern in keyword_patterns
        ]

        element_format = QTextCharFormat()
        element_format.setForeground(QColor("#117700"))
        self.highlightingRules.append(
            (QRegExp("\\b[A-Za-z_\\-]+(?=[\\s\\/>:;])"), element_format))

        nominatim_area_format = QTextCharFormat()
        nominatim_area_format.setFontItalic(True)
        nominatim_area_format.setFontWeight(QFont.Bold)
        nominatim_area_format.setForeground(QColor("#FF7C00"))
        self.highlightingRules.append(
            (QRegExp(r"\{\{[A-Za-z0-9:, ]*\}\}"), nominatim_area_format))

        attribute_format = QTextCharFormat()
        attribute_format.setFontItalic(True)
        attribute_format.setForeground(QColor("#2020D2"))
        self.highlightingRules.append(
            (QRegExp("\\b[A-Za-z0-9_-]+(?=\\=|\\[|\\(|$|\\.)"), attribute_format))

        value_format = QTextCharFormat()
        value_format.setForeground(Qt.red)
        self.highlightingRules.append(
            (QRegExp("(\"[A-Za-z0-9:, _.]*\"|\\:([0-9]+)(?=\\,|\\]))"), value_format))

        area_format = QTextCharFormat()
        area_format.setForeground(QColor("#11CC00"))
        area_pattern = [
            "\\.([A-Za-z0-9_]{2,})(?=\\)|\\;)",
            r"\(([0-9]{2,})\)", "[0-9]+[.]+[0-9]+"
        ]
        for pattern in area_pattern:
            self.highlightingRules.append(
                (QRegExp(pattern), area_format))

        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(Qt.gray)
        self.highlightingRules.append(
            (QRegExp("(<!--[^\n]*-->|//[^\n]*)"), single_line_comment_format))

        # Multi lines comment
        self.oql_start_comment = QRegExp(r"\/\*")
        self.oql_end_comment = QRegExp(r'\*\/')

    def match_multiline(
            self, text: str,
            start_delimiter: QRegExp,
            end_delimiter: QRegExp,
            in_state: int,
            style: Qt) -> bool:
        """Do highlight of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = start_delimiter.indexIn(text)
            # Move past this match
            add = start_delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = end_delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + end_delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = end_delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        return self.currentBlockState() == in_state

    def highlightBlock(self, text: str):
        """Highlight of a comment block"""
        # for every pattern
        for pattern, char_format in self.highlightingRules:

            # Create a regular expression from the retrieved pattern
            expression = QRegExp(pattern)

            # Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)

            # While the index is greater than 0
            while index >= 0:

                # Get the length of how long the expression is true,
                # set the format from the start to the length with
                # the text format
                length = expression.matchedLength()
                self.setFormat(index, length, char_format)

                # Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)

        # Do multi-line strings
        self.match_multiline(
            text,
            self.oql_start_comment,
            self.oql_end_comment,
            1,
            Qt.gray)
