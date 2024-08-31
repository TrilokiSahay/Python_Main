
# # import argparse
# from typing import Sequence

# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai
# from typing import List, Sequence
# import pandas as pd
# import os
# import json

# credential_path = "E:/python/google_Doc_AI/Json file google auth/silken-math-407910-d0b9438c6004.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# folder = "E:\\python\\google_Doc_AI"
# file_path = "E:\\python\\google_Doc_AI\\Invoice.pdf"

# project_id= 'silken-math-407910'
# location = 'us'
# processor_id = '4513eb762f7b7f18'
# mime_type = 'application/pdf'

# output_file_path = os.path.join(folder, "Output.txt")

# def get_table_data(
#     rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
# ) -> List[List[str]]:
#     """
#     Get Text data from table rows
#     """
#     all_values: List[List[str]] = []
#     for row in rows:
#         current_row_values: List[str] = []
#         for cell in row.cells:
#             current_row_values.append(
#                 text_anchor_to_text(cell.layout.text_anchor, text)
#             )
#         all_values.append(current_row_values)
#     return all_values

# def text_anchor_to_text(text_anchor: documentai.Document.TextAnchor, text: str) -> str:
#     """
#     Document AI identifies table data by their offsets in the entirity of the
#     document's text. This function converts offsets to a string.
#     """
#     response = ""
#     # If a text segment spans several lines, it will
#     # be stored in different text segments.
#     for segment in text_anchor.text_segments:
#         start_index = int(segment.start_index)
#         end_index = int(segment.end_index)
#         response += text[start_index:end_index]
#     return response.strip().replace("\n", " ")

# def process_document_form_sample(
#     project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
# ):
#     # Online processing request to Document AI
#     document = process_document(
#         project_id, location, processor_id, file_path, mime_type
#     )

#     text = document.text

#     print(f"There are {len(document.pages)} page(s) in this document.")

#     # Write output to the text file
#     with open(output_file_path, "w", encoding="utf-8") as output_file:
#         output_file.write(f"There are {len(document.pages)} page(s) in this document.\n\n")

#         # Read the form fields and tables output from the processor
#         i = 0
#         json_dict = {}
#         for page in document.pages:
#             i += 1
#             output_file.write(f"\n\n**** Page {page.page_number} ****\n")

#             output_file.write(f"\nFound {len(page.tables)} table(s):\n")
#             tab_ctr = 0
#             for table in page.tables:
#                 tab_ctr += 1
#                 num_columns = len(table.header_rows[0].cells)
#                 num_rows = len(table.body_rows)
#                 output_file.write(f"Table with {num_columns} columns and {num_rows} rows:\n")

#                 # Print header rows
#                 output_file.write("Columns:\n")
#                 print_table_rows_to_file(table.header_rows, text, output_file)
#                 # Print body rows
#                 output_file.write("Table body data:\n")
#                 print_table_rows_to_file(table.body_rows, text, output_file)

#                 header_row_values: List[List[str]] = []
#                 body_row_values: List[List[str]] = []

#                 header_row_values = get_table_data(table.header_rows, document.text)
#                 body_row_values = get_table_data(table.body_rows, document.text)

#                 df = pd.DataFrame(
#                     data=body_row_values,
#                     columns=pd.MultiIndex.from_arrays(header_row_values),
#                 )

#                 df.to_csv(folder+"/page"+str(i)+"_"+str(tab_ctr)+".csv")
#                 output_file.write(f"\nFound {len(page.form_fields)} form field(s):\n")

#             for field in page.form_fields:
#                 name = layout_to_text(field.field_name, text)
#                 value = layout_to_text(field.field_value, text)
#                 output_file.write(f"    * {repr(name.strip())}: {repr(value.strip())}\n")

#             if(i==1):
#                 for field in page.form_fields:
#                     name = layout_to_text(field.field_name, text)
#                     value = layout_to_text(field.field_value, text)
#                     json_dict[name.strip()] = value.strip()
#                     output_file.write(f"    * {repr(name.strip())}: {repr(value.strip())}\n")

#         jsonString = json.dumps(json_dict, indent=4)

#         with open(folder+"/header.json", "w") as json_file:
#             json.dump(json_dict, json_file)

# def process_document(
#     project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
# ) -> documentai.Document:
#     # You must set the api_endpoint if you use a location other than 'us', e.g.:
#     opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

#     client = documentai.DocumentProcessorServiceClient(client_options=opts)

#     name = client.processor_path(project_id, location, processor_id)

#     # Read the file into memory
#     with open(file_path, "rb") as image:
#         image_content = image.read()

