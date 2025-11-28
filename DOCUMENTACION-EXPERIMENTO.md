# Documentación Técnica del Experimento
## Real o Fake: Detección de Videos Generados por IA

---

## 📋 Índice

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Objetivos del Experimento](#objetivos-del-experimento)
4. [Metodología Técnica](#metodología-técnica)
5. [Arquitectura del Sistema](#arquitectura-del-sistema)
6. [Generador de Videos](#generador-de-videos)
7. [Cuestionario para Participantes](#cuestionario-para-participantes)
8. [Variables Experimentales](#variables-experimentales)
9. [Análisis de Datos](#análisis-de-datos)
10. [Guía de Uso](#guía-de-uso)

---

## 1. Resumen Ejecutivo

**"Real o Fake"** es un experimento de investigación que evalúa la capacidad de las personas para distinguir entre videos reales y videos generados por inteligencia artificial (deepfakes).

### Características del Estudio

- **20 videos por participante**: Incluye videos evidentes, de entretenimiento e informativos
- **Cuestionario interactivo**: Interfaz web compacta y fácil de usar
- **Datos anónimos**: Almacenamiento seguro en formato JSON
- **Exportación a Excel**: Análisis estadístico simplificado

### Contacto del Investigador

**Email:** scrolland@hotmail.com

---

## 2. Acceso al Sistema

El sistema consta de **dos páginas web independientes**:

### 🎬 Cuestionario (Para Participantes)

**URL:** `http://localhost:8000/cuestionario.html`

- Completamente anónimo
- Duración: 10-15 minutos
- 20 videos a evaluar
- Sin conocimientos previos necesarios

### 🎨 Generador de Videos (Para Investigadores)

**URL:** `http://localhost:8000/generador-local.html`

- Requiere API Key de Runway ML
- Genera videos desde imágenes
- Control de calidad (alta/baja)
- Solo para creación de material de estudio

**Tecnología utilizada:**
- **Runway ML Gen-4 Turbo**: Modelo de IA más avanzado para generación de videos de alta calidad
- **Runway ML Gen-3 Alpha Turbo**: Modelo anterior, utilizado para videos de baja calidad
- **Python 3.13**: Procesamiento backend
- **Pillow (PIL)**: Análisis automático de imágenes

**Metodología:**
- Generación automática de 2 versiones por cada imagen (alta y baja calidad)
- Prompts diferenciados y contextuales basados en análisis de imagen
- Modelos de IA diferentes según calidad objetivo
- Encuesta comparativa con videos reales como control

---

## 2. Objetivos del Experimento

### Objetivo Principal
Evaluar la capacidad de detección de deepfakes en población general y analizar los factores que influyen en la percepción de autenticidad.

### Objetivos Específicos

1. **Detectabilidad por Calidad**
   - Medir si videos de alta calidad son más difíciles de identificar como falsos
   - Analizar si la calidad técnica afecta la percepción de autenticidad

2. **Detectabilidad por Tipo de Contenido**
   - Comparar detección en contenido de entretenimiento vs. informativo
   - Identificar si el contexto afecta el nivel de escrutinio del espectador

3. **Factores de Confusión**
   - Determinar qué características técnicas influyen más en la detección
   - Identificar patrones de error en la clasificación

4. **Percepción de Calidad**
   - Medir si los usuarios pueden diferenciar alta calidad de baja calidad
   - Analizar correlación entre percepción de calidad y clasificación como real/fake

---

## 3. Metodología Técnica

### 3.1. Diseño Experimental

**Variables Independientes:**
- Autenticidad: Real vs. Fake (generado por IA)
- Calidad: Alta vs. Baja
- Tipo de contenido: Entretenimiento (e) vs. Informativo (i)

**Variables Dependientes:**
- Tasa de detección correcta (%)
- Tiempo de decisión
- Nivel de confianza en la respuesta

**Grupos Experimentales:**
1. Videos reales - Entretenimiento (control)
2. Videos reales - Informativos (control)
3. Videos fake - Alta calidad - Entretenimiento
4. Videos fake - Baja calidad - Entretenimiento
5. Videos fake - Alta calidad - Informativos
6. Videos fake - Baja calidad - Informativos

### 3.2. Nomenclatura de Archivos

El sistema utiliza una nomenclatura específica para organizar los videos:

```
VIDEOS/
├── f{calidad}{tipo}_{nombre}/
│   ├── imagen_original.jpg
│   ├── video_high_quality.mp4
│   └── video_low_quality.mp4
```

**Donde:**
- `f` = fake (video generado por IA)
- `{calidad}` = `a` (alta) o `b` (baja)
- `{tipo}` = `e` (entretenimiento) o `i` (informativo)
- `{nombre}` = identificador único

**Ejemplos:**
- `fae_persona1/` = Fake, Alta calidad, Entretenimiento, persona 1
- `fbi_noticia1/` = Fake, Baja calidad, Informativo, noticia 1

---

## 4. Arquitectura del Sistema

### 4.1. Componentes del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   NAVEGADOR WEB                          │
│              generador-local.html                        │
│         (Interfaz de selección de carpeta)               │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP POST (multipart/form-data)
                     ↓
┌─────────────────────────────────────────────────────────┐
│                SERVIDOR PYTHON (server.py)               │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │  1. Recepción y parseo de imagen               │     │
│  │  2. Detección automática de tipo (e/i)         │     │
│  │  3. Análisis de imagen (image_analyzer.py)     │     │
│  │  4. Generación de prompts diferenciados        │     │
│  │  5. Llamadas a API Runway ML                   │     │
│  │  6. Polling de estado de generación            │     │
│  │  7. Descarga y procesamiento de videos         │     │
│  │  8. Compresión adicional (si necesario)        │     │
│  └────────────────────────────────────────────────┘     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS (REST API)
                     ↓
┌─────────────────────────────────────────────────────────┐
│              RUNWAY ML API                               │
│                                                          │
│  Alta calidad: gen4_turbo (Modelo más avanzado)         │
│  Baja calidad: gen3a_turbo (Modelo anterior)            │
│                                                          │
│  Tiempo estimado: ~30 segundos por video de 10 seg      │
└─────────────────────────────────────────────────────────┘
```

### 4.2. Flujo de Datos

1. **Input**: Usuario selecciona carpeta con imagen
2. **Análisis**: Sistema analiza automáticamente la imagen
3. **Clasificación**: Detecta tipo de contenido (e/i)
4. **Generación de Prompts**: Crea 2 prompts diferenciados
5. **API Calls**: Envía 2 peticiones simultáneas a Runway ML
6. **Procesamiento**: Descarga y procesa ambos videos
7. **Output**: Guarda videos en carpeta especificada

---

## 5. Proceso de Generación de Videos

### 5.1. Preparación de Imagen

```python
# 1. Validación de tamaño
max_size = 3.3 MB  # Límite por API (se convierte en 5MB tras base64)

# 2. Codificación
image_base64 = base64.b64encode(image_data)
image_data_uri = f"data:image/jpg;base64,{image_base64}"

# 3. Detección de formato
- JPEG: 0xFF 0xD8 0xFF
- PNG: 0x89 0x50 0x4E 0x47
- GIF: 0x47 0x49 0x46
```

### 5.2. Generación Paralela

El sistema genera **ambos videos simultáneamente** para eficiencia:

```python
# Configuración Alta Calidad
{
    'model': 'gen4_turbo',
    'ratio': '1280:720',
    'duration': 10,
    'bitrate': '4000k',
    'prompt': prompt_alta_calidad
}

# Configuración Baja Calidad
{
    'model': 'gen3a_turbo',  # Modelo más antiguo
    'ratio': '1280:720',
    'duration': 10,
    'bitrate': '600k',
    'prompt': prompt_baja_calidad
}
```

### 5.3. Tiempo de Generación

- **Gen-4 Turbo**: ~30 segundos para 10 segundos de video
- **Gen-3 Alpha Turbo**: ~45 segundos para 10 segundos de video
- **Procesamiento total**: 2-4 minutos (incluye descarga y compresión)

---

## 6. Diferenciación de Calidades

### 6.1. Diferencias Técnicas

| Aspecto | Alta Calidad | Baja Calidad |
|---------|-------------|--------------|
| **Modelo IA** | Gen-4 Turbo | Gen-3 Alpha Turbo |
| **Resolución** | 1280x720 | 1280x720 |
| **Bitrate** | 4000 kbps | 600 kbps |
| **Tamaño archivo** | ~8-10 MB | ~2-3 MB |
| **Prompt** | Detalle máximo | Compresión visible |
| **Artefactos** | Mínimos | Más visibles |

### 6.2. Características Perceptuales

**Alta Calidad:**
- Mayor fluidez de movimiento
- Mejor coherencia temporal
- Detalles faciales más realistas
- Iluminación más consistente
- Menos artefactos de compresión

**Baja Calidad:**
- Movimientos menos fluidos
- Posibles inconsistencias temporales
- Menor definición en detalles
- Compresión más visible
- Artefactos intencionales sutiles

### 6.3. Estrategia de Diferenciación

La diferenciación se logra mediante **3 vectores**:

1. **Modelo de IA diferente**
   - Gen-4 Turbo: Arquitectura más avanzada, mejor comprensión de física
   - Gen-3 Alpha Turbo: Versión anterior con limitaciones conocidas

2. **Prompts diferenciados**
   - Alta: "ultra high definition, professional grade, pristine quality..."
   - Baja: "slight compression, natural grain, soft focus..."

3. **Post-procesamiento**
   - Alta: Bitrate alto, sin compresión adicional
   - Baja: Bitrate bajo, compresión agresiva

---

## 7. Análisis Automático de Imágenes

### 7.1. Características Analizadas

El módulo `image_analyzer.py` extrae las siguientes características:

#### 7.1.1. Aspect Ratio
```python
- horizontal_wide: ratio > 1.5
- horizontal: ratio > 1.2
- square: ratio > 0.9
- vertical: ratio ≤ 0.9
```

#### 7.1.2. Brillo (Brightness)
```python
- dark: promedio < 85/255
- medium: promedio < 170/255
- bright: promedio ≥ 170/255
```

#### 7.1.3. Color Dominante
```python
- neutral: variación RGB < 30
- warm: canal R dominante
- cool: canal B dominante
- natural: canal G dominante
```

#### 7.1.4. Temperatura de Color
```python
- warm: R_avg > B_avg + 10
- cool: B_avg > R_avg + 10
- neutral: diferencia < 10
```

#### 7.1.5. Detección de Rostro
```python
# Heurística basada en varianza en tercio superior
variance_threshold = 500
has_face = variance_upper_half > threshold
```

#### 7.1.6. Composición
```python
# Análisis de detalle por tercios verticales
- top_focused: máximo detalle arriba
- center_focused: máximo detalle centro
- bottom_focused: máximo detalle abajo
```

### 7.2. Implementación del Análisis

```python
class ImageAnalyzer:
    def analyze(self):
        return {
            'aspect_ratio': self._get_aspect_ratio(),
            'brightness': self._get_brightness(),
            'dominant_color': self._get_dominant_color(),
            'color_temperature': self._get_color_temperature(),
            'has_face_region': self._detect_face_region(),
            'composition': self._analyze_composition()
        }
```

---

## 8. Generación de Prompts Inteligentes

### 8.1. Estrategia de Prompts

Los prompts se generan de forma **dinámica** basándose en:
1. Análisis de la imagen
2. Tipo de contenido (e/i)
3. Nivel de calidad objetivo
4. Prompt personalizado del usuario (opcional)

### 8.2. Prompts Base

#### Entretenimiento (e)
```python
[
    "natural subtle movement",
    "gentle ambient motion",
    "organic realistic movement",
    "soft natural gestures",
    "authentic human behavior"
]
```

#### Informativo (i)
```python
[
    "professional subtle movement",
    "slight natural camera movement",
    "minimal realistic motion",
    "steady professional presentation",
    "controlled natural movement"
]
```

### 8.3. Componentes del Prompt

Un prompt completo se construye con:

```python
prompt = [
    base_movement,           # Según tipo (e/i)
    + facial_expressions,    # Si se detecta rostro
    + lighting_description,  # Según brillo analizado
    + color_temperature,     # Según temperatura detectada
    + quality_enhancements   # Según calidad objetivo
]
```

### 8.4. Ejemplos de Prompts Generados

**Ejemplo 1: Retrato - Entretenimiento - Alta Calidad**
```
Input: Imagen brillante con rostro centrado, temperatura cálida
Output: "natural subtle movement, subtle facial expressions, natural eye
movement, natural daylight, warm color tones, cinematic quality,
photorealistic, high detail, ultra high definition, professional grade,
pristine quality, sharp details, natural motion blur, authentic depth of
field, realistic lighting gradients, subtle micro-expressions"
```

**Ejemplo 2: Retrato - Entretenimiento - Baja Calidad**
```
Input: Misma imagen
Output: "natural subtle movement, subtle facial expressions, natural eye
movement, natural daylight, warm color tones, cinematic quality,
photorealistic, high detail, slight compression, natural grain, soft focus,
subtle motion artifacts, minimal detail loss, organic imperfections"
```

**Ejemplo 3: Escena - Informativo - Alta Calidad**
```
Input: Imagen oscura, composición centrada, temperatura neutra
Output: "professional subtle movement, centered subject movement, ambient
indoor lighting, cinematic quality, photorealistic, high detail, ultra high
definition, professional grade, pristine quality, sharp details, natural
motion blur, authentic depth of field"
```

### 8.5. Lógica de Personalización

```python
def generate_prompt(image_analysis, custom_prompt=None):
    if custom_prompt:
        base = custom_prompt
    else:
        base = auto_generate(image_analysis)

    return {
        'high_quality': enhance_for_high(base, analysis),
        'low_quality': enhance_for_low(base, analysis)
    }
```

---

## 9. Variables Experimentales

### 9.1. Variables Controladas

| Variable | Control |
|----------|---------|
| Duración | 10 segundos (fija) |
| Formato | 1280x720 horizontal (fijo) |
| Modelo Alta | Gen-4 Turbo (fijo) |
| Modelo Baja | Gen-3 Alpha Turbo (fijo) |
| Imagen origen | Una por condición |

### 9.2. Variables Manipuladas

1. **Autenticidad** (2 niveles)
   - Real
   - Fake (generado por IA)

2. **Calidad** (2 niveles)
   - Alta (Gen-4 Turbo + bitrate alto)
   - Baja (Gen-3 Alpha Turbo + bitrate bajo)

3. **Tipo de Contenido** (2 niveles)
   - Entretenimiento
   - Informativo

### 9.3. Variables Medidas

1. **Detección**
   - Clasificación (Real/Fake)
   - Confianza (escala 1-5)
   - Tiempo de decisión

2. **Percepción de Calidad**
   - Calidad percibida (escala 1-5)
   - Factores de calidad identificados

3. **Variables Demográficas**
   - Edad
   - Género
   - Experiencia con medios digitales
   - Exposición previa a deepfakes

---

## 7. Cuestionario para Participantes

### 7.1. Diseño del Cuestionario

El cuestionario ha sido optimizado para una experiencia compacta y eficiente:

**Características principales:**
- Interfaz ultra-compacta (todo visible sin scroll)
- Videos sin sonido por defecto
- 20 videos por participante
- Duración estimada: 10-15 minutos

### 7.2. Estructura del Cuestionario

**Paso 1: Bienvenida y Consentimiento** (2 min)
- Información del estudio
- 20 videos a evaluar
- Consentimiento informado
- Datos demográficos:
  - Edad (mayor de 18 años)
  - Género

**Paso 2: Evaluación de Videos** (10-12 min)
Por cada uno de los 20 videos:

1. **Valoración con Slider** (1-10)
   - 1 = Completamente REAL
   - 5 = No estoy seguro
   - 10 = Completamente FAKE/IA

2. **Causa de Sospecha** (solo si valoración > 1)
   - Desplegable con 14 opciones:
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
     - Diferencias en el balance de color general
     - Fondos borrosos
     - Letras ilegibles
     - Otra razón

3. **Tiempo de respuesta** (automático)
   - Se registra el tiempo desde que carga el video hasta que avanza

**Paso 3: Finalización**
- Mensaje de agradecimiento
- Email de contacto: scrolland@hotmail.com

### 7.3. Composición de los 20 Videos

El sistema selecciona automáticamente:

1. **6 videos evidentes** (SIEMPRE incluidos)
   - De carpetas e2, e9, e11
   - Alta y baja calidad

2. **4 videos IA entretenimiento**
   - 2 alta calidad + 2 baja calidad
   - Selección aleatoria

3. **4 videos reales entretenimiento**
   - Selección aleatoria de carpeta `reales/`

4. **4 videos IA informativos**
   - 2 alta calidad + 2 baja calidad
   - Selección aleatoria

5. **4 videos reales informativos**
   - Selección aleatoria de carpeta `reales/`

**Orden:** Aleatorizado para cada participante
   - [ ] Baja
   - [ ] Media
   - [ ] Alta
   - [ ] Muy alta

4. (Opcional) ¿Qué aspectos te ayudaron a decidir?
   - Texto abierto

### 10.2. Balanceo de Condiciones

Para un diseño balanceado 2x2x2:

| Condición | N videos | Distribución |
|-----------|----------|--------------|
| Real - E | 2 | Control |
| Real - I | 2 | Control |
| Fake Alta - E | 2 | Experimental |
| Fake Baja - E | 2 | Experimental |
| Fake Alta - I | 2 | Experimental |
| Fake Baja - I | 2 | Experimental |
| **TOTAL** | **12** | Balanceado |

### 10.3. Consideraciones Éticas

1. **Consentimiento Informado**
   - Explicar propósito del estudio
   - Indicar que verán videos reales y generados
   - Derecho a retirarse en cualquier momento

2. **Debriefing**
   - Al finalizar, revelar cuáles eran fake
   - Explicar la tecnología utilizada
   - Discutir implicaciones

3. **Privacidad**
   - Anonimizar respuestas
   - No recopilar información personal identificable

---

## 9. Análisis de Datos

### 9.1. Almacenamiento de Datos

Los datos se guardan automáticamente en formato JSON:

**Ubicación:** `experiment_data/P{timestamp}.json`

**Contenido por participante:**
```json
{
  "id": "P1732789123456",
  "genero": "Masculino",
  "edad": 25,
  "fecha_inicio": "2024-11-28T10:30:00",
  "fecha_finalizacion": "2024-11-28T10:45:00",
  "completado": true,
  "videos": [...],
  "respuestas": [
    {
      "fecha_hora": "2024-11-28T10:31:15",
      "numero_video": 1,
      "video_path": "VIDEOS/e2/video_high_quality.mp4",
      "tipo_contenido": "entretenimiento",
      "es_fake": true,
      "es_evidente": true,
      "calidad": "alta",
      "respuesta_slider": 8,
      "causa_fake": "gestos_extranos",
      "tiempo_respuesta_segundos": 12
    }
  ]
}
```

### 9.2. Exportación a Excel/CSV

**Comando:**
```bash
python export_to_excel.py
```

**Archivo generado:** `resultados_experimento_YYYYMMDD_HHMMSS.csv`

**Columnas del CSV:**
- `participante_id`: ID único
- `genero`: Género del participante
- `edad`: Edad del participante
- `fecha_inicio_experimento`: Timestamp de inicio
- `fecha_finalizacion_experimento`: Timestamp de finalización
- `completado`: Si completó todos los videos
- `fecha_hora_respuesta`: Timestamp de cada respuesta
- `numero_video`: Orden del video (1-20)
- `video_path`: Ruta del archivo
- `tipo_contenido`: entretenimiento o informativo
- `es_fake`: Sí/No
- `es_evidente`: Si es video evidentemente fake
- `calidad`: alta/baja/real
- `respuesta_slider`: Valoración 1-10
- `causa_fake`: Razón seleccionada
- `tiempo_respuesta_segundos`: Tiempo de decisión

### 9.3. Análisis Estadístico Rápido

**Comando:**
```bash
python analizar_resultados.py
```

**Muestra:**
- Total de participantes
- Demografía (edad, género)
- Valoraciones promedio por tipo
- Tasa de detección (fake vs real)
- Causas más comunes
- Tiempos de respuesta

### 9.4. Métricas de Análisis

#### Tasa de Detección

```
Accuracy = (TP + TN) / Total
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)

Donde:
TP = True Positive (fake identificado como fake)
TN = True Negative (real identificado como real)
FP = False Positive (real identificado como fake)
FN = False Negative (fake identificado como real)
```

#### 11.2.2. Análisis por Condición

```python
# Por cada condición (Alta/Baja x E/I):
- Tasa de detección correcta
- Nivel de confianza promedio
- Tiempo de decisión promedio
- Correlación calidad percibida vs. detección
```

### 11.3. Análisis Estadísticos

#### 11.3.1. ANOVA Factorial

```
DV: Tasa de detección correcta
IV1: Calidad (Alta vs. Baja)
IV2: Tipo (E vs. I)
IV3: Autenticidad (Real vs. Fake)
```

#### 11.3.2. Regresión Logística

```python
P(detectado_como_fake) = β0
    + β1(calidad_tecnica)
    + β2(tipo_contenido)
    + β3(confianza_usuario)
    + β4(experiencia_previa)
    + ε
```

### 11.4. Visualizaciones Esperadas

1. **Matriz de Confusión** por condición
2. **Curvas ROC** para cada modelo
3. **Box plots** de confianza por acierto/error
4. **Heat map** de correlaciones
5. **Gráficos de barras** comparando tasas de detección

---

## 12. Archivos del Sistema

### 12.1. Archivos Principales

| Archivo | Propósito |
|---------|-----------|
| `server.py` | Servidor backend principal |
| `image_analyzer.py` | Análisis automático de imágenes |
| `generador-local.html` | Interfaz web de usuario |
| `INICIAR-SERVIDOR.bat` | Script de inicio rápido |
| `test-simple-gen4.py` | Test de API |

### 12.2. Documentación

| Archivo | Contenido |
|---------|-----------|
| `DOCUMENTACION-EXPERIMENTO.md` | Este documento |
| `INSTRUCCIONES-RAPIDAS.txt` | Guía de uso rápido |
| `LEEME.txt` | Documentación completa |
| `README-GENERADOR-LOCAL.md` | Documentación técnica |

### 12.3. Estructura de Directorios

```
experimentos2/
├── server.py                      # Servidor principal
├── image_analyzer.py              # Análisis de imágenes
├── generador-local.html           # Interfaz web
├── INICIAR-SERVIDOR.bat          # Inicio rápido
├── DOCUMENTACION-EXPERIMENTO.md  # Esta documentación
├── INSTRUCCIONES-RAPIDAS.txt     # Guía rápida
└── VIDEOS/                       # Videos generados
    ├── fae_sujeto1/             # Fake, Alta, Entretenimiento
    │   ├── imagen.jpg
    │   ├── video_high_quality.mp4
    │   └── video_low_quality.mp4
    ├── fbi_noticia1/            # Fake, Baja, Informativo
    │   └── ...
    └── ...
```

---

## 13. Limitaciones y Consideraciones

### 13.1. Limitaciones Técnicas

1. **Tamaño de imagen**: Máximo 3.3 MB (limitación de API)
2. **Duración**: Fija en 10 segundos
3. **Formato**: Solo horizontal 1280x720
4. **Coste**: 100 créditos por generación (2 videos)

### 13.2. Limitaciones Metodológicas

1. **Muestra**: Depende del tamaño de muestra de encuestados
2. **Contexto**: Videos cortos pueden no representar uso real
3. **Orden**: Efectos de orden si no se randomiza adecuadamente

### 13.3. Consideraciones de Validez

**Validez Interna:**
- Control de variables técnicas
- Asignación aleatoria de condiciones
- Balanceo de estímulos

**Validez Externa:**
- Generalización a otros tipos de deepfakes
- Aplicabilidad a videos más largos
- Transferencia a otros contextos

---

## 14. Conclusiones y Trabajo Futuro

### 14.1. Aportaciones del Sistema

1. **Automatización**: Generación automática de prompts contextuales
2. **Diferenciación**: Uso de modelos diferentes para calidades diferentes
3. **Análisis**: Sistema de análisis de imagen integrado
4. **Documentación**: Completa trazabilidad del proceso

### 14.2. Mejoras Futuras

1. **Análisis facial avanzado**: Integrar detección de rostros con ML
2. **Más modelos**: Comparar con otros generadores (Stable Diffusion Video, etc.)
3. **Duraciones variables**: Estudiar efecto de duración en detección
4. **Contenido específico**: Generar categorías más específicas

### 14.3. Aplicaciones

1. **Educación**: Formación en detección de deepfakes
2. **Investigación**: Base para estudios sobre percepción
3. **Desarrollo**: Mejora de algoritmos de detección
4. **Política**: Informar legislación sobre medios sintéticos

---

## 15. Referencias Técnicas

### 15.1. APIs y Modelos

- **Runway ML Gen-4 Turbo**: https://docs.dev.runwayml.com/
- **Runway ML Gen-3 Alpha Turbo**: https://help.runwayml.com/
- **Pillow (PIL)**: https://pillow.readthedocs.io/

### 15.2. Especificaciones

- **Ratios válidos Gen-4**: 1280:720, 720:1280, 1104:832, 832:1104, 960:960, 1584:672
- **Duración máxima**: 10 segundos
- **Coste**: 5 créditos/segundo
- **Tiempo de generación**: ~30 seg (Gen-4), ~45 seg (Gen-3)

---

## Apéndices

### Apéndice A: Ejemplo de Salida del Análisis

```json
{
  "analysis": {
    "aspect_ratio": "horizontal",
    "brightness": "bright",
    "dominant_color": "warm",
    "color_temperature": "warm",
    "has_face_region": true,
    "composition": "top_focused"
  },
  "prompts": {
    "high_quality": "natural subtle movement, subtle facial expressions, natural eye movement, natural daylight, warm color tones, cinematic quality, photorealistic, high detail, ultra high definition, professional grade, pristine quality, sharp details, natural motion blur, authentic depth of field, realistic lighting gradients, subtle micro-expressions",
    "low_quality": "natural subtle movement, subtle facial expressions, natural eye movement, natural daylight, warm color tones, cinematic quality, photorealistic, high detail, slight compression, natural grain, soft focus, subtle motion artifacts, minimal detail loss, organic imperfections"
  },
  "video_type": "entretenimiento"
}
```

### Apéndice B: Configuración de Calidades

```python
QUALITY_CONFIGS = {
    'high': {
        'model': 'gen4_turbo',
        'ratio': '1280:720',
        'bitrate': '4000k',
        'target_size': '10 MB'
    },
    'low': {
        'model': 'gen3a_turbo',
        'ratio': '1280:720',
        'bitrate': '600k',
        'target_size': '2 MB'
    }
}
```

---

**Documento generado el**: 27 de Noviembre, 2025
**Versión**: 1.0
**Sistema**: Generador de Videos Local - Runway ML
**Propósito**: Investigación en Detección de Deepfakes
