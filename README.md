# PDF2TXT
Convert PDF documents to TXT, cleaning as well as able to remove formulas, diagrams, line breaks, separated hyphens, etc.

The text conversion uses the Pdfminer.six library - https://github.com/pdfminer/pdfminer.six
- Pdfminer installation on Conda: conda install -c conda-forge pdfminer.six

Instructions: Place script and the accompanying py and the English_words.txt in the same directory as your PDF files. The script will convert all PDF files in this directory.

Thanks:
1. Pdfminer function obtained from https://github.com/Shahabks/Converter-pdf-files-to-.txt-or-.html
2. English word list obtained from https://github.com/dwyl/english-words/ - Words not in this list are used to identify diagrams and formulas. Using this local list is much faster than using NLTK's words.words().
