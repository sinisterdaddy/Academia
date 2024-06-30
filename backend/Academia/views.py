from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Academia
import json
from . import openai_integration



@csrf_exempt
def create(request):


    if request.method == 'POST':
        try:
            # Parse JSON data sent from the client
            data = json.loads(request.body)

            # Check if the data contains a "value" key
            if 'email' in data:

                # try:
                #     record = Academia.objects.get(email=data['email'])  # Replace 'id' with the actual field you're using for identification
                # except Academia.DoesNotExist:
                #     instance = Academia(email=data['email'], name=data['name'], major=data['major'],
                #                     interests=data['interests'])
                #     instance.save()

                interest_list = None

                if Academia.objects.filter(email=data['email']).exists():
                    record = Academia.objects.get(email=data['email'])
                    record.name = data['name']
                    record.major = data['major']
                    # Assuming interests is a string of interests separated by commas
                    current_interests = record.interests.split(',') if record.interests else []
                    if data['interests'] not in current_interests:
                        current_interests.append(data['interests'])
                        record.interests = ','.join(current_interests)
                    record.save()
                    interest_list = record.interests.split(',') if record.interests else []
                    


                else:
                    instance = Academia(email=data['email'], name=data['name'], major=data['major'],
                                    interests=[data['interests']])
                    interest_list = [data['interests']]
                    instance.save()

                gptresponse = openai_integration.get_gpt_response(data['name'], data['major'], data['interests'])
                json_obj = openai_integration.extract_branch(gptresponse, data['email'], interest_list)




                return JsonResponse(json_obj, safe=False)

            else:
                return JsonResponse({'error': 'Missing "value" in data.'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def getinterests(request):

    if request.method == 'GET':
        try:
            # Parse JSON data sent from the client
            data = json.loads(request.body)

            # Check if the data contains a "value" key
            if 'email' in data:

                if Academia.objects.filter(email=data['email']).exists():
                    record = Academia.objects.get(email=data['email'])
                    data_dict = {"interests": record.interests}
                    json_obj = json.dumps(data_dict, indent = 4)
                    return JsonResponse(json_obj, safe=False) 
                else:
                    json_obj = json.dumps({}, indent = 4)
                    return JsonResponse(json_obj, safe=False)


            else:
                return JsonResponse({'error': 'Missing "value" in data.'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt  
def clicknode(request):
  
    if request.method == 'PUT':
        try:
            # Parse JSON data sent from the client
            data = json.loads(request.body)

            # Check if the data contains a "value" key
            if 'email' in data:

                # try:
                #     record = Academia.objects.get(email=data['email'])  # Replace 'id' with the actual field you're using for identification
                # except Academia.DoesNotExist:
                #     instance = Academia(email=data['email'], name=data['name'], major=data['major'],
                #                     interests=data['interests'])
                #     instance.save()

                if Academia.objects.filter(email=data['email']).exists():
                    record = Academia.objects.get(email=data['email'])
                    if data['interest'] not in record.interests:
                        record.interests.append(data['interest']) #= record.interests['interests'].append(data['interests'])
                    record.save()

                    gptresponse = openai_integration.get_gpt_response(record.name, record.major, data['interest'])
                    json_obj = openai_integration.extract_branch(gptresponse, data['email'])

                    return JsonResponse(json_obj, safe=False)

            else:
                return JsonResponse({'error': 'Missing "value" in data.'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def returnhome(request):
    
    if request.method == 'POST':
        try:
            # Parse JSON data sent from the client
            data = json.loads(request.body)

            # Check if the data contains a "value" key
            if 'email' in data:

                if Academia.objects.filter(email=data['email']).exists():
                    record = Academia.objects.get(email=data['email'])
                    data_dict = {"name": record.name, "major": record.major, "email": record.email}
                    json_obj = json.dumps(data_dict, indent = 4)
                    return JsonResponse(json_obj, safe=False) 
                else:
                    json_obj = json.dumps({}, indent = 4)
                    return JsonResponse(json_obj, safe=False)


            else:
                return JsonResponse({'error': 'Missing "value" in data.'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def getquestion(request):
    
    if request.method == 'POST':
        try:
            # Parse JSON data sent from the client
            data = json.loads(request.body)

            json_obj = openai_integration.get_question(data['interest'])
            return JsonResponse(json_obj, safe=False)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def feedbackans(request):
    
    if request.method == 'POST':
        try:
            # Parse JSON data sent from the client
            data = json.loads(request.body)

            json_obj = openai_integration.feedback_ans(data['question'], data['answer'], data['major'])
            return JsonResponse(json_obj, safe=False)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def explainmore(request):
    
    if request.method == 'POST':
        try:
            # Parse JSON data sent from the client
            data = json.loads(request.body)

            json_obj = openai_integration.explain_more(data['interest'], data['major'])
            return JsonResponse(json_obj, safe=False)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
