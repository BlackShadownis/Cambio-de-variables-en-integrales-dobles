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

class AverageValuesTab:
    """Pestaña para el cálculo de valores promedio"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de valores promedio"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Valores Promedio")
        
        # Título
        title_label = ttk.Label(self.frame, text="Cálculo de Valores Promedio", 
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
        self.example_var = tk.StringVar(value="temperatura")
        examples = ttk.Combobox(controls_frame, textvariable=self.example_var, 
                              values=["temperatura", "cardioide"])
        examples.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        examples.bind("<<ComboboxSelected>>", self.update_example)
        
        # Marco para parámetros
        params_frame = ttk.LabelFrame(controls_frame, text="Parámetros")
        params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Parámetro R (radio)
        ttk.Label(params_frame, text="Radio (R):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.param_r = ttk.Scale(params_frame, from_=1.0, to=20.0, orient=tk.HORIZONTAL, length=200)
        self.param_r.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.param_r.set(10.0)
        self.param_r_label = ttk.Label(params_frame, text="10.0")
        self.param_r_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.param_r.bind("<Motion>", self.update_param_r)
        
        # Parámetro T_0 (temperatura en el centro)
        ttk.Label(params_frame, text="Valor máximo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.param_t0 = ttk.Scale(params_frame, from_=50.0, to=200.0, orient=tk.HORIZONTAL, length=200)
        self.param_t0.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.param_t0.set(100.0)
        self.param_t0_label = ttk.Label(params_frame, text="100.0")
        self.param_t0_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.param_t0.bind("<Motion>", self.update_param_t0)
        
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
        
        # Pestaña para la distribución
        self.distribution_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.distribution_frame, text="Distribución")
        
        # Pestaña para el perfil
        self.profile_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.profile_frame, text="Perfil")
        
        # Crear figuras iniciales
        self.create_distribution_figure()
        self.create_profile_figure()
        
        # Calcular el ejemplo inicial
        self.calculate_example()
    
    def update_param_r(self, event=None):
        """Actualiza la etiqueta del parámetro R"""
        value = self.param_r.get()
        self.param_r_label.config(text=f"{value:.1f}")
    
    def update_param_t0(self, event=None):
        """Actualiza la etiqueta del parámetro T_0"""
        value = self.param_t0.get()
        self.param_t0_label.config(text=f"{value:.1f}")
    
    def update_example(self, event=None):
        """Actualiza el ejemplo seleccionado"""
        self.calculate_example()
    
    def calculate_example(self):
        """Calcula el ejemplo seleccionado"""
        example = self.example_var.get()
        R = self.param_r.get()
        T_0 = self.param_t0.get()
        
        if example == "temperatura":
            # Función de temperatura
            def temperatura(r):
                return T_0 * (1 - (r/R)**2)
            
            # Para calcular el valor promedio, necesitamos:
            # T_avg = ∫∫ T(r,θ) dA / ∫∫ dA
            
            # Integrando para el numerador
            def integrando_temp(r, theta):
                return temperatura(r) * r  # Temperatura * jacobiano
            
            # Integrando para el denominador (área)
            def integrando_area(r, theta):
                return r  # Solo el jacobiano
            
            # Integración numérica para el numerador
            num, error_num = integrate.dblquad(
                integrando_temp,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, lambda theta: R  # límites de r
            )
            
            # Integración numérica para el denominador (área)
            denom, error_denom = integrate.dblquad(
                integrando_area,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, lambda theta: R  # límites de r
            )
            
            # Valor promedio
            temp_avg = num / denom
            
            # Cálculo analítico
            # T_avg = (2π·T₀·∫(r - r³/R²)dr) / (πR²) desde 0 hasta R
            # T_avg = (2π·T₀·[r²/2 - r⁴/(4R²)]₀ᴿ) / (πR²)
            # T_avg = (2π·T₀·[R²/2 - R⁴/(4R²)]) / (πR²)
            # T_avg = (2π·T₀·R²·(1/2 - 1/4)) / (πR²)
            # T_avg = 2·T₀·(1/4) = T₀/2
            teorico = T_0 / 2
            
            # Mostrar resultados
            result_text = f"Temperatura en un disco:\n"
            result_text += f"T(r) = T₀(1 - r²/R²)\n\n"
            result_text += f"Radio del disco: {R:.1f} cm\n"
            result_text += f"Temperatura en el centro: {T_0:.1f} °C\n\n"
            result_text += f"Temperatura promedio (numérica):\n{temp_avg:.4f} °C\n\n"
            result_text += f"Temperatura promedio (teórica):\n{teorico:.4f} °C\n\n"
            result_text += f"Error relativo: {abs(temp_avg-teorico)/teorico*100:.8f}%"
            
        elif example == "cardioide":
            # Parámetro del cardioide
            a = R / 5  # Ajustar el parámetro para que el cardioide tenga un tamaño razonable
            
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # Función a promediar: f(r,θ) = r·cos(θ) = x
            def f_polar(r, theta):
                return r * np.cos(theta) * r  # f * jacobiano
            
            # Integrando para el denominador (área)
            def integrando_area(r, theta):
                return r  # Solo el jacobiano
            
            # Integración numérica para el numerador
            num_card, error_num = integrate.dblquad(
                f_polar,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, r_cardioide  # límites de r
            )
            
            # Integración numérica para el denominador (área)
            denom_card, error_denom = integrate.dblquad(
                integrando_area,
                0, 2*np.pi,  # límites de theta
                lambda theta: 0, r_cardioide  # límites de r
            )
            
            # Valor promedio
            f_avg = num_card / denom_card
            
            # Mostrar resultados
            result_text = f"Valor promedio sobre cardioide:\n"
            result_text += f"f(r,θ) = r·cos(θ) = x\n\n"
            result_text += f"Parámetro del cardioide: a = {a:.2f}\n"
            result_text += f"Valor promedio de f(r,θ):\n{f_avg:.4f}\n\n"
            result_text += f"Área del cardioide: {denom_card:.4f}"
        
        # Actualizar la etiqueta de resultados
        self.result_label.config(text=result_text)
        
        # Actualizar las figuras
        self.create_distribution_figure()
        self.create_profile_figure()
    
    def create_distribution_figure(self):
        """Crea la figura para visualizar la distribución"""
        # Limpiar el marco
        for widget in self.distribution_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        
        # Obtener los parámetros
        example = self.example_var.get()
        R = self.param_r.get()
        T_0 = self.param_t0.get()
        
        if example == "temperatura":
            # Función de temperatura
            def temperatura(r):
                return T_0 * (1 - (r/R)**2)
            
            # Crear una malla de puntos
            r_vals = np.linspace(0, R, 100)
            theta_vals = np.linspace(0, 2*np.pi, 100)
            r_grid, theta_grid = np.meshgrid(r_vals, theta_vals)
            x_grid = r_grid * np.cos(theta_grid)
            y_grid = r_grid * np.sin(theta_grid)
            z_grid = temperatura(r_grid)
            
            # Dibujar el contorno de temperatura
            contour = ax.contourf(x_grid, y_grid, z_grid, cmap='hot', levels=20)
            ax.set_aspect('equal')
            ax.set_xlabel('x (cm)')
            ax.set_ylabel('y (cm)')
            ax.set_title('Distribución de temperatura T(r)')
            fig.colorbar(contour, ax=ax, label='Temperatura (°C)')
            
        elif example == "cardioide":
            # Parámetro del cardioide
            a = R / 5  # Ajustar el parámetro para que el cardioide tenga un tamaño razonable
            
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # Valores para graficar
            theta_vals = np.linspace(0, 2*np.pi, 200)
            r_vals = r_cardioide(theta_vals)
            x = r_vals * np.cos(theta_vals)
            y = r_vals * np.sin(theta_vals)
            
            # Crear una malla para visualizar la función
            x_grid = np.linspace(-4*a, 4*a, 100)
            y_grid = np.linspace(-4*a, 4*a, 100)
            X, Y = np.meshgrid(x_grid, y_grid)
            Z = X  # La función es f(x,y) = x
            
            # Dibujar el contorno
            contour = ax.contourf(X, Y, Z, cmap='coolwarm', levels=20)
            ax.plot(x, y, 'k-', linewidth=2)
            ax.set_aspect('equal')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('f(x,y) = x sobre el cardioide')
            fig.colorbar(contour, ax=ax, label='f(x,y) = x')
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.distribution_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.distribution_frame)
        toolbar.update()
    
    def create_profile_figure(self):
        """Crea la figura para visualizar el perfil"""
        # Limpiar el marco
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        
        # Obtener los parámetros
        example = self.example_var.get()
        R = self.param_r.get()
        T_0 = self.param_t0.get()
        
        if example == "temperatura":
            # Función de temperatura
            def temperatura(r):
                return T_0 * (1 - (r/R)**2)
            
            # Para calcular el valor promedio
            def integrando_temp(r, theta):
                return temperatura(r) * r
            
            def integrando_area(r, theta):
                return r
            
            # Integración numérica
            num, error_num = integrate.dblquad(
                integrando_temp,
                0, 2*np.pi,
                lambda theta: 0, lambda theta: R
            )
            
            denom, error_denom = integrate.dblquad(
                integrando_area,
                0, 2*np.pi,
                lambda theta: 0, lambda theta: R
            )
            
            # Valor promedio
            temp_avg = num / denom
            
            # Perfil de temperatura
            ax = fig.add_subplot(111)
            r_vals = np.linspace(0, R, 100)
            ax.plot(r_vals, temperatura(r_vals), 'r-', linewidth=2)
            ax.axhline(y=temp_avg, color='b', linestyle='--', label=f'Promedio: {temp_avg:.1f} °C')
            ax.set_xlabel('r (cm)')
            ax.set_ylabel('T(r) (°C)')
            ax.set_title('Perfil de temperatura')
            ax.grid(True)
            ax.legend()
            
        elif example == "cardioide":
            # Parámetro del cardioide
            a = R / 5  # Ajustar el parámetro para que el cardioide tenga un tamaño razonable
            
            # Función que define el cardioide
            def r_cardioide(theta):
                return a * (1 + np.cos(theta))
            
            # Función a promediar: f(r,θ) = r·cos(θ) = x
            def f_polar(r, theta):
                return r * np.cos(theta) * r
            
            def integrando_area(r, theta):
                return r
            
            # Integración numérica
            num_card, error_num = integrate.dblquad(
                f_polar,
                0, 2*np.pi,
                lambda theta: 0, r_cardioide
            )
            
            denom_card, error_denom = integrate.dblquad(
                integrando_area,
                0, 2*np.pi,
                lambda theta: 0, r_cardioide
            )
            
            # Valor promedio
            f_avg = num_card / denom_card
            
            # Visualización 3D
            ax = fig.add_subplot(111, projection='3d')
            
            # Convertir a coordenadas cartesianas para visualización
            r_grid, theta_grid = np.meshgrid(np.linspace(0, 3*a, 50), np.linspace(0, 2*np.pi, 50))
            x_grid = r_grid * np.cos(theta_grid)
            y_grid = r_grid * np.sin(theta_grid)
            z_grid = x_grid  # La función es f(x,y) = x
            
            # Crear una máscara para mostrar solo dentro del cardioide
            mask = r_grid <= np.array([r_cardioide(t) for t in theta_grid[0, :]])
            
            # Dibujar la superficie
            surf = ax.plot_surface(
                x_grid * mask, y_grid * mask, z_grid * mask, 
                cmap='coolwarm', alpha=0.8
            )
            
            # Configurar los ejes
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('f(x,y) = x')
            ax.set_title(f'Valor promedio: {f_avg:.4f}')
            
            # Agregar una barra de colores
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='f(x,y) = x')
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.profile_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.profile_frame)
        toolbar.update()
