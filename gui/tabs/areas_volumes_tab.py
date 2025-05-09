import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from matplotlib import cm
from scipy import integrate
import sympy as sp
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class AreasVolumesTab:
    """Pestaña para el cálculo de áreas y volúmenes"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de áreas y volúmenes"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Áreas y Volúmenes")
        
        # Título
        title_label = ttk.Label(self.frame, text="Cálculo de Áreas y Volúmenes", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Marco principal con dos columnas
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Marco para controles (izquierda)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, expand=False)
        
        # Selector de ejemplo
        ttk.Label(controls_frame, text="Seleccione un ejemplo:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.example_var = tk.StringVar(value="cardioide")
        examples = ttk.Combobox(controls_frame, textvariable=self.example_var, 
                              values=["cardioide", "paraboloide"])
        examples.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        examples.bind("<<ComboboxSelected>>", self.update_example)
        
        # Marco para parámetros
        params_frame = ttk.LabelFrame(controls_frame, text="Parámetros")
        params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Parámetro a
        ttk.Label(params_frame, text="Parámetro a:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.param_a = ttk.Scale(params_frame, from_=0.5, to=3.0, orient=tk.HORIZONTAL, length=200)
        self.param_a.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.param_a.set(2.0)
        self.param_a_label = ttk.Label(params_frame, text="2.0")
        self.param_a_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.param_a.bind("<Motion>", self.update_param_a)
        
        # Botón para calcular
        calculate_button = ttk.Button(controls_frame, text="Calcular", command=self.calculate_example)
        calculate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        
        # Marco para resultados
        results_frame = ttk.LabelFrame(controls_frame, text="Resultados")
        results_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Etiqueta para resultados
        self.result_label = ttk.Label(results_frame, text="", wraplength=300)
        self.result_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Marco para la visualización (derecha)
        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas para diferentes visualizaciones
        viz_notebook = ttk.Notebook(viz_frame)
        viz_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña para la región
        self.region_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.region_frame, text="Región")
        
        # Pestaña para la visualización 3D
        self.viz_3d_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.viz_3d_frame, text="Visualización 3D")
        
        # Crear figuras iniciales
        self.create_region_figure()
        self.create_3d_figure()
        
        # Calcular el ejemplo inicial
        self.calculate_example()
    
    def update_param_a(self, event=None):
        """Actualiza la etiqueta del parámetro a"""
        value = self.param_a.get()
        self.param_a_label.config(text=f"{value:.1f}")
    
    def update_example(self, event=None):
        """Actualiza el ejemplo seleccionado"""
        self.calculate_example()
    
    def calculate_example(self):
        """Calcula el ejemplo seleccionado"""
        example = self.example_var.get()
        a = self.param_a.get()
        
        if example == "cardioide":
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # En coordenadas polares, el área es ∫∫ r dr dθ
            def integrando_area(r, theta):
                return r  # Solo el jacobiano para calcular el área
            
            # Integración numérica
            area_numerica, error = integrate.dblquad(
                integrando_area,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, r_cardioide  # límites de r
            )
            
            # Cálculo simbólico para verificar
            theta = sp.symbols('theta')
            r_sym = a * (1 + sp.cos(theta))
            area_simbolica = sp.integrate(r_sym**2 / 2, (theta, 0, 2*sp.pi))
            
            # Mostrar resultados
            result_text = f"Cardioide: r = {a:.1f}(1 + cos(θ))\n\n"
            result_text += f"Área numérica: {area_numerica:.6f}\n"
            if area_simbolica is not None:
                result_text += f"Área simbólica: {float(area_simbolica):.6f}\n"
            else:
                result_text += f"Área simbólica: No disponible\n"
            result_text += f"Fórmula exacta: 6πa² = {6*np.pi*a**2:.6f}"
            
        elif example == "paraboloide":
            # Definimos la función a integrar
            def f_cartesiana(x, y):
                return 4 - x**2 - y**2
            
            # En coordenadas polares
            def f_polar(r, theta):
                # x = r*cos(theta), y = r*sin(theta)
                # x² + y² = r²
                return (4 - r**2) * r  # Multiplicamos por r (jacobiano)
            
            # Integración numérica
            volumen, error = integrate.dblquad(
                f_polar,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, lambda theta: 1  # límites de r (círculo de radio 1)
            )
            
            # Cálculo simbólico
            r, theta = sp.symbols('r theta')
            f_sym = (4 - r**2) * r
            vol_simbolico = sp.integrate(f_sym, (r, 0, 1))
            vol_simbolico = sp.integrate(vol_simbolico, (theta, 0, 2*sp.pi))
            
            # Mostrar resultados
            result_text = f"Volumen bajo z = 4 - x² - y²\n"
            result_text += f"sobre un círculo de radio 1\n\n"
            result_text += f"Volumen numérico: {volumen:.6f}\n"
            if vol_simbolico is not None:
                result_text += f"Volumen simbólico: {float(vol_simbolico):.6f}\n"
            else:
                result_text += f"Volumen simbólico: No disponible\n"
            result_text += f"Fórmula exacta: 2π = {2*np.pi:.6f}"
        
        # Actualizar la etiqueta de resultados
        self.result_label.config(text=result_text)
        
        # Actualizar las figuras
        self.create_region_figure()
        self.create_3d_figure()
    
    def create_region_figure(self):
        """Crea la figura para visualizar la región"""
        # Limpiar el marco
        for widget in self.region_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111, aspect='equal')
        
        # Obtener los parámetros
        example = self.example_var.get()
        a = self.param_a.get()
        
        if example == "cardioide":
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
            ax.set_xlim(-3*a, 3*a)
            ax.set_ylim(-3*a, 3*a)
            ax.grid(True)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f"Cardioide: r = {a:.1f}(1 + cos(θ))")
            
        elif example == "paraboloide":
            # Dibujar un círculo de radio 1
            circle = plt.Circle((0, 0), 1, fill=True, alpha=0.3)
            ax.add_patch(circle)
            
            # Configurar los ejes
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.grid(True)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title("Región: círculo de radio 1")
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.region_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.region_frame)
        toolbar.update()
    
    def create_3d_figure(self):
        """Crea la figura para visualización 3D"""
        # Limpiar el marco
        for widget in self.viz_3d_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        # Obtener los parámetros
        example = self.example_var.get()
        a = self.param_a.get()
        
        if example == "cardioide":
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # Valores para graficar
            theta_vals = np.linspace(0, 2*np.pi, 50)
            r_vals = np.linspace(0, 3*a, 20)
            
            # Crear una malla
            Theta, R = np.meshgrid(theta_vals, r_vals)
            X = R * np.cos(Theta)
            Y = R * np.sin(Theta)
            Z = np.ones_like(X)  # Superficie plana z = 1
            
            # Crear una máscara para mostrar solo dentro del cardioide
            mask = R <= np.array([r_cardioide(t) for t in Theta[0, :]])
            
            # Dibujar la superficie
            surf = ax.plot_surface(
                X * mask, Y * mask, Z * mask,
                cmap='viridis', alpha=0.8
            )
            
            # Configurar los ejes
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title(f"Superficie z = 1 sobre cardioide")
            
        elif example == "paraboloide":
            # Crear una malla de puntos
            r = np.linspace(0, 1, 50)
            theta = np.linspace(0, 2*np.pi, 50)
            r, theta = np.meshgrid(r, theta)
            
            # Convertir a coordenadas cartesianas
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            # Calcular z
            z = 4 - x**2 - y**2
            
            # Dibujar la superficie
            surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.8)
            
            # Configurar los ejes
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title('Superficie z = 4 - x² - y²')
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.viz_3d_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.viz_3d_frame)
        toolbar.update()