#     # Load Binary Data into ADocument I RawDocument Object
#     raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

#     # Configure the process request
#     request = documentai.ProcessRequest(name=name, raw_document=raw_document)

#     result = client.process_document(request=request)

#     return result.document

# def print_table_rows_to_file(
#     table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str, output_file
# ) -> None:
#     for table_row in table_rows:
#         row_text = ""
#         for cell in table_row.cells:
#             cell_text = text_anchor_to_text(cell.layout.text_anchor, text) #layout_to_text(cell.layout, text)  
#             row_text += f"{repr(cell_text.strip())} | "
#         output_file.write(row_text + "\n")



# def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
#     """
#     Document AI identifies text in different parts of the document by their
#     offsets in the entirety of the document's text. This function converts
#     offsets to a string.
#     """
#     response = ""
#     # If a text segment spans several lines, it will
#     # be stored in different text segments.
#     for segment in layout.text_anchor.text_segments:
#         start_index = int(segment.start_index)
#         end_index = int(segment.end_index)
#         response += text[start_index:end_index]
#     return response

# process_document_form_sample(project_id, location, processor_id, file_path,mime_type)

##########################################################################################################################3
#############################################################################################################################

# from typing import Sequence, List
# import os
# import json
# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai_v1 as documentai
# import pandas as pd

# credential_path = "E:/python/google_Doc_AI/Json file google auth/silken-math-407910-d0b9438c6004.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# folder = "E:\\python\\google_Doc_AI"
# file_path = "E:\\python\\google_Doc_AI\\Invoice.pdf"

# project_id= 'silken-math-407910'
# location = 'us'
# processor_id_ocr = '25295dd5b90c6c65'
# processor_id_invoice = '4513eb762f7b7f18'
# mime_type = 'application/pdf'

# output_file_path = os.path.join(folder, "Output.txt")

# def process_document(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> documentai.Document:
#     opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
#     client = documentai.DocumentProcessorServiceClient(client_options=opts)
#     name = client.processor_path(project_id, location, processor_id)

#     with open(file_path, "rb") as image:
#         image_content = image.read()

#     raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
#     request = documentai.ProcessRequest(name=name, raw_document=raw_document)

#     result = client.process_document(request=request)
#     return result.document

# def process_ocr_document(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str):
#     document = process_document(project_id, location, processor_id, file_path, mime_type)
#     text = document.text
#     return text

# def process_invoice_document(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str):
#     document = process_document(project_id, location, processor_id, file_path, mime_type)
#     # Extract invoice data from document and return as needed
#     # Example:
#     invoice_data = {
#         "invoice_number": "123456",
#         "date": "2022-05-01",
#         "total_amount": "$100.00",
#         # Add more fields as needed
#     }
#     return invoice_data

# def process_document_form_sample(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str):
#     if processor_id == processor_id_ocr:
#         text = process_ocr_document(project_id, location, processor_id, file_path, mime_type)
#         with open(output_file_path, "w", encoding="utf-8") as output_file:
#             output_file.write(text)
#     elif processor_id == processor_id_invoice:
#         invoice_data = process_invoice_document(project_id, location, processor_id, file_path, mime_type)
#         with open(output_file_path, "w", encoding="utf-8") as output_file:
#             json.dump(invoice_data, output_file, indent=4)
#             # Alternatively, you can write the invoice data in a structured format (e.g., CSV, Excel) using pandas
#             # Example:
#             # df = pd.DataFrame(invoice_data)
#             # df.to_csv(output_file_path)

# process_document_form_sample(project_id, location, processor_id_invoice, file_path, mime_type)


##########################################################################################################################33
##########################################################################################################################
###########################################               O    C    R             #######################################################################################


# from typing import Optional, Sequence

# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai


# def process_document_ocr_sample(
#     project_id: str,
#     location: str,
#     processor_id: str,
#     processor_version: str,
#     file_path: str,
#     mime_type: str,
# ) -> None:
#     # Optional: Additional configurations for Document OCR Processor.
#     # For more information: https://cloud.google.com/document-ai/docs/document-ocr
#     process_options = documentai.ProcessOptions(
#         ocr_config=documentai.OcrConfig(
#             enable_native_pdf_parsing=True,
#             enable_image_quality_scores=True,
#         )
#     )
#     # Online processing request to Document AI
#     document = process_document(
#         project_id,
#         location,
#         processor_id,
#         processor_version,
#         file_path,
#         mime_type,
#         process_options=process_options,
#     )

