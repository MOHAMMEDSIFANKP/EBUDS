__all__ = (
        'GState',
        )

import sys
try:
    import cairocffi as cairo   #prefer cairocffi
except ImportError:
    import cairo
from reportlab.lib.colors import toColor
from reportlab.graphics.transform import mmult
from PIL import Image as PILImage

class GState(object):
    __fill_rule_values = (1,0)

    def __init__(self, width=1, height=1, bg='white', fmt='RGB24'):
        self._fmt = fmt
        self.surface = cairo.ImageSurface(self.__str2format(fmt), width, height)
        self.width = width
        self.height = height
        self.ctx = ctx = cairo.Context(self.surface)
        if fmt=='RGB24':
            self.__set_source_color__ = lambda c:ctx.set_source_rgb(*c.rgb())
        elif fmt=='ARGB32':
            self.__set_source_color__ = lambda c:ctx.set_source_rgba(*c.rgba())
        else:
            raise ValueError('Bad fmt=%r for rlPyCairo.GState' % fmt)
        ctx.set_antialias(cairo.ANTIALIAS_BEST)
        self._in_transform = self._out_transform = (1,0,0,-1,0,height)
        self.ctm = (1,0,0,1,0,0)
        self.fillColor = bg
        ctx.rectangle(0,0,width,height)
        self.pathFill()
        self.pathBegin()
        self.__fillColor = self.__strokeColor = None
        def _text2PathDescription(text, x, y):
            try:
                from reportlab.graphics.utils import text2PathDescription, FTTextPath
                gs = FTTextPath()
            except ImportError:
                try:
                    from _rl_renderPM import gstate
                except ImportError:
                    try:
                        from reportlab.graphics._renderPM import gstate
                    except ImportError as _e:
                        raise ImportError('freetype-py is not installed and no libart based _renderPM can be imported') from _e
                from reportlab.graphics.utils import text2PathDescription
                gs = gstate(1,1)
            def _text2PathDescription(text, x, y):
                return text2PathDescription(
                                text, x=x, y=y,
                                fontName=self.fontName, fontSize=self.fontSize,
                                truncate=False, gs=gs,
                                )
            self._text2PathDescription = _text2PathDescription
            return _text2PathDescription(text, x, y)
        self._text2PathDescription = _text2PathDescription
        self.__pathOpMap__ = dict(
                moveTo=ctx.move_to,
                lineTo=ctx.line_to,
                curveTo=ctx.curve_to,
                closePath=ctx.close_path,
                )
        self.textRenderMode = 0

    @staticmethod
    def __str2format(fmt):
        return getattr(cairo,'FORMAT_'+fmt)

    @property
    def pixBuf(self):
        ba = self.surface.get_data()
        if self._fmt=='RGB24':
            #despite the name they store it in 32 bits; we need to remove 8
            ba = bytearray(ba)
            if sys.byteorder=='little':
                #we expect spare blue green red 
                for i in range(0,len(ba),4):
                    ba[i:i+4] = bytearray(reversed(ba[i:i+4]))
            del ba[0::4] #we have spare red green blue so remove the spare
        return bytes(ba)

    @property
    def ctm(self):
        return mmult(self._out_transform,tuple(self.ctx.get_matrix()))

    @ctm.setter
    def ctm(self,mx):
        nctm = mmult(self._in_transform,mx)
        self.ctx.set_matrix(cairo.Matrix(*nctm))

    @property
    def fillColor(self):
        return self.__fillColor

    @fillColor.setter
    def fillColor(self,c):
        self.__fillColor = toColor(c) if c is not None else c

    @property
    def strokeColor(self):
        return self.__strokeColor

    @strokeColor.setter
    def strokeColor(self,c):
        self.__strokeColor = toColor(c) if c is not None else c

    @property
    def strokeWidth(self):
        return self.ctx.get_line_width()

    @strokeWidth.setter
    def strokeWidth(self, w):
        return self.ctx.set_line_width(w)

    @property
    def dashArray(self):
        return self.ctx.get_dash()

    @dashArray.setter
    def dashArray(self, da):
        if not da or not isinstance(da,(list,tuple)):
            da = 0, ()
        else:
            if isinstance(da[0],(list,tuple)):
                da = da[1],da[0]

        return self.ctx.set_dash(da[1], da[0])

    #lucky Cairo uses the same linCap/Join number values as PDF
    @property
    def lineCap(self):
        return int(self.ctx.get_line_cap())

    @lineCap.setter
    def lineCap(self, v):
        return self.ctx.set_line_cap(int(v))

    @property
    def lineJoin(self):
        return int(self.ctx.get_line_join())

    @lineJoin.setter
    def lineJoin(self, v):
        return self.ctx.set_line_join(int(v))

    #the values are the other way round from PDF
    @property
    def fillMode(self):
        return self.__fill_rule_values[int(self.ctx.get_fill_rule())]

    @fillMode.setter
    def fillMode(self, v):
        return self.ctx.set_fill_rule(self.__fill_rule_values[int(v)])

    def beginPath(self):
        self.ctx.new_path()

    def moveTo(self, x, y):
        self.ctx.move_to(float(x), float(y))

    def lineTo(self, x, y):
        self.ctx.line_to(float(x), float(y))

    def pathClose(self):
        self.ctx.close_path()

    def pathFill(self,fillMode=None):
        if self.__fillColor:
            if fillMode is not None:
                ofm = self.fillMode
                if ofm!=fillMode: self.fillMode = fillMode
            self.__set_source_color__(self.__fillColor)
            self.ctx.fill_preserve()
            if fillMode is not None and ofm!=fillMode: self.fillMode = ofm

    def pathStroke(self):
        if self.__strokeColor and self.strokeWidth>0:
            self.__set_source_color__(self.__strokeColor)
            self.ctx.stroke_preserve()

    def curveTo(self, x1, y1, x2, y2, x3, y3):
        self.ctx.curve_to(float(x1), float(y1),float(x2), float(y2),float(x3), float(y3))

    def pathBegin(self):
        self.ctx.new_path()

    def clipPathClear(self):
        self.ctx.rest_clip()

    def clipPathSet(self):
        ctx = self.ctx
        oPath = ctx.copy_path()
        ctx.new_path()
        ctx.clip()
        ctx.new_path()
        ctx.append_path(oPath)

    def clipPathAdd(self):
        self.ctx.clip_preserve()

    def setFont(self, fontName, fontSize):
        self.fontName = fontName
        self.fontSize = fontSize

    def drawString(self, x, y, text): 
        opMap = self.__pathOpMap__
        oPath = self.ctx.copy_path()
        oFM = self.fillMode
        tRM = self.textRenderMode
        try:
            self.ctx.new_path()
            for op in self._text2PathDescription(text, x, y):
                #call one of ctx.move_to/line_to/curve_to/close_path
                opMap[op[0]](*op[1:])
            if tRM in (0,2,4,6):
                self.pathFill(0)
            if tRM in (1,2,5,6):
                self.pathStroke()
            if tRM>=4:
                self.ctx.clip_preserve()
        finally:
            self.ctx.new_path()
            self.ctx.append_path(oPath)
            self.fillMode = oFM

    @classmethod
    def __fromPIL(cls, im, fmt='RGB24', alpha=1.0, forceAlpha=False):
        if 'A' not in im.getbands() or forceAlpha:
            im.putalpha(int(alpha * 255))
        fmt = cls.__str2format(fmt)
        return cairo.ImageSurface.create_for_data(bytearray(im.tobytes('raw', 'BGRa')),
                fmt, im.width, im.height,
                cairo.ImageSurface.format_stride_for_width(fmt,im.width),
                )

    def _aapixbuf(self, x, y, dstW, dstH,
                    data, srcW, srcH, planes=3,
                    ):
        ctx = self.ctx
        ctx.save()
        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.translate(x,y+dstH)
        ctx.scale(dstW/float(srcW),-dstH/float(srcH))
        ctx.set_source_surface(self.__fromPIL(data,self._fmt, forceAlpha=False))
        ctx.paint()
        ctx.restore()
