def extract_headers(extracted_data):
    """
    Returns list of field names (used to drive html table) in data table returned from opml extracted data node.

    Doesn't check that all records have same fields.

    :param extracted_data: A list of dicts, all with same fields, one for each row of extracted data.
    :return:
    """

    fields = [field for field in extracted_data[0]]
    return fields


def extract_data_fields(extracted_data):
    headers = extract_headers(extracted_data)
    data_fields = []
    for record in extracted_data:
        record_fields = []
        for field in headers:
            record_fields.append(record[field])
        data_fields.append(record_fields)
    return headers, data_fields


def to_html_table():
    pass
