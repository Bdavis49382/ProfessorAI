from django.shortcuts import render
from .form import EditorBox
import sys
import io

def index(request):
    terminal = ''
    if request.method == 'POST':
        form = EditorBox(request.POST)
        if form.is_valid():
            code_string = form.cleaned_data['python_code']
            output_buffer = io.StringIO()

            normal_stdout = sys.stdout
            sys.stdout = output_buffer
            try:
                exec(code_string)
                sys.stdout = normal_stdout
                terminal = output_buffer.getvalue()
                terminal = terminal.replace('\n','<br>')
                output_buffer.close()
            except Exception as error:
                terminal = error
            
    else:
        form = EditorBox()

    return render(request, "editor/editor.html", {'form': form, 'terminal': terminal})
