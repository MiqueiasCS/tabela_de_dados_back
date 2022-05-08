from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vunerabilities
from .serializers import ReportSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import ipdb

class ReportsView(APIView):
    def get(self,request, report_id=''):

        if report_id:
            try:
                report = Vunerabilities.objects.get(id=report_id)
                serializer = ReportSerializer(report)

                return Response(serializer.data,status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response({'error': 'Invalid report_id'},status=status.HTTP_404_NOT_FOUND)

        reports = Vunerabilities.objects.all()

        serializer = ReportSerializer(reports,many=True)
        
        paginator = Paginator(serializer.data,50)
        page_number = request.GET.get('page',1)

        if page_number == "all":
            return Response(serializer.data,status=status.HTTP_200_OK)

        page_response = paginator.get_page(page_number)
        
        return Response(page_response.object_list,status=status.HTTP_200_OK)
