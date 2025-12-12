from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from api import models, serializers

class TipoCalificacionViewSet(viewsets.ModelViewSet):
    queryset = models.TipoCalificacion.objects.all()
    serializer_class = serializers.TipoCalificacionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo', 'descripcion']
    ordering_fields = ['fecha_creacion', 'codigo']
