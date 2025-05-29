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
    """Pestaña para resolver integrales dobles personalizadas con conversión entre sistemas"""

    def __init__(self, notebook):
        """Inicializa la pestaña de integrales personalizadas"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Integrales Personalizadas")
        
        # Título
        title_label = ttk.Label(self.frame, text="Conversión Automática entre Sistemas de Coordenadas", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Marco principal con dos columnas
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Marco para controles (izquierda)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, expand=False)
        
        # Selector de sistema de coordenadas de entrada
        ttk.Label(controls_frame, text="Sistema de entrada:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.input_system = tk.StringVar(value="cartesianas")
        coord_combo = ttk.Combobox(controls_frame, textvariable=self.input_system, 
                                  values=["cartesianas", "polares"])
        coord_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        coord_combo.bind("<<ComboboxSelected>>", self.update_input_system)
        
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
        self.examples_label = ttk.Label(function_frame, text="x**2 + y**2\nexp(-(x**2 + y**2))\nlog(x**2 + y**2 + 1)", justify=tk.LEFT)
        self.examples_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Marco para los límites de integración
        limits_frame = ttk.LabelFrame(controls_frame, text="Límites de integración")
        limits_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Variables para los límites
        self.limits_vars = {}
        
        # Crear campos para los límites según el sistema de coordenadas
        self.create_limits_fields(limits_frame)
        
        # Botón para calcular y convertir
        calculate_button = ttk.Button(controls_frame, text="Calcular y Convertir", command=self.calculate_and_convert)
        calculate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Marco para resultados
        self.results_frame = ttk.LabelFrame(controls_frame, text="Resultados de Conversión")
        self.results_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Crear notebook para resultados
        self.results_notebook = ttk.Notebook(self.results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña para sistema original
        self.original_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.original_frame, text="Sistema Original")
        
        self.original_result_label = ttk.Label(self.original_frame, text="", font=("Arial", 10), wraplength=350)
        self.original_result_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Pestaña para sistema convertido
        self.converted_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.converted_frame, text="Sistema Convertido")
        
        self.converted_result_label = ttk.Label(self.converted_frame, text="", font=("Arial", 10), wraplength=350)
        self.converted_result_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Pestaña para comparación
        self.comparison_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.comparison_frame, text="Comparación")
        
        self.comparison_result_label = ttk.Label(self.comparison_frame, text="", font=("Arial", 10), wraplength=350)
        self.comparison_result_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Marco para la visualización (derecha)
        visualization_frame = ttk.Frame(main_frame)
        visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas para diferentes visualizaciones
        viz_notebook = ttk.Notebook(visualization_frame)
        viz_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña para la región de integración
        self.region_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.region_frame, text="Región")
        
        # Pestaña para comparación de funciones
        self.function_comparison_frame = ttk.Frame(viz_notebook)
        viz_notebook.add(self.function_comparison_frame, text="Comparación de Funciones")
        
        # Crear figuras iniciales
        self.create_region_figure()
        self.create_function_comparison_figure()

    def create_limits_fields(self, parent_frame):
        """Crea los campos para los límites de integración según el sistema de coordenadas"""
        # Limpiar el marco
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        coord_system = self.input_system.get()
        
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
            self.limits_vars["y_lower"].insert(0, "-sqrt(1-x**2)")
            
            ttk.Label(parent_frame, text="Límite superior de y:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_upper"] = ttk.Entry(parent_frame, width=10)
            self.limits_vars["y_upper"].grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            self.limits_vars["y_upper"].insert(0, "sqrt(1-x**2)")
            
            # Actualizar ejemplos
            self.examples_label.config(text="x**2 + y**2\nexp(-(x**2 + y**2))\nlog(x**2 + y**2 + 1)")
            
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
            
            # Actualizar ejemplos
            self.examples_label.config(text="r**2\nr*cos(theta)\nlog(r**2 + 1)")

    def update_input_system(self, event=None):
        """Actualiza el formulario cuando cambia el sistema de coordenadas de entrada"""
        coord_system = self.input_system.get()
        
        # Actualizar etiqueta de la función
        if coord_system == "cartesianas":
            self.function_label.config(text="f(x,y) =")
            # Cambiar función de ejemplo
            self.function_entry.delete(0, tk.END)
            self.function_entry.insert(0, "x**2 + y**2")
        else:
            self.function_label.config(text="f(r,θ) =")
            # Cambiar función de ejemplo
            self.function_entry.delete(0, tk.END)
            self.function_entry.insert(0, "r**2")
        
        # Actualizar campos de límites
        if hasattr(self, 'limits_vars') and self.limits_vars:
            parent_frame = next(iter(self.limits_vars.values())).master
            self.create_limits_fields(parent_frame)

    def safe_eval(self, expr, variables):
        """Evaluación segura de expresiones matemáticas"""
        # Diccionario de funciones permitidas
        safe_dict = {
            "__builtins__": {},
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
            "pi": np.pi, "e": np.e, "abs": np.abs,
            "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
            "atan2": np.arctan2
        }
        safe_dict.update(variables)
        
        try:
            return eval(expr, safe_dict)
        except:
            return 0.0

    def convert_function_cartesian_to_polar(self, func_str):
        """Convierte una función de coordenadas cartesianas a polares"""
        try:
            # Reemplazar x e y por sus equivalentes en polares
            converted = func_str.replace('x', '(r*cos(theta))')
            converted = converted.replace('y', '(r*sin(theta))')
            
            # Simplificar expresiones comunes usando sympy
            r, theta = sp.symbols('r theta')
            x_expr = r * sp.cos(theta)
            y_expr = r * sp.sin(theta)
            
            # Casos especiales comunes
            if func_str == "x**2 + y**2":
                return "r**2"
            elif "x**2 + y**2" in func_str:
                converted = converted.replace('(r*cos(theta))**2 + (r*sin(theta))**2', 'r**2')
                converted = converted.replace('((r*cos(theta))**2 + (r*sin(theta))**2)', 'r**2')
            
            return converted
        except:
            return f"r**2"  # Fallback seguro

    def convert_function_polar_to_cartesian(self, func_str):
        """Convierte una función de coordenadas polares a cartesianas"""
        try:
            if func_str == "r**2":
                return "x**2 + y**2"
            
            # Reemplazar r y theta por sus equivalentes en cartesianas
            converted = func_str.replace('r**2', '(x**2 + y**2)')
            converted = converted.replace('r', 'sqrt(x**2 + y**2)')
            converted = converted.replace('theta', 'atan2(y, x)')
            
            return converted
        except:
            return "x**2 + y**2"  # Fallback seguro

    def convert_limits_cartesian_to_polar(self, limits):
        """Convierte límites de cartesianas a polares"""
        try:
            x_lower = float(limits["x_lower"].get())
            x_upper = float(limits["x_upper"].get())
            y_lower_str = limits["y_lower"].get()
            y_upper_str = limits["y_upper"].get()
            
            # Detectar círculo unitario
            if ("sqrt(1-x**2)" in y_lower_str and "sqrt(1-x**2)" in y_upper_str and 
                x_lower == -1 and x_upper == 1):
                return {
                    "r_lower": "0",
                    "r_upper": "1", 
                    "theta_lower": "0",
                    "theta_upper": "2*pi"
                }
            # Detectar círculo de radio 2
            elif ("sqrt(4-x**2)" in y_lower_str and "sqrt(4-x**2)" in y_upper_str and
                  x_lower == -2 and x_upper == 2):
                return {
                    "r_lower": "0",
                    "r_upper": "2",
                    "theta_lower": "0", 
                    "theta_upper": "2*pi"
                }
            else:
                # Estimación general
                r_max = max(abs(x_lower), abs(x_upper))
                return {
                    "r_lower": "0",
                    "r_upper": str(r_max),
                    "theta_lower": "0",
                    "theta_upper": "2*pi"
                }
        except:
            return {
                "r_lower": "0",
                "r_upper": "1",
                "theta_lower": "0",
                "theta_upper": "2*pi"
            }

    def convert_limits_polar_to_cartesian(self, limits):
        """Convierte límites de polares a cartesianas"""
        try:
            r_upper = float(limits["r_upper"].get())
            
            return {
                "x_lower": str(-r_upper),
                "x_upper": str(r_upper),
                "y_lower": f"-sqrt({r_upper}**2-x**2)",
                "y_upper": f"sqrt({r_upper}**2-x**2)"
            }
        except:
            return {
                "x_lower": "-1",
                "x_upper": "1",
                "y_lower": "-sqrt(1-x**2)",
                "y_upper": "sqrt(1-x**2)"
            }

    def calculate_and_convert(self):
        """Calcula la integral en el sistema original y la convierte al otro sistema"""
        try:
            # Obtener la función y los límites originales
            func_str = self.function_entry.get()
            input_system = self.input_system.get()
            
            # Determinar el sistema de salida
            output_system = "polares" if input_system == "cartesianas" else "cartesianas"
            
            # Calcular en el sistema original
            if input_system == "cartesianas":
                # Calcular en cartesianas
                original_result, original_error = self.calculate_cartesian_integral(func_str)
                
                # Convertir a polares
                converted_func = self.convert_function_cartesian_to_polar(func_str)
                converted_limits = self.convert_limits_cartesian_to_polar(self.limits_vars)
                converted_result, converted_error = self.calculate_polar_integral(converted_func, converted_limits)
                
            else:
                # Calcular en polares
                original_result, original_error = self.calculate_polar_integral(func_str, self.limits_vars)
                
                # Convertir a cartesianas
                converted_func = self.convert_function_polar_to_cartesian(func_str)
                converted_limits = self.convert_limits_polar_to_cartesian(self.limits_vars)
                converted_result, converted_error = self.calculate_cartesian_integral_with_limits(converted_func, converted_limits)
            
            # Mostrar resultados
            self.display_results(func_str, converted_func, input_system, output_system, 
                               original_result, original_error, converted_result, converted_error)
            
            # Actualizar figuras
            self.create_region_figure()
            self.create_function_comparison_figure()
            
        except Exception as e:
            self.original_result_label.config(text=f"Error: {str(e)}")
            self.converted_result_label.config(text=f"Error: {str(e)}")
            self.comparison_result_label.config(text=f"Error: {str(e)}")

    def calculate_cartesian_integral(self, func_str):
        """Calcula integral en coordenadas cartesianas - CORREGIDO"""
        try:
            x_lower = float(self.limits_vars["x_lower"].get())
            x_upper = float(self.limits_vars["x_upper"].get())
            y_lower_str = self.limits_vars["y_lower"].get()
            y_upper_str = self.limits_vars["y_upper"].get()
            
            def integrand(y, x):
                return self.safe_eval(func_str, {'x': x, 'y': y})
            
            def y_lower_func(x):
                return self.safe_eval(y_lower_str, {'x': x})
            
            def y_upper_func(x):
                return self.safe_eval(y_upper_str, {'x': x})
            
            # dblquad(func, a, b, gfun, hfun) donde func(y,x)
            result, error = integrate.dblquad(integrand, x_lower, x_upper, y_lower_func, y_upper_func)
            return result, error
            
        except Exception as e:
            print(f"Error en cálculo cartesiano: {e}")
            return 0, float('inf')

    def calculate_cartesian_integral_with_limits(self, func_str, limits):
        """Calcula integral en cartesianas con límites dados - CORREGIDO"""
        try:
            x_lower = float(limits["x_lower"])
            x_upper = float(limits["x_upper"])
            y_lower_str = limits["y_lower"]
            y_upper_str = limits["y_upper"]
            
            def integrand(y, x):
                return self.safe_eval(func_str, {'x': x, 'y': y})
            
            def y_lower_func(x):
                return self.safe_eval(y_lower_str, {'x': x})
            
            def y_upper_func(x):
                return self.safe_eval(y_upper_str, {'x': x})
            
            result, error = integrate.dblquad(integrand, x_lower, x_upper, y_lower_func, y_upper_func)
            return result, error
            
        except Exception as e:
            print(f"Error en cálculo cartesiano con límites: {e}")
            return 0, float('inf')

    def calculate_polar_integral(self, func_str, limits):
        """Calcula integral en coordenadas polares - CORREGIDO"""
        try:
            r_lower = float(limits["r_lower"].get() if hasattr(limits["r_lower"], 'get') else limits["r_lower"])
            r_upper = float(limits["r_upper"].get() if hasattr(limits["r_upper"], 'get') else limits["r_upper"])
            theta_lower_str = limits["theta_lower"].get() if hasattr(limits["theta_lower"], 'get') else limits["theta_lower"]
            theta_upper_str = limits["theta_upper"].get() if hasattr(limits["theta_upper"], 'get') else limits["theta_upper"]
        
            theta_lower = self.safe_eval(theta_lower_str, {})
            theta_upper = self.safe_eval(theta_upper_str, {})
        
            def integrand(r, theta):
                # La función evaluada en coordenadas polares multiplicada por el jacobiano r
                f_value = self.safe_eval(func_str, {'r': r, 'theta': theta})
                return f_value * r  # Jacobiano
        
            # CORRECCIÓN CRÍTICA: Orden correcto para dblquad
            # dblquad(func, a, b, gfun, hfun) integra func(y,x) desde x=a hasta x=b, y desde y=gfun(x) hasta y=hfun(x)
            # Para polares: integramos ∫∫ f(r,θ) r dr dθ = ∫[θ_lower]^[θ_upper] ∫[r_lower]^[r_upper] f(r,θ) r dr dθ
            result, error = integrate.dblquad(
                lambda r, theta: integrand(r, theta),  # función a integrar
                theta_lower, theta_upper,              # límites de θ (variable exterior)
                lambda theta: r_lower,                 # límite inferior de r
                lambda theta: r_upper                  # límite superior de r
            )
        
            return result, error
        
        except Exception as e:
            print(f"Error en cálculo polar: {e}")
            return 0, float('inf')

    def display_results(self, original_func, converted_func, input_system, output_system,
                       original_result, original_error, converted_result, converted_error):
        """Muestra los resultados de la conversión"""
        
        # Resultado original
        original_text = f"SISTEMA ORIGINAL: {input_system.upper()}\n\n"
        original_text += f"Función: {original_func}\n\n"
        if input_system == "cartesianas":
            original_text += f"Límites:\n"
            original_text += f"x: {self.limits_vars['x_lower'].get()} ≤ x ≤ {self.limits_vars['x_upper'].get()}\n"
            original_text += f"y: {self.limits_vars['y_lower'].get()} ≤ y ≤ {self.limits_vars['y_upper'].get()}\n\n"
        else:
            original_text += f"Límites:\n"
            original_text += f"r: {self.limits_vars['r_lower'].get()} ≤ r ≤ {self.limits_vars['r_upper'].get()}\n"
            original_text += f"θ: {self.limits_vars['theta_lower'].get()} ≤ θ ≤ {self.limits_vars['theta_upper'].get()}\n\n"
        
        original_text += f"Resultado: {original_result:.8f}\n"
        original_text += f"Error estimado: {original_error:.2e}"
        
        self.original_result_label.config(text=original_text)
        
        # Resultado convertido
        converted_text = f"SISTEMA CONVERTIDO: {output_system.upper()}\n\n"
        converted_text += f"Función convertida:\n{converted_func}\n\n"
        
        if output_system == "polares":
            converted_text += f"Transformación aplicada:\n"
            converted_text += f"x = r·cos(θ)\n"
            converted_text += f"y = r·sin(θ)\n"
            converted_text += f"dA = r dr dθ (Jacobiano = r)\n\n"
        else:
            converted_text += f"Transformación aplicada:\n"
            converted_text += f"r = √(x² + y²)\n"
            converted_text += f"θ = arctan(y/x)\n"
            converted_text += f"dA = dx dy\n\n"
        
        converted_text += f"Resultado: {converted_result:.8f}\n"
        converted_text += f"Error estimado: {converted_error:.2e}"
        
        self.converted_result_label.config(text=converted_text)
        
        # Comparación
        difference = abs(original_result - converted_result)
        relative_error = difference / abs(original_result) * 100 if original_result != 0 else 0
        
        comparison_text = f"VERIFICACIÓN DEL CAMBIO DE VARIABLES\n\n"
        comparison_text += f"Resultado en {input_system}: {original_result:.8f}\n"
        comparison_text += f"Resultado en {output_system}: {converted_result:.8f}\n\n"
        comparison_text += f"Diferencia absoluta: {difference:.2e}\n"
        comparison_text += f"Error relativo: {relative_error:.6f}%\n\n"
        
        # Mostrar valor teórico esperado
        if original_func == "x**2 + y**2" and input_system == "cartesianas":
            # Detectar el radio del círculo
            x_lower = float(self.limits_vars["x_lower"].get())
            x_upper = float(self.limits_vars["x_upper"].get())
            if x_lower == -1 and x_upper == 1:
                theoretical = np.pi / 2
                comparison_text += f"Valor teórico esperado: π/2 = {theoretical:.8f}\n"
            elif x_lower == -2 and x_upper == 2:
                theoretical = 8 * np.pi
                comparison_text += f"Valor teórico esperado: 8π = {theoretical:.8f}\n"
        
        if relative_error < 1.0:
            comparison_text += "✅ CONVERSIÓN EXITOSA\n"
            comparison_text += "Los resultados coinciden, confirmando\n"
            comparison_text += "que el cambio de variables es correcto."
        else:
            comparison_text += "⚠️ DIFERENCIA SIGNIFICATIVA\n"
            comparison_text += "Puede deberse a:\n"
            comparison_text += "- Aproximaciones numéricas\n"
            comparison_text += "- Límites de integración diferentes\n"
            comparison_text += "- Complejidad de la conversión"
        
        self.comparison_result_label.config(text=comparison_text)

    def create_region_figure(self):
        """Crea la figura para visualizar la región de integración"""
        # Limpiar el marco
        for widget in self.region_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111, aspect='equal')
        
        try:
            # Obtener los límites actuales
            if self.input_system.get() == "cartesianas":
                x_lower = float(self.limits_vars["x_lower"].get())
                x_upper = float(self.limits_vars["x_upper"].get())
                
                # Determinar el radio del círculo
                if x_lower == -1 and x_upper == 1:
                    radius = 1
                elif x_lower == -2 and x_upper == 2:
                    radius = 2
                else:
                    radius = max(abs(x_lower), abs(x_upper))
                
                # Dibujar círculo
                circle = plt.Circle((0, 0), radius, fill=True, alpha=0.3, color='blue')
                ax.add_patch(circle)
                
                ax.set_xlim(-radius*1.2, radius*1.2)
                ax.set_ylim(-radius*1.2, radius*1.2)
                ax.set_title(f'Región de Integración\nCírculo de radio {radius}')
            else:
                # Sistema polar
                radius = float(self.limits_vars["r_upper"].get())
                circle = plt.Circle((0, 0), radius, fill=True, alpha=0.3, color='red')
                ax.add_patch(circle)
                
                ax.set_xlim(-radius*1.2, radius*1.2)
                ax.set_ylim(-radius*1.2, radius*1.2)
                ax.set_title(f'Región de Integración\nCírculo de radio {radius}')
            
            ax.grid(True)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            
        except Exception as e:
            ax.text(0.5, 0.5, f"Error al visualizar:\n{str(e)}", 
                   ha='center', va='center', transform=ax.transAxes)
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.region_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_function_comparison_figure(self):
        """Crea la figura para comparar las funciones en ambos sistemas"""
        # Limpiar el marco
        for widget in self.function_comparison_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        fig = plt.Figure(figsize=(12, 5))
        
        # Gráfico en coordenadas cartesianas
        ax1 = fig.add_subplot(121, projection='3d')
        ax2 = fig.add_subplot(122, projection='3d')
        
        try:
            # Determinar el radio basado en los límites actuales
            if self.input_system.get() == "cartesianas":
                x_lower = float(self.limits_vars["x_lower"].get())
                x_upper = float(self.limits_vars["x_upper"].get())
                radius = max(abs(x_lower), abs(x_upper))
            else:
                radius = float(self.limits_vars["r_upper"].get())
            
            # Crear malla de puntos
            x = np.linspace(-radius, radius, 30)
            y = np.linspace(-radius, radius, 30)
            X, Y = np.meshgrid(x, y)
            
            # Función ejemplo: x² + y²
            Z1 = X**2 + Y**2
            
            # Convertir a coordenadas polares
            r = np.sqrt(X**2 + Y**2)
            Z2 = r**2  # Equivalente en polares
            
            # Máscara para círculo
            mask = X**2 + Y**2 <= radius**2
            
            # Gráfico cartesiano
            surf1 = ax1.plot_surface(X*mask, Y*mask, Z1*mask, cmap='viridis', alpha=0.8)
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_zlabel('f(x,y)')
            ax1.set_title('Coordenadas Cartesianas\nf(x,y) = x² + y²')
            
            # Gráfico polar
            surf2 = ax2.plot_surface(X*mask, Y*mask, Z2*mask, cmap='plasma', alpha=0.8)
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            ax2.set_zlabel('f(r,θ)')
            ax2.set_title('Coordenadas Polares\nf(r,θ) = r²')
            
        except Exception as e:
            ax1.text2D(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', transform=ax1.transAxes)
            ax2.text2D(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', transform=ax2.transAxes)
        
        # Ajustar la figura
        fig.tight_layout()
        
        # Agregar la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.function_comparison_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
