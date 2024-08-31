# import PyPDF2

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with open(pdf_path, "rb") as file:
#         reader = PyPDF2.PdfReader(file)
#         num_pages = len(reader.pages)
#         for page_num in range(num_pages):
#             page = reader.pages[page_num]
#             text += page.extract_text()
#     return text

# # Example usage
# pdf_path = "E:\\python\\google_Doc_AI\\Invoice.pdf"
# extracted_text = extract_text_from_pdf(pdf_path)
# print(extracted_text)

######################################################################################
##########################################################################################
# import pdfplumber

# def extract_text_with_coordinates(pdf_path):
#     text_with_coordinates = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page_num, page in enumerate(pdf.pages, start=1):
#             for word in page.extract_words():
#                 text_with_coordinates.append({
#                     'text': word['text'],
#                     'x0': word['x0'],
#                     'y0': word['top'],
#                     'x1': word['x1'],
#                     'y1': word['bottom'],
#                     'page_num': page_num
#                 })
#     return text_with_coordinates

# # Example usage
# pdf_path = "E:\\python\\google_Doc_AI\\Invoice.pdf"
# extracted_text = extract_text_with_coordinates(pdf_path)

# # Print the extracted text with coordinates
# for item in extracted_text:
#     print(f"Text: {item['text']}, Page: {item['page_num']}, Coordinates: ({item['x0']}, {item['y0']}) to ({item['x1']}, {item['y1']})")

#######################################################################################################################################################

################################                    STRING FOR THE OCR                     #################################################################

###########################################################################################################################################3


# from typing import Optional, Sequence
# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai
# from tabulate import tabulate
# import json
# import os

# def get_latest_processor_version(project_id: str, location: str, processor_id: str) -> str:
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     response = client.list_processor_versions(parent=f"projects/{project_id}/locations/{location}/processors/{processor_id}")
#     latest_version = response.processor_versions[0].name.split('/')[-1]
#     return latest_version

# def process_document_ocr_sample(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> str:
#     # Fetch the latest processor version dynamically
#     processor_version = get_latest_processor_version(project_id, location, processor_id)

#     # No OCR configuration included
#     document = process_document(project_id, location, processor_id, processor_version, file_path, mime_type)

#     # Initialize the dictionary to store extracted data
#     json_dict = {}

#     output_str = ""

#     for i, page in enumerate(document.pages, start=1):
#         # Two lines of distance between pages
#         # output_str += "\n\n"
#         # Write page number
#         output_str += f" This is Page {i} of the PDF:\n\n"
#         for block in page.blocks:
#             output_str += layout_to_text(block.layout, document.text) + "\n\n"

#         tables = []
#         for table in page.tables:
#             table_data = []
#             for row in table.header_rows:
#                 table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#             for row in table.body_rows:
#                 table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#             tables.append(tabulate(table_data, tablefmt="grid"))
#         output_str += "\n".join(tables)
#         output_str += "\n"

#         # Two lines of distance between tables and extracted data
#         output_str += "\n\n"

#         output_str += "EXTRACTED OCR DATA FROM THE PDF :\n\n"
#         for block in page.blocks:
#             extracted_text = layout_to_text(block.layout, document.text)
#             output_str += extracted_text + "\n"
#             output_str += "\n"

#         # Extract form fields and store them in the dictionary
#         form_fields_dict = process_form_fields(page, document.text)
#         json_dict.update(form_fields_dict)

#     jsonString = json.dumps(json_dict, indent=4)
#     # Write extracted data to a JSON string
#     output_str += jsonString

#     return output_str

# def process_form_fields(page: documentai.Document.Page, text: str) -> dict:
#     """
#     Extract form fields from a document page and return them as a dictionary.
#     """
#     form_fields_dict = {}
#     for field in page.form_fields:
#         name = layout_to_text(field.field_name, text)
#         value = layout_to_text(field.field_value, text)
#         form_fields_dict[name.strip()] = value.strip()
#     return form_fields_dict

