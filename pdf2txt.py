# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 05:21:16 2020

@author: Joshua Been
pdfminer installation on Conda: conda install -c conda-forge pdfminer.six
Purpose: Convert PDF documents to TXT, cleaning as well as able to remove 
         formulas, diagrams, line breaks, etc.
Instructions: Place script and the accompanying py and the English_words.txt
              in the same directory as your PDF files. The script will convert
              all PDF files in this directory.
Thanks:
    (1) pdfminer function obtained from https://github.com/Shahabks/Converter-pdf-files-to-.txt-or-.html
    (2) English word list obtained from https://github.com/dwyl/english-words/
    
"""

import io, re, glob
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


# Fuunction obtained from
# https://github.com/Shahabks/Converter-pdf-files-to-.txt-or-.html
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def clean_text(r):
    print('...cleaning text')
    # Fix line breaks that were to force column layout
    r=r.replace('\n\n','||')
    r=r.replace('\n',' ')
    r=r.replace('||','\n\n')
    
    q=''
    i=1
    for par in r.split('\n\n'):
        if i==1 or i%50==0:
            print(i, '/', len(r.split('\n\n')), 'chunks')
        # Removes illustrations
        par=re.sub('\(cid:+',' ', par)
        # Fix hyphen line breaks
        par=re.sub('- ','', par)
        par=re.sub('-\n\n','', par)
        par=re.sub('-\n','', par)
        # Remove references to Figures (i.e., Figure 1)
        i+=1
        if 'Figure' in par and len(par.split(' '))<5:
           q=q+'\n\n'
        # Remove repeated citations
        elif '©' in par and 'INFORMS' in par:
            q=q+'\n\n'
        # Remove paginations
        elif not re.search('[a-zA-Z]', par):
            q=q+'\n\n'
        # Remove paragraphs with less than 3 characters
        elif len(par)<=3:
            q=q+'\n\n'
        else:
            # Remove lines with only formulas
            w=0
            clean_par=0
            for word in par.split():
                if clean_par==0 and not word=='':
                    if not word.lower() in WRDS:
                        w+=1
                    elif len(word)==1 or len(word)==2:
                        w+=1
                else:
                    clean_par=1
            if w==len(par.split()):
                q=q+'\n\n'
            # Keeps footnotes - Change to q=q+'\n\n' to remove 
            elif re.search('[0-9]', par[:1]) and not re.search('[0-9]+\.', par[:2]):
                q=q+par+'\n\n'
                # q=q+'\n\n'
            else:
                q=q+par+'\n\n'
    while '\n\n\n' in q:
        q=q.replace('\n\n\n\n','\n\n').replace('\n\n\n','\n')
    return q

# English word list obtained from
# https://github.com/dwyl/english-words/
# (Faster than NLTK.words())
def eng_words():
    f=open('english_words.txt')
    f1=f.read()
    f.close()
    w=[]
    for word in f1.split('\n'):
        if len(word)>2:
            w.append(word)
    return w

def files_directory():
    return glob.glob('*.pdf')

WRDS=eng_words()
for pdf in files_directory():
    print('Processing', pdf, '\n...converting to raw text')
    r=clean_text(convert_pdf_to_txt(pdf))
    f=open(pdf.replace('.pdf','.txt'),'w',encoding='utf-8')
    f.write(r)
    f.close()
