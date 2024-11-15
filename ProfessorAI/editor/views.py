from django.shortcuts import render
from .form import EditorBox, RequestProblem, OpenChatBox
from .openAI import get_coding_problem, get_coding_feedback
from .models import users
import sys, io, json



def editor(request):
    customer_list = ''.join([str(x['first_name']) for x in users.find()])
    cid = [x['_id'] for x in users.find()][0]
    terminal = ''
    ai_message = ''
    chat_open = False
    user = users.find_one({'_id':cid})
    if 'last_message' in user:
        last_message = user['last_message']
    else:
        last_message = ''
    if request.method == 'POST':
        if 'run_code' in request.POST:
            editor_form = EditorBox(request.POST)
            if editor_form.is_valid():
                code_string = editor_form.cleaned_data['python_code']
                terminal = get_code_result(code_string)
                users.update_one({"_id":cid},{"$set": {"last_code": code_string}})
        elif 'request_button' in request.POST:
            editor_form = EditorBox()
            ai_message = get_coding_problem()
            users.update_one({"_id":cid},{"$set": {"last_message": ai_message,"last_problem": ai_message, "last_code": ""}})
            last_message = ai_message
        elif 'chat_button' in request.POST:
            editor_form = EditorBox()
            if 'last_code' in user:
                editor_form = EditorBox({'python_code':user['last_code']})
            else:
                editor_form = EditorBox()
            chat_open = not chat_open
        elif 'submit_code' in request.POST:
            editor_form = EditorBox(request.POST)
            if editor_form.is_valid():
                code_string = editor_form.cleaned_data['python_code']

                # Make sure that a problem was given.
                if 'last_problem' in user and user['last_problem'] != '':
                    
                    # Get and display the AI feedback.
                    last_problem = user['last_problem']
                    feedback = get_coding_feedback(last_problem, code_string)
                    feedback = json.loads(feedback)
                    last_message = format_feedback(feedback)

                    # If the problem was solved, get rid of it, otherwise, add it to the message for reference.
                    if feedback['success']:
                        users.update_one({"_id":cid},{"$set": {"last_problem": ""}})
                    else:
                        users.update_one({"_id":cid},{"$set": {"last_message": last_message}})
                        last_message += user['last_problem']
        else:
            editor_form = EditorBox()
    else:
        if 'last_code' in user:
            editor_form = EditorBox({'python_code':user['last_code']})
        else:
            editor_form = EditorBox()

    request_form = RequestProblem()
    open_chat_form = OpenChatBox()


    return render(request, "editor/editor.html", {'editor_form': editor_form, 'request_form' : request_form, 'terminal': terminal, 'AI_message': last_message, 'customer_list': customer_list, 'open_chat_form': open_chat_form, 'chat_open': chat_open})

def get_code_result(code_string):
    output_buffer = io.StringIO()

    normal_stdout = sys.stdout
    sys.stdout = output_buffer
    try:
        exec(code_string)
        sys.stdout = normal_stdout
        terminal = output_buffer.getvalue()
        output_buffer.close()
        return terminal.replace('\n','<br>')
    except Exception as error:
        return error


def format_feedback(feedback):
    output = ''
    if feedback['success']:
        output += '<h2>Problem Solved Successfully!</h2>'
    else:
        output += '<h2>Incorrect Solution. Try again.</h2>'
    return output + f'<p>{feedback['feedback']}<p>'