#     text = document.text
#     print(f"Full document text: {text}\n")
#     # print(f"There are {len(document.pages)} page(s) in this document.\n")

#     # for page in document.pages:
#     #     print(f"Page {page.page_number}:")
#         # print_page_dimensions(page.dimension)
#         # print_detected_langauges(page.detected_languages)

#         # print_blocks(page.blocks, text)
#         # print_paragraphs(page.paragraphs, text)
#         # print_lines(page.lines, text)
#         # print_tokens(page.tokens, text)

#         # if page.image_quality_scores:
#         #     print_image_quality_scores(page.image_quality_scores)


# # def print_page_dimensions(dimension: documentai.Document.Page.Dimension) -> None:
# #     print(f"    Width: {str(dimension.width)}")
# #     print(f"    Height: {str(dimension.height)}")


# # def print_detected_langauges(
# #     detected_languages: Sequence[documentai.Document.Page.DetectedLanguage],
# # ) -> None:
# #     print("    Detected languages:")
# #     for lang in detected_languages:
# #         print(f"        {lang.language_code} ({lang.confidence:.1%} confidence)")


# # def print_blocks(blocks: Sequence[documentai.Document.Page.Block], text: str) -> None:
# #     print(f"    {len(blocks)} blocks detected:")
# #     for block in blocks:
# #         block_text = layout_to_text(block.layout, text)
# #         print(f"        Block text: {repr(block_text)}")
# #         print(f"        Bounding box coordinates: {block.layout.bounding_poly.normalized_vertices}")
#     # first_block_text = layout_to_text(blocks[0].layout, text)
#     # print(f"        First text block: {repr(first_block_text)}")
#     # last_block_text = layout_to_text(blocks[-1].layout, text)
#     # print(f"        Last text block: {repr(last_block_text)}")


# # def print_paragraphs(
# #     paragraphs: Sequence[documentai.Document.Page.Paragraph], text: str
# # ) -> None:
# #     print(f"    {len(paragraphs)} paragraphs detected:")
# #     first_paragraph_text = layout_to_text(paragraphs[0].layout, text)
# #     print(f"        First paragraph text: {repr(first_paragraph_text)}")
# #     last_paragraph_text = layout_to_text(paragraphs[-1].layout, text)
# #     print(f"        Last paragraph text: {repr(last_paragraph_text)}")


# def print_lines(lines: Sequence[documentai.Document.Page.Line], text: str) -> None:
#     print(f"    {len(lines)} lines detected:")
#     first_line_text = layout_to_text(lines[0].layout, text)
#     print(f"        First line text: {repr(first_line_text)}")
#     last_line_text = layout_to_text(lines[-1].layout, text)
#     print(f"        Last line text: {repr(last_line_text)}")


# # def print_tokens(tokens: Sequence[documentai.Document.Page.Token], text: str) -> None:
# #     print(f"    {len(tokens)} tokens detected:")
# #     first_token_text = layout_to_text(tokens[0].layout, text)
# #     first_token_break_type = tokens[0].detected_break.type_.name
# #     print(f"        First token text: {repr(first_token_text)}")
# #     print(f"        First token break type: {repr(first_token_break_type)}")
# #     last_token_text = layout_to_text(tokens[-1].layout, text)
# #     last_token_break_type = tokens[-1].detected_break.type_.name
# #     print(f"        Last token text: {repr(last_token_text)}")
# #     print(f"        Last token break type: {repr(last_token_break_type)}")


# # def print_image_quality_scores(
# #     image_quality_scores: documentai.Document.Page.ImageQualityScores,
# # ) -> None:
# #     print(f"    Quality score: {image_quality_scores.quality_score:.1%}")
# #     print("    Detected defects:")

# #     for detected_defect in image_quality_scores.detected_defects:
# #         print(f"        {detected_defect.type_}: {detected_defect.confidence:.1%}")


# def process_document(
#     project_id: str,
#     location: str,
#     processor_id: str,
#     processor_version: str,
#     file_path: str,
#     mime_type: str,
#     process_options: Optional[documentai.ProcessOptions] = None,
# ) -> documentai.Document:
#     # You must set the `api_endpoint` if you use a location other than "us".
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     # The full resource name of the processor version, e.g.:
#     # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
#     # You must create a processor before running this sample.
#     name = client.processor_version_path(
#         project_id, location, processor_id, processor_version
#     )

#     # Read the file into memory
#     with open(file_path, "rb") as image:
#         image_content = image.read()

#     # Configure the process request
#     request = documentai.ProcessRequest(
#         name=name,
#         raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
#         # Only supported for Document OCR processor
#         process_options=process_options,
#     )

