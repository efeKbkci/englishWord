import PyPDF2

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

# TODO: PDF işlemlerini not al

def png_to_pdf(png_path):

    image = Image.open(png_path)
    img_width, img_height = image.size
    c = canvas.Canvas("gecicipdf.pdf", pagesize=(img_width,img_height))
    img = ImageReader(png_path)
    c.drawImage(img, 0, 0, width=img_width, height=img_height)
    c.save()

def putTogether(pdf1, eklenecek_sayfa, hedef_pdf):    

    with open(pdf1, 'rb') as dosya1:
        pdf1_okuyucu = PyPDF2.PdfReader(dosya1)
        
        with open("gecicipdf.pdf", 'rb') as dosya2:
            pdf2_okuyucu = PyPDF2.PdfReader(dosya2)
            
            hedef = PyPDF2.PdfWriter()

            for sayfa_numarasi in range(len(pdf1_okuyucu.pages)):
                if sayfa_numarasi == eklenecek_sayfa:
                    sayfa = pdf2_okuyucu.pages[0]
                else:
                    sayfa = pdf1_okuyucu.pages[sayfa_numarasi]
                hedef.add_page(sayfa)
            
            # Hedef PDF dosyasını oluştur
            with open(hedef_pdf, 'wb') as hedef_dosya:
                hedef.write(hedef_dosya)
