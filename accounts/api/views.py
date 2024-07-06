from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pymongo import MongoClient
from django.conf import settings
from .serializers import CompanyUserSerializer
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime, timedelta
import pytz
from rest_framework.permissions import IsAuthenticated
from accounts.api.authentication import JWTAuthentication

# client = MongoClient(settings.MONGODB_NAME, settings.MONGODB_PORT)
# db = client[settings.MONGODB_NAME]
# users_collection = db['company_user']

client = MongoClient('localhost', 27017)
db = client['SalesSage']
users_collection = db['company_user']

class UsernameAvailable(APIView):
    def post(self, request):
        username = request.data.get('username')
        if users_collection.find_one({'username': username}):
            return Response({'error': 'Username is not available'}, status=status.HTTP_409_CONFLICT)
        return Response({'message': 'Username is available'}, status=status.HTTP_200_OK)

class CompanyUserView(APIView):
    def post(self, request):
        serializer = CompanyUserSerializer(data=request.data)

        if users_collection.find_one({'$or': [{'username': request.data.get('username')}, {'email': request.data.get('email')}]}):
            return Response({'error': 'Username or Email already exists'}, status=status.HTTP_409_CONFLICT)
        
        if serializer.is_valid():
            user = serializer.save()
            sales_collection_name = f"{user.username}_sales"
            item_collection_name = f"{user.username}_items"
            db.create_collection(item_collection_name)
            db.create_collection(sales_collection_name)
            return Response(CompanyUserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = list(users_collection.find())
        for user in users:
            user['_id'] = str(user['_id'])
            user.pop('password', None)
        return Response(users, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = users_collection.find_one({'username': data.get('username')})
        if user and check_password(data.get('password'), user['password']):
            access_token = self.generate_access_token(user)
            refresh_token = self.generate_refresh_token(user)
            
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def generate_access_token(self, user):
        access_token_payload = {
            'username': user['username'],
            'exp': datetime.now(pytz.UTC) + timedelta(minutes=5),
            'iat': datetime.now(pytz.UTC)
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
        return access_token

    def generate_refresh_token(self, user):
        refresh_token_payload = {
            'username': user['username'],
            'exp': datetime.now(pytz.UTC) + timedelta(days=7),
            'iat': datetime.now(pytz.UTC)
        }
        refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')
        return refresh_token
    
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
    
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token is None:
            return Response({'error': 'Please provide a refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=status.HTTP_403_FORBIDDEN)
        
        user = users_collection.find_one({'username': payload['username']})
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        access_token = self.generate_access_token(user)
        return Response({'access_token': access_token})

    def generate_access_token(self, user):
        access_token_payload = {
            'username': user['username'],
            'exp': datetime.now(pytz.UTC) + timedelta(minutes=5),
            'iat': datetime.now(pytz.UTC)
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
        return access_token