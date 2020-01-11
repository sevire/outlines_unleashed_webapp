import os

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from opml.node_matching_criteria import NodeAncestryMatchingCriteria
from opml.outline import Outline

from ou_app.utilities import data_node_output
from outlines_unleashed_webapp import settings
from .forms import TransformationForm


def unleash_outline(request):
    test_data_node_specifier_01 = {
        'section_name': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'slide_name': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'bullet': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        }
    }

    if request.method == 'POST':
        form = TransformationForm(request.POST, request.FILES)
        if form.is_valid():
            transformation_instance = form.save(commit=False)
            transformation_instance.file = request.FILES['file']
            file_type = transformation_instance.file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type != 'opml':
                return render(request, 'ou_app/error.html')

            transformation_instance.save()

            # We have saved the file.  Let's process it now.
            # ToDo: Check whether this should be BASE_DIR or MEDIA_DIR (Media duplicates media folder)
            outline_full_path = os.path.join(settings.BASE_DIR, transformation_instance.file.url)

            outline = Outline.from_opml(outline_full_path)
            # For testing assume that the data node is in node 1 (first node below root)

            outline_node_list = list(outline.list_all_nodes())
            data_node = outline_node_list[1].node()

            # Convert data fields into lists of fields to make easier processing by template
            extracted_data_records = data_node.extract_data_node(test_data_node_specifier_01)
            fields, data_records = data_node_output.extract_data_fields(extracted_data_records)

            return render(request, 'ou_app/result.html', {
                'transformation': transformation_instance,
                'data_records': data_records,
                'fields': fields
            })
    elif request.method == "GET":
        form = TransformationForm
        context = {"form": form, }
        return render(request, 'ou_app/unleash_outline.html', context)
    else:
        raise ValueError(f'Unexpected HTTP method {request.method}')


def result(request):
    return render(request, 'ou_app/result.html')