from django.shortcuts import render, redirect
from .form import EditorBox, RequestProblem, ChatBox, LogOut
from .openAI import get_coding_problem, get_coding_feedback, get_answer
from .models import users
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
import sys, io, json, os


@csrf_exempt
def editor(request):
    if 'user_data' not in request.session:
        return redirect('login')
    print(request.session['user_data'])
    session_user = request.session['user_data']
    name = session_user['given_name']
    user = users.find_one({"email":session_user['email']})
    if user:
        cid = user['_id']
    else:
        result = users.insert_one({'email':session_user['email']})
        cid = result.inserted_id
        user = users.find_one({'_id':cid})

    terminal = ''
    ai_message = ''
    chat_open = False
    if 'last_message' in user:
        last_message = user['last_message']
    else:
        last_message = {}

    if 'active_conversation' in user:
        conversation = user['active_conversation']
    else:
        conversation = []

    if request.method == 'POST':
        if 'run_code' in request.POST:
            editor_form = EditorBox(request.POST)
            if editor_form.is_valid():
                code_string = editor_form.cleaned_data['python_code']
                terminal = get_code_result(code_string)
                users.update_one({"_id":cid},{"$set": {"last_code": code_string}})
        elif 'chat_box' in request.POST:
            if 'last_code' in user:
                editor_form = EditorBox({'python_code':user['last_code']})
            else:
                editor_form = EditorBox()
            chat_open = True
            chat_box = ChatBox(request.POST)
            if chat_box.is_valid():
                if (chat_box.cleaned_data['chat_box'] == 'empty'):
                    conversation.clear()
                else:
                    conversation.append(chat_box.cleaned_data['chat_box'])
                    conversation.append(get_answer(chat_box.cleaned_data['chat_box'],{'conversation':conversation[:-1],'problem':user['last_problem'],'message':user['last_message'],'code':user['last_code']}))
                users.update_one({"_id":cid},{"$set": {"active_conversation": conversation}})
        elif 'request_button' in request.POST:
            editor_form = EditorBox()
            ai_message = get_coding_problem()
            users.update_one({"_id":cid},{"$set": {"last_message": ai_message,"last_problem": ai_message, "last_code": "", "active_conversation":[]}})
            conversation = []
            last_message = ai_message
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
                    last_message['feedback'] = format_feedback(feedback)

                    # If the problem was solved, get rid of it, otherwise, add it to the message for reference.
                    if feedback['success']:
                        users.update_one({"_id":cid},{"$set": {"last_problem": "","active_conversation": []}})
                        last_message['finished'] = True
                    else:
                        users.update_one({"_id":cid},{"$set": {"last_message": last_message}})
                        last_message['finished'] = False
        else:
            editor_form = EditorBox()
    else:
        if 'last_code' in user:
            editor_form = EditorBox({'python_code':user['last_code']})
        else:
            editor_form = EditorBox()

    request_form = RequestProblem()
    log_out = LogOut()
    chat_box = ChatBox()
    
    # last_message['feedback'] = 'something'
    # last_message['finished'] = True
    return render(request, "editor/editor.html", {'name':name, 'editor_form': editor_form, 'request_form' : request_form, 'terminal': terminal, 'AI_message': last_message, 'chat_box': chat_box, 'chat_open': chat_open, 'conversation': conversation, 'log_out':log_out} )

@csrf_exempt
def callback(request):
    token = request.POST['credential']
    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID')
        )
    except ValueError as e:
        print('failed to log in successfully',e)
        return
    
    request.session['user_data'] = user_data

    return redirect('editor')

@csrf_exempt
def login(request):
    if request.method == "POST" and 'logout_button' in request.POST:
        request.session.pop('user_data')
    return render(request, "editor/login.html")


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
