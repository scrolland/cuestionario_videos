#!/usr/bin/env python3
"""
Script para analizar resultados del experimento
Ejecuta: python analizar_resultados.py
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

DATA_DIR = Path('experiment_data')

def analizar_resultados():
    """Analiza y muestra estadísticas de los resultados"""

    if not DATA_DIR.exists():
        print(f"ERROR: No se encontró la carpeta {DATA_DIR}")
        return

    participant_files = list(DATA_DIR.glob('P*.json'))

    if not participant_files:
        print(f"No se encontraron participantes en {DATA_DIR}")
        return

    # Estadísticas globales
    total_participantes = len(participant_files)
    completados = 0
    total_respuestas = 0

    # Por tipo de video
    respuestas_fake = []
    respuestas_real = []
    respuestas_evidentes = []

    # Causas fake
    causas_counter = Counter()

    # Tiempos de respuesta
    tiempos = []

    # Demografía
    generos = Counter()
    edades = []

    print("\n" + "="*70)
    print("  ANÁLISIS DE RESULTADOS DEL EXPERIMENTO")
    print("="*70)

    # Procesar cada participante
    for participant_file in participant_files:
        with open(participant_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if data.get('completado', False):
            completados += 1

        generos[data['genero']] += 1
        edades.append(data['edad'])

        for respuesta in data.get('respuestas', []):
            total_respuestas += 1

            # Clasificar por tipo
            if respuesta.get('es_evidente', False):
                respuestas_evidentes.append(respuesta['respuesta_slider'])
            elif respuesta.get('es_fake', False):
                respuestas_fake.append(respuesta['respuesta_slider'])
            else:
                respuestas_real.append(respuesta['respuesta_slider'])

            # Causas
            if respuesta.get('causa_fake'):
                causas_counter[respuesta['causa_fake']] += 1

            # Tiempos
            tiempos.append(respuesta.get('tiempo_respuesta_segundos', 0))

    # Mostrar resultados
    print(f"\n📊 RESUMEN GENERAL")
    print(f"  Total de participantes: {total_participantes}")
    print(f"  Participantes que completaron: {completados} ({completados/total_participantes*100:.1f}%)")
    print(f"  Total de respuestas: {total_respuestas}")

    print(f"\n👥 DEMOGRAFÍA")
    print(f"  Edad promedio: {sum(edades)/len(edades):.1f} años")
    print(f"  Edad mínima: {min(edades)} años")
    print(f"  Edad máxima: {max(edades)} años")
    print(f"  Distribución por género:")
    for genero, count in generos.items():
        print(f"    - {genero}: {count} ({count/total_participantes*100:.1f}%)")

    print(f"\n🎬 VALORACIONES PROMEDIO (Escala 1-10)")
    print(f"  Videos evidentes (fake obvio): {sum(respuestas_evidentes)/len(respuestas_evidentes):.2f}" if respuestas_evidentes else "  Videos evidentes: N/A")
    print(f"  Videos fake (no evidentes): {sum(respuestas_fake)/len(respuestas_fake):.2f}" if respuestas_fake else "  Videos fake: N/A")
    print(f"  Videos reales: {sum(respuestas_real)/len(respuestas_real):.2f}" if respuestas_real else "  Videos reales: N/A")

    # Tasa de detección
    if respuestas_fake:
        fake_detectados = sum(1 for r in respuestas_fake if r >= 6)
        print(f"\n🎯 TASA DE DETECCIÓN")
        print(f"  Videos fake detectados (slider ≥ 6): {fake_detectados}/{len(respuestas_fake)} ({fake_detectados/len(respuestas_fake)*100:.1f}%)")

    if respuestas_real:
        real_correctos = sum(1 for r in respuestas_real if r <= 5)
        print(f"  Videos reales correctos (slider ≤ 5): {real_correctos}/{len(respuestas_real)} ({real_correctos/len(respuestas_real)*100:.1f}%)")

    print(f"\n⏱️  TIEMPOS DE RESPUESTA")
    print(f"  Promedio: {sum(tiempos)/len(tiempos):.1f} segundos")
    print(f"  Mínimo: {min(tiempos)} segundos")
    print(f"  Máximo: {max(tiempos)} segundos")

    if causas_counter:
        print(f"\n🔍 CAUSAS MÁS COMUNES PARA DETECTAR FAKE (Top 10)")
        for causa, count in causas_counter.most_common(10):
            # Convertir código a texto legible
            causa_texto = causa.replace('_', ' ').title()
            print(f"  {count:3d}x  {causa_texto}")

    print("\n" + "="*70)
    print("  Para análisis detallado, exporta los datos a Excel")
    print("  Ejecuta: python export_to_excel.py")
    print("="*70 + "\n")

if __name__ == '__main__':
    analizar_resultados()
