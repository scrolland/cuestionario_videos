#!/usr/bin/env python3
"""
Script para verificar que el sistema esté configurado correctamente
Ejecuta: python verificar_sistema.py
"""

from pathlib import Path
import sys

def verificar_sistema():
    """Verifica que todo esté listo para el experimento"""

    print("\n" + "="*70)
    print("  VERIFICACIÓN DEL SISTEMA DE CUESTIONARIO")
    print("="*70 + "\n")

    todo_ok = True

    # 1. Verificar carpeta VIDEOS
    print("[1] Verificando carpeta VIDEOS...")
    videos_dir = Path('VIDEOS')
    if not videos_dir.exists():
        print("   [X] ERROR: No se encontro la carpeta VIDEOS/")
        todo_ok = False
    else:
        print("   [OK] Carpeta VIDEOS encontrada")

        # Verificar carpeta reales
        reales_dir = videos_dir / 'reales'
        if not reales_dir.exists():
            print("   [X] ERROR: No se encontro VIDEOS/reales/")
            todo_ok = False
        else:
            reales_videos = list(reales_dir.glob('*.mp4'))
            print(f"   [OK] Carpeta reales: {len(reales_videos)} videos")

        # Verificar carpetas evidentes
        evidentes = ['e2', 'e9', 'e11']
        for carpeta in evidentes:
            evidente_dir = videos_dir / carpeta
            if not evidente_dir.exists():
                print(f"   [!] ADVERTENCIA: No se encontro carpeta evidente {carpeta}/")
            else:
                videos = list(evidente_dir.glob('video_*.mp4'))
                print(f"   [OK] Carpeta {carpeta}: {len(videos)} videos")

        # Contar carpetas e* e i*
        carpetas_e = [d for d in videos_dir.iterdir() if d.is_dir() and d.name.startswith('e') and d.name != 'e2' and d.name != 'e9' and d.name != 'e11']
        carpetas_i = [d for d in videos_dir.iterdir() if d.is_dir() and d.name.startswith('i')]

        print(f"   [OK] Carpetas entretenimiento (e*): {len(carpetas_e)}")
        print(f"   [OK] Carpetas informativo (i*): {len(carpetas_i)}")

        # Verificar que tengan video_high y video_low
        total_videos_ia = 0
        for carpeta in carpetas_e + carpetas_i:
            high = (carpeta / 'video_high_quality.mp4').exists()
            low = (carpeta / 'video_low_quality.mp4').exists()
            if high and low:
                total_videos_ia += 2
            elif high or low:
                print(f"   [!] ADVERTENCIA: {carpeta.name}/ solo tiene un video")
                total_videos_ia += 1

        print(f"   [OK] Total videos IA disponibles: {total_videos_ia}")

    # 2. Verificar archivos del sistema
    print(f"\n[2] Verificando archivos del sistema...")
    archivos_requeridos = [
        'server.py',
        'cuestionario.html',
        'export_to_excel.py',
        'analizar_resultados.py'
    ]

    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"   [OK] {archivo}")
        else:
            print(f"   [X] ERROR: No se encontro {archivo}")
            todo_ok = False

    # 3. Verificar carpeta de datos
    print(f"\n[3] Verificando carpeta de datos...")
    data_dir = Path('experiment_data')
    if not data_dir.exists():
        print("   [i] Creando carpeta experiment_data/...")
        data_dir.mkdir(exist_ok=True)
        print("   [OK] Carpeta experiment_data/ creada")
    else:
        participantes = list(data_dir.glob('P*.json'))
        print(f"   [OK] Carpeta experiment_data/ existe")
        if participantes:
            print(f"   [i] Hay {len(participantes)} participantes previos")

    # 4. Verificar módulos Python
    print(f"\n[4] Verificando modulos Python...")
    modulos = {
        'json': 'json',
        'pathlib': 'pathlib',
        'csv': 'csv',
        'datetime': 'datetime'
    }

    for modulo, import_name in modulos.items():
        try:
            __import__(import_name)
            print(f"   [OK] {modulo}")
        except ImportError:
            print(f"   [X] ERROR: Modulo {modulo} no disponible")
            todo_ok = False

    # 5. Resumen final
    print("\n" + "="*70)
    if todo_ok:
        print("  [OK] SISTEMA LISTO PARA USAR")
        print("="*70)
        print("\n  Para iniciar el cuestionario:")
        print("  1. Ejecuta: python server.py")
        print("  2. Abre: http://localhost:8000/cuestionario.html")
        print("\n  O simplemente ejecuta: INICIAR-CUESTIONARIO.bat")
    else:
        print("  [X] HAY PROBLEMAS QUE RESOLVER")
        print("="*70)
        print("\n  Revisa los errores marcados arriba antes de continuar")

    print("="*70 + "\n")

    return 0 if todo_ok else 1

if __name__ == '__main__':
    sys.exit(verificar_sistema())
