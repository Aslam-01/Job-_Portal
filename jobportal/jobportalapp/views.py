from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserEducationSerializer, UserExperienceSerializer, UserPersonalInfoSerializer, UserProfileSerializer, UserSkillsSerializer
from django.contrib.auth import authenticate
from jobportalapp.renders import UserRender
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from jobportalapp.models import User, PersonalInfo, Education, Experience, Skill, Profile

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    # renderer_classes = [UserRender]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRender]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            # user = User.objects.filter(email=email, password=password)
            user = authenticate(request,email=email,password=password)
            print(user)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPersonalInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, format=None):
        personal_info = PersonalInfo.objects.get(id=id)
        serializer = UserPersonalInfoSerializer(personal_info)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserPersonalInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Personal information updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,id,format=None):
        user = get_object_or_404(PersonalInfo, user=id)
        serializer=UserPersonalInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Personal information updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    
    def delete(self,request,id,format=None):
        user =PersonalInfo.objects.filter(user=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserEducationView(APIView):
    renderer_classes = [UserRender]
    def post(self, request, format=None):
        user = request.user # Assuming you are using authentication and the user is available in the request
        # Check if the user already has an education record
        education = request.data.get('education')

        if Education.objects.filter(education=education,user=user).exists():
                return Response({'error': 'Education record already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserEducationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',serializer.validated_data)
            serializer.save(user=user)
            return Response({'msg' :'Education Information Field Successfull'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
    def put(self,request,id,format=None):
        user=Education.objects.get(user=id)
        serializer=UserEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Response({'msg' :'Education updated successfully'},status= status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,id,format=None):
        user=Education.objects.get(user=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserExperienceView(APIView):
    renderer_classes = [UserRender]
    def post(self, request, format=None):
        user = request.user
          # Assuming you are using authentication and the user is available in the request
        company = request.data.get('company_name')
        if Experience.objects.filter(company_name=company,user=user).exists():
                return Response({'error': 'Experience record already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer=UserExperienceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response({'msg' :'Experience Information Field Added Successfull'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,id,format=None):
        user=Experience.objects.get(user=id)
        serializer=UserExperienceSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' :'Experience updated successfully'},status= status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        user=Experience.objects.get(user=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserSkillsView(APIView):
   def post(self,request):
       user = request.user
       serializer = UserSkillsSerializer(data=request.data)
       skill = request.data.get('skill')
       existing_skill = Skill.object.filter(user=user,skills=skill).first()
       if existing_skill:
           return Response({'message':'skill already exist for the user'})
       if serializer.is_valid(raise_exception=True):
           serializer.save(user=user)
           return Response({'message':'Skill created successfully'})
   

   def put(self,request,id,format=None):
       skills=Skill.objects.filter(id=id).first()
       if not skills:
           return Response({'message':'skills does not exist for the user'},status=400)
       serializer = UserSkillsSerializer(skills,data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response({'message': 'Skills updated successfully'}, status=200)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


   def delete(self, request, id, format=None):
        skills = Skill.objects.filter(id=id).first()
        if not skills:
            return Response({"message": "Skill does not exist for the user"}, status=400)

        skills.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class UserProfileView(APIView):
    renderer_classes = [UserRender]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # Get the current user

        try:
            profile = Profile.objects.get(user=user)
            personal_info = PersonalInfo.objects.get(user=user)
            education = Education.objects.get(user=user)
            experience = Experience.objects.get(user=user)
            skills = Skill.objects.get(user=user)

            profile_serializer = UserProfileSerializer(profile)
            personal_info_serializer = UserPersonalInfoSerializer(personal_info)
            education_serializer = UserEducationSerializer(education)
            experience_serializer = UserExperienceSerializer(experience)
            skills_serializer = UserSkillsSerializer(skills)

            response_data = {
                'profile': profile_serializer.data,
                'personal_info': personal_info_serializer.data,
                'education': education_serializer.data,
                'experience': experience_serializer.data,
                'skills': skills_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except (Profile.DoesNotExist, PersonalInfo.DoesNotExist, Education.DoesNotExist, Experience.DoesNotExist, Skill.DoesNotExist):
            return Response({'message': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)