# def process_document(project_id: str, location: str, processor_id: str, processor_version: str, file_path: str, mime_type: str) -> documentai.Document:
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     name = client.processor_version_path(
#         project_id, location, processor_id, processor_version
#     )

#     with open(file_path, "rb") as image:
#         image_content = image.read()

#     request = documentai.ProcessRequest(name=name, raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type))

#     result = client.process_document(request=request)

#     return result.document

# def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
#     result = ""
#     for segment in layout.text_anchor.text_segments:
#         result += text[int(segment.start_index):int(segment.end_index)]
#     return result

# def process_documents_in_folder(project_id: str, location: str, processor_id: str, folder_path: str, mime_type: str) -> None:
#     # Iterate through all files in the folder
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".pdf") or filename.endswith(".PDF"): 
#             file_path = os.path.join(folder_path, filename) 
#             output_string = process_document_ocr_sample(project_id, location, processor_id, file_path, mime_type)
#             # Print or save the output string as needed
#             #print(output_string)
#             output_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_output.txt")
#             with open(output_file_path, "w", encoding="utf-8") as output_file:
#                 output_file.write(output_string)


# project_id = "silken-math-407910"
# location = "us"
# processor_id = "afec3f70ecec4b87"
# folder_path = "C:\\Users\\HP\\Desktop\\output"
# mime_type = "application/pdf"

# process_documents_in_folder(project_id, location, processor_id, folder_path, mime_type)
#####################################################################################################lkjdlkjpzd
# # Example usage:
# project_id = "silken-math-407910"
# location = "us"
# processor_id = "afec3f70ecec4b87"
# file_path = "E:\\python\\google_Doc_AI\\20240227113111.pdf"
# mime_type = "application/pdf"

# output_string = process_document_ocr_sample(project_id=project_id, location=location, processor_id=processor_id, file_path=file_path, mime_type=mime_type)
# print(output_string)  # Or do whatever you want with the output string


##############################################################################################################################################################
##########################################################################################################################################3
###################################################################################################################################################

# import io
# from pdfminer.high_level import extract_text

# def extract_pdf_text(pdf_path):
#     with open(pdf_path, 'rb') as f:
#         text = extract_text(f)
#     return text

# pdf_path = 'E:\\python\\google_Doc_AI\\Invoice.pdf'
# extracted_text = extract_pdf_text(pdf_path)

# # Write the extracted text into a text file with UTF-8 encoding
# output_text_file = 'E:\\python\\google_Doc_AI\\extracted_text.txt'
# with open(output_text_file, 'w', encoding='utf-8') as text_file:
#     text_file.write(extracted_text)

# print(f"Extracted text has been saved to '{output_text_file}'")


#########################################################################################################################33
########################################################################################################
######################################################################################################################

# import PyPDF2
# import Split
# from subprocess import call
# import sys

# if (len(sys.argv) < 2):
#     print("Error\nFormat: \n\tpython main.py your-pdf-file")
# else:
#     filename = sys.argv[1]
#     directory = "splitted/" + filename

#     Split.split(directory, filename)
#     pdfFileObj = open(filename, 'rb')
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#     for i in range(pdfReader.numPages):
#         splitted_file_name = directory + "/" + repr(i)
#         call(["pdftotext", splitted_file_name + ".pdf"])
#         # f = open(splitted_file_name + '.txt', 'r')
#         # print("Page %s" % repr(i+1))
#         # print(f.read())
#         # print("====================")

########################################################################################################################
##########################################################################################################################
##########################################################################################################################

# import fitz  # PyMuPDF

# # Open the PDF file
# pdf_document = fitz.open('E:\\python\\google_Doc_AI\\Invoice.pdf')

# # Extract text from each page
# for page_num in range(len(pdf_document)):
#     page = pdf_document.load_page(page_num)
#     text = page.get_text("text")
#     print(text)


# import fitz  # PyMuPDF
# import re

# def clean_text(text):
#     text = re.sub(r'\s+', ' ', text)
#     text = text.strip()
#     return text

# # def extract_information(text):
# #     dates = re.findall(r'\d{2}/\d{2}/\d{4}', text)
# #     return dates

# # Open the PDF file
# pdf_document = fitz.open('E:\\python\\google_Doc_AI\\Invoice.pdf')

# all_text = ""
# for page_num in range(len(pdf_document)):
#     page = pdf_document.load_page(page_num)
#     text_dict = page.get_text("dict")
#     blocks = text_dict["blocks"]
#     for block in blocks:
#         for line in block["lines"]:
#             for span in line["spans"]:
#                 all_text += span["text"] + "\n"

