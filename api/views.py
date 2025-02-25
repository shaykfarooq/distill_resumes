import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pandas as pd
from api.llm import get_resume_in_relational_form
from api.resume_utils import process_document_get_text
from api.models import Resume
from django.db import connection
from api.llm import generate_sqlite_select_query
from django.template import Template, Context
import traceback
from api.models import ChatHistory
from django.utils.timezone import localtime
from django.contrib.humanize.templatetags.humanize import naturaltime

@method_decorator(csrf_exempt, name='dispatch')
class UploadFileView(View):
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        file = request.FILES['file']
        model = request.POST['model']
        if not file.name.endswith(('.pdf', '.docx')):
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        file_path = os.path.join(settings.RESUME_DIR, file.name)
        path = default_storage.save(file_path, ContentFile(file.read()))

        text = process_document_get_text(path)

        resume_dict = get_resume_in_relational_form(text,model)

        resume = Resume(**resume_dict)
        resume.file_path = path
        resume.save()

        return JsonResponse({'message': 'File under proccess', 'file_path': path, 'text':text})



@method_decorator(csrf_exempt, name='dispatch')
class ExecuteQueryView(View):
    def get(self, request, *args, **kwargs):
        prompt = request.GET.get('prompt')
        model = request.GET.get('model')
        if not prompt:
            return JsonResponse({'error': 'No prompt provided'}, status=400)

        sql_query,reply_template = generate_sqlite_select_query(prompt,model)

        print(sql_query)
        if sql_query:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_query)
                    df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

                except Exception as e:
                    print(e)
                    traceback.format_exc()
                    df = pd.DataFrame([])

                df.columns = [c.replace("_"," ").upper() for c in df.columns]

                results = df.to_html(classes=['table table-bordered table-striped table-hover table-sm'],index=False,escape=False).replace('\n',' ')
            if not df.empty:
                response = f"""{reply_template} <br><div class="table-responsive">{results}</div>"""
            else:
                response = f"""Unable to get reponse at this time."""

            chat_history = ChatHistory(prompt=prompt, response=response, user='anonymous')
            chat_history.save()
        
            return HttpResponse(response)
        else:
            print("sql_query not found")
            return HttpResponse(f"""Unable to get reponse at this time.""")



            

@method_decorator(csrf_exempt, name='dispatch')
class GetChatHistoryView(View):
    def get(self, request, *args, **kwargs):
        chat_history = ChatHistory.objects.all().values('prompt', 'response', 'timestamp')
        for chat in chat_history:
            chat['timestamp'] = naturaltime(chat['timestamp'])
        return JsonResponse(list(chat_history), safe=False)
    

@method_decorator(csrf_exempt, name='dispatch')
class GetResumesView(View):
    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all().values('candidate_name', 'file_path','created_at').order_by('-created_at')
        resumes_list = []
        for resume in resumes:
            resumes_list.append({
                'candidateName': resume['candidate_name'],
                'fileName': os.path.basename(resume['file_path']),
                'downloadUrl': request.build_absolute_uri(resume['file_path']).replace('api/', ''),
                'uploaded': naturaltime(resume['created_at'])
            })
        return JsonResponse(resumes_list, safe=False)