# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pymongo import MongoClient
from rest_framework.permissions import IsAuthenticated
from accounts.api.authentication import JWTAuthentication

# client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
# db = client[settings.DATABASES['default']['NAME']]
# collection = db['inventory_items']

client = MongoClient('localhost', 27017)
db = client['SalesSage']
collection = db['inventory_items']

class ItemsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        result = collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request):
        items = list(collection.find())
        for item in items:
            item['_id'] = str(item['_id'])
        return Response(items, status=status.HTTP_200_OK)