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

project_id = "s407910"
location = "us"
processor_id = "afe"
folder_path = "C:\\HP\\Desktop\\Test IDP"
mime_type = "application/"

output_string = process_documents_in_folder(project_id, location, processor_id, folder_path, mime_type)
# print(output_string)  # Output the combined result for all documents
