# services/ingestion/consumer.py
import os
import django
import json
import traceback
from confluent_kafka import Consumer, KafkaError
import pandas as pd
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nuamproject.settings")
django.setup()

from api import models
from api.serializers import CalificacionTributariaSerializer

KAFKA = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
    'group.id': 'ingestion-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(KAFKA)
consumer.subscribe(['cargas'])

print("Ingestion consumer started, listening to 'cargas'...")

def parse_bool(val):
    if val is None: return False
    if isinstance(val, bool): return val
    s = str(val).strip().lower()
    return s in ['1','true','yes','si','sí']

def parse_date(val):
    if not val: return None
    if isinstance(val, (datetime,)):
        return val.date().isoformat()
    try:
        # pandas can parse many formats
        return pd.to_datetime(val).date().isoformat()
    except Exception:
        return None

def process_carga(carga: models.CargaArchivo):
    carga.estado = 'EN_PROCESO'
    carga.detalle_error = ''
    carga.procesados = 0
    carga.rechazados = 0
    carga.save()

    path = carga.file_path()
    if not path or not os.path.exists(path):
        carga.estado = 'ERROR'
        carga.detalle_error = 'Archivo no encontrado en filesystem'
        carga.save()
        return

    try:
        # detect extension
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.xls', '.xlsx']:
            df = pd.read_excel(path, dtype=str)
        else:
            # CSV
            df = pd.read_csv(path, dtype=str)

        # normalize column names: lower, strip
        df.columns = [c.strip() for c in df.columns]

        # expected columns mapping: try to be flexible
        # prefer exact names used by serializer: rut_contribuyente_id, codigo_tipo_calificacion_id, fecha_calificacion, monto_anual, periodo, estado, observaciones, fecha_vencimiento, vigente, usuario_creacion
        required = ['rut_contribuyente_id','codigo_tipo_calificacion_id','fecha_calificacion','monto_anual','periodo']
        processed = 0
        rejected = 0

        for idx, row in df.iterrows():
            # build payload
            payload = {}
            try:
                # get values with fallback to common names
                def getcol(name, alt=[]):
                    for key in [name] + alt:
                        if key in row and pd.notna(row[key]):
                            return str(row[key]).strip()
                    return None

                rut = getcol('rut_contribuyente_id', ['rut','RUT','rut_contribuyente'])
                tipo = getcol('codigo_tipo_calificacion_id', ['tipo','codigo_tipo_calificacion','tipo_codigo'])
                fecha = getcol('fecha_calificacion', ['fecha','fecha_calificacion'])
                monto = getcol('monto_anual', ['monto','monto_anual'])
                periodo = getcol('periodo', ['periodo','anio','año'])
                estado = getcol('estado', ['estado'])
                observ = getcol('observaciones', ['observaciones','observacion','obs'])
                fecha_venc = getcol('fecha_vencimiento', ['fecha_vencimiento','vencimiento'])
                vigente = getcol('vigente', ['vigente','activo'])
                usuario = getcol('usuario_creacion', ['usuario','usuario_creacion','usuario_sistema'])

                # basic required check
                if not (rut and tipo and fecha and monto and periodo):
                    raise ValueError("Faltan campos requeridos")

                payload['rut_contribuyente_id'] = rut
                payload['codigo_tipo_calificacion_id'] = tipo
                payload['fecha_calificacion'] = parse_date(fecha) or fecha
                payload['monto_anual'] = float(str(monto).replace(',', '').strip())
                payload['periodo'] = int(float(periodo))
                if estado: payload['estado'] = estado
                if observ: payload['observaciones'] = observ
                if fecha_venc: payload['fecha_vencimiento'] = parse_date(fecha_venc) or fecha_venc
                if vigente is not None: payload['vigente'] = parse_bool(vigente)
                payload['usuario_creacion'] = usuario or carga.usuario or 'system'

                # validate & create through serializer (ensures DB constraints)
                ser = CalificacionTributariaSerializer(data=payload)
                if ser.is_valid():
                    ser.save()
                    processed += 1
                else:
                    rejected += 1
                    # optionally log ser.errors somewhere (Auditoria or LogError)
                    print("Validation error row", idx, ser.errors)
            except Exception as e:
                rejected += 1
                print("Row processing error:", str(e))
                print(traceback.format_exc())

        carga.procesados = processed
        carga.rechazados = rejected
        carga.estado = 'COMPLETADO' if rejected == 0 else 'ERROR' if processed==0 else 'COMPLETADO'
        carga.save()

    except Exception as e:
        carga.estado = 'ERROR'
        carga.detalle_error = str(e) + "\n" + traceback.format_exc()
        carga.save()
        print("Error processing carga:", e)

def consume_loop():
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print("Kafka error:", msg.error())
                continue
            data = json.loads(msg.value().decode('utf-8'))
            carga_id = data.get('carga_id')
            if not carga_id:
                continue
            try:
                carga = models.CargaArchivo.objects.get(pk=carga_id)
            except models.CargaArchivo.DoesNotExist:
                print("Carga no existe:", carga_id)
                continue
            print("Procesando carga:", carga_id)
            process_carga(carga)
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_loop()
