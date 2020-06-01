# Simple Mail Merge

A simple tool that allows you to read data from csv file and insert to template(document)

#### Requirement
This tool requires several modules:
- python-docx
- pandas
- xlrd

##### Install Module
```pip
pip install python-docx
pip install pandas
pip install xlrd
```
#### Usage
1. Admend the template document and excel sheet path in the source code.
2. In template document, use {} to wrap the header name in spread sheet.
    - example: column's header name in spread sheet is "firstname". In template document, place `{firstname}` to desire place then the tool will generate the document based on the given data in spread sheet
3. Document generated will save in `Generated/` directory
4. `** There are two demo document and spread sheet available in this repo. Might try the sample for better understanding.**`


#### Constraint 
- Not working on words appear inside a "container" element inside the XML.
- only generate plain text


