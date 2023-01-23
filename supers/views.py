from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from . models import Super
from super_types.serializers import SuperTypeSerializer
from super_types.models import SuperType

# @api_view(['GET']) # get all supers with custom response
# def supers_list(request):
#     supers = Super.objects.all()
#     super_types = SuperType.objects.all()
#     serializer = SuperSerializer(supers, many=True)
#     super_type_serializer = SuperTypeSerializer(super_types, many=True)
#     custom_response_dict = {}
#     if request.method == 'GET':
#         custom_response_dict = {
#             'supers': serializer.data,
#             'super_types': super_type_serializer.data
#         }
#         return Response(custom_response_dict)



@api_view(['GET', 'POST']) # Get all filtered supers in a list; POST to add new supers 
def supers_list(request):
    supers = Super.objects.all()
    super_types = SuperType.objects.all()
    type_param = request.query_params.get('super_type')
    serializer = SuperSerializer(supers, many=True)
    super_type_serializer = SuperTypeSerializer(super_types, many=True)
    
    
    if request.method == 'GET':
        if type_param:
            supers = Super.objects.filter(super_type__type=type_param)
            serializer = SuperSerializer(supers, many=True)
        return Response(serializer.data)
        else:
        serializer = SuperSerializer(supers, many=True)
        super_type_serializer = SuperTypeSerializer(super_types, many=True)
        custom_response_dict = {
            'supers': serializer.data,
            'super_types': super_type_serializer.data
        }
        return Response(custom_response_dict)   
        
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def supers_id_list(request, pk):
    super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(super);
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

