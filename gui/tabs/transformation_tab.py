import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from scipy import integrate
import sympy as sp
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.calculations import calculate_area, calculate_volume
from utils.plotting import plot_region, plot_surface

class TransformationTab:
    """Pestaña para ejemplos de transformación de coordenadas"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de transformación"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Ejemplos de Transformación")
        
        # Título
        title_label = ttk.Label(self.frame, text="Ejemplos de Transformación a Coordenadas Polares", 
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
                              values=["cardioide", "círculo", "lemniscata", "espiral"])
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
            def r_func(theta):
                return a * (1 + np.cos(theta))
            
            # Límites de integración
            theta_limits = (0, 2*np.pi)
            
            # Calcular el área
            area, area_symbolic = calculate_area(r_func, theta_limits)
            
            # Mostrar resultados
            result_text = f"Cardioide: r = {a:.1f}(1 + cos(θ))\n\n"
            result_text += f"Área numérica: {area:.6f}\n"
            if area_symbolic is not None:
                result_text += f"Área simbólica: {float(area_symbolic):.6f}\n"
            else:
                result_text += f"Área simbólica: No disponible\n"
            result_text += f"Fórmula exacta: 6π·a² = {6*np.pi*a**2:.6f}"
            
        elif example == "círculo":
            # Función que define el círculo
            def r_func(theta):
                return a
            
            # Límites de integración
            theta_limits = (0, 2*np.pi)
            
            # Calcular el área
            area, area_symbolic = calculate_area(r_func, theta_limits)
            
            # Mostrar resultados
            result_text = f"Círculo: r = {a:.1f}\n\n"
            result_text += f"Área numérica: {area:.6f}\n"
            if area_symbolic is not None:
                result_text += f"Área simbólica: {float(area_symbolic):.6f}\n"
            else:
                result_text += f"Área simbólica: No disponible\n"
            result_text += f"Fórmula exacta: π·a² = {np.pi*a**2:.6f}"
            
        elif example == "lemniscata":
            # Función que define la lemniscata
            def r_func(theta):
                return a * np.sqrt(np.cos(2*theta))
            
            # Límites de integración
            theta_limits = (-np.pi/4, np.pi/4)
            
            # Calcular el área
            area, area_symbolic = calculate_area(r_func, theta_limits)
            area *= 2  # Multiplicar por 2 para obtener el área total
            
            # Mostrar resultados
            result_text = f"Lemniscata: r² = {a:.1f}²·cos(2θ)\n\n"
            result_text += f"Área numérica: {area:.6f}\n"
            result_text += f"Fórmula exacta: a² = {a**2:.6f}"
            if area_symbolic is not None:
                result_text += f"Área simbólica: {float(area_symbolic):.6f}\n"
            else:
                result_text += f"Área simbólica: No disponible\n"
            
        elif example == "espiral":
            # Función que define la espiral
            def r_func(theta):
                return a * theta / (2*np.pi)
            
            # Límites de integración
            theta_limits = (0, 2*np.pi)
            
            # Calcular el área
            area, area_symbolic = calculate_area(r_func, theta_limits)
            
            # Mostrar resultados
            result_text = f"Espiral: r = {a:.1f}·θ/(2π)\n\n"
            result_text += f"Área numérica: {area:.6f}\n"
            if area_symbolic is not None:
                result_text += f"Área simbólica: {float(area_symbolic):.6f}\n"
            else:
                result_text += f"Área simbólica: No disponible\n"
            result_text += f"Fórmula exacta: π·a²/3 = {np.pi*a**2/3:.6f}"
        
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
        
        # Dibujar la región según el ejemplo
        if example == "cardioide":
            def r_func(theta):
                return a * (1 + np.cos(theta))
            theta_range = (0, 2*np.pi)
            title = f"Cardioide: r = {a:.1f}(1 + cos(θ))"
            
        elif example == "círculo":
            def r_func(theta):
                return a
            theta_range = (0, 2*np.pi)
            title = f"Círculo: r = {a:.1f}"
            
        elif example == "lemniscata":
            def r_func(theta):
                return a * np.sqrt(np.cos(2*theta))
            theta_range = (-np.pi/4, np.pi/4)
            title = f"Lemniscata: r² = {a:.1f}²·cos(2θ)"
            
        elif example == "espiral":
            def r_func(theta):
                return a * theta / (2*np.pi)
            theta_range = (0, 2*np.pi)
            title = f"Espiral: r = {a:.1f}·θ/(2π)"
        
        # Dibujar la región
        plot_region(ax, r_func, theta_range, title)
        
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
        
        # Dibujar la superficie según el ejemplo
        if example == "cardioide":
            def r_func(theta):
                return a * (1 + np.cos(theta))
            theta_range = (0, 2*np.pi)
            title = f"Superficie z = 1 sobre cardioide"
            
        elif example == "círculo":
            def r_func(theta):
                return a
            theta_range = (0, 2*np.pi)
            title = f"Superficie z = 1 sobre círculo"
            
        elif example == "lemniscata":
            def r_func(theta):
                return a * np.sqrt(np.cos(2*theta))
            theta_range = (-np.pi/4, np.pi/4)
            title = f"Superficie z = 1 sobre lemniscata"
            
        elif example == "espiral":
            def r_func(theta):
                return a * theta / (2*np.pi)
            theta_range = (0, 2*np.pi)
            title = f"Superficie z = 1 sobre espiral"
        
        # Función constante z = 1
        def z_func(r, theta):
            return np.ones_like(r)
        
        # Dibujar la superficie
        plot_surface(ax, r_func, z_func, theta_range, title)
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.viz_3d_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.viz_3d_frame)
        toolbar.update()