#     result = client.process_document(request=request)

#     # For a full list of `Document` object attributes, reference this page:
#     # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
#     return result.document


# def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
#     """
#     Document AI identifies text in different parts of the document by their
#     offsets in the entirety of the document"s text. This function converts
#     offsets to a string.
#     """
#     # If a text segment spans several lines, it will
#     # be stored in different text segments.
#     return "".join(
#         text[int(segment.start_index) : int(segment.end_index)]
#         for segment in layout.text_anchor.text_segments
#     )


# # TODO(developer): Edit these variables before running the sample.
# project_id = "silken-math-407910"
# location = "us"  # Format is 'us' or 'eu'
# processor_id = "25295dd5b90c6c65"  # Create processor before running sample   
# processor_version = "pretrained-ocr-v2.0-2023-06-02"
# file_path = "E:\\python\\google_Doc_AI\\Invoice.pdf"
# mime_type = "application/pdf"  

# process_document_ocr_sample(
#     project_id=project_id,
#     location=location,
#     processor_id=processor_id,
#     processor_version=processor_version,
#     file_path=file_path,
#     mime_type=mime_type,
# )

###############################################################################################################################################
################################################################################################################################################3
##############################################################################################################################################3#
###################################################################################################################################################

# from typing import Optional, Sequence
# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai
# from tabulate import tabulate
# import json

# def process_document_ocr_sample(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str, output_file: str) -> None:
#     # Fetch the latest processor version dynamically
#     processor_version = get_latest_processor_version(project_id, location, processor_id)

#     # No OCR configuration included
#     document = process_document(project_id, location, processor_id, processor_version, file_path, mime_type)

#     # Initialize the dictionary to store extracted data
#     json_dict = {}

#     with open(output_file, "w", encoding="utf-8") as f:
#         for i, page in enumerate(document.pages, start=1):
#             # Two lines of distance between pages
#             f.write("\n\n")
#             # Write page number
#             f.write(f" This is Page {i} of the PDF:\n\n")

#             tables = []
#             for table in page.tables:
#                 table_data = []
#                 for row in table.header_rows:
#                     table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#                 for row in table.body_rows:
#                     table_data.append([layout_to_text(cell.layout, document.text) for cell in row.cells])
#                 tables.append(tabulate(table_data, tablefmt="grid"))
#             f.write("\n".join(tables))
#             f.write("\n")

#             # Two lines of distance between tables and extracted data
#             f.write("\n\n")

#             f.write("EXTRACTED OCR DATA FROM THE PDF :\n\n")
#             for block in page.blocks:
#                extracted_text = layout_to_text(block.layout, document.text)
#                f.write(extracted_text + "\n")
#                f.write("\n")

#             # Extract form fields and store them in the dictionary
#             form_fields_dict = process_form_fields(page, document.text, f)
#             json_dict.update(form_fields_dict)

#             #    # Extract form fields and store in the dictionary
#             # for field in page.form_fields:
#             #        name = layout_to_text(field.field_name, document.text)
#             #        value = layout_to_text(field.field_value, document.text)
#             #        json_dict[name.strip()] = value.strip()

#     jsonString = json.dumps(json_dict, indent=4)
#      # Write extracted data to a JSON file
#     with open("E:\\python\\google_Doc_AI\\Json file google auth\\header.json", "w") as json_file:
#         json.dump(json_dict, json_file)

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

# def get_latest_processor_version(project_id: str, location: str, processor_id: str) -> str:
#     client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(
#             api_endpoint=f"{location}-documentai.googleapis.com"
#         )
#     )

#     response = client.list_processor_versions(parent=f"projects/{project_id}/locations/{location}/processors/{processor_id}")
#     latest_version = response.processor_versions[0].name.split('/')[-1]
#     return latest_version

# def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
#     result = ""
#     for segment in layout.text_anchor.text_segments:
#         result += text[int(segment.start_index):int(segment.end_index)]
#     return result

# def process_form_fields(page: documentai.Document.Page, text: str, output_file) -> dict:
#     """
#     Extract form fields from a document page and return them as a dictionary.
#     Write the form fields to the output file.
#     """
#     form_fields_dict = {}
#     output_file.write(f"\nFound {len(page.form_fields)} form field(s):\n")
#     for field in page.form_fields:
#         name = layout_to_text(field.field_name, text)
#         value = layout_to_text(field.field_value, text)
#         form_fields_dict[name.strip()] = value.strip()
#         output_file.write(f"    * {repr(name.strip())}: {repr(value.strip())}\n")
#     return form_fields_dict


