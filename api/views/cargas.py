# api/views/cargas.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from api.serializers import CargaArchivoSerializer
from api import models
from api.utils.kafka_producer import publish
from django.conf import settings

class CargaCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        f = request.FILES.get('archivo')
        tipo = request.data.get('tipo', 'CALIFICACIONES')
        if not f:
            return Response({'error': 'Archivo requerido'}, status=status.HTTP_400_BAD_REQUEST)

        carga = models.CargaArchivo.objects.create(
            archivo=f,
            nombre_original=getattr(f, 'name', ''),
            tipo=tipo,
            usuario=request.user.username if request.user and request.user.is_authenticated else request.data.get('usuario', '')
        )

        # publish to kafka
        publish('cargas', {'carga_id': carga.id})

        serializer = CargaArchivoSerializer(carga)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CargaListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CargaArchivoSerializer
    queryset = models.CargaArchivo.objects.all().order_by('-fecha_carga')

class CargaDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        carga = get_object_or_404(models.CargaArchivo, pk=pk)
        # servir el archivo usando Django sendfile o Url de media
        from django.http import FileResponse, Http404
        path = carga.file_path()
        try:
            return FileResponse(open(path, 'rb'), as_attachment=True, filename=carga.nombre_original or 'archivo')
        except Exception:
            raise Http404

class CargaDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, format=None):
        carga = get_object_or_404(models.CargaArchivo, pk=pk)
        carga.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
