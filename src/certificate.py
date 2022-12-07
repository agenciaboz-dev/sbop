from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# copyfile("newPDF.pdf", "basePDF.pdf")

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)

# drawing member name
can.setFillColorRGB(0.86328, 0.8, 0.496)
pdfmetrics.registerFont(TTFont('Montserrat', 'static/fonts/Montserrat-Regular.ttf'))
can.setFont("Montserrat", 30)
can.drawCentredString(420, 220, "Marcos Testador")

# drawing member membership
can.setFillColorRGB(0.082, 0.38281, 0.58593)
pdfmetrics.registerFont(TTFont('Montserrat-SemiBold', 'static/fonts/Montserrat-SemiBold.ttf'))
can.setFont("Montserrat-SemiBold", 12)
can.drawCentredString(362, 181, "Associado".upper())
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("src/template.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("static/documents/certificate.pdf", "wb")
output.write(outputStream)
outputStream.close()