# Sistema de Cuestionario para Experimento de Detección de Deepfakes

## Descripción del Experimento

Sistema completo para realizar experimentos sobre la percepción humana de videos generados por IA (deepfakes) vs videos reales.

### Especificaciones del Cuestionario

- **Total de videos por participante:** 20 videos
- **Composición:**
  - 6 videos **evidentes** con IA (de carpetas e2, e9, e11) - SIEMPRE incluidos
  - 4 videos de IA **entretenimiento** (2 alta calidad + 2 baja calidad)
  - 4 videos **reales** entretenimiento
  - 4 videos de IA **informativos** (2 alta calidad + 2 baja calidad)
  - 4 videos **reales** informativos

### Datos Recopilados

Para cada participante se registra:

**Datos demográficos:**
- Género
- Edad
- Fecha y hora de inicio/finalización

**Por cada video evaluado:**
- Fecha y hora de respuesta
- Número de video en la secuencia
- Ruta del video
- Tipo de contenido (entretenimiento/informativo)
- Si es fake o real
- Si es evidente (videos especialmente malos)
- Calidad (alta/baja/real)
- Valoración del slider (1-10)
- Causa por la que considera que es fake (si slider ≥ 6)
- Tiempo de respuesta en segundos

## Estructura de Carpetas VIDEOS

```
VIDEOS/
├── reales/              # Videos reales
│   ├── e1.mp4          # Real entretenimiento
│   ├── e2.mp4
│   ├── i1.mp4          # Real informativo
│   └── i2.mp4
│
├── e1/                 # IA entretenimiento
│   ├── video_high_quality.mp4
│   └── video_low_quality.mp4
│
├── e2/                 # IA entretenimiento EVIDENTE
│   ├── video_high_quality.mp4
│   └── video_low_quality.mp4
│
├── e9/                 # IA entretenimiento EVIDENTE
│   ├── video_high_quality.mp4
│   └── video_low_quality.mp4
│
├── e11/                # IA entretenimiento EVIDENTE
│   ├── video_high_quality.mp4
│   └── video_low_quality.mp4
│
├── i1/                 # IA informativo
│   ├── video_high_quality.mp4
│   └── video_low_quality.mp4
│
└── ...
```

## Instalación y Uso

### 1. Iniciar el Servidor

```bash
python server.py
```

El servidor se iniciará en: `http://localhost:8000`

### 2. Acceder al Cuestionario

Abre tu navegador y ve a:
```
http://localhost:8000/cuestionario.html
```

### 3. Realizar el Experimento

1. El participante lee el consentimiento informado
2. Completa datos demográficos (género y edad)
3. Click en "Comenzar Experimento"
4. Para cada uno de los 20 videos:
   - Ver el video (se reproduce automáticamente)
   - Mover el slider de 1 a 10 según su percepción
   - Si el slider es ≥ 6, seleccionar la causa de por qué considera que es fake
   - Click en "Siguiente Video"
5. Al finalizar, se muestra mensaje de agradecimiento

### 4. Exportar Resultados a Excel

Una vez que tengas participantes, exporta los datos:

```bash
python export_to_excel.py
```

Esto generará un archivo CSV con nombre:
```
resultados_experimento_20241128_153045.csv
```

Puedes abrir este archivo directamente en:
- Microsoft Excel
- Google Sheets
- LibreOffice Calc

## Opciones de Causa Fake

Cuando el participante valora un video con slider ≥ 6, debe seleccionar una causa:

- Parpadeo antinatural
- Gestos extraños
- Movimientos corporales poco fluidos
- Texturas de piel demasiado suaves
- Piel pixelada
- Bordes difusos alrededor de la cara
- Distorsiones faciales
- Reflejos inconsistentes
- Sombras inconsistentes
- Iluminación inconsistente
- Movimiento labial que no coincide con el audio
- Diferencias sutiles en la coloración de la piel
- Diferencias en el balance de color general
- Fondos borrosos
- Fondos con pocos detalles
- Falta de detalles en el fondo
- Letras ilegibles
- Otra razón

## Almacenamiento de Datos

Los datos se guardan en formato JSON en la carpeta:
```
experiment_data/
├── P1732789123456.json
├── P1732789234567.json
└── ...
```

Cada archivo contiene:
- Datos del participante
- Lista de videos mostrados
- Todas las respuestas con timestamps
- Estado de completado

## Formato de Exportación CSV

El archivo CSV contiene las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| participante_id | ID único del participante |
| genero | Género del participante |
| edad | Edad del participante |
| fecha_inicio_experimento | Cuándo empezó el experimento |
| fecha_finalizacion_experimento | Cuándo terminó |
| completado | Si completó todos los videos |
| fecha_hora_respuesta | Timestamp de cada respuesta |
| numero_video | Posición del video (1-20) |
| video_path | Ruta del archivo de video |
| tipo_contenido | entretenimiento o informativo |
| es_fake | Sí/No |
| es_evidente | Si es un video evidentemente fake |
| calidad | alta/baja/real |
| respuesta_slider | Valoración del usuario (1-10) |
| causa_fake | Razón por la que considera fake |
| tiempo_respuesta_segundos | Tiempo que tardó en responder |

## Notas Técnicas

- El servidor es compatible con Python 3.7+
- No requiere base de datos (usa archivos JSON)
- Compatible con todos los navegadores modernos
- Los videos se reproducen en bucle automáticamente
- El orden de los videos es aleatorio para cada participante
- Los datos se guardan inmediatamente después de cada respuesta

## Troubleshooting

**Problema:** No se encuentran videos
- Verifica que la carpeta `VIDEOS/` exista
- Verifica que las carpetas tengan los nombres correctos (e1, e2, i1, etc.)
- Verifica que los archivos sean .mp4

**Problema:** Error al guardar respuestas
- Verifica que el servidor esté corriendo
- Verifica que la carpeta `experiment_data/` tenga permisos de escritura

**Problema:** El CSV no se abre correctamente en Excel
- Usa la opción "Importar datos" en Excel
- Selecciona codificación UTF-8
- El archivo está en formato CSV con delimitador de coma
