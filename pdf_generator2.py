# -*- coding: utf-8 -*-
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import *
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, PageBreak,Spacer
import cPickle
import logging
import reportlab.rl_config
from reportlab.lib.utils import ImageReader
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import redis
from reportlab.platypus.flowables import Image
from cStringIO import StringIO
from functools import partial
from reportlab.lib import fonts
pdfmetrics.registerFont(TTFont('hei', 'msyh.ttf'))
pdfmetrics.registerFont(TTFont('yhb', 'msyhbd.ttf'))
class pdfGenerator():
    def __init__(self,title,content,type):
        self.title=title
        self.content=content
        self.type=type
    def header_footer(self,canvas, doc):
        canvas.saveState()
        footer = ImageReader('pdf_image/footer.png')
        canvas.drawImage(footer,x=20.5*mm,y=3*mm,width=175*mm,preserveAspectRatio=True)
        canvas.linkURL('http://www.smartstudy.com/', (10*mm, 10*mm, 300.5*mm, 50*mm), relative=0)
        header=ImageReader("pdf_image/"+self.type+"-header.png")
        canvas.drawImage(header,x=21.5*mm,y=270*mm,width=171.9*mm,preserveAspectRatio=True)
        canvas.linkURL('http://www.smartstudy.com/', (21.5*mm, 270*mm, 193*mm, 300*mm), relative=0)
        canvas.restoreState()

    def build_pdf(self,path):
        fonts.addMapping('hei', 0, 0, 'hei')
        fonts.addMapping('hei', 0, 1, 'hei')
        stylesheet=getSampleStyleSheet()
        elements = []
        doc = BaseDocTemplate(path,title=self.title)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
               id='normal')
        template = PageTemplate(id='test', frames=frame, onPage=self.header_footer)
        doc.addPageTemplates([template])
        covername={"GRE":"G R E","TOEFL":"托 福","SAT":"S A T","IELTS":"雅 思","GMAT":"G M A T","kaoyan":"考 研"}
        covertitle="智 课 网 "+covername[self.type]+" 备 考 资 料"
        elements.append(Spacer(40,250))
        stylesheet["Title"].fontSize=35
        fonts.addMapping('yhb', 0, 0, 'yhb')
        fonts.addMapping('yhb', 0, 1, 'yhb')
        bigTitle=Paragraph('<font name="yhb">'+covertitle+"</font>",stylesheet["Title"])
        elements.append(bigTitle)
        elements.append(PageBreak())
        stylesheet['Normal'].fontSize=14
        stylesheet['Normal'].leading=14*1.5
        stylesheet['Normal'].firstLineIndent=28
        stylesheet['Heading1'].leading=20*1.5
        stylesheet["Heading1"].alignment=1

        title_pra=Paragraph('<font name="hei">'+self.title+"</font>",stylesheet["Heading1"])
        elements.append(title_pra)
        for item in self.content.split("\n"):
            try:
              content = Paragraph('<font name="hei">'+item+'</font>', stylesheet['Normal'])
              elements.append(content)
            except Exception:
              print "some error"
              logging.warning("some error with" +item)
        elements.append(PageBreak())
        data = open("pdf_image/thelastpage.png").read()
        img1 = StringIO(data)
        elements.append(Image(img1,width=110*mm,height=226*mm))
        doc.build(elements)
if __name__=="__main__":
   s=redis.StrictRedis('172.16.3.190')
   url_tuple_tem=s.brpop("my_contents")
   url_tuple=cPickle.loads(url_tuple_tem[1])
   title=url_tuple[0]
   print title
   content=url_tuple[1]
   mypdf=pdfGenerator(title,content,"GRE")
   mypdf.build_pdf("test.pdf")



