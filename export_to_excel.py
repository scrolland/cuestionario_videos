#!/usr/bin/env python3
"""
Script para exportar datos del experimento a formato CSV (compatible con Excel)
Ejecuta: python export_to_excel.py
"""

import json
import csv
from pathlib import Path
from datetime import datetime

DATA_DIR = Path('experiment_data')
OUTPUT_FILE = f'resultados_experimento_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def export_to_csv():
    """Export all participant data to CSV"""

    if not DATA_DIR.exists():
        print(f"ERROR: No se encontró la carpeta {DATA_DIR}")
        return

    # Obtener todos los archivos JSON de participantes
    participant_files = list(DATA_DIR.glob('P*.json'))

    if not participant_files:
        print(f"No se encontraron participantes en {DATA_DIR}")
        return

    print(f"\nEncontrados {len(participant_files)} participantes")
    print(f"Exportando a: {OUTPUT_FILE}\n")

    # Abrir archivo CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = [
            'participante_id',
            'genero',
            'edad',
            'fecha_inicio_experimento',
            'fecha_finalizacion_experimento',
            'completado',
            'fecha_hora_respuesta',
            'numero_video',
            'video_path',
            'tipo_contenido',
            'es_fake',
            'es_evidente',
            'calidad',
            'respuesta_slider',
            'causa_fake',
            'tiempo_respuesta_segundos'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        total_respuestas = 0

        # Procesar cada participante
        for participant_file in sorted(participant_files):
            try:
                with open(participant_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                participante_id = data['id']
                genero = data['genero']
                edad = data['edad']
                fecha_inicio = data['fecha_inicio']
                fecha_fin = data.get('fecha_finalizacion', '')
                completado = data.get('completado', False)

                # Escribir una fila por cada respuesta
                for respuesta in data.get('respuestas', []):
                    row = {
                        'participante_id': participante_id,
                        'genero': genero,
                        'edad': edad,
                        'fecha_inicio_experimento': fecha_inicio,
                        'fecha_finalizacion_experimento': fecha_fin,
                        'completado': 'Sí' if completado else 'No',
                        'fecha_hora_respuesta': respuesta.get('fecha_hora', ''),
                        'numero_video': respuesta.get('numero_video', ''),
                        'video_path': respuesta.get('video_path', ''),
                        'tipo_contenido': respuesta.get('tipo_contenido', ''),
                        'es_fake': 'Sí' if respuesta.get('es_fake', False) else 'No',
                        'es_evidente': 'Sí' if respuesta.get('es_evidente', False) else 'No',
                        'calidad': respuesta.get('calidad', ''),
                        'respuesta_slider': respuesta.get('respuesta_slider', ''),
                        'causa_fake': respuesta.get('causa_fake', ''),
                        'tiempo_respuesta_segundos': respuesta.get('tiempo_respuesta_segundos', 0)
                    }
                    writer.writerow(row)
                    total_respuestas += 1

                print(f"✓ {participante_id}: {len(data.get('respuestas', []))} respuestas")

            except Exception as e:
                print(f"✗ Error procesando {participant_file.name}: {e}")

    print(f"\n{'='*60}")
    print(f"EXPORTACIÓN COMPLETADA")
    print(f"{'='*60}")
    print(f"Archivo generado: {OUTPUT_FILE}")
    print(f"Total participantes: {len(participant_files)}")
    print(f"Total respuestas: {total_respuestas}")
    print(f"\nPuedes abrir este archivo con Microsoft Excel o Google Sheets")

if __name__ == '__main__':
    export_to_csv()
