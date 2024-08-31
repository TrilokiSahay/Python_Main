
# import argparse
from typing import Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from typing import List, Sequence
import pandas as pd
import os
import json

credential_path = "E:/python/google_Doc_AI/Json file google auth/silken-math-407910-d0b9438c6004.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

folder = "E:\\python\\google_Doc_AI"
file_path = "E:\\python\\google_Doc_AI\\IN104956.pdf"

project_id= 'silken-math-407910'
location = 'us'
processor_id = 'afec3f70ecec4b87'
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

def process_document_form_sample(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
):
    # Online processing request to Document AI
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

        with open(folder+"/header.json", "w") as json_file:
            json.dump(json_dict, json_file)

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

    # Load Binary Data into ADocument I RawDocument Object
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
            cell_text = text_anchor_to_text(cell.layout.text_anchor, text) #layout_to_text(cell.layout, text)  
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

process_document_form_sample(project_id, location, processor_id, file_path,mime_type)
