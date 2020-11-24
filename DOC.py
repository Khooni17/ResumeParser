from docx import Document
from docx.shared import Inches



document = Document('resume/khooni.docx')

for p in document.paragraphs:
	print(p.text)