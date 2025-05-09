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

class MomentsTab:
    """Pestaña para el cálculo de momentos de inercia"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de momentos de inercia"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Momentos de Inercia")
        
        # Título
        title_label = ttk.Label(self.frame, text="Cálculo de Momentos de Inercia", 
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
        self.example_var = tk.StringVar(value="disco")
        examples = ttk.Combobox(controls_frame, textvariable=self.example_var, 
                              values=["disco", "cardioide"])
        examples.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        examples.bind("<<ComboboxSelected>>", self.update_example)
        
        # Marco para parámetros
        params_frame = ttk.LabelFrame(controls_frame, text="Parámetros")
        params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Parámetro R (radio)
        ttk.Label(params_frame, text="Radio (R):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.param_r = ttk.Scale(params_frame, from_=1.0, to=10.0, orient=tk.HORIZONTAL, length=200)
        self.param_r.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.param_r.set(5.0)
        self.param_r_label = ttk.Label(params_frame, text="5.0")
        self.param_r_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.param_r.bind("<Motion>", self.update_param_r)
        
        # Parámetro rho_0 (densidad en el centro)
        ttk.Label(params_frame, text="Densidad (ρ₀):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.param_rho = ttk.Scale(params_frame, from_=1.0, to=5.0, orient=tk.HORIZONTAL, length=200)
        self.param_rho.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.param_rho.set(3.0)
        self.param_rho_label = ttk.Label(params_frame, text="3.0")
        self.param_rho_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.param_rho.bind("<Motion>", self.update_param_rho)
        
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
        
        # Pestaña para la densidad
        self.density_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.density_frame, text="Densidad")
        
        # Pestaña para el perfil
        self.profile_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.profile_frame, text="Perfil")
        
        # Crear figuras iniciales
        self.create_density_figure()
        self.create_profile_figure()
        
        # Calcular el ejemplo inicial
        self.calculate_example()
    
    def update_param_r(self, event=None):
        """Actualiza la etiqueta del parámetro R"""
        value = self.param_r.get()
        self.param_r_label.config(text=f"{value:.1f}")
    
    def update_param_rho(self, event=None):
        """Actualiza la etiqueta del parámetro rho_0"""
        value = self.param_rho.get()
        self.param_rho_label.config(text=f"{value:.1f}")
    
    def update_example(self, event=None):
        """Actualiza el ejemplo seleccionado"""
        self.calculate_example()
    
    def calculate_example(self):
        """Calcula el ejemplo seleccionado"""
        example = self.example_var.get()
        R = self.param_r.get()
        rho_0 = self.param_rho.get()
        
        if example == "disco":
            # Función de densidad
            def densidad(r):
                return rho_0 * (1 - (r/R)**2)
            
            # En coordenadas polares, el momento de inercia respecto al eje z es:
            # I_z = ∫∫ ρ(r,θ) · r² · r dr dθ
            def integrando_momento(r, theta):
                return densidad(r) * r**2 * r  # Densidad * r² * jacobiano
            
            # Integración numérica
            momento, error = integrate.dblquad(
                integrando_momento,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, lambda theta: R  # límites de r
            )
            
            # Cálculo analítico
            # I = 2π·ρ₀·∫(r³ - r⁵/R²)dr desde 0 hasta R
            # I = 2π·ρ₀·[r⁴/4 - r⁶/(6R²)]₀ᴿ
            # I = 2π·ρ₀·[R⁴/4 - R⁶/(6R²)] = 2π·ρ₀·[R⁴/4 - R⁴/6] = 2π·ρ₀·R⁴·(1/4 - 1/6)
            # I = 2π·ρ₀·R⁴·(3-2)/12 = 2π·ρ₀·R⁴/12 = π·ρ₀·R⁴/6
            teorico = np.pi * rho_0 * R**4 / 6
            
            # Mostrar resultados
            result_text = f"Disco con densidad variable:\n"
            result_text += f"ρ(r) = ρ₀(1 - r²/R²)\n\n"
            result_text += f"Radio: {R:.1f} cm\n"
            result_text += f"Densidad en el centro: {rho_0:.1f} g/cm³\n\n"
            result_text += f"Momento de inercia (numérico):\n{momento:.4f} g·cm²\n\n"
            result_text += f"Momento de inercia (teórico):\n{teorico:.4f} g·cm²\n\n"
            result_text += f"Error relativo: {abs(momento-teorico)/teorico*100:.8f}%"
            
        elif example == "cardioide":
            # Parámetro del cardioide
            a = R / 3  # Ajustar el parámetro para que el cardioide tenga un tamaño razonable
            
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # Momento de inercia respecto al origen
            def integrando_momento_cardioide(r, theta):
                return rho_0 * r**2 * r  # Densidad * r² * jacobiano
            
            # Integración numérica
            momento_cardioide, error = integrate.dblquad(
                integrando_momento_cardioide,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, r_cardioide  # límites de r
            )
            
            # Mostrar resultados
            result_text = f"Cardioide con densidad uniforme:\n"
            result_text += f"r = a(1 + cos(θ))\n\n"
            result_text += f"Parámetro a: {a:.2f} cm\n"
            result_text += f"Densidad: {rho_0:.1f} g/cm³\n\n"
            result_text += f"Momento de inercia respecto al origen:\n{momento_cardioide:.4f} g·cm²"
        
        # Actualizar la etiqueta de resultados
        self.result_label.config(text=result_text)
        
        # Actualizar las figuras
        self.create_density_figure()
        self.create_profile_figure()
    
    def create_density_figure(self):
        """Crea la figura para visualizar la densidad"""
        # Limpiar el marco
        for widget in self.density_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        
        # Obtener los parámetros
        example = self.example_var.get()
        R = self.param_r.get()
        rho_0 = self.param_rho.get()
        
        if example == "disco":
            # Función de densidad
            def densidad(r):
                return rho_0 * (1 - (r/R)**2)
            
            # Crear una malla de puntos
            r_vals = np.linspace(0, R, 100)
            theta_vals = np.linspace(0, 2*np.pi, 100)
            r_grid, theta_grid = np.meshgrid(r_vals, theta_vals)
            x_grid = r_grid * np.cos(theta_grid)
            y_grid = r_grid * np.sin(theta_grid)
            z_grid = densidad(r_grid)
            
            # Dibujar el contorno de densidad
            contour = ax.contourf(x_grid, y_grid, z_grid, cmap='viridis', levels=20)
            ax.set_aspect('equal')
            ax.set_xlabel('x (cm)')
            ax.set_ylabel('y (cm)')
            ax.set_title('Distribución de densidad ρ(r)')
            fig.colorbar(contour, ax=ax, label='Densidad (g/cm³)')
            
        elif example == "cardioide":
            # Parámetro del cardioide
            a = R / 3  # Ajustar el parámetro para que el cardioide tenga un tamaño razonable
            
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # Valores para graficar
            theta_vals = np.linspace(0, 2*np.pi, 200)
            r_vals = r_cardioide(theta_vals)
            x = r_vals * np.cos(theta_vals)
            y = r_vals * np.sin(theta_vals)
            
            # Dibujar el cardioide
            ax.plot(x, y, 'k-', linewidth=2)
            ax.fill(x, y, alpha=0.7, color='blue')
            
            # Configurar los ejes
            ax.set_xlim(-3*a, 3*a)
            ax.set_ylim(-3*a, 3*a)
            ax.grid(True)
            ax.set_xlabel('x (cm)')
            ax.set_ylabel('y (cm)')
            ax.set_title(f"Cardioide con densidad uniforme ρ = {rho_0:.1f} g/cm³")
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.density_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.density_frame)
        toolbar.update()
    
    def create_profile_figure(self):
        """Crea la figura para visualizar el perfil de densidad"""
        # Limpiar el marco
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        
        # Obtener los parámetros
        example = self.example_var.get()
        R = self.param_r.get()
        rho_0 = self.param_rho.get()
        
        if example == "disco":
            # Función de densidad
            def densidad(r):
                return rho_0 * (1 - (r/R)**2)
            
            # Perfil de densidad
            ax = fig.add_subplot(111)
            r_vals = np.linspace(0, R, 100)
            ax.plot(r_vals, densidad(r_vals), 'b-', linewidth=2)
            ax.set_xlabel('r (cm)')
            ax.set_ylabel('ρ(r) (g/cm³)')
            ax.set_title('Perfil de densidad')
            ax.grid(True)
            
        elif example == "cardioide":
            # Parámetro del cardioide
            a = R / 3  # Ajustar el parámetro para que el cardioide tenga un tamaño razonable
            
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # Representación 3D
            ax = fig.add_subplot(111, projection='3d')
            
            # Valores para graficar
            theta_vals = np.linspace(0, 2*np.pi, 50)
            r_vals = np.linspace(0, 3*a, 20)
            
            # Crear una malla
            Theta, R_grid = np.meshgrid(theta_vals, r_vals)
            X = R_grid * np.cos(Theta)
            Y = R_grid * np.sin(Theta)
            Z = np.ones_like(X) * rho_0  # Densidad constante
            
            # Crear una máscara para mostrar solo dentro del cardioide
            mask = R_grid <= np.array([r_cardioide(t) for t in Theta[0, :]])
            
            # Dibujar la superficie
            surf = ax.plot_surface(
                X * mask, Y * mask, Z * mask,
                cmap='viridis', alpha=0.8
            )
            
            # Configurar los ejes
            ax.set_xlabel('x (cm)')
            ax.set_ylabel('y (cm)')
            ax.set_zlabel('ρ (g/cm³)')
            ax.set_title(f"Densidad uniforme en cardioide")
            
            # Agregar una barra de colores
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Densidad (g/cm³)')
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.profile_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.profile_frame)
        toolbar.update()
