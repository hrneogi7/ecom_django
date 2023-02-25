from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login, logout
from django.views.decorators.csrf import csrf_exempt

import random, re

# Create your views here.
def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)] + 
                    [str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt
def signIn(request):
    if not request.method == 'POST':
        return JsonResponse({'error':'Invalid Request! Send a POST request with valid parameter'})

    username = request.POST['email']
    password = request.POST['password']

    #Validation of user data
    if not re.match("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$",password):
        return JsonResponse({'error': 'Invalid password! password should be \n - at least 8 characters \n - must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number \n - Can contain special characters'})
    
    if not re.match("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",username):
        return JsonResponse({'error': 'Invalid mail format! Enter valid email'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            user_dict = UserModel.objects.filter(email=username).values().first()
            user_dict.pop('password')

            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({'error': 'Previous Session is running'})
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)

            return JsonResponse({'token':token, 'user': user_dict})

        else:
            return JsonResponse({'error': 'Wrong Password'})
    except UserModel.DoesNotExist:
        return JsonResponse({'error' : 'Invalid email! user dnt exist'})


def signOut(request, id):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
    
    except UserModel.DoesNotExist:
        return JsonResponse({'error' : 'Invalid user id!'})

    logout(request)
    return JsonResponse({'success': 'Logout Successful!'})

class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            return [permission() for permission in self.permission_classes]

