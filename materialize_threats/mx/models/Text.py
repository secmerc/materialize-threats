from ..utils import MxConst
from .Styles import Styles


class Text:
    def __init__(self, anchor, family, size, text, color):
        self.anchor = anchor
        self.family = family
        self.size = size
        self.text = text
        self.color = color

    def get_mx_style(self):
        align = MxConst.CENTER if self.anchor == MxConst.MIDDLE else MxConst.START
        # TODO: add right
        margin = (
            "margin-top:4px;" if self.anchor == MxConst.MIDDLE else "margin-left:4px;"
        )
        rescaled_size = 10.0 * (self.size / 14.0)
        return Styles.TEXT.format(
            align=align,
            margin=margin,
            size=rescaled_size,
            family=self.family or MxConst.DEFAULT_FONT_FAMILY,
            color=self.color or MxConst.DEFAULT_FONT_COLOR,
        )

    @staticmethod
    def from_xml(text):
        if text != None:
            text =  text.replace("<", "&lt;").replace(">", "&gt;")
        else: 
            text = ""

        return Text(
            text = text,
            anchor=None,
            family=MxConst.DEFAULT_FONT_FAMILY,
            size=MxConst.DEFAULT_TEXT_SIZE,
            color=None,
        )
