#!/usr/bin/env python3
"""
Simple HTTP server with file upload support for Runway ML video generation
"""

import http.server
import socketserver
import json
import base64
import os
import time
import urllib.request
import urllib.parse
from pathlib import Path
from io import BytesIO
import re
from datetime import datetime
import glob
import random
from image_analyzer import generate_prompts_for_experiment

PORT = 8000
RUNWAY_API_KEY = 'key_657eb6a1e66411ca3e285d1b2a9ccebc5e329abcdaa3f77a68d702fc1f6236652d8b2ccc1553f839924ea5e5f80b012d04cbbd4ece748ae6bd501e897a0ee133'
RUNWAY_API_BASE = 'https://api.dev.runwayml.com/v1'
DATA_DIR = Path('experiment_data')

class RunwayHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get-stats':
            self.handle_get_stats()
        elif self.path == '/export-csv':
            self.handle_export_csv()
        elif self.path == '/export-json':
            self.handle_export_json()
        else:
            # Default behavior for all other GET requests
            super().do_GET()

    def do_POST(self):
        if self.path == '/generate-from-local-image':
            self.handle_video_generation()
        elif self.path == '/init-experiment.php' or self.path == '/init-experiment':
            self.handle_init_experiment()
        elif self.path == '/save-response.php' or self.path == '/save-response':
            self.handle_save_response()
        elif self.path == '/finish-experiment.php' or self.path == '/finish-experiment':
            self.handle_finish_experiment()
        else:
            self.send_error(404, "Not Found")

    def parse_multipart(self, body, boundary):
        """Simple multipart/form-data parser for Python 3.13+"""
        parts = {}
        boundary = boundary.encode() if isinstance(boundary, str) else boundary

        # Split by boundary
        sections = body.split(b'--' + boundary)

        for section in sections:
            if not section or section == b'--\r\n' or section == b'--':
                continue

            # Find headers end
            header_end = section.find(b'\r\n\r\n')
            if header_end == -1:
                continue

            headers = section[:header_end].decode('utf-8', errors='ignore')
            content = section[header_end + 4:]

            # Remove trailing \r\n
            if content.endswith(b'\r\n'):
                content = content[:-2]

            # Extract field name
            name_match = re.search(r'name="([^"]+)"', headers)
            if not name_match:
                continue

            field_name = name_match.group(1)

            # Check if it's a file
            if 'filename=' in headers:
                parts[field_name] = content
            else:
                # Text field
                parts[field_name] = content.decode('utf-8', errors='ignore')

        return parts

    def handle_video_generation(self):
        try:
            # Parse multipart form data
            content_type = self.headers['Content-Type']

            if 'multipart/form-data' not in content_type:
                self.send_json_response({'success': False, 'message': 'Invalid content type'}, 400)
                return

            # Get boundary
            boundary_match = re.search(r'boundary=(.+)', content_type)
            if not boundary_match:
                self.send_json_response({'success': False, 'message': 'No boundary found'}, 400)
                return

            boundary = boundary_match.group(1).strip()

            # Read body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            # Parse multipart data
            parts = self.parse_multipart(body, boundary)

            # Get image data
            if 'image' not in parts:
                self.send_json_response({'success': False, 'message': 'No image received'}, 400)
                return

            image_data = parts['image']
            if isinstance(image_data, str):
                image_data = image_data.encode('latin1')

            # Get other fields
            folder_path = parts.get('folderPath', '')
            prompt_text = parts.get('promptText', '')

            if not image_data:
                self.send_json_response({'success': False, 'message': 'Empty image data'}, 400)
                return

            # Detect image type FIRST (before processing)
            if image_data.startswith(b'\xff\xd8\xff'):
                original_format = 'JPEG'
                mime_type = 'image/jpg'
            elif image_data.startswith(b'\x89PNG'):
                original_format = 'PNG'
                mime_type = 'image/png'
            elif image_data.startswith(b'GIF'):
                original_format = 'GIF'
                mime_type = 'image/gif'
            else:
                original_format = 'JPEG'
                mime_type = 'image/jpg'

            # Check and fix image aspect ratio
            # Runway ML requires width/height ratio <= 2.0
            from PIL import Image
            from io import BytesIO

            img = Image.open(BytesIO(image_data))
            width, height = img.size
            aspect_ratio = width / height

            print(f"==> Image original: {width}x{height} (ratio: {aspect_ratio:.3f})")

            # If aspect ratio is too wide, crop or resize
            if aspect_ratio > 2.0:
                # Resize to max 2:1 ratio
                new_width = int(height * 2.0)
                # Crop from center
                left = (width - new_width) // 2
                img = img.crop((left, 0, left + new_width, height))
                width, height = img.size
                aspect_ratio = width / height
                print(f"==> Image adjusted: {width}x{height} (ratio: {aspect_ratio:.3f})")

                # Convert back to bytes
                buffer = BytesIO()
                img.save(buffer, format=original_format, quality=95)
                image_data = buffer.getvalue()

            # Check image size (must be <3.3MB to fit in 5MB after base64 encoding)
            image_size_mb = len(image_data) / (1024 * 1024)
            if image_size_mb > 3.3:
                self.send_json_response({
                    'success': False,
                    'message': f'Image too large: {image_size_mb:.2f}MB. Must be less than 3.3MB (becomes 5MB after encoding)',
                    'suggestion': 'Please resize or compress the image before uploading'
                }, 400)
                return

            # Convert image to base64 data URI
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            # Format: data:content/type;base64,{encoded_data}
            image_data_uri = f"data:{mime_type};base64,{image_base64}"

            # IMPORTANTE: Detectar tipo de video desde el nombre de carpeta
            # Formato esperado: cualquier cosa con 'e' o 'i' en el nombre
            video_type = 'e'  # default: entretenimiento
            if folder_path:
                folder_lower = folder_path.lower()
                if 'informativ' in folder_lower or '_i' in folder_lower or folder_lower.endswith('i'):
                    video_type = 'i'

            # Analizar imagen y generar prompts inteligentes
            print(f"\n==> Analizando imagen...")
            prompt_data = generate_prompts_for_experiment(
                image_data,
                video_type,
                prompt_text if prompt_text else None
            )

            print(f"==> Análisis de imagen:")
            print(f"    Tipo: {prompt_data['video_type']}")
            print(f"    Brillo: {prompt_data['analysis']['brightness']}")
            print(f"    Composición: {prompt_data['analysis']['composition']}")
            print(f"    Temperatura: {prompt_data['analysis']['color_temperature']}")

            print(f"\n==> Generando videos...")
            print(f"    Folder: {folder_path}")
            print(f"    Image size: {len(image_data)} bytes")

            # Generate videos with differentiated prompts
            result = self.generate_videos(
                image_data_uri,
                prompt_data['prompts'],
                folder_path,
                prompt_data['analysis']
            )

            if result['success']:
                print(f"==> Success! Videos generated")
                self.send_json_response(result, 200)
            else:
                print(f"==> Error: {result.get('message', 'Unknown error')}")
                self.send_json_response(result, 500)

        except Exception as e:
            print(f"\n==> ERROR in handle_video_generation:")
            print(f"    {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({
                'success': False,
                'message': f'Server error: {str(e)}',
                'error_type': type(e).__name__
            }, 500)

    def generate_videos(self, image_data_uri, prompts_dict, folder_path, image_analysis):
        """
        Generate both high and low quality videos with different prompts

        Args:
            image_data_uri: Base64 encoded image
            prompts_dict: dict with 'high_quality' and 'low_quality' prompts
            folder_path: Destination folder
            image_analysis: Image analysis results
        """

        # Configuración que funcionaba:
        # Gen-4 Turbo para ALTA calidad (mejor calidad)
        # Gen-3 Alpha Turbo para BAJA calidad (ahorro de créditos)

        quality_configs = {
            'high': {
                'duration': 10,
                'model': 'gen4_turbo',  # VOLVIENDO a Gen-4 para alta calidad
                'ratio': '1280:720',  # Gen-4 acepta este ratio
                'target_size_mb': 10,
                'bitrate': '4000k',  # High bitrate
                'label': 'Alta',
                'fileName': 'video_high_quality.mp4',
                'prompt': prompts_dict['high_quality'],
                'compress': False  # No comprimir
            },
            'low': {
                'duration': 10,
                'model': 'gen3a_turbo',  # Gen-3 para baja calidad (ahorra créditos)
                'ratio': '1280:768',  # Gen-3 solo acepta 1280:768 o 768:1280
                'target_size_mb': 2,
                'bitrate': '600k',  # Low bitrate
                'label': 'Baja',
                'fileName': 'video_low_quality.mp4',
                'prompt': prompts_dict['low_quality'],
                'compress': True  # Comprimir agresivamente
            }
        }

        # COSTE TOTAL: 50 + 20 = 70 créditos
        # Para tu experimento: 4 imágenes × 70 = 280 créditos

        video_task_ids = {}

        # Create both video generation tasks with DIFFERENT PROMPTS
        for quality, config in quality_configs.items():
            # Request data for gen4_turbo with quality-specific prompt
            request_data = {
                'promptImage': image_data_uri,
                'promptText': config['prompt'],  # Different prompt per quality!
                'model': config['model'],
                'duration': config['duration'],
                'ratio': config['ratio']  # Required for gen4_turbo
            }

            print(f"\n==> Creating {quality} quality video task...")
            print(f"    Model: {config['model']}")
            print(f"    Duration: {config['duration']}s")
            print(f"    Ratio: {config['ratio']}")
            print(f"    Prompt: {config['prompt'][:80]}...")

            req = urllib.request.Request(
                f"{RUNWAY_API_BASE}/image_to_video",
                data=json.dumps(request_data).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {RUNWAY_API_KEY}',
                    'X-Runway-Version': '2024-11-06'
                }
            )

            try:
                with urllib.request.urlopen(req) as response:
                    response_data = json.loads(response.read().decode('utf-8'))
                    task_id = response_data.get('id')

                    if not task_id:
                        print(f"==> ERROR: No task ID in response")
                        print(f"    Response: {response_data}")
                        return {
                            'success': False,
                            'message': f'No task ID received for {quality} quality',
                            'response': response_data
                        }

                    print(f"==> Task created: {task_id}")
                    video_task_ids[quality] = {
                        'taskId': task_id,
                        'config': config
                    }
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                print(f"\n==> API ERROR (HTTP {e.code}):")
                print(f"    {error_body}")
                try:
                    error_json = json.loads(error_body)
                    return {
                        'success': False,
                        'message': f'API error for {quality} quality (HTTP {e.code})',
                        'details': error_json
                    }
                except:
                    return {
                        'success': False,
                        'message': f'API error for {quality} quality (HTTP {e.code})',
                        'details': error_body
                    }

        # Poll for both videos to complete
        max_attempts = 48  # 4 minutes
        attempt = 0
        completed_videos = {}

        while attempt < max_attempts and len(completed_videos) < 2:
            time.sleep(5)

            for quality, task_info in video_task_ids.items():
                if quality in completed_videos:
                    continue

                req = urllib.request.Request(
                    f"{RUNWAY_API_BASE}/tasks/{task_info['taskId']}",
                    headers={
                        'Authorization': f'Bearer {RUNWAY_API_KEY}',
                        'X-Runway-Version': '2024-11-06'
                    }
                )

                try:
                    with urllib.request.urlopen(req) as response:
                        status_data = json.loads(response.read().decode('utf-8'))

                        if status_data.get('status') == 'SUCCEEDED':
                            video_url = (status_data.get('output') or [None])[0] or \
                                       (status_data.get('artifacts') or [{}])[0].get('url')
                            if video_url:
                                completed_videos[quality] = {
                                    'url': video_url,
                                    'config': task_info['config']
                                }
                        elif status_data.get('status') == 'FAILED':
                            return {
                                'success': False,
                                'message': f'Video generation failed for {quality} quality',
                                'details': status_data
                            }
                except Exception as e:
                    print(f"Error checking status: {e}")

            attempt += 1

        if len(completed_videos) < 2:
            return {
                'success': False,
                'message': f'Timeout generating videos (completed: {len(completed_videos)}/2)'
            }

        # Download and save videos
        base_path = Path('VIDEOS') / folder_path
        base_path.mkdir(parents=True, exist_ok=True)

        results = {}

        for quality, video_info in completed_videos.items():
            config = video_info['config']
            video_url = video_info['url']

            # Download video
            with urllib.request.urlopen(video_url) as response:
                video_content = response.read()

            # Save video
            file_name = config['fileName']
            file_path = base_path / file_name

            with open(file_path, 'wb') as f:
                f.write(video_content)

                    # Get file size
            file_size_mb = file_path.stat().st_size / (1024 * 1024)

            # Aplicar compresión adicional si es necesario
            if config.get('compress', False) or file_size_mb > config['target_size_mb'] * 1.2:
                compressed_path = base_path / 'temp_compressed.mp4'
                bitrate = config['bitrate']

                # Comando ffmpeg para compresión
                cmd = f'ffmpeg -i "{file_path}" -b:v {bitrate} -maxrate {bitrate} -bufsize 1M -y "{compressed_path}"'

                try:
                    import subprocess
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                    if result.returncode == 0 and compressed_path.exists():
                        # Reemplazar con versión comprimida
                        file_path.unlink()
                        compressed_path.rename(file_path)
                        file_size_mb = file_path.stat().st_size / (1024 * 1024)
                        print(f"==> Video comprimido a {file_size_mb:.2f} MB")
                except Exception as e:
                    print(f"==> Advertencia: No se pudo comprimir con ffmpeg: {e}")

            relative_path = f'VIDEOS/{folder_path}/{file_name}'

            results[quality] = {
                'fileName': file_name,
                'videoPath': relative_path,
                'fileSize': f'{file_size_mb:.2f} MB',
                'duration': config['duration'],
                'taskId': video_task_ids[quality]['taskId'],
                'label': config['label']
            }

        return {
            'success': True,
            'message': 'Ambos videos generados y guardados exitosamente',
            'folderPath': str(base_path),
            'imageUsed': 'uploaded_image',
            'videos': results
        }

    def handle_init_experiment(self):
        """Initialize experiment - create participant and select random videos"""
        try:
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            genero = data.get('genero', '')
            edad = data.get('edad', 0)

            if not genero or edad < 18:
                self.send_json_response({
                    'success': False,
                    'message': 'Datos demográficos inválidos'
                }, 400)
                return

            # Create data directory if not exists
            DATA_DIR.mkdir(exist_ok=True)

            # Generate participant ID
            timestamp = int(time.time() * 1000)
            participante_id = f"P{timestamp}"

            # Scan VIDEOS folder
            videos_folder = Path('VIDEOS')

            # Videos evidentes con IA (SIEMPRE se incluyen todos)
            evidentes_folders = ['e2', 'e9', 'e11']
            videos_evidentes = []

            # Videos IA entretenimiento (e1, e3, e4, etc. - excluyendo evidentes)
            videos_ia_entretenimiento = []

            # Videos IA informativos (i1, i2, i3, etc.)
            videos_ia_informativos = []

            # Videos reales de la carpeta 'reales'
            videos_reales_entretenimiento = []
            videos_reales_informativos = []

            if not videos_folder.exists():
                self.send_json_response({
                    'success': False,
                    'message': 'No se encontró la carpeta VIDEOS'
                }, 404)
                return

            # Escanear carpeta reales
            reales_folder = videos_folder / 'reales'
            if reales_folder.exists():
                for video_file in reales_folder.glob('*.mp4'):
                    # Determinar tipo por nombre: e*.mp4 o i*.mp4
                    if video_file.name.startswith('e'):
                        videos_reales_entretenimiento.append({
                            'path': str(video_file.as_posix()),
                            'es_fake': False,
                            'calidad': 'real',  # Los reales son todos misma calidad
                            'tipo_contenido': 'entretenimiento',
                            'es_evidente': False,
                            'folder': 'reales'
                        })
                    elif video_file.name.startswith('i'):
                        videos_reales_informativos.append({
                            'path': str(video_file.as_posix()),
                            'es_fake': False,
                            'calidad': 'real',
                            'tipo_contenido': 'informativo',
                            'es_evidente': False,
                            'folder': 'reales'
                        })

            # Escanear carpetas e* e i*
            for subfolder in videos_folder.iterdir():
                if not subfolder.is_dir() or subfolder.name == 'reales':
                    continue

                folder_name = subfolder.name

                # Carpetas evidentes
                if folder_name in evidentes_folders:
                    for video_file in subfolder.glob('video_*.mp4'):
                        calidad = 'alta' if 'high' in video_file.name else 'baja'
                        videos_evidentes.append({
                            'path': str(video_file.as_posix()),
                            'es_fake': True,
                            'calidad': calidad,
                            'tipo_contenido': 'entretenimiento',
                            'es_evidente': True,
                            'folder': folder_name
                        })

                # Carpetas entretenimiento (e*)
                elif folder_name.startswith('e'):
                    for video_file in subfolder.glob('video_*.mp4'):
                        calidad = 'alta' if 'high' in video_file.name else 'baja'
                        videos_ia_entretenimiento.append({
                            'path': str(video_file.as_posix()),
                            'es_fake': True,
                            'calidad': calidad,
                            'tipo_contenido': 'entretenimiento',
                            'es_evidente': False,
                            'folder': folder_name
                        })

                # Carpetas informativo (i*)
                elif folder_name.startswith('i'):
                    for video_file in subfolder.glob('video_*.mp4'):
                        calidad = 'alta' if 'high' in video_file.name else 'baja'
                        videos_ia_informativos.append({
                            'path': str(video_file.as_posix()),
                            'es_fake': True,
                            'calidad': calidad,
                            'tipo_contenido': 'informativo',
                            'es_evidente': False,
                            'folder': folder_name
                        })

            print(f"\n==> Videos encontrados:")
            print(f"    Evidentes: {len(videos_evidentes)}")
            print(f"    IA Entretenimiento: {len(videos_ia_entretenimiento)}")
            print(f"    IA Informativos: {len(videos_ia_informativos)}")
            print(f"    Reales Entretenimiento: {len(videos_reales_entretenimiento)}")
            print(f"    Reales Informativos: {len(videos_reales_informativos)}")

            # Selección de videos según especificación:
            # TOTAL: 20 videos
            # - 4 evidentes (TODOS los disponibles de e2, e9, e11)
            # - 8 entretenimiento (4 IA + 4 reales) - balanceados en calidad
            # - 8 informativos (4 IA + 4 reales) - balanceados en calidad

            selected_videos = []

            # 1. Agregar TODOS los evidentes disponibles (debería haber 6: 3 carpetas × 2 calidades)
            selected_videos.extend(videos_evidentes)

            # 2. Seleccionar 4 IA entretenimiento (2 alta + 2 baja)
            random.shuffle(videos_ia_entretenimiento)
            ia_ent_alta = [v for v in videos_ia_entretenimiento if v['calidad'] == 'alta']
            ia_ent_baja = [v for v in videos_ia_entretenimiento if v['calidad'] == 'baja']
            selected_videos.extend(ia_ent_alta[:2])
            selected_videos.extend(ia_ent_baja[:2])

            # 3. Seleccionar 4 reales entretenimiento
            random.shuffle(videos_reales_entretenimiento)
            selected_videos.extend(videos_reales_entretenimiento[:4])

            # 4. Seleccionar 4 IA informativos (2 alta + 2 baja)
            random.shuffle(videos_ia_informativos)
            ia_inf_alta = [v for v in videos_ia_informativos if v['calidad'] == 'alta']
            ia_inf_baja = [v for v in videos_ia_informativos if v['calidad'] == 'baja']
            selected_videos.extend(ia_inf_alta[:2])
            selected_videos.extend(ia_inf_baja[:2])

            # 5. Seleccionar 4 reales informativos
            random.shuffle(videos_reales_informativos)
            selected_videos.extend(videos_reales_informativos[:4])

            # Mezclar el orden final (pero conservar la info de cada video)
            random.shuffle(selected_videos)

            print(f"\n==> Videos seleccionados: {len(selected_videos)}")
            print(f"    Evidentes: {len([v for v in selected_videos if v['es_evidente']])}")
            print(f"    Entretenimiento: {len([v for v in selected_videos if v['tipo_contenido'] == 'entretenimiento'])}")
            print(f"    Informativos: {len([v for v in selected_videos if v['tipo_contenido'] == 'informativo'])}")
            print(f"    Fake: {len([v for v in selected_videos if v['es_fake']])}")
            print(f"    Real: {len([v for v in selected_videos if not v['es_fake']])}")

            # Save participant data
            participant_data = {
                'id': participante_id,
                'genero': genero,
                'edad': edad,
                'fecha_inicio': datetime.now().isoformat(),
                'videos': selected_videos,
                'respuestas': [],
                'completado': False
            }

            participant_file = DATA_DIR / f'{participante_id}.json'
            with open(participant_file, 'w', encoding='utf-8') as f:
                json.dump(participant_data, f, indent=2, ensure_ascii=False)

            print(f"==> Experimento iniciado para participante {participante_id}")
            print(f"    Género: {genero}, Edad: {edad}")

            self.send_json_response({
                'success': True,
                'participanteId': participante_id,
                'videos': selected_videos,
                'totalVideos': len(selected_videos),
                'message': 'Experimento inicializado correctamente'
            })

        except Exception as e:
            print(f"==> Error en init_experiment: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({
                'success': False,
                'message': f'Error al inicializar experimento: {str(e)}'
            }, 500)

    def handle_save_response(self):
        """Save participant response for a video"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            participante_id = data.get('participante_id')
            numero_video = data.get('numero_video')
            respuesta_slider = data.get('respuesta_slider')

            if not participante_id or not numero_video or respuesta_slider is None:
                self.send_json_response({
                    'success': False,
                    'message': 'Datos incompletos'
                }, 400)
                return

            # Load participant data
            participant_file = DATA_DIR / f'{participante_id}.json'

            if not participant_file.exists():
                self.send_json_response({
                    'success': False,
                    'message': 'Participante no encontrado'
                }, 404)
                return

            with open(participant_file, 'r', encoding='utf-8') as f:
                participant_data = json.load(f)

            # Add response with all fields
            response = {
                'fecha_hora': data.get('fecha_hora', datetime.now().isoformat()),
                'numero_video': numero_video,
                'video_path': data.get('video_path', ''),
                'tipo_contenido': data.get('tipo_contenido', ''),
                'es_fake': data.get('es_fake', False),
                'es_evidente': data.get('es_evidente', False),
                'calidad': data.get('calidad', ''),
                'respuesta_slider': respuesta_slider,
                'causa_fake': data.get('causa_fake', ''),
                'tiempo_respuesta_segundos': data.get('tiempo_respuesta_segundos', 0)
            }

            participant_data['respuestas'].append(response)

            # Save updated data
            with open(participant_file, 'w', encoding='utf-8') as f:
                json.dump(participant_data, f, indent=2, ensure_ascii=False)

            causa_info = f" - Causa: {response['causa_fake']}" if response['causa_fake'] else ""
            print(f"==> Respuesta guardada: {participante_id} - Video {numero_video} - Slider: {respuesta_slider}{causa_info}")

            self.send_json_response({
                'success': True,
                'message': 'Respuesta guardada correctamente'
            })

        except Exception as e:
            print(f"==> Error en save_response: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({
                'success': False,
                'message': f'Error al guardar respuesta: {str(e)}'
            }, 500)

    def handle_finish_experiment(self):
        """Mark experiment as completed"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            participante_id = data.get('participante_id')

            if not participante_id:
                self.send_json_response({
                    'success': False,
                    'message': 'ID de participante no válido'
                }, 400)
                return

            # Load participant data
            participant_file = DATA_DIR / f'{participante_id}.json'

            if not participant_file.exists():
                self.send_json_response({
                    'success': False,
                    'message': 'Participante no encontrado'
                }, 404)
                return

            with open(participant_file, 'r', encoding='utf-8') as f:
                participant_data = json.load(f)

            # Mark as completed
            participant_data['completado'] = True
            participant_data['fecha_finalizacion'] = datetime.now().isoformat()

            # Save updated data
            with open(participant_file, 'w', encoding='utf-8') as f:
                json.dump(participant_data, f, indent=2, ensure_ascii=False)

            print(f"==> Experimento finalizado: {participante_id}")
            print(f"    Total respuestas: {len(participant_data['respuestas'])}")

            self.send_json_response({
                'success': True,
                'message': 'Experimento finalizado correctamente'
            })

        except Exception as e:
            print(f"==> Error en finish_experiment: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({
                'success': False,
                'message': f'Error al finalizar experimento: {str(e)}'
            }, 500)

    def handle_get_stats(self):
        """Get statistics from all experiment data"""
        try:
            # Ensure data directory exists
            if not DATA_DIR.exists():
                DATA_DIR.mkdir(parents=True)

            # Get all participant files
            json_files = list(DATA_DIR.glob('P*.json'))

            if len(json_files) == 0:
                self.send_json_response({
                    'success': True,
                    'stats': {
                        'total_participantes': 0,
                        'edad_promedio': 0,
                        'genero': {
                            'masculino': 0,
                            'femenino': 0,
                            'otro': 0,
                            'porcentaje_masculino': 0,
                            'porcentaje_femenino': 0,
                            'porcentaje_otro': 0
                        },
                        'total_respuestas': 0
                    }
                })
                return

            # Collect stats
            total_participantes = 0
            edades = []
            generos = {'masculino': 0, 'femenino': 0, 'otro': 0}
            total_respuestas = 0

            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        total_participantes += 1

                        # Age
                        edad = data.get('edad')
                        if edad and isinstance(edad, (int, float)):
                            edades.append(edad)

                        # Gender
                        genero = data.get('genero', '').lower()
                        if genero in generos:
                            generos[genero] += 1

                        # Responses
                        respuestas = data.get('respuestas', [])
                        total_respuestas += len(respuestas)

                except Exception as e:
                    print(f"Error reading {json_file}: {e}")
                    continue

            # Calculate averages and percentages
            edad_promedio = sum(edades) / len(edades) if edades else 0

            # Gender percentages
            total_genero = sum(generos.values())
            if total_genero > 0:
                porcentaje_masculino = round((generos['masculino'] / total_genero) * 100, 1)
                porcentaje_femenino = round((generos['femenino'] / total_genero) * 100, 1)
                porcentaje_otro = round((generos['otro'] / total_genero) * 100, 1)
            else:
                porcentaje_masculino = porcentaje_femenino = porcentaje_otro = 0

            stats = {
                'total_participantes': total_participantes,
                'edad_promedio': edad_promedio,
                'genero': {
                    'masculino': generos['masculino'],
                    'femenino': generos['femenino'],
                    'otro': generos['otro'],
                    'porcentaje_masculino': porcentaje_masculino,
                    'porcentaje_femenino': porcentaje_femenino,
                    'porcentaje_otro': porcentaje_otro
                },
                'total_respuestas': total_respuestas
            }

            self.send_json_response({
                'success': True,
                'stats': stats
            })

        except Exception as e:
            print(f"Error getting stats: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({
                'success': False,
                'message': f'Error al obtener estadísticas: {str(e)}'
            }, 500)

    def handle_export_csv(self):
        """Export data to CSV"""
        try:
            import csv
            import io

            # Ensure data directory exists
            if not DATA_DIR.exists():
                self.send_error(404, "No data available")
                return

            # Get all participant files
            json_files = list(DATA_DIR.glob('P*.json'))

            if len(json_files) == 0:
                self.send_error(404, "No data available")
                return

            # Create CSV in memory
            output = io.StringIO()
            fieldnames = [
                'participante_id', 'genero', 'edad',
                'fecha_hora_respuesta', 'numero_video',
                'tipo_contenido', 'es_fake', 'es_evidente',
                'calidad', 'respuesta_slider', 'causa_fake',
                'tiempo_respuesta_segundos'
            ]

            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            # Process each participant
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        participante_id = data.get('participante_id', json_file.stem)
                        genero = data.get('genero', '')
                        edad = data.get('edad', '')

                        for respuesta in data.get('respuestas', []):
                            writer.writerow({
                                'participante_id': participante_id,
                                'genero': genero,
                                'edad': edad,
                                'fecha_hora_respuesta': respuesta.get('fecha_hora', ''),
                                'numero_video': respuesta.get('numero_video', ''),
                                'tipo_contenido': respuesta.get('tipo_contenido', ''),
                                'es_fake': respuesta.get('es_fake', ''),
                                'es_evidente': respuesta.get('es_evidente', ''),
                                'calidad': respuesta.get('calidad', ''),
                                'respuesta_slider': respuesta.get('respuesta_slider', ''),
                                'causa_fake': respuesta.get('causa_fake', ''),
                                'tiempo_respuesta_segundos': respuesta.get('tiempo_respuesta_segundos', '')
                            })

                except Exception as e:
                    print(f"Error processing {json_file}: {e}")
                    continue

            # Send CSV file
            csv_content = output.getvalue()
            csv_bytes = csv_content.encode('utf-8-sig')  # UTF-8 with BOM for Excel

            self.send_response(200)
            self.send_header('Content-Type', 'text/csv; charset=utf-8')
            self.send_header('Content-Disposition', f'attachment; filename="resultados_experimento.csv"')
            self.send_header('Content-Length', str(len(csv_bytes)))
            self.end_headers()
            self.wfile.write(csv_bytes)

        except Exception as e:
            print(f"Error exporting CSV: {e}")
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Error exporting CSV: {str(e)}")

    def handle_export_json(self):
        """Export all data as JSON"""
        try:
            # Ensure data directory exists
            if not DATA_DIR.exists():
                self.send_error(404, "No data available")
                return

            # Get all participant files
            json_files = list(DATA_DIR.glob('P*.json'))

            if len(json_files) == 0:
                self.send_error(404, "No data available")
                return

            # Collect all data
            all_data = []
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_data.append(data)
                except Exception as e:
                    print(f"Error reading {json_file}: {e}")
                    continue

            # Send JSON file
            json_content = json.dumps(all_data, indent=2, ensure_ascii=False)
            json_bytes = json_content.encode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Disposition', f'attachment; filename="resultados_experimento.json"')
            self.send_header('Content-Length', str(len(json_bytes)))
            self.end_headers()
            self.wfile.write(json_bytes)

        except Exception as e:
            print(f"Error exporting JSON: {e}")
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Error exporting JSON: {str(e)}")

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Try to find an available port
    port = PORT
    max_attempts = 10

    for attempt in range(max_attempts):
        try:
            httpd = socketserver.TCPServer(("", port), RunwayHandler)
            break
        except OSError as e:
            if e.errno == 10048:  # Port already in use
                print(f"==> Puerto {port} ocupado, probando {port + 1}...")
                port += 1
                if attempt == max_attempts - 1:
                    print(f"\n==> ERROR: No se pudo encontrar un puerto libre")
                    print(f"==> Ejecuta este comando para liberar puertos:")
                    print(f"    taskkill /F /IM python.exe")
                    input("\nPresiona Enter para salir...")
                    exit(1)
            else:
                raise

    print(f"==> Servidor iniciado en http://localhost:{port}")
    print(f"==> Directorio: {os.getcwd()}")
    print(f"\n==> Abre tu navegador en: http://localhost:{port}/generador-local.html\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n==> Servidor detenido")
    finally:
        httpd.server_close()
