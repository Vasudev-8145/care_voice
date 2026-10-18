from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from medivoice.serializers import UserSerializer,ComplaintSerializer
from medivoice.models import Complaint
from medivoice.permissions import IsOwner


class RegistrationView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance._validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializer(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class ComplaintListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = Complaint.objects.filter(owner=auth_user)

        serializer_instance = ComplaintSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = ComplaintSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class ComplaintRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        instance =  get_object_or_404(Complaint,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = ComplaintSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(Complaint,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = ComplaintSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(Complaint,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response({"messgae":"deleted..."})

class ComplaintFilterView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        complaint_type = request.query_params.get("complaint_type")
        priority = request.query_params.get("priority")
        status = request.query_params.get("status")

        instance = Complaint.objects.filter(owner=request.user)

        if complaint_type:

            instance = instance.filter(complaint_type__icontains=complaint_type)

        if priority:

            instance = instance.filter(priority__icontains=priority)

        if status:

            instance = instance.filter(status__icontains=status)

        serializer_instance = ComplaintSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

class ComplaintSearchView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        title = request.query_params.get("title")
        description = request.query_params.get("description")

        instance = Complaint.objects.filter(owner=request.user)

        if title:

            instance = instance.filter(title__icontains=title)

        if description:

            instance = instance.filter(description__icontains=description)

        serializer_instance = ComplaintSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

class ComplaintUnresolvedView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = Complaint.objects.filter(owner=auth_user,status__in=["SUBMITTED","IN PROGRESS","UNDER REVIEW"])

        serializer_instance = ComplaintSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

class ComplaintCountView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data = ({"total complaints":0})

        status_count = Complaint.objects.filter(owner=request.user)

        if status_count:

            total_complaints = status_count.values("id").aggregate(count=Count("id")).get("count")
            total_category_complaints = status_count.values("status").annotate(count=Count("id"))

            response_data["total complaints"] = total_complaints
            response_data["total_category_complaints"] = total_category_complaints

        return Response(data=response_data)

class ComplaintPriorityView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        instance = Complaint.objects.filter(owner=request.user,priority__in=["HIGH","CRITICAL"])

        serializer_instance = ComplaintSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    