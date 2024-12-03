from langchain_google_genai import ChatGoogleGenerativeAI
from .RoutePlanning.route_planning import PerformRoutePlanning
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyCve8Wj4fQj52DNw9qvjzcOesPfko4D084'
    )
@csrf_exempt
def get_routes(request,*args,**kwargs):
    if request.method=='POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            source=data.get('source')
            destination=data.get('destination')
            results=PerformRoutePlanning(model,source,destination)
            print(results)
            try:
                return JsonResponse(results, status=200)

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        except Exception as e:
            print(e)
    else:
        print('The request is not Post method!!!')