# cleaned_text = clean_text(all_text)
# # information = extract_information(cleaned_text)

# print("Cleaned Text:", cleaned_text)
# # print("Extracted Information:", information)

#############################################################################################################################################
################################################################################################################################################
##########################################                     MAIN IDP SOLUTION                    ######################################################################################################
###############################################################################################################################################
##############################################################################################################################################33
# pip show google-cloud-core
# # pip show google-cloud-documentai
# from typing import Optional, Sequence
# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai
# from tabulate import tabulate
# import json
# import os

# def get_latest_processor_version(project_id: str, location: str, processor_id: str) -> str:
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     response = client.list_processor_versions(parent=f"projects/{project_id}/locations/{location}/processors/{processor_id}")
#     latest_version = response.processor_versions[0].name.split('/')[-1]
#     return latest_version

# def process_document_ocr_sample(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> str:
#     processor_version = get_latest_processor_version(project_id, location, processor_id)
#     document = process_document(project_id, location, processor_id, processor_version, file_path, mime_type)
#     json_dict = {}
#     output_str = ""

#     for i, page in enumerate(document.pages, start=1):
#         output_str += f"\n\nThis is Page {i} of the PDF:\n\n"

#         for block in page.blocks:
#             output_str += layout_to_text(block.layout, document.text) + "\n\n"

#         tables = []
#         for table in page.tables:
#             table_data = []
#             for row in table.header_rows:
#                 table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#             for row in table.body_rows:
#                 table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#             tables.append(tabulate(table_data, tablefmt="grid"))
#         output_str += "\n".join(tables) + "\n\n"

#         form_fields_dict = process_form_fields(page, document.text)
#         json_dict.update(form_fields_dict)

#     jsonString = json.dumps(json_dict, indent=4)
#     output_str += jsonString

#     return output_str

# def process_form_fields(page: documentai.Document.Page, text: str) -> dict:
#     form_fields_dict = {}
#     for field in page.form_fields:
#         name = layout_to_text(field.field_name, text)
#         value = layout_to_text(field.field_value, text)
#         form_fields_dict[name.strip()] = value.strip()
#     return form_fields_dict

