from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import VPS
from .serializers import VPSSerializer
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter


class VPSViewSet(viewsets.ModelViewSet):
    queryset = VPS.objects.all()
    serializer_class = VPSSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['uid', 'status']
    ordering_fields = ['cpu', 'ram', 'hdd', 'created_at']


    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        vps = self.get_object()
        new_status = request.data.get('status')
        if new_status in [stat[0] for stat in vps._meta.get_field('status').choices]:
            vps.status = new_status
            vps.save()
            serializer = self.get_serializer(vps)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
