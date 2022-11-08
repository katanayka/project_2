import docx

def ReadOtcRev(filedir):
    # Read docx file at filedir (only text)
    doc = docx.Document(filedir)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return fullText
