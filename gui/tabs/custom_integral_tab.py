import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import sympy as sp
from scipy import integrate
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.custom_integral import parse_expression, evaluate_double_integral, get_integration_limits

class CustomIntegralTab:
    """Pestaña para resolver integrales dobles personalizadas"""

    def __init__(self, notebook):
        """Inicializa la pestaña de integrales personalizadas"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Integrales Personalizadas")
        
        # Título
        title_label = ttk.Label(self.frame, text="Resolución de Integrales Dobles Personalizadas", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Marco principal con dos columnas
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Marco para controles (izquierda)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, expand=False)
        
        # Selector de sistema de coordenadas
        ttk.Label(controls_frame, text="Sistema de coordenadas:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.coord_system = tk.StringVar(value="cartesianas")
        coord_combo = ttk.Combobox(controls_frame, textvariable=self.coord_system, 
                                  values=["cartesianas", "polares"])
        coord_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        coord_combo.bind("<<ComboboxSelected>>", self.update_integral_form)
        
        # Marco para la función a integrar
        function_frame = ttk.LabelFrame(controls_frame, text="Función a integrar")
        function_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Etiqueta y entrada para la función
        self.function_label = ttk.Label(function_frame, text="f(x,y) =")
        self.function_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.function_entry = ttk.Entry(function_frame, width=30)
        self.function_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.function_entry.insert(0, "x**2 + y**2")  # Valor predeterminado
        
        # Ejemplos de funciones
        ttk.Label(function_frame, text="Ejemplos:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        examples_text = "x**2 + y**2\nexp(-(x**2 + y**2))\nsin(x)*cos(y)"
        examples_label = ttk.Label(function_frame, text=examples_text, justify=tk.LEFT)
        examples_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Marco para los límites de integración
        limits_frame = ttk.LabelFrame(controls_frame, text="Límites de integración")
        limits_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Variables para los límites
        self.limits_vars = {}
        
        # Crear campos para los límites según el sistema de coordenadas
        self.create_limits_fields(limits_frame)
        
        # Botón para calcular
        calculate_button = ttk.Button(controls_frame, text="Calcular Integral", command=self.calculate_custom_integral)
        calculate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Marco para resultados
        self.integral_results_frame = ttk.LabelFrame(controls_frame, text="Resultados")
        self.integral_results_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Etiqueta para resultados
        self.integral_result_label = ttk.Label(self.integral_results_frame, text="", font=("Arial", 11), wraplength=350)
        self.integral_result_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Marco para la visualización (derecha)
        visualization_frame = ttk.Frame(main_frame)
        visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas para diferentes visualizaciones
        viz_notebook = ttk.Notebook(visualization_frame)
        viz_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña para la región de integración
        self.region_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.region_frame, text="Región de integración")
        
        # Pestaña para la función
        self.function_viz_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.function_viz_frame, text="Función")
        
        # Pestaña para el integrando
        self.integrand_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.integrand_frame, text="Integrando")
        
        # Crear figuras iniciales
        self.create_region_figure()
        self.create_function_figure()
        self.create_integrand_figure()

    def create_limits_fields(self, parent_frame):
        """Crea los campos para los límites de integración según el sistema de coordenadas"""
        # Limpiar el marco
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        coord_system = self.coord_system.get()
        
        if coord_system == "cartesianas":
            # Límites para x
            ttk.Label(parent_frame, text="Límite inferior de x:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["x_lower"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["x_lower"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["x_lower"].insert(0, "-1")
            
            ttk.Label(parent_frame, text="Límite superior de x:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["x_upper"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["x_upper"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["x_upper"].insert(0, "1")
            
            # Límites para y
            ttk.Label(parent_frame, text="Límite inferior de y:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_lower"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["y_lower"].grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_lower"].insert(0, "-1")
            
            ttk.Label(parent_frame, text="Límite superior de y:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_upper"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["y_upper"].grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_upper"].insert(0, "1")
            
            # Opción para límites variables
            self.variable_limits = tk.BooleanVar(value=False)
            variable_check = ttk.Checkbutton(parent_frame, text="Límites variables", variable=self.variable_limits,
                                           command=self.toggle_variable_limits)
            variable_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
            
            # Marco para límites variables (inicialmente oculto)
            self.variable_limits_frame = ttk.Frame(parent_frame)
            self.variable_limits_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
            self.variable_limits_frame.grid_remove()  # Ocultar inicialmente
            
            ttk.Label(self.variable_limits_frame, text="y inferior = f(x):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_lower_expr"] = ttk.Entry(self.variable_limits_frame, width=20)
            self.limits_vars["y_lower_expr"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
            self.limits_vars["y_lower_expr"].insert(0, "-sqrt(1-x**2)")
            
            ttk.Label(self.variable_limits_frame, text="y superior = g(x):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_upper_expr"] = ttk.Entry(self.variable_limits_frame, width=20)
            self.limits_vars["y_upper_expr"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
            self.limits_vars["y_upper_expr"].insert(0, "sqrt(1-x**2)")
            
        elif coord_system == "polares":
            # Límites para r
            ttk.Label(parent_frame, text="Límite inferior de r:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["r_lower"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["r_lower"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["r_lower"].insert(0, "0")
            
            ttk.Label(parent_frame, text="Límite superior de r:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["r_upper"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["r_upper"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["r_upper"].insert(0, "1")
            
            # Límites para theta
            ttk.Label(parent_frame, text="Límite inferior de θ:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["theta_lower"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["theta_lower"].grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["theta_lower"].insert(0, "0")
            
            ttk.Label(parent_frame, text="Límite superior de θ:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["theta_upper"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["theta_upper"].grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["theta_upper"].insert(0, "2*pi")
            
            # Opción para límites variables
            self.variable_limits = tk.BooleanVar(value=False)
            variable_check = ttk.Checkbutton(parent_frame, text="Límites variables", variable=self.variable_limits,
                                           command=self.toggle_variable_limits)
            variable_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
            
            # Marco para límites variables (inicialmente oculto)
            self.variable_limits_frame = ttk.Frame(parent_frame)
            self.variable_limits_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
            self.variable_limits_frame.grid_remove()  # Ocultar inicialmente
            
            ttk.Label(self.variable_limits_frame, text="r superior = f(θ):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["r_upper_expr"] = ttk.Entry(self.variable_limits_frame, width=20)
            self.limits_vars["r_upper_expr"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
            self.limits_vars["r_upper_expr"].insert(0, "1 + cos(theta)")

    def toggle_variable_limits(self):
        """Muestra u oculta los campos para límites variables"""
        if self.variable_limits.get():
            self.variable_limits_frame.grid()
        else:
            self.variable_limits_frame.grid_remove()

    def update_integral_form(self, event=None):
        """Actualiza el formulario de la integral cuando cambia el sistema de coordenadas"""
        coord_system = self.coord_system.get()
        
        # Actualizar etiqueta de la función
        if coord_system == "cartesianas":
            self.function_label.config(text="f(x,y) =")
        else:
            self.function_label.config(text="f(r,θ) =")
        
        # Actualizar campos de límites
        if hasattr(self, 'limits_vars') and self.limits_vars:
            parent_frame = next(iter(self.limits_vars.values())).master
            self.create_limits_fields(parent_frame)
        
        # Actualizar figuras
        self.create_region_figure()
        self.create_function_figure()
        self.create_integrand_figure()

    def calculate_custom_integral(self):
        """Calcula la integral doble personalizada"""
        try:
            # Obtener la función y los límites
            func_str = self.function_entry.get()
            coord_system = self.coord_system.get()
            
            # Calcular la integral
            result, error, symbolic_result = evaluate_double_integral(
                func_str, 
                coord_system, 
                get_integration_limits(coord_system, self.limits_vars, self.variable_limits.get()),
                self.variable_limits.get()
            )
            
            # Mostrar resultados
            if coord_system == "cartesianas":
                if self.variable_limits.get():
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    y_lower_expr = self.limits_vars["y_lower_expr"].get()
                    y_upper_expr = self.limits_vars["y_upper_expr"].get()
                    
                    result_text = f"Integral de {func_str} sobre la región:\n"
                    result_text += f"{x_lower} ≤ x ≤ {x_upper}\n"
                    result_text += f"{y_lower_expr} ≤ y ≤ {y_upper_expr}\n\n"
                else:
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    y_lower = float(self.limits_vars["y_lower"].get())
                    y_upper = float(self.limits_vars["y_upper"].get())
                    
                    result_text = f"Integral de {func_str} sobre el rectángulo:\n"
                    result_text += f"{x_lower} ≤ x ≤ {x_upper}\n"
                    result_text += f"{y_lower} ≤ y ≤ {y_upper}\n\n"
            else:  # polares
                r_lower = float(self.limits_vars["r_lower"].get())
                theta_lower_str = self.limits_vars["theta_lower"].get()
                theta_upper_str = self.limits_vars["theta_upper"].get()
                
                if self.variable_limits.get():
                    r_upper_expr = self.limits_vars["r_upper_expr"].get()
                    
                    result_text = f"Integral de {func_str} en coordenadas polares sobre la región:\n"
                    result_text += f"{r_lower} ≤ r ≤ {r_upper_expr}\n"
                    result_text += f"{theta_lower_str} ≤ θ ≤ {theta_upper_str}\n\n"
                else:
                    r_upper = float(self.limits_vars["r_upper"].get())
                    
                    result_text = f"Integral de {func_str} en coordenadas polares sobre la región:\n"
                    result_text += f"{r_lower} ≤ r ≤ {r_upper}\n"
                    result_text += f"{theta_lower_str} ≤ θ ≤ {theta_upper_str}\n\n"
            
            result_text += f"Resultado numérico: {result:.8f}\n"
            result_text += f"Error estimado: {error:.8e}\n"
            
            if symbolic_result is not None:
                symbolic_value = float(symbolic_result.evalf())
                symbolic_latex = sp.latex(symbolic_result)
                result_text += f"\nResultado simbólico: {symbolic_value:.8f}\n"
                result_text += f"Expresión: {symbolic_latex}"
            
            self.integral_result_label.config(text=result_text)
            
            # Actualizar figuras
            self.create_region_figure()
            self.create_function_figure()
            self.create_integrand_figure()
            
        except Exception as e:
            self.integral_result_label.config(text=f"Error: {str(e)}\n\nVerifique que la función y los límites estén correctamente definidos.")

    def create_region_figure(self):
        """Crea la figura para visualizar la región de integración"""
        # Limpiar el marco
        for widget in self.region_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111, aspect='equal')
        
        try:
            # Obtener el sistema de coordenadas y los límites
            coord_system = self.coord_system.get()
            
            if coord_system == "cartesianas":
                if self.variable_limits.get():
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    y_lower_expr = self.limits_vars["y_lower_expr"].get()
                    y_upper_expr = self.limits_vars["y_upper_expr"].get()
                    
                    # Crear una malla de puntos en x
                    x = np.linspace(x_lower, x_upper, 100)
                    
                    # Evaluar las expresiones para los límites de y
                    y_lower = eval(y_lower_expr.replace('x', 'x_val') for x_val in x)
                    y_upper = eval(y_upper_expr.replace('x', 'x_val') for x_val in x)
                    
                    # Dibujar la región
                    ax.fill_between(x, y_lower, y_upper, alpha=0.3)
                    ax.plot(x, y_lower, 'b-')
                    ax.plot(x, y_upper, 'b-')
                    
                    # Configurar los ejes
                    ax.set_xlim(x_lower - 0.5, x_upper + 0.5)
                    y_min = min(np.min(y_lower), -1)
                    y_max = max(np.max(y_upper), 1)
                    ax.set_ylim(y_min - 0.5, y_max + 0.5)
                    
                    # Título
                    ax.set_title(f"Región: {x_lower} ≤ x ≤ {x_upper}, {y_lower_expr} ≤ y ≤ {y_upper_expr}")
                    
                else:
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    y_lower = float(self.limits_vars["y_lower"].get())
                    y_upper = float(self.limits_vars["y_upper"].get())
                    
                    # Dibujar el rectángulo
                    rect = plt.Rectangle((x_lower, y_lower), x_upper - x_lower, y_upper - y_lower, 
                                        fill=True, alpha=0.3)
                    ax.add_patch(rect)
                    
                    # Configurar los ejes
                    ax.set_xlim(x_lower - 0.5, x_upper + 0.5)
                    ax.set_ylim(y_lower - 0.5, y_upper + 0.5)
                    
                    # Título
                    ax.set_title(f"Región: {x_lower} ≤ x ≤ {x_upper}, {y_lower} ≤ y ≤ {y_upper}")
                
                # Etiquetas de los ejes
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                
            else:  # polares
                r_lower = float(self.limits_vars["r_lower"].get())
                theta_lower_str = self.limits_vars["theta_lower"].get()
                theta_upper_str = self.limits_vars["theta_upper"].get()
                
                # Convertir expresiones de límites a valores numéricos
                theta_lower = eval(theta_lower_str.replace('pi', 'np.pi'))
                theta_upper = eval(theta_upper_str.replace('pi', 'np.pi'))
                
                if self.variable_limits.get():
                    r_upper_expr = self.limits_vars["r_upper_expr"].get()
                    
                    # Crear una malla de puntos en theta
                    theta = np.linspace(theta_lower, theta_upper, 100)
                    
                    # Evaluar la expresión para el límite superior de r
                    r_upper = np.array([eval(r_upper_expr.replace('theta', 'theta_val')) for theta_val in theta])
                    
                    # Convertir a coordenadas cartesianas
                    x_lower = r_lower * np.cos(theta)
                    y_lower = r_lower * np.sin(theta)
                    x_upper = r_upper * np.cos(theta)
                    y_upper = r_upper * np.sin(theta)
                    
                    # Dibujar la región
                    ax.fill(x_upper, y_upper, alpha=0.3)
                    ax.plot(x_upper, y_upper, 'b-')
                    
                    # Configurar los ejes
                    r_max = np.max(r_upper)
                    ax.set_xlim(-r_max - 0.5, r_max + 0.5)
                    ax.set_ylim(-r_max - 0.5, r_max + 0.5)
                    
                    # Título
                    ax.set_title(f"Región: {r_lower} ≤ r ≤ {r_upper_expr}, {theta_lower_str} ≤ θ ≤ {theta_upper_str}")
                    
                else:
                    r_upper = float(self.limits_vars["r_upper"].get())
                    
                    # Dibujar el sector circular
                    theta = np.linspace(theta_lower, theta_upper, 100)
                    x_outer = r_upper * np.cos(theta)
                    y_outer = r_upper * np.sin(theta)
                    
                    if r_lower > 0:
                        x_inner = r_lower * np.cos(theta)
                        y_inner = r_lower * np.sin(theta)
                        
                        # Crear un polígono para el sector anular
                        x = np.concatenate([x_outer, x_inner[::-1], [x_outer[0]]])
                        y = np.concatenate([y_outer, y_inner[::-1], [y_outer[0]]])
                        ax.fill(x, y, alpha=0.3)
                        ax.plot(x_outer, y_outer, 'b-')
                        ax.plot(x_inner, y_inner, 'b-')
                    else:
                        # Crear un polígono para el sector circular
                        x = np.concatenate([x_outer, [0, x_outer[0]]])
                        y = np.concatenate([y_outer, [0, y_outer[0]]])
                        ax.fill(x, y, alpha=0.3)
                        ax.plot(x_outer, y_outer, 'b-')
                    
                    # Configurar los ejes
                    ax.set_xlim(-r_upper - 0.5, r_upper + 0.5)
                    ax.set_ylim(-r_upper - 0.5, r_upper + 0.5)
                    
                    # Título
                    ax.set_title(f"Región: {r_lower} ≤ r ≤ {r_upper}, {theta_lower_str} ≤ θ ≤ {theta_upper_str}")
                
                # Etiquetas de los ejes
                ax.set_xlabel('x')
                ax.set_ylabel('y')
            
            # Agregar una cuadrícula
            ax.grid(True)
            
        except Exception as e:
            ax.text(0.5, 0.5, f"Error al visualizar la región:\n{str(e)}", 
                   ha='center', va='center', transform=ax.transAxes)
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.region_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.region_frame)
        toolbar.update()

    def create_function_figure(self):
        """Crea la figura para visualizar la función a integrar"""
        # Limpiar el marco
        for widget in self.function_viz_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        try:
            # Obtener la función y el sistema de coordenadas
            func_str = self.function_entry.get()
            coord_system = self.coord_system.get()
            
            # Crear una malla de puntos
            if coord_system == "cartesianas":
                # Obtener los límites
                if self.variable_limits.get():
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    # Usar límites fijos para la visualización
                    y_lower = -2
                    y_upper = 2
                else:
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    y_lower = float(self.limits_vars["y_lower"].get())
                    y_upper = float(self.limits_vars["y_upper"].get())
                
                # Crear una malla de puntos
                x = np.linspace(x_lower - 0.5, x_upper + 0.5, 30)
                y = np.linspace(y_lower - 0.5, y_upper + 0.5, 30)
                X, Y = np.meshgrid(x, y)
                
                # Evaluar la función
                Z = np.zeros_like(X)
                for i in range(X.shape[0]):
                    for j in range(X.shape[1]):
                        try:
                            # Reemplazar x e y por sus valores
                            expr = func_str.replace('x', str(X[i, j])).replace('y', str(Y[i, j]))
                            # Reemplazar funciones matemáticas
                            expr = expr.replace('sin', 'np.sin').replace('cos', 'np.cos')
                            expr = expr.replace('tan', 'np.tan').replace('exp', 'np.exp')
                            expr = expr.replace('log', 'np.log').replace('sqrt', 'np.sqrt')
                            expr = expr.replace('pi', 'np.pi').replace('e', 'np.e')
                            # Evaluar la expresión
                            Z[i, j] = eval(expr)
                        except:
                            Z[i, j] = np.nan
                
                # Dibujar la superficie
                surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
                
                # Título y etiquetas
                ax.set_title(f"Función: f(x,y) = {func_str}")
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('f(x,y)')
                
            else:  # polares
                # Obtener los límites
                r_lower = float(self.limits_vars["r_lower"].get())
                theta_lower_str = self.limits_vars["theta_lower"].get()
                theta_upper_str = self.limits_vars["theta_upper"].get()
                
                # Convertir expresiones de límites a valores numéricos
                theta_lower = eval(theta_lower_str.replace('pi', 'np.pi'))
                theta_upper = eval(theta_upper_str.replace('pi', 'np.pi'))
                
                if self.variable_limits.get():
                    # Usar un límite fijo para la visualización
                    r_upper = 3
                else:
                    r_upper = float(self.limits_vars["r_upper"].get())
                
                # Crear una malla de puntos en coordenadas polares
                r = np.linspace(0, r_upper + 0.5, 30)
                theta = np.linspace(0, 2*np.pi, 30)
                R, Theta = np.meshgrid(r, theta)
                
                # Convertir a coordenadas cartesianas
                X = R * np.cos(Theta)
                Y = R * np.sin(Theta)
                
                # Evaluar la función
                Z = np.zeros_like(X)
                for i in range(X.shape[0]):
                    for j in range(X.shape[1]):
                        try:
                            # Reemplazar r y theta por sus valores
                            expr = func_str.replace('r', str(R[i, j])).replace('theta', str(Theta[i, j]))
                            # Reemplazar funciones matemáticas
                            expr = expr.replace('sin', 'np.sin').replace('cos', 'np.cos')
                            expr = expr.replace('tan', 'np.tan').replace('exp', 'np.exp')
                            expr = expr.replace('log', 'np.log').replace('sqrt', 'np.sqrt')
                            expr = expr.replace('pi', 'np.pi').replace('e', 'np.e')
                            # Evaluar la expresión
                            Z[i, j] = eval(expr)
                        except:
                            Z[i, j] = np.nan
                
                # Dibujar la superficie
                surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
                
                # Título y etiquetas
                ax.set_title(f"Función: f(r,θ) = {func_str}")
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('f(r,θ)')
            
            # Agregar una barra de colores
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            
        except Exception as e:
            ax.text2D(0.5, 0.5, f"Error al visualizar la función:\n{str(e)}", 
                     ha='center', va='center', transform=ax.transAxes)
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.function_viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.function_viz_frame)
        toolbar.update()

    def create_integrand_figure(self):
        """Crea la figura para visualizar el integrando (incluyendo el jacobiano)"""
        # Limpiar el marco
        for widget in self.integrand_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        try:
            # Obtener la función y el sistema de coordenadas
            func_str = self.function_entry.get()
            coord_system = self.coord_system.get()
            
            # Crear una malla de puntos
            if coord_system == "cartesianas":
                # El integrando es simplemente la función
                integrand_str = func_str
                
                # Obtener los límites
                if self.variable_limits.get():
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    # Usar límites fijos para la visualización
                    y_lower = -2
                    y_upper = 2
                else:
                    x_lower = float(self.limits_vars["x_lower"].get())
                    x_upper = float(self.limits_vars["x_upper"].get())
                    y_lower = float(self.limits_vars["y_lower"].get())
                    y_upper = float(self.limits_vars["y_upper"].get())
                
                # Crear una malla de puntos
                x = np.linspace(x_lower - 0.5, x_upper + 0.5, 30)
                y = np.linspace(y_lower - 0.5, y_upper + 0.5, 30)
                X, Y = np.meshgrid(x, y)
                
                # Evaluar el integrando
                Z = np.zeros_like(X)
                for i in range(X.shape[0]):
                    for j in range(X.shape[1]):
                        try:
                            # Reemplazar x e y por sus valores
                            expr = integrand_str.replace('x', str(X[i, j])).replace('y', str(Y[i, j]))
                            # Reemplazar funciones matemáticas
                            expr = expr.replace('sin', 'np.sin').replace('cos', 'np.cos')
                            expr = expr.replace('tan', 'np.tan').replace('exp', 'np.exp')
                            expr = expr.replace('log', 'np.log').replace('sqrt', 'np.sqrt')
                            expr = expr.replace('pi', 'np.pi').replace('e', 'np.e')
                            # Evaluar la expresión
                            Z[i, j] = eval(expr)
                        except:
                            Z[i, j] = np.nan
                
                # Dibujar la superficie
                surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
                
                # Título y etiquetas
                ax.set_title(f"Integrando: {integrand_str}")
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('f(x,y)')
                
            else:  # polares
                # El integrando incluye el jacobiano r
                integrand_str = f"({func_str}) * r"
                
                # Obtener los límites
                r_lower = float(self.limits_vars["r_lower"].get())
                theta_lower_str = self.limits_vars["theta_lower"].get()
                theta_upper_str = self.limits_vars["theta_upper"].get()
                
                # Convertir expresiones de límites a valores numéricos
                theta_lower = eval(theta_lower_str.replace('pi', 'np.pi'))
                theta_upper = eval(theta_upper_str.replace('pi', 'np.pi'))
                
                if self.variable_limits.get():
                    # Usar un límite fijo para la visualización
                    r_upper = 3
                else:
                    r_upper = float(self.limits_vars["r_upper"].get())
                
                # Crear una malla de puntos en coordenadas polares
                r = np.linspace(0, r_upper + 0.5, 30)
                theta = np.linspace(0, 2*np.pi, 30)
                R, Theta = np.meshgrid(r, theta)
                
                # Convertir a coordenadas cartesianas
                X = R * np.cos(Theta)
                Y = R * np.sin(Theta)
                
                # Evaluar el integrando
                Z = np.zeros_like(X)
                for i in range(X.shape[0]):
                    for j in range(X.shape[1]):
                        try:
                            # Reemplazar r y theta por sus valores
                            expr = func_str.replace('r', str(R[i, j])).replace('theta', str(Theta[i, j]))
                            # Reemplazar funciones matemáticas
                            expr = expr.replace('sin', 'np.sin').replace('cos', 'np.cos')
                            expr = expr.replace('tan', 'np.tan').replace('exp', 'np.exp')
                            expr = expr.replace('log', 'np.log').replace('sqrt', 'np.sqrt')
                            expr = expr.replace('pi', 'np.pi').replace('e', 'np.e')
                            # Evaluar la expresión y multiplicar por el jacobiano
                            Z[i, j] = eval(expr) * R[i, j]
                        except:
                            Z[i, j] = np.nan
                
                # Dibujar la superficie
                surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
                
                # Título y etiquetas
                ax.set_title(f"Integrando: {integrand_str}")
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('f(r,θ)·r')
            
            # Agregar una barra de colores
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            
        except Exception as e:
            ax.text2D(0.5, 0.5, f"Error al visualizar el integrando:\n{str(e)}", 
                     ha='center', va='center', transform=ax.transAxes)
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.integrand_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, self.integrand_frame)
        toolbar.update()
