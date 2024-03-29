from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PostOffice, Package
from .serializers import PostOfficeSerializer, PackageSerializer
from .tasks import register_package_task, record_arrival_task, document_departure_task, confirm_arrival_task

@api_view(['POST'])
def register_package(request):
    """
    API endpoint to register a new package.
    """
    if request.method == 'POST':
        serializer = PackageSerializer(data=request.data)
        if serializer.is_valid():
            # Enqueue task to register package asynchronously
            print('------------------------------------------------------')
            # package_id = register_package_task.delay(serializer.validated_data)
            package_id = register_package_task(serializer.validated_data)
            return Response({'package_id': package_id}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def record_arrival(request, package_id, office_id):
    """
    API endpoint to record the arrival of a package at an intermediate post office.
    """
    # Enqueue task to record arrival asynchronously
    # record_arrival_task.delay(package_id, office_id)
    record_arrival_task(package_id, office_id)
    return Response({'message': 'Recording arrival...'}, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def document_departure(request, package_id, office_id):
    """
    API endpoint to document the departure of a package from an intermediate post office.
    """
    # Enqueue task to document departure asynchronously
    # document_departure_task.delay(package_id, office_id)
    document_departure_task(package_id, office_id)
    return Response({'message': 'Documenting departure...'}, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def confirm_arrival(request, package_id, office_id):
    """
    API endpoint to confirm the arrival of a package at the destination post office.
    """
    # Enqueue task to confirm arrival asynchronously
    # confirm_arrival_task.delay(package_id, office_id)
    confirm_arrival_task(package_id, office_id)
    return Response({'message': 'Confirming arrival...'}, status=status.HTTP_202_ACCEPTED)