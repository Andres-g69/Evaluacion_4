from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils.dateparse import parse_date

from api import models
from api.serializers import CalificacionTributariaSerializer

try:
    from api.utils.kafka_producer import publish as kafka_publish
except Exception:
    kafka_publish = None

class CalificacionTributariaViewSet(viewsets.ModelViewSet):
    queryset = models.CalificacionTributaria.objects.select_related(
        'rut_contribuyente', 'codigo_tipo_calificacion'
    ).all().order_by('-fecha_creacion')
    serializer_class = CalificacionTributariaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id_calificacion', 'rut_contribuyente__rut', 'rut_contribuyente__razon_social']
    ordering_fields = ['fecha_calificacion', 'monto_anual', 'fecha_creacion']

    def perform_create(self, serializer):
        obj = serializer.save(
            usuario_creacion=self.request.user.username if self.request.user and self.request.user.is_authenticated else 'anonymous',
            usuario_actualizacion=self.request.user.username if self.request.user and self.request.user.is_authenticated else 'anonymous'
        )
        # publish event to kafka if available
        if kafka_publish:
            try:
                kafka_publish('calificaciones', {
                    'evento': 'calificacion_creada',
                    'id': obj.id_calificacion,
                    'rut': obj.rut_contribuyente_id,
                    'estado': obj.estado
                })
            except Exception:
                pass

    def perform_update(self, serializer):
        obj = serializer.save(
            usuario_actualizacion=self.request.user.username if self.request.user and self.request.user.is_authenticated else 'anonymous'
        )
        if kafka_publish:
            try:
                kafka_publish('calificaciones', {
                    'evento': 'calificacion_actualizada',
                    'id': obj.id_calificacion,
                    'rut': obj.rut_contribuyente_id,
                    'estado': obj.estado
                })
            except Exception:
                pass

    def perform_destroy(self, instance):
        data = {
            'evento': 'calificacion_eliminada',
            'id': instance.id_calificacion,
            'rut': instance.rut_contribuyente_id
        }
        if kafka_publish:
            try:
                kafka_publish('calificaciones', data)
            except Exception:
                pass
        instance.delete()

class CalificacionSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        qs = models.CalificacionTributaria.objects.select_related('rut_contribuyente', 'codigo_tipo_calificacion').all()

        rut = request.GET.get('rut')
        tipo = request.GET.get('tipo')
        estado = request.GET.get('estado')
        fecha_from = request.GET.get('fecha_from')
        fecha_to = request.GET.get('fecha_to')

        if rut:
            qs = qs.filter(
                Q(rut_contribuyente__rut__icontains=rut) |
                Q(rut_contribuyente__razon_social__icontains=rut)
            )

        if tipo:
            qs = qs.filter(codigo_tipo_calificacion__codigo=tipo)

        if estado:
            qs = qs.filter(estado__iexact=estado)

        if fecha_from:
            d1 = parse_date(fecha_from)
            if d1:
                qs = qs.filter(fecha_calificacion__gte=d1)

        if fecha_to:
            d2 = parse_date(fecha_to)
            if d2:
                qs = qs.filter(fecha_calificacion__lte=d2)

        qs = qs.order_by('-fecha_calificacion')

        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 20))
        except Exception:
            page = 1
            page_size = 20

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]

        serializer = CalificacionTributariaSerializer(page_qs, many=True, context={'request': request})
        resp = {
            'count': total,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        }

        return Response(resp, status=status.HTTP_200_OK)