# def process_document(project_id: str, location: str, processor_id: str, processor_version: str, file_path: str, mime_type: str) -> documentai.Document: #str
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     name = client.processor_version_path(
#         project_id, location, processor_id, processor_version
#     )

#     with open(file_path, "rb") as image:
#         image_content = image.read()

#     request = documentai.ProcessRequest(name=name, raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type))
#     result = client.process_document(request=request)
#     return result.document

# def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
#     result = ""
#     for segment in layout.text_anchor.text_segments:
#         result += text[int(segment.start_index):int(segment.end_index)]
#     return result

# def process_documents_in_folder(project_id: str, location: str, processor_id: str, folder_path: str, mime_type: str) -> None:
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(folder_path, filename)
#             output_string = process_document_ocr_sample(project_id, location, processor_id, file_path, mime_type)
#             #print(output_string)
#             output_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_output.txt")
#             with open(output_file_path, "w", encoding="utf-8") as output_file:
#                 output_file.write(output_string)


# project_id = "silken-math-407910"
# location = "us"
# processor_id = "afec3f70ecec4b87"
# folder_path = "C:\\Users\\HP\\Desktop\\output"
# mime_type = "application/pdf"

# process_documents_in_folder(project_id, location, processor_id, folder_path, mime_type)   # = 

###################################################################################################################3
#######################################################################################################################3
##########33#######################################################################################################
####################################################################################################################
###########################################################################################################################
# from typing import Optional, Sequence
# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai
# from tabulate import tabulate
# import json
# import os

# def get_latest_processor_version(project_id: str, location: str, processor_id: str) -> str:
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     response = client.list_processor_versions(parent=f"projects/{project_id}/locations/{location}/processors/{processor_id}")
#     latest_version = response.processor_versions[0].name.split('/')[-1]
#     return latest_version

# def process_document_ocr_sample(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> str:
#     processor_version = get_latest_processor_version(project_id, location, processor_id)
#     document = process_document(project_id, location, processor_id, processor_version, file_path, mime_type)
#     json_dict = {}
#     output_str = ""

#     for i, page in enumerate(document.pages, start=1):
#         output_str += f"\n\nThis is Page {i} of the PDF:\n\n"

#         for block in page.blocks:
#             output_str += layout_to_text(block.layout, document.text) + "\n\n"

#         tables = []
#         for table in page.tables:
#             table_data = []
#             for row in table.header_rows:
#                 table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#             for row in table.body_rows:
#                 table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#             tables.append(tabulate(table_data, tablefmt="grid"))
#         output_str += "\n".join(tables) + "\n\n"

#         form_fields_dict = process_form_fields(page, document.text)
#         json_dict.update(form_fields_dict)

#     jsonString = json.dumps(json_dict, indent=4)
#     output_str += jsonString

#     return output_str

# def process_form_fields(page: documentai.Document.Page, text: str) -> dict:
#     form_fields_dict = {}
#     for field in page.form_fields:
#         name = layout_to_text(field.field_name, text)
#         value = layout_to_text(field.field_value, text)
#         form_fields_dict[name.strip()] = value.strip()
#     return form_fields_dict

# def process_document(project_id: str, location: str, processor_id: str, processor_version: str, file_path: str, mime_type: str) -> documentai.Document: #str
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     name = client.processor_version_path(
#         project_id, location, processor_id, processor_version
#     )

#     with open(file_path, "rb") as image:
#         image_content = image.read()

#     request = documentai.ProcessRequest(name=name, raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type))
#     result = client.process_document(request=request)
#     return result.document

# def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
#     result = ""
#     for segment in layout.text_anchor.text_segments:
#         result += text[int(segment.start_index):int(segment.end_index)]
#     return result

# # def process_documents_in_folder(project_id: str, location: str, processor_id: str, folder_path: str, mime_type: str) -> None:
# #     for filename in os.listdir(folder_path):
# #         if filename.endswith(".pdf"):
# #             file_path = os.path.join(folder_path, filename)
# #             output_string = process_document_ocr_sample(project_id, location, processor_id, file_path, mime_type)
# #             #print(output_string)
# #             output_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_output.txt")
# #             with open(output_file_path, "w", encoding="utf-8") as output_file:
# #                 output_file.write(output_string)
# def process_documents_in_folder(project_id: str, location: str, processor_id: str, folder_path: str, mime_type: str) -> str:
#     all_output_strings = ""  # Accumulator for all output strings

#     for filename in os.listdir(folder_path):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(folder_path, filename)
#             output_string = process_document_ocr_sample(project_id, location, processor_id, file_path, mime_type)
#             all_output_strings += output_string  # Append current output string to accumulator

#     return all_output_strings  # Return accumulated output strings


# project_id = "silken-math-407910"
# location = "us"
# processor_id = "afec3f70ecec4b87"
# folder_path = "C:\\Users\\HP\\Desktop\\output"
# mime_type = "application/pdf"

# output_string = process_documents_in_folder(project_id, location, processor_id, folder_path, mime_type)
# print(output_string)  # Output the combined result for all documents
# # process_documents_in_folder(project_id, location, processor_id, folder_path, mime_type)   # = 



###################################################################################################################3
#######################################################################################################################3
###################################################################################################################
####################################################################################################################
###########################################################################################################################

from typing import Optional, Sequence
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from tabulate import tabulate
import json
import os

def get_latest_processor_version(project_id: str, location: str, processor_id: str) -> str:
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    response = client.list_processor_versions(parent=f"projects/{project_id}/locations/{location}/processors/{processor_id}")
    latest_version = response.processor_versions[0].name.split('/')[-1]
    return latest_version

def process_document_ocr_sample(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> str:
    processor_version = get_latest_processor_version(project_id, location, processor_id)
    document_json = process_document(project_id, location, processor_id, processor_version, file_path, mime_type)
    document = json.loads(document_json)  # JSON string ko waps into a dictionary Parse krne ke liye 

    json_dict = {}
    output_str = ""

    for i, page in enumerate(document['pages'], start=1):
        output_str += f"\n\nThis is Page {i} of the PDF:\n\n"

        for block in page.get('blocks', []):
            output_str += layout_to_text(block['layout'], document['text']) + "\n\n"

        tables = []
        for table in page.get('tables', []):
            table_data = []
            for row in table.get('headerRows', []):
                table_data.append([layout_to_text(cell['layout'], document['text']) for cell in row['cells']])
            for row in table.get('bodyRows', []):
                table_data.append([layout_to_text(cell['layout'], document['text']) for cell in row['cells']])
            tables.append(tabulate(table_data, tablefmt="grid"))
        output_str += "\n".join(tables) + "\n\n"

        form_fields_dict = process_form_fields(page, document['text'])
        json_dict.update(form_fields_dict)

    jsonString = json.dumps(json_dict, indent=4)
    output_str += jsonString

    return output_str


def process_form_fields(page: dict, text: str) -> dict:
    form_fields_dict = {}
    for field in page.get('formFields', []):
        name = layout_to_text(field['fieldName'], text)
        value = layout_to_text(field['fieldValue'], text)
        form_fields_dict[name.strip()] = value.strip()
    return form_fields_dict

def process_document(project_id: str, location: str, processor_id: str, processor_version: str, file_path: str, mime_type: str) -> str:
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )
    mime_type = "application/pdf"
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    with open(file_path, "rb") as image:
        image_content = image.read()

    request = documentai.ProcessRequest(name=name, raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type))
    result = client.process_document(request=request)

    document_dict = {
        'text': result.document.text,
        'pages': [
            {
                'blocks': [
                    {
                        'layout': {
                            'textAnchor': {
                                'textSegments': [
                                    {'startIndex': segment.start_index, 'endIndex': segment.end_index}
                                    for segment in block.layout.text_anchor.text_segments
                                ]
                            }
                        }
                    } for block in page.blocks
                ] if page.blocks else [],
                'tables': [
                    {
                        'headerRows': [
                            {'cells': [
                                {'layout': {
                                    'textAnchor': {
                                        'textSegments': [
                                            {'startIndex': segment.start_index, 'endIndex': segment.end_index}
                                            for segment in cell.layout.text_anchor.text_segments
                                        ]
                                    }
                                }} for cell in row.cells
                            ]} for row in table.header_rows
                        ],
                        'bodyRows': [
                            {'cells': [
                                {'layout': {
                                    'textAnchor': {
                                        'textSegments': [
                                            {'startIndex': segment.start_index, 'endIndex': segment.end_index}
                                            for segment in cell.layout.text_anchor.text_segments
                                        ]
                                    }
                                }} for cell in row.cells
                            ]} for row in table.body_rows
                        ],
                    } for table in page.tables
                ] if page.tables else [],
                'formFields': [
                    {
                        'fieldName': {
                            'textAnchor': {
                                'textSegments': [
                                    {'startIndex': segment.start_index, 'endIndex': segment.end_index}
                                    for segment in field.field_name.text_anchor.text_segments
                                ]
                            }
                        },
                        'fieldValue': {
                            'textAnchor': {
                                'textSegments': [
                                    {'startIndex': segment.start_index, 'endIndex': segment.end_index}
                                    for segment in field.field_value.text_anchor.text_segments
                                ]
                            }
                        }
                    } for field in page.form_fields
                ] if page.form_fields else []
            } for page in result.document.pages
        ]
    }

    json_string = json.dumps(document_dict, indent=4)  #  dictionary ko Convert kr raha hoon JSON string
    return json_string  #yaha ab mai json sting return kr raha hoon 

def layout_to_text(layout: dict, text: str) -> str:
    result = ""
    for segment in layout['textAnchor']['textSegments']:
        result += text[int(segment['startIndex']):int(segment['endIndex'])]
    return result

def process_documents_in_folder(project_id: str, location: str, processor_id: str, folder_path: str, mime_type: str) -> str:
    all_output_strings = ""  # Accumulator subhi output string ke liye 

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf") or filename.endswith(".PDF") or filename.endswith(".PNG"):
            file_path = os.path.join(folder_path, filename)
            output_string = process_document_ocr_sample(project_id, location, processor_id, file_path, mime_type)
            output_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_output.txt")
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(output_string)
            all_output_strings += output_string  # abhi wale output string ko accumulator me append krega 

    return all_output_strings  # accumulated output strings return krega 

project_id = "silken-math-407910"
location = "us"
processor_id = "afec3f70ecec4b87"
folder_path = "C:\\Users\\HP\\Desktop\\Test IDP"
mime_type = "application/"

output_string = process_documents_in_folder(project_id, location, processor_id, folder_path, mime_type)
# print(output_string)  # Output the combined result for all documents
