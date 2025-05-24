# 🧮 Integrales Dobles - Software Educativo

Un software educativo interactivo diseñado para facilitar la comprensión y visualización de integrales dobles, con énfasis en el cambio de variables a coordenadas polares y sus aplicaciones prácticas.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Uso del Software](#-uso-del-software)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Descripción de Módulos](#-descripción-de-módulos)
- [Ejemplos de Aplicación](#-ejemplos-de-aplicación)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)
- [Contacto](#-contacto)
- [Créditos](#-créditos)

## ✨ Características

### 🎯 Características Principales

- **Visualización Interactiva**: Gráficos 2D y 3D de alta calidad con herramientas de zoom, rotación y desplazamiento
- **Cálculos Precisos**: Integración numérica y simbólica con comparación de resultados teóricos
- **Interfaz Intuitiva**: Diseño amigable con pestañas organizadas por temas
- **Personalización**: Parámetros ajustables en tiempo real para explorar diferentes escenarios
- **Enfoque Educativo**: Explicaciones teóricas claras con ejemplos progresivos

### 📚 Módulos Educativos

1. **Introducción Teórica**: Conceptos fundamentales de integrales dobles
2. **Transformación de Coordenadas**: Visualización de curvas en coordenadas polares
3. **Cálculo de Áreas y Volúmenes**: Aplicaciones geométricas
4. **Momentos de Inercia**: Aplicaciones en física e ingeniería
5. **Valores Promedio**: Aplicaciones en termodinámica y electromagnetismo
6. **Integrales Personalizadas**: Herramienta para definir problemas propios
7. **Ayuda y Documentación**: Guías de uso e información de contacto

## 💻 Requisitos del Sistema

### Requisitos Mínimos

- **Sistema Operativo**: Windows 10, macOS 10.14, o Linux (Ubuntu 18.04+)
- **Python**: Versión 3.7 o superior
- **RAM**: 4 GB mínimo, 8 GB recomendado
- **Espacio en Disco**: 500 MB libres
- **Resolución**: 1024x768 mínimo, 1920x1080 recomendado

### Dependencias de Python

\`\`\`
matplotlib >= 3.3.0
numpy >= 1.19.0
scipy >= 1.5.0
sympy >= 1.6.0
tkinter (incluido con Python)
\`\`\`

## 🚀 Instalación

### Opción 1: Instalación Rápida

1. **Clonar el repositorio**:
   \`\`\`bash
   git clone https://github.com/tu-usuario/integrales-dobles.git
   cd integrales-dobles
   \`\`\`

2. **Instalar dependencias**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Ejecutar el programa**:
   \`\`\`bash
   python main.py
   \`\`\`

### Opción 2: Instalación con Entorno Virtual

1. **Crear entorno virtual**:
   \`\`\`bash
   python -m venv venv
   \`\`\`

2. **Activar entorno virtual**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Instalar dependencias**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Ejecutar el programa**:
   \`\`\`bash
   python main.py
   \`\`\`

### Opción 3: Instalación Manual

Si prefieres instalar las dependencias manualmente:

\`\`\`bash
pip install matplotlib numpy scipy sympy
python main.py
\`\`\`

## 📖 Uso del Software

### Inicio Rápido

1. **Ejecutar el programa**: `python main.py`
2. **Explorar la pestaña de Introducción** para familiarizarte con los conceptos
3. **Navegar por las diferentes pestañas** según tu interés
4. **Ajustar parámetros** para ver cómo afectan los resultados
5. **Utilizar las herramientas de visualización** para explorar los gráficos

### Guía por Pestañas

#### 🏠 Introducción
- Conceptos teóricos fundamentales
- Visualización de transformaciones de coordenadas
- Ejemplos básicos de regiones y funciones

#### 🔄 Ejemplos de Transformación
- Selecciona entre cardioide, círculo, lemniscata y espiral
- Ajusta parámetros para modificar las curvas
- Observa cálculos de área en tiempo real

#### 📐 Áreas y Volúmenes
- Calcula áreas de cardioides
- Determina volúmenes de semiesperas
- Compara resultados numéricos con fórmulas exactas

#### ⚖️ Momentos de Inercia
- Explora distribuciones de densidad variable
- Calcula momentos de inercia para diferentes geometrías
- Visualiza el efecto de los parámetros físicos

#### 📊 Valores Promedio
- Calcula valores promedio de funciones sobre regiones
- Ejemplos de distribución de temperatura
- Aplicaciones en campos vectoriales

#### ⚙️ Integrales Personalizadas
- Define tus propias funciones para integrar
- Establece límites de integración personalizados
- Elige entre coordenadas cartesianas y polares

## 📁 Estructura del Proyecto

\`\`\`
integrales-dobles/
├── 📄 main.py                     # Punto de entrada principal
├── 📄 requirements.txt            # Dependencias del proyecto
├── 📄 README.md                   # Este archivo
├── 📁 gui/                        # Módulo de interfaz gráfica
│   ├── 📄 __init__.py
│   ├── 📄 app.py                  # Aplicación principal
│   └── 📁 tabs/                   # Pestañas de la aplicación
│       ├── 📄 __init__.py
│       ├── 📄 intro_tab.py        # Pestaña de introducción
│       ├── 📄 transformation_tab.py # Transformaciones
│       ├── 📄 areas_volumes_tab.py # Áreas y volúmenes
│       ├── 📄 moments_tab.py      # Momentos de inercia
│       ├── 📄 average_values_tab.py # Valores promedio
│       ├── 📄 custom_integral_tab.py # Integrales personalizadas
│       ├── 📄 help_tab.py         # Ayuda
│       └── 📄 credits_tab.py      # Créditos
└── 📁 utils/                      # Módulo de utilidades
    ├── 📄 __init__.py
    ├── 📄 calculations.py         # Cálculos matemáticos
    ├── 📄 plotting.py             # Funciones de visualización
    ├── 📄 transformations.py      # Transformaciones de coordenadas
    └── 📄 custom_integral.py      # Integrales personalizadas
\`\`\`

## 🔧 Descripción de Módulos

### main.py
Punto de entrada principal que inicializa la aplicación Tkinter y crea la ventana principal.

### gui/app.py
Contiene la clase `IntegralesApp`, que gestiona la interfaz de usuario y las pestañas.

### gui/tabs/
Directorio con las diferentes pestañas de la aplicación:
- **intro_tab.py**: Introducción teórica y conceptos básicos
- **transformation_tab.py**: Visualización de transformaciones de coordenadas
- **areas_volumes_tab.py**: Cálculo de áreas y volúmenes
- **moments_tab.py**: Cálculo de momentos de inercia
- **average_values_tab.py**: Cálculo de valores promedio
- **custom_integral_tab.py**: Herramienta para integrales personalizadas
- **help_tab.py**: Información de ayuda y contacto
- **credits_tab.py**: Información de desarrolladores

### utils/
Directorio con funciones de utilidad:
- **calculations.py**: Funciones para cálculos matemáticos
- **plotting.py**: Funciones para visualización de gráficos
- **transformations.py**: Transformaciones entre sistemas de coordenadas
- **custom_integral.py**: Evaluación de integrales dobles personalizadas

## 🎯 Ejemplos de Aplicación

### Cálculo del Área de un Cardioide

\`\`\`python
# Función que define el cardioide
def r_cardioide(theta):
    return a * (1 + np.cos(theta))

# Cálculo del área usando coordenadas polares
area = ∫∫ r dr dθ = 6πa²
\`\`\`

### Volumen de una Semiesfera

\`\`\`python
# Función de la semiesfera
def f(r, theta):
    return np.sqrt(R**2 - r**2) * r  # Incluye jacobiano

# Volumen = (2/3)πR³
\`\`\`

### Momento de Inercia con Densidad Variable

\`\`\`python
# Densidad variable
def densidad(r):
    return rho_0 * (1 - (r/R)**2)

# Momento de inercia = πρ₀R⁴/6
\`\`\`

## 📸 Capturas de Pantalla

### Pestaña de Introducción
![Introducción](docs/images/intro_tab.png)

### Visualización de Cardioide
![Cardioide](docs/images/cardioid_example.png)

### Cálculo de Volumen 3D
![Volumen 3D](docs/images/volume_3d.png)

*Nota: Las imágenes se encuentran en el directorio `docs/images/`*

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto:

### Cómo Contribuir

1. **Fork el repositorio**
2. **Crea una rama para tu característica**:
   \`\`\`bash
   git checkout -b feature/nueva-caracteristica
   \`\`\`
3. **Realiza tus cambios y haz commit**:
   \`\`\`bash
   git commit -am 'Añadir nueva característica'
   \`\`\`
4. **Push a la rama**:
   \`\`\`bash
   git push origin feature/nueva-caracteristica
   \`\`\`
5. **Crea un Pull Request**

### Tipos de Contribuciones

- 🐛 Reportar bugs
- 💡 Sugerir nuevas características
- 📝 Mejorar documentación
- 🎨 Mejorar la interfaz de usuario
- ⚡ Optimizar rendimiento
- 🧪 Añadir tests

### Guías de Contribución

- Sigue el estilo de código existente
- Incluye documentación para nuevas características
- Añade tests cuando sea apropiado
- Actualiza el README si es necesario

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

\`\`\`
MIT License

Copyright (c) 2023 Integrales Dobles Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
\`\`\`

## 📞 Contacto

### Información de Contacto

- **📱 WhatsApp**: +57 3106014652
- **✉️ Email**: dylanjaredbautistasierra03@gmail.com
- **🌐 GitHub**: [https://github.com/tu-usuario/integrales-dobles](https://github.com/tu-usuario/integrales-dobles)

### Soporte

Si tienes preguntas, problemas o sugerencias:

1. **Revisa la documentación** en la pestaña de Ayuda del software
2. **Busca en los issues** existentes en GitHub
3. **Crea un nuevo issue** si no encuentras solución
4. **Contacta directamente** usando la información proporcionada

## 👥 Créditos

### Desarrolladores

- **👨‍💻 Dylan Jared Bautista Sierra** - Desarrollador Principal
- **👨‍💻 Daniel Alejandro Arevalo Guecha** - Desarrollador
- **👨‍💻 Juan Marco Parada Carpio** - Desarrollador

### Docente

- **👨‍🏫 ING. Darwin Orlando Cardozo Sarmiento** - Supervisor Académico

### Institución

**Universidad Francisco de Paula Santander**  
Departamento de Matemáticas  
2023

### Agradecimientos

- A la Universidad Francisco de Paula Santander por el apoyo institucional
- Al Departamento de Matemáticas por los recursos proporcionados
- A la comunidad de Python por las excelentes bibliotecas utilizadas
- A todos los estudiantes que proporcionaron retroalimentación durante el desarrollo

---

### 🌟 ¿Te gusta el proyecto?

Si este software te ha sido útil, considera:

- ⭐ Dar una estrella al repositorio
- 🐛 Reportar bugs o sugerir mejoras
- 📢 Compartir el proyecto con otros estudiantes
- 🤝 Contribuir al desarrollo

---

**Desarrollado con ❤️ para estudiantes de cálculo multivariable**

*Última actualización: Diciembre 2023*
\`\`\`

Este README es completo y profesional, incluyendo todas las secciones importantes que debe tener un proyecto de software educativo. Incluye badges, emojis para mejor legibilidad, estructura clara, y toda la información necesaria para que cualquier persona pueda entender, instalar y usar el software.
