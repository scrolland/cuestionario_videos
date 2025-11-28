# Real o Fake - Experimento de Detección de Deepfakes

Experimento de investigación para evaluar la capacidad humana de distinguir entre videos reales y videos generados por IA.

## 🎯 Descripción

**"Real o Fake"** es un sistema completo de investigación que incluye:
- **Cuestionario interactivo** para participantes
- **Generador de videos** con IA para investigadores
- **Sistema de almacenamiento** de datos anónimos
- **Exportación a Excel** para análisis estadístico

**Investigador:** Silvia Charles Roland (scrolland@hotmail.com)

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install pillow
```

### 2. Iniciar el Servidor

**Opción A (Windows):**
```bash
INICIAR-CUESTIONARIO.bat
```

**Opción B (Manual):**
```bash
python server.py
```

El servidor se iniciará en: `http://localhost:8000`

### 3. Acceder al Sistema

#### Para Participantes (Cuestionario)
```
http://localhost:8000/cuestionario.html
```

#### Para Investigadores (Generador)
```
http://localhost:8000/generador-local.html
```

---

## 📊 Cuestionario

### Características

- **20 videos** por participante
- **Duración:** 10-15 minutos
- **Completamente anónimo**
- **Interfaz compacta** (sin scroll)
- **Videos sin sonido** por defecto

### Composición de Videos

1. **6 videos evidentes** con IA (siempre incluidos)
2. **4 videos IA entretenimiento** (2 alta + 2 baja calidad)
3. **4 videos reales entretenimiento**
4. **4 videos IA informativos** (2 alta + 2 baja calidad)
5. **4 videos reales informativos**

### Datos Recopilados

Por cada participante:
- Género y edad
- Fecha/hora de inicio y finalización

Por cada video:
- Valoración (slider 1-10)
- Causa de sospecha (si valoración > 1)
- Tiempo de respuesta
- Metadata del video (tipo, calidad, real/fake)

---

## 🎨 Generador de Videos

### Requisitos

- **API Key de Runway ML** (requerida)
- Modelos utilizados:
  - Gen-4 Turbo (alta calidad)
  - Gen-3 Alpha Turbo (baja calidad)

### Uso

1. Acceder a `http://localhost:8000/generador-local.html`
2. Ingresar API Key de Runway ML
3. Seleccionar carpeta de destino
4. Subir imagen
5. Generar videos (alta y baja calidad)

---

## 📁 Estructura del Proyecto

```
cuestionario_videos/
├── server.py                     # Servidor principal
├── cuestionario.html             # Interfaz del cuestionario
├── generador-local.html          # Generador de videos
├── export_to_excel.py            # Exportador a CSV
├── analizar_resultados.py        # Análisis estadístico
├── verificar_sistema.py          # Verificación del sistema
├── image_analyzer.py             # Análisis de imágenes
├
├── VIDEOS/                       # Videos del experimento
│   ├── reales/                   # Videos reales
│   ├── e1/, e3/, ...            # Videos IA entretenimiento
│   ├── e2/, e9/, e11/           # Videos evidentes
│   └── i1/, i2/, ...            # Videos IA informativos
│
├── experiment_data/              # Datos JSON de participantes
│   └── P*.json
│
├── DOCUMENTACION-EXPERIMENTO.md  # Documentación técnica
├── README-CUESTIONARIO.md        # Guía del cuestionario
└── README.md                     # Este archivo
```

---

## 📈 Exportar Resultados

### A Excel/CSV

```bash
python export_to_excel.py
```

Genera: `resultados_experimento_YYYYMMDD_HHMMSS.csv`

### Análisis Rápido

```bash
python analizar_resultados.py
```

Muestra:
- Total de participantes
- Demografía
- Tasas de detección
- Causas más comunes
- Tiempos de respuesta

---

## 🔧 Verificar Sistema

Antes de usar, verificar que todo esté configurado:

```bash
python verificar_sistema.py
```

Comprueba:
- Carpeta VIDEOS con estructura correcta
- Archivos del sistema presentes
- Módulos Python disponibles
- Carpeta de datos creada

---

## 📝 Notas Importantes

### Videos Reales

Los videos reales deben estar en `VIDEOS/reales/`:
- `e*.mp4` - Videos reales de entretenimiento
- `i*.mp4` - Videos reales informativos

### Videos IA

Las carpetas de videos IA siguen el patrón:
- `e#` - Entretenimiento (e1, e3, e4, ...)
- `i#` - Informativos (i1, i2, i3, ...)
- `e2, e9, e11` - **Videos evidentes** (siempre incluidos)

Cada carpeta debe contener:
- `video_high_quality.mp4`
- `video_low_quality.mp4`

---

## 🔒 Privacidad

- **Datos completamente anónimos**
- Sin identificadores personales
- Almacenamiento local en JSON
- No se envían datos a servidores externos

---

## 📧 Contacto

**Investigador:** Silvia Charles Roland (scrolland@hotmail.com)

Para preguntas sobre:
- Participación en el estudio
- Uso del sistema
- Resultados de la investigación
- Colaboraciones

---

## 📄 Licencia

Este proyecto es para fines de investigación académica.

---

## 🙏 Agradecimientos

Gracias a todos los participantes que contribuyen a esta investigación sobre detección de deepfakes.

**Tecnología utilizada:**
- Runway ML (Gen-4 Turbo, Gen-3 Alpha Turbo)
- Python 3.x
- Pillow (PIL)
- HTML5/CSS3/JavaScript
