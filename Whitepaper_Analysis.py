from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import language_tool_python
import enchant
tool = language_tool_python.LanguageTool('en-US')
dictionary =     enchant.Dict("en_US")
output_string = StringIO()
filename= "test_maidsafe_whitepaper.pdf"
try:
    # Choose the whitepaper you want to scan in PDF format
    with open(filename, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        issues = 0
        total = 0

        # The for loop runs a check of all the individual words in the PDF against a dictionary library (enchant)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            output = output_string.getvalue()
            print(output)
            for i in output.split():
                # print(i)
                dictionary.check(i)
                total += 1
                if (dictionary.check(i) == False):
                    print('Please look for the suspected word ie %s and below suggestions' % i)
                    print(dictionary.suggest(i))
                    issues += 1

        matches = tool.check(output)
        match2 = tool.correct(output)
        percentage = issues / total * 100
        percentage2 = len(matches) / total * 100

        # Whitepapers usually range between 3000 and 5000 words which is normal unless its lesser than 3000.
        if total < 3000:
            print("There are a total of " + str(total) + " elements.The length of the whitepaper is way too short. Red Flag!")
        elif total < 5000:
            print("There are a total of " + str(total) + " elements.The length of the whitepaper seems suspiciously short.")
        else:
            print("There are a total of " + str(total) + " elements.The length of the whitepaper seems legitimate")

        if  percentage2 < 5:
            print("ERRORS FOUND: " + str(len(matches)) + " The errors found in this whitepaper is: " + str(round(percentage2, 2)) + "%. The amount of grammatical errors is ok.")
            #print(len(matches)) #number of grammatical errors
            #print(issues) #number of spelling or unknown elements error
            #print(total) # number of total words.
        else:
            print("ERRORS FOUND: " + str(len(matches)) + " The errors found in this whitepaper is: " + str(
                round(percentage2, 2)) + "%. The amount of grammatical errors is high,red flag.")
            # print(len(matches)) #number of grammatical errors
            # print(issues) #number of spelling or unknown elements error
            # print(total) # number of total words.



except FileNotFoundError:
    msg = "Sorry the Whitepaper (" + filename + ") does not exist."
    print(msg)
