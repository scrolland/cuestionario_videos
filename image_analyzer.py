#!/usr/bin/env python3
"""
Análisis automático de imágenes para generar prompts realistas
Parte del experimento de detección de deepfakes
"""

from PIL import Image
import io
import colorsys

class ImageAnalyzer:
    """Analiza imágenes para generar prompts contextuales y realistas"""

    def __init__(self, image_data):
        """
        Args:
            image_data: bytes de la imagen
        """
        self.image = Image.open(io.BytesIO(image_data))
        self.width, self.height = self.image.size

    def analyze(self):
        """Analiza la imagen y retorna características detectadas"""
        return {
            'aspect_ratio': self._get_aspect_ratio(),
            'brightness': self._get_brightness(),
            'dominant_color': self._get_dominant_color(),
            'color_temperature': self._get_color_temperature(),
            'has_face_region': self._detect_face_region(),
            'composition': self._analyze_composition()
        }

    def _get_aspect_ratio(self):
        """Determina el ratio de aspecto"""
        ratio = self.width / self.height
        if ratio > 1.5:
            return 'horizontal_wide'
        elif ratio > 1.2:
            return 'horizontal'
        elif ratio > 0.9:
            return 'square'
        else:
            return 'vertical'

    def _get_brightness(self):
        """Calcula el brillo promedio de la imagen"""
        # Convert to grayscale and get average
        grayscale = self.image.convert('L')
        pixels = list(grayscale.getdata())
        avg_brightness = sum(pixels) / len(pixels)

        if avg_brightness < 85:
            return 'dark'
        elif avg_brightness < 170:
            return 'medium'
        else:
            return 'bright'

    def _get_dominant_color(self):
        """Obtiene el color dominante"""
        # Resize for faster processing
        small_image = self.image.resize((50, 50))
        pixels = list(small_image.getdata())

        # Get average RGB
        r = sum(p[0] for p in pixels if len(p) >= 3) / len(pixels)
        g = sum(p[1] for p in pixels if len(p) >= 3) / len(pixels)
        b = sum(p[2] for p in pixels if len(p) >= 3) / len(pixels)

        # Determine dominant color category
        max_channel = max(r, g, b)

        if max_channel - min(r, g, b) < 30:
            return 'neutral'  # Grayish
        elif r > g and r > b:
            return 'warm'  # Reddish
        elif b > r and b > g:
            return 'cool'  # Bluish
        else:
            return 'natural'  # Greenish

    def _get_color_temperature(self):
        """Determina la temperatura de color (cálida/fría)"""
        # Sample center region
        center_x = self.width // 2
        center_y = self.height // 2
        sample_size = min(self.width, self.height) // 4

        try:
            region = self.image.crop((
                center_x - sample_size,
                center_y - sample_size,
                center_x + sample_size,
                center_y + sample_size
            ))

            pixels = list(region.getdata())
            r_avg = sum(p[0] for p in pixels if len(p) >= 3) / len(pixels)
            b_avg = sum(p[2] for p in pixels if len(p) >= 3) / len(pixels)

            if r_avg > b_avg + 10:
                return 'warm'
            elif b_avg > r_avg + 10:
                return 'cool'
            else:
                return 'neutral'
        except:
            return 'neutral'

    def _detect_face_region(self):
        """Detecta si hay una región probable de rostro (basado en composición)"""
        # Simple heuristic: check if there's a concentrated region in upper half
        upper_half = self.image.crop((0, 0, self.width, self.height // 2))

        # Convert to grayscale and check variance
        grayscale = upper_half.convert('L')
        pixels = list(grayscale.getdata())

        avg = sum(pixels) / len(pixels)
        variance = sum((p - avg) ** 2 for p in pixels) / len(pixels)

        # High variance in upper half suggests possible face/subject
        return variance > 500

    def _analyze_composition(self):
        """Analiza la composición general de la imagen"""
        # Check vertical distribution of detail
        third_height = self.height // 3

        top_third = self.image.crop((0, 0, self.width, third_height))
        middle_third = self.image.crop((0, third_height, self.width, third_height * 2))
        bottom_third = self.image.crop((0, third_height * 2, self.width, self.height))

        def get_detail_score(region):
            gray = region.convert('L')
            pixels = list(gray.getdata())
            avg = sum(pixels) / len(pixels)
            variance = sum((p - avg) ** 2 for p in pixels) / len(pixels)
            return variance

        top_detail = get_detail_score(top_third)
        middle_detail = get_detail_score(middle_third)
        bottom_detail = get_detail_score(bottom_third)

        max_detail = max(top_detail, middle_detail, bottom_detail)

        if max_detail == top_detail:
            return 'top_focused'
        elif max_detail == middle_detail:
            return 'center_focused'
        else:
            return 'bottom_focused'


class PromptGenerator:
    """Genera prompts realistas basados en el análisis de la imagen"""

    # Prompts base según tipo de contenido
    ENTERTAINMENT_BASE = [
        "natural subtle movement",
        "gentle ambient motion",
        "organic realistic movement",
        "soft natural gestures",
        "authentic human behavior"
    ]

    INFORMATIVE_BASE = [
        "professional subtle movement",
        "slight natural camera movement",
        "minimal realistic motion",
        "steady professional presentation",
        "controlled natural movement"
    ]

    def __init__(self, video_type='e'):
        """
        Args:
            video_type: 'e' para entretenimiento, 'i' para informativo
        """
        self.video_type = video_type

    def generate_prompt(self, image_analysis, custom_prompt=None):
        """
        Genera un prompt optimizado para realismo

        Args:
            image_analysis: dict con características de la imagen
            custom_prompt: str, prompt personalizado del usuario (opcional)

        Returns:
            dict con 'high_quality' y 'low_quality' prompts
        """
        if custom_prompt and custom_prompt.strip():
            # Usuario proporcionó prompt personalizado
            base_prompt = custom_prompt.strip()
        else:
            # Generar prompt automático basado en análisis
            base_prompt = self._generate_automatic_prompt(image_analysis)

        # Prompts diferenciados para alta y baja calidad
        return {
            'high_quality': self._enhance_for_quality(base_prompt, 'high', image_analysis),
            'low_quality': self._enhance_for_quality(base_prompt, 'low', image_analysis)
        }

    def _generate_automatic_prompt(self, analysis):
        """Genera un prompt automático basado en el análisis de la imagen"""

        components = []

        # 1. Tipo de movimiento base
        if self.video_type == 'e':
            import random
            components.append(random.choice(self.ENTERTAINMENT_BASE))
        else:
            import random
            components.append(random.choice(self.INFORMATIVE_BASE))

        # 2. Ajustes por composición
        if analysis['composition'] == 'top_focused' or analysis['has_face_region']:
            components.append("subtle facial expressions")
            components.append("natural eye movement")
        elif analysis['composition'] == 'center_focused':
            components.append("centered subject movement")

        # 3. Iluminación
        if analysis['brightness'] == 'bright':
            components.append("natural daylight")
        elif analysis['brightness'] == 'dark':
            components.append("ambient indoor lighting")
        else:
            components.append("balanced natural lighting")

        # 4. Temperatura de color
        if analysis['color_temperature'] == 'warm':
            components.append("warm color tones")
        elif analysis['color_temperature'] == 'cool':
            components.append("cool color tones")

        # 5. Calidad cinematográfica
        components.append("cinematic quality")
        components.append("photorealistic")
        components.append("high detail")

        return ", ".join(components)

    def _enhance_for_quality(self, base_prompt, quality_level, analysis):
        """
        Mejora el prompt según el nivel de calidad

        IMPORTANTE: Para baja calidad, usamos términos que pueden generar
        artefactos sutiles que dificulten la detección pero mantengan realismo
        """

        enhancements = []

        if quality_level == 'high':
            # Alta calidad: máximo realismo y detalle
            enhancements = [
                "ultra high definition",
                "professional grade",
                "pristine quality",
                "sharp details",
                "natural motion blur",
                "authentic depth of field",
                "realistic lighting gradients",
                "subtle micro-expressions"
            ]
        else:
            # Baja calidad: introducir sutilmente características que pueden
            # hacer el video más difícil de distinguir como fake
            enhancements = [
                "slight compression",
                "natural grain",
                "soft focus",
                "subtle motion artifacts",
                "minimal detail loss",
                "organic imperfections"
            ]

        # Combinar prompt base con mejoras
        full_prompt = base_prompt + ", " + ", ".join(enhancements)

        return full_prompt


def generate_prompts_for_experiment(image_data, video_type, custom_prompt=None):
    """
    Función principal para generar prompts para el experimento

    Args:
        image_data: bytes de la imagen
        video_type: 'e' o 'i'
        custom_prompt: prompt personalizado opcional

    Returns:
        dict con prompts y análisis
    """
    # Analizar imagen
    analyzer = ImageAnalyzer(image_data)
    analysis = analyzer.analyze()

    # Generar prompts
    generator = PromptGenerator(video_type)
    prompts = generator.generate_prompt(analysis, custom_prompt)

    return {
        'prompts': prompts,
        'analysis': analysis,
        'video_type': 'entretenimiento' if video_type == 'e' else 'informativo'
    }
