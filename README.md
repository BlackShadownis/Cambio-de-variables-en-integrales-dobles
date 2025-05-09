### Integrales Dobles - Software Educativo











Un software educativo interactivo para visualizar y comprender integrales dobles, transformaciones de coordenadas y sus aplicaciones en física y matemáticas.





## 📋 Contenido

- [Características](#características)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Documentación Técnica](#documentación-técnica)
- [Contribuir](#contribuir)
- [Preguntas Frecuentes](#preguntas-frecuentes)
- [Licencia](#licencia)
- [Contacto](#contacto)


## ✨ Características

- **Visualización Interactiva**: Explora conceptos matemáticos complejos a través de gráficos interactivos
- **Transformación de Coordenadas**: Animaciones que muestran la transformación entre coordenadas cartesianas y polares
- **Proceso de Integración**: Visualización paso a paso del proceso de integración doble
- **Aplicaciones Prácticas**:

- 📏 Cálculo de áreas y volúmenes
- 🔄 Momentos de inercia
- 📊 Valores promedio



- **Integrales Personalizadas**: Define tus propias funciones y límites de integración
- **Interfaz Amigable**: Diseñada para estudiantes y educadores


## 📸 Capturas de Pantalla






![Captura de pantalla 2025-05-08 210828](https://github.com/user-attachments/assets/5791477d-3fad-4777-887e-8502ae7dce55)





</div>## 🔧 Requisitos

- Python 3.7 o superior
- Bibliotecas:

- tkinter (incluido en la mayoría de instalaciones de Python)
- matplotlib
- numpy
- scipy
- sympy





## 💻 Instalación

### Usando Git

```shellscript
# Clonar el repositorio
git clone https://github.com/tu-usuario/integrales-dobles.git
cd integrales-dobles

# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Descarga directa

1. Descarga el [archivo ZIP](https://github.com/tu-usuario/integrales-dobles/archive/refs/heads/main.zip)
2. Extrae el contenido
3. Abre una terminal en la carpeta extraída
4. Instala las dependencias:


```shellscript
pip install matplotlib numpy scipy sympy
```

## 🚀 Uso

Para iniciar la aplicación:

```shellscript
python main.py
```

### Guía rápida

1. **Pestaña de Introducción**: Familiarízate con los conceptos teóricos
2. **Pestaña de Animaciones**: Explora la transformación entre sistemas de coordenadas

1. Selecciona el tipo de animación
2. Ajusta la velocidad y número de puntos
3. Usa los controles para reproducir, pausar y reiniciar



3. **Pestaña de Proceso de Integración**: Visualiza el proceso de integración paso a paso

1. Elige entre diferentes ejemplos (círculo, cardioide, paraboloide)
2. Ajusta el número de divisiones para ver cómo afecta la precisión



4. **Pestañas de Aplicaciones**: Explora las aplicaciones prácticas (áreas, volúmenes, momentos, valores promedio)
5. **Pestaña de Integrales Personalizadas**: Define y calcula tus propias integrales


## 📁 Estructura del Proyecto

```plaintext
integrales_dobles/
├── main.py                  # Punto de entrada principal
├── requirements.txt         # Dependencias del proyecto
├── gui/                     # Módulo de interfaz gráfica
│   ├── __init__.py
│   ├── app.py               # Clase principal de la aplicación
│   └── tabs/                # Pestañas de la aplicación
│       ├── __init__.py
│       ├── intro_tab.py             # Introducción teórica
│       ├── transformation_tab.py    # Transformación de coordenadas
│       ├── areas_volumes_tab.py     # Cálculo de áreas y volúmenes
│       ├── moments_tab.py           # Momentos de inercia
│       ├── average_values_tab.py    # Valores promedio
│       ├── custom_integral_tab.py   # Integrales personalizadas
│       ├── animation_tab.py         # Animaciones de transformación
│       └── integration_steps_tab.py # Proceso de integración
└── utils/                   # Módulo de utilidades
    ├── __init__.py
    ├── calculations.py      # Funciones para cálculos matemáticos
    ├── plotting.py          # Funciones para visualización
    ├── transformations.py   # Transformaciones de coordenadas
    └── custom_integral.py   # Evaluación de integrales personalizadas
```

## 📚 Documentación Técnica

### Módulos Principales

#### main.py

Punto de entrada que inicializa la aplicación Tkinter y crea la ventana principal.

#### gui/app.py

Contiene la clase `IntegralesApp` que gestiona la interfaz de usuario y crea las pestañas.

#### gui/tabs/

Cada archivo en este directorio implementa una pestaña específica de la aplicación:

- **intro_tab.py**: Introducción teórica a integrales dobles
- **transformation_tab.py**: Visualización de transformaciones de coordenadas
- **animation_tab.py**: Animaciones interactivas de transformación
- **integration_steps_tab.py**: Visualización paso a paso del proceso de integración
- **areas_volumes_tab.py**, **moments_tab.py**, **average_values_tab.py**: Aplicaciones prácticas
- **custom_integral_tab.py**: Evaluación de integrales personalizadas


#### utils/

Funciones de utilidad para cálculos y visualización:

- **calculations.py**: Funciones matemáticas para áreas, volúmenes, etc.
- **plotting.py**: Funciones para crear visualizaciones
- **transformations.py**: Funciones para transformar entre sistemas de coordenadas
- **custom_integral.py**: Funciones para evaluar integrales personalizadas


### Extensión del Software

Para extender el software:

1. **Agregar nuevas pestañas**: Crea un nuevo archivo en `gui/tabs/` siguiendo el patrón de las pestañas existentes
2. **Implementar nuevos cálculos**: Añade funciones en `utils/calculations.py`
3. **Crear nuevas visualizaciones**: Implementa funciones en `utils/plotting.py`
4. **Añadir sistemas de coordenadas**: Extiende `utils/transformations.py`


