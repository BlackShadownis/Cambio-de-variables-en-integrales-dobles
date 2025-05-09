import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class IntroTab:
    """Pestaña de introducción a las integrales dobles"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de introducción"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Introducción")
        
        # Título
        title_label = ttk.Label(self.frame, text="Integrales Dobles con Cambio de Variables", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Marco principal con dos columnas
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Marco para texto (izquierda)
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        # Texto de introducción
        intro_text = """
        TEORÍA DE CAMBIO DE VARIABLES EN INTEGRALES DOBLES
        --------------------------------------------------
        
        En coordenadas cartesianas, una integral doble se expresa como:
        ∫∫_R f(x,y) dA = ∫_a^b ∫_c^d f(x,y) dy dx
        
        En coordenadas polares, usamos la transformación:
        x = r·cos(θ), y = r·sin(θ)
        
        El jacobiano de esta transformación es |J| = r
        
        Por lo tanto, la integral se convierte en:
        ∫∫_R f(x,y) dA = ∫_α^β ∫_0^h(θ) f(r·cos(θ), r·sin(θ)) · r dr dθ
        
        Este cambio es especialmente útil cuando la región de integración
        o la función tienen simetría circular o radial.
        
        APLICACIONES PRINCIPALES:
        
        1. Cálculo de áreas y volúmenes
        2. Momentos de inercia
        3. Valores promedio
        
        Explore las diferentes pestañas para ver ejemplos y aplicaciones.
        """
        
        intro_label = ttk.Label(text_frame, text=intro_text, justify=tk.LEFT, wraplength=500)
        intro_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Marco para visualización (derecha)
        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        # Crear figura para visualización
        self.fig = plt.Figure(figsize=(6, 6))
        
        # Transformación de coordenadas
        ax1 = self.fig.add_subplot(221, aspect='equal')
        self.plot_coordinate_transformation(ax1)
        ax1.set_title("Transformación de coordenadas")
        
        # Ejemplo de región circular
        ax2 = self.fig.add_subplot(222, aspect='equal')
        self.plot_circular_region(ax2)
        ax2.set_title("Región circular")
        
        # Ejemplo de cardioide
        ax3 = self.fig.add_subplot(223, aspect='equal')
        self.plot_cardioid(ax3)
        ax3.set_title("Cardioide r = a(1 + cos(θ))")
        
        # Ejemplo de función
        ax4 = self.fig.add_subplot(224, projection='3d')
        self.plot_3d_function(ax4)
        ax4.set_title("Función z = 4 - x² - y²")
        
        # Ajustar espaciado
        self.fig.tight_layout()
        
        # Agregar el lienzo a la interfaz
        canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def plot_coordinate_transformation(self, ax):
        """Dibuja la transformación de coordenadas cartesianas a polares"""
        # Crear una malla de puntos en coordenadas polares
        r = np.linspace(0, 2, 5)
        theta = np.linspace(0, 2*np.pi, 13)[:-1]  # Excluir el último para evitar duplicados
        
        r_grid, theta_grid = np.meshgrid(r, theta)
        x_grid = r_grid * np.cos(theta_grid)
        y_grid = r_grid * np.sin(theta_grid)
        
        # Dibujar las líneas de coordenadas
        for i in range(len(r)):
            circle = plt.Circle((0, 0), r[i], fill=False, color='blue', alpha=0.5)
            ax.add_patch(circle)
        
        for i in range(len(theta)):
            ax.plot([0, 2*np.cos(theta[i])], [0, 2*np.sin(theta[i])], 'r-', alpha=0.5)
        
        # Dibujar los puntos de la malla
        ax.plot(x_grid, y_grid, 'ko', markersize=3)
        
        # Configurar los ejes
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
    def plot_circular_region(self, ax):
        """Dibuja una región circular"""
        # Crear un círculo
        circle = plt.Circle((0, 0), 1, fill=True, color='blue', alpha=0.3)
        ax.add_patch(circle)
        
        # Configurar los ejes
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
    def plot_cardioid(self, ax):
        """Dibuja un cardioide"""
        # Parámetros
        a = 1.0
        
        # Función que define el cardioide
        def r_cardioide(theta):
            return a * (1 + np.cos(theta))
        
        # Valores para graficar
        theta_vals = np.linspace(0, 2*np.pi, 200)
        r_vals = r_cardioide(theta_vals)
        x = r_vals * np.cos(theta_vals)
        y = r_vals * np.sin(theta_vals)
        
        # Dibujar el cardioide
        ax.plot(x, y, 'b-')
        ax.fill(x, y, alpha=0.3, color='blue')
        
        # Configurar los ejes
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
    def plot_3d_function(self, ax):
        """Dibuja una función 3D"""
        # Crear una malla de puntos
        x = np.linspace(-1, 1, 30)
        y = np.linspace(-1, 1, 30)
        X, Y = np.meshgrid(x, y)
        
        # Calcular los valores de z
        Z = 4 - X**2 - Y**2
        
        # Dibujar la superficie
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        
        # Configurar los ejes
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
