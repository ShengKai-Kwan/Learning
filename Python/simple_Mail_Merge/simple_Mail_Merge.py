import docx
import pandas as pd
import os

df = pd.read_excel('./data.xlsx', header=None) #Replace the spreadsheet here

for i in range(1, len(df)):#for i in every row
    filename = df[0].iloc[i] #i-th row first column, which is the filename
    items = {}
    for j in range(1, len(df.columns)): #for j in every column
        items['{' + df[j].iloc[0] + '}'] = df[j].iloc[i] #formatting key becomes '{key}'

    doc = docx.Document("./template.docx") #Replace the template doc here

    for i in items:
        for p in doc.paragraphs:
            if p.text.find(i)>=0:
                p.text=p.text.replace(i,items[i])

    if not os.path.exists ('Generated'):
        os.makedirs ('Generated')

    doc.save('./Generated/' + filename + '.docx')

