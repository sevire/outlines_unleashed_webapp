import os

from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.template import loader
from opml.outline import Outline
from opml.outline_node import OutlineNode
from output_generators.ppt_output_generators import PowerPointGenerator

from ou_app.data_drivers.dropdown_driver import node_specifier_powerpoint_slides, dropdown_select_list, get_specifier
from ou_app.models import DataNodeDescriptor
from ou_app.utilities import data_node_output
from outlines_unleashed_webapp import settings
from .forms import TransformationForm

output_ppt_filepath = os.path.join(settings.BASE_DIR, "ou_app/resources/ppt_output_01.pptx")
template_ppt_filepath = os.path.join(settings.BASE_DIR, "ou_app/resources/ppt_template_01.pptx")


def unleash_outline(request):
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

            # Get file name and trans type chosen by user (not actual filename saved) to display on result
            file = form.cleaned_data['file']
            descriptor = form.cleaned_data['transformation']

            if descriptor.name == "PPT-01":
                # For now this is hard-coded to route through create ppt treatment.
                # This will be changed to be more generic.
                # ToDo: Remove hard-coding of PPT processing and replace with more general approach.

                outline = Outline.from_opml(outline_full_path,
                                            tag_text_delimiter=("", ":"),
                                            tag_note_delimiter=("", ":")
                                            )

                # For testing assume that the data node is in node 1 (first node below root)
                outline_node_list = list(outline.list_all_nodes())
                data_node = outline_node_list[1].node()

                # Generate PowerPoint file from table
                output_generator = PowerPointGenerator()
                output_generator.create_power_point_skeleton(
                    data_node,
                    template_ppt_filepath,
                    output_ppt_filepath
                )
                return render(request, 'ou_app/ppt_download.html')
            else:
                # descriptor.name is a key into the data node descriptor table, so extract the record and use the JSON
                # as the descriptor.  Exception is that if descriptor is PPT - hard-code to process as PPT file
                # (for now).

                descriptor_json = descriptor.json
                descriptor_object = OutlineNode.from_json(descriptor_json)

                tag_text_delimiter = tuple(descriptor_object['header']['tag_delimiters']['text_delimiters'])
                tag_note_delimiter = tuple(descriptor_object['header']['tag_delimiters']['note_delimiters'])

                outline = Outline.from_opml(outline_full_path,
                                            tag_text_delimiter=tag_text_delimiter,
                                            tag_note_delimiter=tag_note_delimiter)

                # For testing assume that the data node is in node 1 (first node below root)
                outline_node_list = list(outline.list_all_nodes())
                data_node = outline_node_list[1].node()

                # Convert data fields into lists of fields to make easier processing by template
                extracted_data_records = data_node.extract_data_node(descriptor_object)
                fields, data_records = data_node_output.extract_data_fields(extracted_data_records)

                return render(request, 'ou_app/result.html', {
                    'transformation': descriptor.name,
                    'file': file,
                    'data_records': data_records,
                    'fields': fields
                })
    elif request.method == "GET":
        form = TransformationForm
        context = {
            "form": form,
        }
        return render(request, 'ou_app/unleash_outline.html', context)
    else:
        raise ValueError(f'Unexpected HTTP method {request.method}')


def result(request):
    return render(request, 'ou_app/result.html')


def download_ppt(request):
    file_path = os.path.abspath("ou_app/resources/ppt_output_01.pptx")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response


def index(request):
    template = loader.get_template('ou_app/home.html')
    return HttpResponse(template.render())
