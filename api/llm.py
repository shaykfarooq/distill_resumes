import requests
import json
from django.conf import settings

from api.models import ChatHistory

OPEN_ROUTER_API_KEY = settings.OPEN_ROUTER_API_KEY

OPEN_ROUTER_COMPLETION_URL = settings.OPEN_ROUTER_COMPLETION_URL

def get_resume_in_relational_form(text,model):
    
    response = requests.post(
    url=OPEN_ROUTER_COMPLETION_URL,
    headers={
        "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
    },
    data=json.dumps({
        "model": model, # Optional
        "messages": [
        {
            "role": "user",
            "content": f"""{text}
    from above cv get fields in below json format value of each field should be the text only no array or nested objects
    {{
        "candidate_name" : "",
        "personal_information" : "",
        "education_history" : "",
        "work_experience" : "",
        "skills" : "",
        "projects" : "",
        "certifications" : "",
        "minified_context" : "<give here the minified context of the cv>"
    }}
    """
        }
        ]
    })
    )

    content = response.json()['choices'][0]['message']['content']

    try:
        start_index = content.index('{')
        end_index = content.rindex('}') + 1
        json_content = content[start_index:end_index]
        resume_dict = json.loads(json_content)
    except (ValueError, json.JSONDecodeError) as e:
        return {}
    return resume_dict


def generate_sqlite_select_query(user_prompt,model):
    previous_chat_history = ""
    i =0  
    for r in ChatHistory.objects.all().values('prompt', 'response', 'timestamp'):
        i += 1
        previous_chat_history += f"""
                Prompt {i}: {r['prompt']}
                Response {i}: {r['response']}
                Timestamp {i}: {r['timestamp']}
        """

    


    response = requests.post(
        url=OPEN_ROUTER_COMPLETION_URL,
        headers={
            "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
        },
        data=json.dumps({
            "model": model, # Optional
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    History:
                    {previous_chat_history if previous_chat_history else 'No previous chat history'}
                    
                    
                    Based on previous chat history Generate a SQLite SELECT query only (nothing other than select) for the following table schema based on the user prompt:{user_prompt} 
CREATE TABLE "api_resume" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "candidate_name" varchar(240) NULL,
    "personal_information" text NULL,
    "education_history" text NULL,
    "skills" text NULL,
    "projects" text NULL,
    "certifications" text NULL,
    "work_experience" text NULL
);


In the generated query handle in where clause the case of the words by doing upper on both sides and handle plural also, if there is space in where condition then replace it with % and show only candidate name and only fields used in the where condition. In the sql query add file_path column in select clause towards the end
in your response share only sql query nothing else.
"""
                }
            ]
        })
    )

    content = response.json()['choices'][0]['message']['content']

    sql_query = content.replace('```','').replace('sqlite','').replace('sql','')


    return sql_query,''
