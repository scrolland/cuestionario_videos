// ==========================================================================
// Gráficos Interactivos - Investigación Deepfakes y C2PA
// Datos extraídos del documento de investigación
// ==========================================================================

// Configuración global de Chart.js
Chart.defaults.font.family = "'Helvetica Neue', 'Arial', sans-serif";
Chart.defaults.color = '#2c3e50';

// Colores del tema
const colors = {
    primary: '#1a5490',
    secondary: '#2c7ab5',
    accent: '#f39c12',
    success: '#27ae60',
    warning: '#e67e22',
    danger: '#c0392b',
    info: '#3498db',
    purple: '#9b59b6',
    teal: '#16a085'
};

// Función helper para crear gradientes
function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}

// ==========================================================================
// 1. Diseño Factorial del Corpus
// ==========================================================================
window.addEventListener('load', function() {
    const factorialCtx = document.getElementById('factorialDesignChart');
    if (factorialCtx) {
        new Chart(factorialCtx, {
            type: 'bar',
            data: {
                labels: ['Autenticidad', 'Calidad Técnica', 'Temática', 'Duración'],
                datasets: [{
                    label: 'Niveles por Factor',
                    data: [2, 3, 3, 3],
                    backgroundColor: [
                        colors.primary,
                        colors.secondary,
                        colors.accent,
                        colors.success
                    ],
                    borderColor: colors.primary,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Diseño Factorial Completo: 2 × 3 × 3 × 3 = 162 Estímulos',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 4,
                        title: {
                            display: true,
                            text: 'Número de Niveles'
                        }
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 2. Sistema de Etiquetado Multimodal
    // ==========================================================================
    const labelingCtx = document.getElementById('labelingSystemChart');
    if (labelingCtx) {
        new Chart(labelingCtx, {
            type: 'radar',
            data: {
                labels: ['Tasa Detección', 'Calidad Visual', 'Resistencia', 'Velocidad', 'Compatibilidad'],
                datasets: [
                    {
                        label: 'Visible - Alta Opacidad',
                        data: [100, 60, 0, 98, 100],
                        backgroundColor: 'rgba(26, 84, 144, 0.2)',
                        borderColor: colors.primary,
                        borderWidth: 2
                    },
                    {
                        label: 'Marca de Agua DCT',
                        data: [88, 95, 85, 80, 90],
                        backgroundColor: 'rgba(39, 174, 96, 0.2)',
                        borderColor: colors.success,
                        borderWidth: 2
                    },
                    {
                        label: 'Metadatos XMP',
                        data: [95, 100, 60, 95, 85],
                        backgroundColor: 'rgba(243, 156, 18, 0.2)',
                        borderColor: colors.accent,
                        borderWidth: 2
                    },
                    {
                        label: 'C2PA Completo',
                        data: [100, 98, 95, 70, 95],
                        backgroundColor: 'rgba(192, 57, 43, 0.2)',
                        borderColor: colors.danger,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Comparación de Sistemas de Etiquetado (Escala 0-100)',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 3. Diseño Experimental
    // ==========================================================================
    const experimentalCtx = document.getElementById('experimentalDesignChart');
    if (experimentalCtx) {
        new Chart(experimentalCtx, {
            type: 'doughnut',
            data: {
                labels: ['Condición A: Control', 'Condición B: Visible', 'Condición C: C2PA'],
                datasets: [{
                    label: 'Distribución de Participantes',
                    data: [39, 40, 39],
                    backgroundColor: [
                        colors.danger,
                        colors.warning,
                        colors.success
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Distribución de Participantes por Condición (N=118)',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 4. Características de la Muestra
    // ==========================================================================
    const sampleCtx = document.getElementById('sampleCharacteristicsChart');
    if (sampleCtx) {
        new Chart(sampleCtx, {
            type: 'bar',
            data: {
                labels: ['Condición A', 'Condición B', 'Condición C'],
                datasets: [
                    {
                        label: 'Edad Media (años)',
                        data: [37.9, 39.2, 38.1],
                        backgroundColor: colors.primary,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Alfabetización Digital (1-5)',
                        data: [3.7, 3.9, 3.8],
                        backgroundColor: colors.accent,
                        yAxisID: 'y1'
                    },
                    {
                        label: 'Familiaridad IA (1-5)',
                        data: [3.1, 3.3, 3.2],
                        backgroundColor: colors.success,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Características Demográficas por Condición',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Edad (años)'
                        },
                        min: 0,
                        max: 50
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Escalas 1-5'
                        },
                        min: 0,
                        max: 5,
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 5. Rendimiento de Runway ML
    // ==========================================================================
    const runwayCtx = document.getElementById('runwayPerformanceChart');
    if (runwayCtx) {
        new Chart(runwayCtx, {
            type: 'line',
            data: {
                labels: ['CFG 7.5', 'CFG 12.5', 'CFG 15.0', '25 Steps', '50 Steps', '100 Steps'],
                datasets: [
                    {
                        label: 'Tasa de Éxito (%)',
                        data: [92, 85, 78, 80, 88, 87],
                        borderColor: colors.success,
                        backgroundColor: 'rgba(39, 174, 96, 0.1)',
                        tension: 0.3,
                        fill: true,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Tiempo Promedio (s)',
                        data: [45, 52, 61, 38, 55, 89],
                        borderColor: colors.danger,
                        backgroundColor: 'rgba(192, 57, 43, 0.1)',
                        tension: 0.3,
                        fill: true,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Rendimiento de Runway ML según Parámetros de Configuración',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Tasa de Éxito (%)'
                        },
                        min: 70,
                        max: 100
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Tiempo (segundos)'
                        },
                        min: 0,
                        max: 100,
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 6. Métricas de Calidad Objetiva
    // ==========================================================================
    const qualityCtx = document.getElementById('qualityMetricsChart');
    if (qualityCtx) {
        new Chart(qualityCtx, {
            type: 'bar',
            data: {
                labels: ['Real - Alta', 'Sintético - Alta', 'Sintético - Media', 'Sintético - Baja'],
                datasets: [
                    {
                        label: 'PSNR (dB)',
                        data: [38.2, 32.8, 29.4, 25.1],
                        backgroundColor: colors.primary
                    },
                    {
                        label: 'SSIM (×100)',
                        data: [95, 88, 82, 73],
                        backgroundColor: colors.secondary
                    },
                    {
                        label: 'VMAF',
                        data: [92.5, 85.3, 76.8, 65.4],
                        backgroundColor: colors.accent
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Métricas de Calidad Objetiva del Corpus Generado',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Puntuación'
                        }
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 7. Evaluación Sistema de Etiquetado
    // ==========================================================================
    const labelingEvalCtx = document.getElementById('labelingEvaluationChart');
    if (labelingEvalCtx) {
        new Chart(labelingEvalCtx, {
            type: 'horizontalBar',
            data: {
                labels: ['Visible - Alta', 'Visible - Baja', 'Marca Agua DCT', 'Metadatos XMP', 'Código QR', 'C2PA'],
                datasets: [
                    {
                        label: 'Tasa de Detección (%)',
                        data: [100, 92, 88, 95, 98, 100],
                        backgroundColor: colors.success
                    },
                    {
                        label: 'Resistencia a Manipulación (%)',
                        data: [0, 0, 85, 60, 20, 95],
                        backgroundColor: colors.warning
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Efectividad de Sistemas de Etiquetado Multimodal',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Porcentaje'
                        }
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 8. Credibilidad Percibida
    // ==========================================================================
    const credibilityCtx = document.getElementById('credibilityChart');
    if (credibilityCtx) {
        new Chart(credibilityCtx, {
            type: 'bar',
            data: {
                labels: ['Real - Sin etiqueta', 'Real - Visible', 'Real - C2PA',
                         'Sintético - Sin etiqueta', 'Sintético - Visible', 'Sintético - C2PA'],
                datasets: [{
                    label: 'Credibilidad Percibida (Escala 1-7)',
                    data: [5.1, 4.9, 5.0, 3.8, 3.2, 3.0],
                    backgroundColor: [
                        colors.success, colors.success, colors.success,
                        colors.danger, colors.danger, colors.danger
                    ],
                    borderColor: colors.primary,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Credibilidad Percibida por Condición Experimental',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 7,
                        title: {
                            display: true,
                            text: 'Puntuación Likert (1-7)'
                        }
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 9. Exactitud en Detección
    // ==========================================================================
    const detectionCtx = document.getElementById('detectionAccuracyChart');
    if (detectionCtx) {
        new Chart(detectionCtx, {
            type: 'line',
            data: {
                labels: ['Sin etiqueta', 'Etiqueta visible', 'C2PA completo'],
                datasets: [
                    {
                        label: 'Precisión (%)',
                        data: [58.3, 64.7, 68.9],
                        borderColor: colors.primary,
                        backgroundColor: 'rgba(26, 84, 144, 0.2)',
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Sensibilidad (%)',
                        data: [55.2, 62.8, 67.5],
                        borderColor: colors.success,
                        backgroundColor: 'rgba(39, 174, 96, 0.2)',
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Especificidad (%)',
                        data: [61.4, 66.6, 70.3],
                        borderColor: colors.accent,
                        backgroundColor: 'rgba(243, 156, 18, 0.2)',
                        tension: 0.3,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Exactitud en Detección de Contenido Sintético',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 80,
                        title: {
                            display: true,
                            text: 'Porcentaje'
                        }
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 10. Curvas ROC
    // ==========================================================================
    const rocCtx = document.getElementById('rocCurveChart');
    if (rocCtx) {
        new Chart(rocCtx, {
            type: 'line',
            data: {
                labels: Array.from({length: 11}, (_, i) => (i * 10).toString()),
                datasets: [
                    {
                        label: 'Sin etiqueta (AUC=0.68)',
                        data: [0, 12, 24, 35, 45, 55, 65, 73, 81, 90, 100],
                        borderColor: colors.danger,
                        backgroundColor: 'rgba(192, 57, 43, 0.1)',
                        tension: 0.3,
                        fill: false,
                        borderWidth: 2
                    },
                    {
                        label: 'Etiqueta visible (AUC=0.75)',
                        data: [0, 15, 30, 44, 56, 67, 77, 85, 92, 97, 100],
                        borderColor: colors.warning,
                        backgroundColor: 'rgba(230, 126, 34, 0.1)',
                        tension: 0.3,
                        fill: false,
                        borderWidth: 2
                    },
                    {
                        label: 'C2PA completo (AUC=0.82)',
                        data: [0, 18, 35, 51, 65, 76, 85, 91, 96, 99, 100],
                        borderColor: colors.success,
                        backgroundColor: 'rgba(39, 174, 96, 0.1)',
                        tension: 0.3,
                        fill: false,
                        borderWidth: 3
                    },
                    {
                        label: 'Referencia (AUC=0.50)',
                        data: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                        borderColor: '#95a5a6',
                        borderDash: [5, 5],
                        tension: 0,
                        fill: false,
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Curvas ROC por Condición Experimental',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Tasa de Falsos Positivos (%)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Tasa de Verdaderos Positivos (%)'
                        },
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 11. Calibración Precisión-Confianza
    // ==========================================================================
    const calibrationCtx = document.getElementById('calibrationChart');
    if (calibrationCtx) {
        new Chart(calibrationCtx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Sin etiqueta (r=0.42)',
                        data: [
                            {x: 30, y: 45}, {x: 45, y: 55}, {x: 55, y: 67},
                            {x: 65, y: 75}, {x: 75, y: 83}, {x: 85, y: 90}
                        ],
                        backgroundColor: colors.danger,
                        borderColor: colors.danger,
                        showLine: true,
                        tension: 0.3
                    },
                    {
                        label: 'Etiqueta visible (r=0.58)',
                        data: [
                            {x: 35, y: 48}, {x: 48, y: 58}, {x: 58, y: 68},
                            {x: 68, y: 77}, {x: 78, y: 85}, {x: 88, y: 92}
                        ],
                        backgroundColor: colors.warning,
                        borderColor: colors.warning,
                        showLine: true,
                        tension: 0.3
                    },
                    {
                        label: 'C2PA completo (r=0.67)',
                        data: [
                            {x: 40, y: 48}, {x: 50, y: 56}, {x: 60, y: 64},
                            {x: 70, y: 73}, {x: 80, y: 84}, {x: 90, y: 93}
                        ],
                        backgroundColor: colors.success,
                        borderColor: colors.success,
                        showLine: true,
                        tension: 0.3
                    },
                    {
                        label: 'Calibración perfecta',
                        data: [{x: 0, y: 0}, {x: 100, y: 100}],
                        borderColor: '#95a5a6',
                        borderDash: [5, 5],
                        showLine: true,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Calibración entre Precisión Objetiva y Confianza Subjetiva',
                        font: { size: 16, weight: 'bold' }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Precisión Real (%)'
                        },
                        min: 0,
                        max: 100
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Confianza Reportada (%)'
                        },
                        min: 0,
                        max: 100
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 12. Factores Moderadores
    // ==========================================================================
    const moderatorsCtx = document.getElementById('moderatorsChart');
    if (moderatorsCtx) {
        new Chart(moderatorsCtx, {
            type: 'bar',
            data: {
                labels: ['Alfabetización Digital', 'Edad', 'Familiaridad IA', 'Consumo Vídeo'],
                datasets: [{
                    label: 'Coeficiente β',
                    data: [0.32, -0.28, 0.25, 0.18],
                    backgroundColor: function(context) {
                        const value = context.parsed.y;
                        return value > 0 ? colors.success : colors.danger;
                    },
                    borderColor: colors.primary,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Efectos de Factores Moderadores en la Efectividad del Etiquetado',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Coeficiente β (Efecto Estandarizado)'
                        },
                        min: -0.4,
                        max: 0.4
                    }
                }
            }
        });
    }

    // ==========================================================================
    // 13. Estrategias de Detección
    // ==========================================================================
    const strategiesCtx = document.getElementById('strategiesChart');
    if (strategiesCtx) {
        new Chart(strategiesCtx, {
            type: 'bubble',
            data: {
                datasets: [
                    {
                        label: 'Análisis Movimientos',
                        data: [{x: 71.2, y: 74.5, r: 34}],
                        backgroundColor: 'rgba(26, 84, 144, 0.6)',
                        borderColor: colors.primary
                    },
                    {
                        label: 'Evaluación Expresiones',
                        data: [{x: 65.8, y: 69.3, r: 28}],
                        backgroundColor: 'rgba(39, 174, 96, 0.6)',
                        borderColor: colors.success
                    },
                    {
                        label: 'Detalle Visual/Texturas',
                        data: [{x: 62.4, y: 66.7, r: 22}],
                        backgroundColor: 'rgba(243, 156, 18, 0.6)',
                        borderColor: colors.accent
                    },
                    {
                        label: 'Coherencia Iluminación',
                        data: [{x: 59.1, y: 63.2, r: 15}],
                        backgroundColor: 'rgba(155, 89, 182, 0.6)',
                        borderColor: colors.purple
                    },
                    {
                        label: 'Intuición General',
                        data: [{x: 53.7, y: 61.8, r: 42}],
                        backgroundColor: 'rgba(192, 57, 43, 0.6)',
                        borderColor: colors.danger
                    },
                    {
                        label: 'Confianza en Etiquetas',
                        data: [{x: 68.9, y: 72.1, r: 67}],
                        backgroundColor: 'rgba(22, 160, 133, 0.6)',
                        borderColor: colors.teal
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Estrategias de Detección: Precisión vs Confianza (tamaño = frecuencia)',
                        font: { size: 16, weight: 'bold' }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += `Precisión ${context.parsed.x}%, Confianza ${context.parsed.y}%, Frecuencia ${context.parsed._custom}%`;
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Precisión Asociada (%)'
                        },
                        min: 45,
                        max: 80
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Confianza Media (%)'
                        },
                        min: 55,
                        max: 80
                    }
                }
            }
        });
    }
});
