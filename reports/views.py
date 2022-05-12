from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vunerabilities
from .serializers import ReportSerializer, UpdateSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .utils import ordering, queryset_filter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ListVunerabilitiesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):

        reports = queryset_filter(Vunerabilities,request)
        ordered_reports = ordering(reports,request)

        serializer = ReportSerializer( ordered_reports,many=True)
        
        page_number = request.GET.get('page',1)

        if page_number == "all":
            return Response(serializer.data,status=status.HTTP_200_OK)

        paginator = Paginator(serializer.data,50)
        page_response = paginator.get_page(page_number)
        
        
        resp = {
            'total' : len(serializer.data),
            'enviados': len(page_response.object_list),
            'itens':page_response.object_list
        }
        return Response(resp,status=status.HTTP_200_OK)


class RetrieveVunerabilitiesByNameView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, hostname=''):
        report = Vunerabilities.objects.filter(hostname__iexact=hostname)
        serializer = ReportSerializer(report,many=True)

        page_number = request.GET.get('page',1)
        paginator = Paginator(serializer.data,50)
        page_response = paginator.get_page(page_number)
        
        
        resp = {
            'total' : len(serializer.data),
            'enviados': len(page_response.object_list),
            'itens':page_response.object_list
        }

        return Response(resp,status=status.HTTP_200_OK)



class RetrieveUpdateVunerabilitiesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, report_id=''):
        try:
            report = Vunerabilities.objects.get(id=report_id)
            serializer = ReportSerializer(report)

            return Response(serializer.data,status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Invalid report_id'},status=status.HTTP_404_NOT_FOUND)


    def patch(self,request, report_id=''):
        try:
            report = Vunerabilities.objects.get(id=report_id)
            serializer = UpdateSerializer(report,data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Invalid report_id'},status=status.HTTP_404_NOT_FOUND)