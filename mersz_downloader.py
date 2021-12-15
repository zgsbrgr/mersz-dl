import pdfkit
from urllib.request import urlopen
import argparse
from PyPDF2 import PdfFileMerger
import os

parser = argparse.ArgumentParser(description='Optional app description')

options = {
	'page-size': 'A4',
   	'enable-local-file-access': None
}
base_url = 'https://mersz.hu/'
document_url = base_url +'/dokumentum/'
pages = []

parser.add_argument('--page_count', '-pc', type=int,
                    help='Page count')
parser.add_argument('--document_pre', '-dp', type=str,
                    help='Document prefix: like dj77mgtan__')
parser.add_argument('--pdf_name', '-pn', type=str,
                    help='Name of the generated pdf document')

args = parser.parse_args()

page_count = args.page_count
document = args.document_pre
pdf_name = args.pdf_name

for page_nr in range(1,page_count+1):
	url = document_url+document+str(page_nr)
	html_text = urlopen(url).read().decode('utf-8')



	html_text = str(html_text).replace('<header', '<header style="display:none" ') \
	                     .replace('<footer', '<footer style="display:none" ') \
	                     .replace('src="/assets/', 'src="'+base_url+'/assets/') \
	                     .replace('href="/assets/', 'href="'+base_url+'/assets/') \
	                     .replace('href="/mod/', 'href="' + base_url + '/mod/') \
	                     .replace('src="/mod/', 'src="'+base_url+'/mod/')



	tmp_dir = '.temp/'
	if not os.path.exists(tmp_dir):
		os.makedirs(tmp_dir)
	tmp = tmp_dir+str(page_nr)+'.pdf'
	
	pdfkit.from_string(html_text, tmp, verbose=True, options = options)
	pages.append(tmp)


# merge PDFS

merger = PdfFileMerger()
[merger.append(pdf,import_bookmarks=False) for pdf in pages]
with open(pdf_name, "wb") as new_file:
	merger.write(new_file)