# project_id = "silken-math-407910"
# location = "us"  
# processor_id = "afec3f70ecec4b87"
# file_path = "C:\\Users\\HP\\Desktop\\output\\223808.pdf"
# mime_type = "application/pdf"  
# output_file = "C:\\Users\\HP\\Desktop\\output\\output.txt"

# process_document_ocr_sample(project_id=project_id, location=location, processor_id=processor_id, file_path=file_path, mime_type=mime_type, output_file=output_file)

#######################################################################################################################3
#################################################################################################################
#########################################################################################################################
#########################################################################################################################3

import argparse
from typing import Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from typing import List, Sequence
import pandas as pd
import os
import json

credential_path = "C:\\Users\\your.json file"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

folder = "C:\\Users\\the folder"
file_path = "C:\\Users\\the.pdf"

project_id= 'math-40'
location = 'us'
processor_id = 'ecec4b87'
mime_type = 'application/pdf'

output_file_path = os.path.join(folder, "Output.txt")

def get_table_data(
    rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
) -> List[List[str]]:
    """
    Get Text data from table rows
    """
    all_values: List[List[str]] = []
    for row in rows:
        current_row_values: List[str] = []
        for cell in row.cells:
            current_row_values.append(
                text_anchor_to_text(cell.layout.text_anchor, text)
            )
        all_values.append(current_row_values)
    return all_values

def text_anchor_to_text(text_anchor: documentai.Document.TextAnchor, text: str) -> str:
    """
    Document AI identifies table data by their offsets in the entirity of the
    document's text. This function converts offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response.strip().replace("\n", " ")



        #with open(folder+"/header.json", "w") as json_file:
         #   json.dump(json_dict, json_file)

def process_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> documentai.Document:
    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    return result.document

def print_table_rows_to_file(
    table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str, output_file
) -> None:
    for table_row in table_rows:
        row_text = ""
        for cell in table_row.cells:
            cell_text = layout_to_text(cell.layout, text)
            row_text += f"{repr(cell_text.strip())} | "
        output_file.write(row_text + "\n")

def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document's text. This function converts
    offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response

def process_document_form_sample(
    project_id: str, location: str, processor_id: str, file_path: str
):
    # Online processing request to Document AI
    mime_type =  "application/pdf"
    document = process_document(
        project_id, location, processor_id, file_path, mime_type
    )
    

    text = document.text

    print(f"There are {len(document.pages)} page(s) in this document.")

    # Write output to the text file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(f"There are {len(document.pages)} page(s) in this document.\n\n")

        # Read the form fields and tables output from the processor
        i = 0
        json_dict = {}
        for page in document.pages:
            i += 1
            output_file.write(f"\n\n**** Page {page.page_number} ****\n")

            output_file.write(f"\nFound {len(page.tables)} table(s):\n")
            tab_ctr = 0
            for table in page.tables:
                tab_ctr += 1
                num_columns = len(table.header_rows[0].cells)
                num_rows = len(table.body_rows)
                output_file.write(f"Table with {num_columns} columns and {num_rows} rows:\n")

                # Print header rows
                output_file.write("Columns:\n")
                print_table_rows_to_file(table.header_rows, text, output_file)
                # Print body rows
                output_file.write("Table body data:\n")
                print_table_rows_to_file(table.body_rows, text, output_file)

                header_row_values: List[List[str]] = []
                body_row_values: List[List[str]] = []

                header_row_values = get_table_data(table.header_rows, document.text)
                body_row_values = get_table_data(table.body_rows, document.text)

                df = pd.DataFrame(
                    data=body_row_values,
                    columns=pd.MultiIndex.from_arrays(header_row_values),
                )

                df.to_csv(folder+"/page"+str(i)+"_"+str(tab_ctr)+".csv")
                output_file.write(f"\nFound {len(page.form_fields)} form field(s):\n")

            for field in page.form_fields:
                name = layout_to_text(field.field_name, text)
                value = layout_to_text(field.field_value, text)
                output_file.write(f"    * {repr(name.strip())}: {repr(value.strip())}\n")

            if(i==1):
                for field in page.form_fields:
                    name = layout_to_text(field.field_name, text)
                    value = layout_to_text(field.field_value, text)
                    json_dict[name.strip()] = value.strip()
                    output_file.write(f"    * {repr(name.strip())}: {repr(value.strip())}\n")

    jsonString = json.dumps(json_dict, indent=4)
    return jsonString
process_document_form_sample(project_id, location, processor_id, file_path)
#def function1(process_document_form_sample):
    #return function







