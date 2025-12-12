# api/serializers.py
from rest_framework import serializers
from . import models
from api.models import CargaArchivo

class CargaArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaArchivo
        fields = "__all__"


class TipoCalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoCalificacion
        fields = '__all__'
        read_only_fields = ('fecha_creacion',)

class ContribuyenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contribuyente
        fields = [
            'rut', 'razon_social', 'direccion', 'telefono', 'email',
            'fecha_inscripcion', 'tipo_contribuyente', 'activo',
            'fecha_creacion', 'fecha_actualizacion',
            'usuario_creacion', 'usuario_actualizacion'
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion')

class CalificacionTributariaSerializer(serializers.ModelSerializer):
    rut_contribuyente = ContribuyenteSerializer(read_only=True)
    rut_contribuyente_id = serializers.CharField(write_only=True, required=True)

    codigo_tipo_calificacion = TipoCalificacionSerializer(read_only=True)
    codigo_tipo_calificacion_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.CalificacionTributaria
        fields = [
            'id_calificacion',
            'rut_contribuyente', 'rut_contribuyente_id',
            'codigo_tipo_calificacion', 'codigo_tipo_calificacion_id',
            'fecha_calificacion', 'monto_anual', 'periodo',
            'estado', 'observaciones', 'fecha_vencimiento', 'vigente',
            'fecha_creacion', 'fecha_actualizacion',
            'usuario_creacion', 'usuario_actualizacion'
        ]
        read_only_fields = ('id_calificacion', 'fecha_creacion', 'fecha_actualizacion')

    def create(self, validated_data):
        rut = validated_data.pop('rut_contribuyente_id')
        tipo = validated_data.pop('codigo_tipo_calificacion_id')
        contrib = models.Contribuyente.objects.get(pk=rut)
        tipo_obj = models.TipoCalificacion.objects.get(pk=tipo)
        cal = models.CalificacionTributaria.objects.create(
            rut_contribuyente=contrib,
            codigo_tipo_calificacion=tipo_obj,
            **validated_data
        )
        return cal

    def update(self, instance, validated_data):
        rut = validated_data.pop('rut_contribuyente_id', None)
        tipo = validated_data.pop('codigo_tipo_calificacion_id', None)
        if rut:
            instance.rut_contribuyente = models.Contribuyente.objects.get(pk=rut)
        if tipo:
            instance.codigo_tipo_calificacion = models.TipoCalificacion.objects.get(pk=tipo)
        return super().update(instance, validated_data)

class DocumentoTributarioSerializer(serializers.ModelSerializer):
    rut_contribuyente = ContribuyenteSerializer(read_only=True)
    rut_contribuyente_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.DocumentoTributario
        fields = '__all__'
        read_only_fields = ('id_documento', 'fecha_creacion', 'fecha_actualizacion')

    def create(self, validated_data):
        rut = validated_data.pop('rut_contribuyente_id')
        contrib = models.Contribuyente.objects.get(pk=rut)
        return models.DocumentoTributario.objects.create(rut_contribuyente=contrib, **validated_data)

class PoblacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Poblacion
        fields = '__all__'
