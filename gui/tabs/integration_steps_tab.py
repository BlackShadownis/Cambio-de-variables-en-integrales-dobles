import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from matplotlib import cm
import matplotlib.animation as animation
from scipy import integrate
import sympy as sp
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class IntegrationStepsTab:
    """Pestaña para visualizar el proceso de integración paso a paso"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de visualización de integración"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Proceso de Integración")
        
        # Título
        title_label = ttk.Label(self.frame, text="Visualización del Proceso de Integración", 
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
        self.example_var = tk.StringVar(value="circulo")
        examples = ttk.Combobox(controls_frame, textvariable=self.example_var, 
                              values=["circulo", "cardioide", "paraboloide"])
        examples.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        examples.bind("<<ComboboxSelected>>", self.update_example)
        
        # Marco para parámetros
        params_frame = ttk.LabelFrame(controls_frame, text="Parámetros")
        params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Número de divisiones
        ttk.Label(params_frame, text="Divisiones:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.divisions_var = tk.IntVar(value=10)
        divisions_scale = ttk.Scale(params_frame, from_=4, to=20, orient=tk.HORIZONTAL, 
                                  variable=self.divisions_var, length=200)
        divisions_scale.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.divisions_label = ttk.Label(params_frame, text="10")
        self.divisions_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        divisions_scale.bind("<Motion>", self.update_divisions_label)
        
        # Velocidad de la animación
        ttk.Label(params_frame, text="Velocidad:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(params_frame, from_=0.1, to=2.0, orient=tk.HORIZONTAL, 
                              variable=self.speed_var, length=200)
        speed_scale.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.speed_label = ttk.Label(params_frame, text="1.0")
        self.speed_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        speed_scale.bind("<Motion>", self.update_speed_label)
        
        # Botones de control
        controls_buttons_frame = ttk.Frame(controls_frame)
        controls_buttons_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        self.play_button = ttk.Button(controls_buttons_frame, text="Reproducir", command=self.play_animation)
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.pause_button = ttk.Button(controls_buttons_frame, text="Pausar", command=self.pause_animation)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reset_button = ttk.Button(controls_buttons_frame, text="Reiniciar", command=self.reset_animation)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Marco para resultados
        results_frame = ttk.LabelFrame(controls_frame, text="Resultados")
        results_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Etiqueta para resultados
        self.result_label = ttk.Label(results_frame, text="", wraplength=300)
        self.result_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Marco para la visualización (derecha)
        self.viz_frame = ttk.Frame(main_frame)
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Variables para la animación
        self.anim = None
        self.paused = False
        self.fig = None
        self.canvas = None
        
        # Crear la animación inicial
        self.create_animation()
    
    def update_divisions_label(self, event=None):
        """Actualiza la etiqueta de divisiones"""
        value = self.divisions_var.get()
        self.divisions_label.config(text=f"{value}")
    
    def update_speed_label(self, event=None):
        """Actualiza la etiqueta de velocidad"""
        value = self.speed_var.get()
        self.speed_label.config(text=f"{value:.1f}")
    
    def update_example(self, event=None):
        """Actualiza el ejemplo seleccionado"""
        self.create_animation()
    
    def play_animation(self):
        """Reproduce la animación"""
        if self.anim and self.paused:
            self.anim.event_source.start()
            self.paused = False
    
    def pause_animation(self):
        """Pausa la animación"""
        if self.anim and not self.paused:
            self.anim.event_source.stop()
            self.paused = True
    
    def reset_animation(self):
        """Reinicia la animación"""
        self.create_animation()
    
    def create_animation(self):
        """Crea la animación seleccionada"""
        # Limpiar el marco de visualización
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        # Crear una nueva figura
        self.fig = plt.Figure(figsize=(8, 8))
        
        # Obtener el tipo de ejemplo
        example_type = self.example_var.get()
        
        if example_type == "circulo":
            self.create_circle_integration_animation()
        elif example_type == "cardioide":
            self.create_cardioid_integration_animation()
        elif example_type == "paraboloide":
            self.create_paraboloid_integration_animation()
        
        # Agregar la figura al marco
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(self.canvas, self.viz_frame)
        toolbar.update()
    
    def create_circle_integration_animation(self):
        """Crea una animación del proceso de integración para un círculo"""
        # Configurar la figura
        ax1 = self.fig.add_subplot(121, aspect='equal')
        ax2 = self.fig.add_subplot(122, projection='3d')
        
        # Parámetros
        R = 2.0  # Radio del círculo
        n_divisions = self.divisions_var.get()
        
        # Crear una malla de puntos en coordenadas polares
        r = np.linspace(0, R, n_divisions)
        theta = np.linspace(0, 2*np.pi, n_divisions)
        dr = R / (n_divisions - 1)
        dtheta = 2*np.pi / (n_divisions - 1)
        
        # Función a integrar (área del círculo)
        def f(r, theta):
            return r  # Jacobiano para el área
        
        # Calcular el valor exacto
        exact_value = np.pi * R**2
        
        # Inicializar los gráficos
        patches = []
        bars = []
        
        # Inicializar el resultado numérico
        self.numerical_result = 0.0
        
        # Función de inicialización
        def init():
            ax1.clear()
            ax2.clear()
            
            # Configurar los ejes
            ax1.set_xlim(-R-0.5, R+0.5)
            ax1.set_ylim(-R-0.5, R+0.5)
            ax1.grid(True)
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_title('Región de Integración')
            
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            ax2.set_zlabel('f(r,θ) = r')
            ax2.set_title('Función a Integrar')
            
            # Dibujar el círculo completo
            circle = plt.Circle((0, 0), R, fill=False, color='blue', linestyle='--')
            ax1.add_patch(circle)
            
            # Dibujar la función completa
            r_grid, theta_grid = np.meshgrid(r, theta)
            x_grid = r_grid * np.cos(theta_grid)
            y_grid = r_grid * np.sin(theta_grid)
            z_grid = f(r_grid, theta_grid)
            
            ax2.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', alpha=0.3)
            
            # Reiniciar el resultado numérico
            self.numerical_result = 0.0
            
            # Actualizar la etiqueta de resultados
            self.result_label.config(text=f"Integral de r dr dθ sobre un círculo de radio {R}\n\n"
                                        f"Valor exacto: {exact_value:.6f}\n\n"
                                        f"Aproximación numérica: {self.numerical_result:.6f}\n\n"
                                        f"Error: {abs(self.numerical_result - exact_value):.6f}")
            
            return []
        
        # Función de animación
        def animate(i):
            if i == 0:
                init()
                return []
            
            # Índices para r y theta
            i_r = (i - 1) // (n_divisions - 1)
            i_theta = (i - 1) % (n_divisions - 1)
            
            if i_r < n_divisions - 1 and i_theta < n_divisions - 1:
                # Coordenadas del sector
                r1 = r[i_r]
                r2 = r[i_r + 1]
                theta1 = theta[i_theta]
                theta2 = theta[i_theta + 1]
                
                # Vértices del sector en coordenadas cartesianas
                x1 = r1 * np.cos(theta1)
                y1 = r1 * np.sin(theta1)
                x2 = r2 * np.cos(theta1)
                y2 = r2 * np.sin(theta1)
                x3 = r2 * np.cos(theta2)
                y3 = r2 * np.sin(theta2)
                x4 = r1 * np.cos(theta2)
                y4 = r1 * np.sin(theta2)
                
                # Dibujar el sector en la región
                sector = plt.Polygon([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 
                                    fill=True, alpha=0.5, color='blue')
                ax1.add_patch(sector)
                patches.append(sector)
                
                # Calcular el valor de la función en el centro del sector
                r_center = (r1 + r2) / 2
                theta_center = (theta1 + theta2) / 2
                f_value = f(r_center, theta_center)
                
                # Coordenadas del centro del sector
                x_center = r_center * np.cos(theta_center)
                y_center = r_center * np.sin(theta_center)
                
                # Dibujar el prisma en 3D
                x_corners = [x1, x2, x3, x4]
                y_corners = [y1, y2, y3, y4]
                z_bottom = np.zeros(4)
                z_top = np.ones(4) * f_value
                
                # Caras del prisma
                verts = [
                    list(zip(x_corners, y_corners, z_bottom)),  # Base inferior
                    list(zip(x_corners, y_corners, z_top)),     # Base superior
                    list(zip([x1, x2, x2, x1], [y1, y2, y2, y1], [z_bottom[0], z_bottom[1], z_top[1], z_top[0]])),  # Cara 1
                    list(zip([x2, x3, x3, x2], [y2, y3, y3, y2], [z_bottom[1], z_bottom[2], z_top[2], z_top[1]])),  # Cara 2
                    list(zip([x3, x4, x4, x3], [y3, y4, y4, y3], [z_bottom[2], z_bottom[3], z_top[3], z_top[2]])),  # Cara 3
                    list(zip([x4, x1, x1, x4], [y4, y1, y1, y4], [z_bottom[3], z_bottom[0], z_top[0], z_top[3]]))   # Cara 4
                ]
                
                # Dibujar el prisma
                collection = ax2.add_collection3d(plt.art3d.Poly3DCollection(
                    verts, alpha=0.5, color='blue'))
                bars.append(collection)
                
                # Actualizar el resultado numérico
                area_element = r_center * dr * dtheta
                self.numerical_result += area_element
                
                # Actualizar la etiqueta de resultados
                self.result_label.config(text=f"Integral de r dr dθ sobre un círculo de radio {R}\n\n"
                                            f"Valor exacto: {exact_value:.6f}\n\n"
                                            f"Aproximación numérica: {self.numerical_result:.6f}\n\n"
                                            f"Error: {abs(self.numerical_result - exact_value):.6f}\n\n"
                                            f"Progreso: {i}/{(n_divisions-1)**2} sectores")
            
            return patches + bars
        
        # Crear la animación
        self.anim = animation.FuncAnimation(
            self.fig, animate, init_func=init, frames=(n_divisions-1)**2 + 1,
            interval=100/self.speed_var.get(), blit=False
        )
        
        # Ajustar la figura
        self.fig.tight_layout()
    
    def create_cardioid_integration_animation(self):
        """Crea una animación del proceso de integración para un cardioide"""
        # Configurar la figura
        ax1 = self.fig.add_subplot(121, aspect='equal')
        ax2 = self.fig.add_subplot(122, projection='3d')
        
        # Parámetros
        a = 1.0  # Parámetro del cardioide
        n_divisions = self.divisions_var.get()
        
        # Función que define el cardioide
        def r_cardioide(theta):
            return a * (1 + np.cos(theta))
        
        # Crear una malla de puntos en coordenadas polares
        theta = np.linspace(0, 2*np.pi, n_divisions)
        dtheta = 2*np.pi / (n_divisions - 1)
        
        # Calcular los valores máximos de r para cada theta
        r_max = np.array([r_cardioide(t) for t in theta])
        
        # Crear una malla de r para cada theta
        r = [np.linspace(0, r_max[i], n_divisions) for i in range(n_divisions)]
        
        # Función a integrar (área del cardioide)
        def f(r, theta):
            return r  # Jacobiano para el área
        
        # Calcular el valor exacto
        exact_value = 6 * np.pi * a**2
        
        # Inicializar los gráficos
        patches = []
        bars = []
        
        # Inicializar el resultado numérico
        self.numerical_result = 0.0
        
        # Función de inicialización
        def init():
            ax1.clear()
            ax2.clear()
            
            # Configurar los ejes
            ax1.set_xlim(-2*a, 2*a)
            ax1.set_ylim(-2*a, 2*a)
            ax1.grid(True)
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_title('Región de Integración')
            
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            ax2.set_zlabel('f(r,θ) = r')
            ax2.set_title('Función a Integrar')
            
            # Dibujar el cardioide completo
            theta_vals = np.linspace(0, 2*np.pi, 200)
            r_vals = r_cardioide(theta_vals)
            x = r_vals * np.cos(theta_vals)
            y = r_vals * np.sin(theta_vals)
            ax1.plot(x, y, 'b--')
            
            # Dibujar la función completa
            r_grid, theta_grid = np.meshgrid(np.linspace(0, 2*a, 30), np.linspace(0, 2*np.pi, 30))
            x_grid = r_grid * np.cos(theta_grid)
            y_grid = r_grid * np.sin(theta_grid)
            z_grid = f(r_grid, theta_grid)
            
            # Crear una máscara para mostrar solo dentro del cardioide
            mask = r_grid <= np.array([r_cardioide(t) for t in theta_grid[0, :]])
            
            ax2.plot_surface(
                x_grid * mask, y_grid * mask, z_grid * mask,
                cmap='viridis', alpha=0.3
            )
            
            # Reiniciar el resultado numérico
            self.numerical_result = 0.0
            
            # Actualizar la etiqueta de resultados
            self.result_label.config(text=f"Integral de r dr dθ sobre un cardioide r = a(1 + cos(θ))\n\n"
                                        f"Valor exacto: {exact_value:.6f}\n\n"
                                        f"Aproximación numérica: {self.numerical_result:.6f}\n\n"
                                        f"Error: {abs(self.numerical_result - exact_value):.6f}")
            
            return []
        
        # Función de animación
        def animate(i):
            if i == 0:
                init()
                return []
            
            # Índices para theta
            i_theta = (i - 1) % (n_divisions - 1)
            
            if i_theta < n_divisions - 1:
                # Coordenadas del sector
                theta1 = theta[i_theta]
                theta2 = theta[i_theta + 1]
                
                # Calcular los valores de r para este sector
                r_vals1 = r[i_theta]
                r_vals2 = r[i_theta + 1]
                
                # Número de divisiones radiales a mostrar en esta iteración
                n_radial = min(n_divisions, (i - 1) // (n_divisions - 1) + 1)
                
                for j in range(n_radial - 1):
                    # Coordenadas del sector
                    r1 = r_vals1[j]
                    r2 = r_vals1[j + 1]
                    r3 = r_vals2[j + 1]
                    r4 = r_vals2[j]
                    
                    # Vértices del sector en coordenadas cartesianas
                    x1 = r1 * np.cos(theta1)
                    y1 = r1 * np.sin(theta1)
                    x2 = r2 * np.cos(theta1)
                    y2 = r2 * np.sin(theta1)
                    x3 = r3 * np.cos(theta2)
                    y3 = r3 * np.sin(theta2)
                    x4 = r4 * np.cos(theta2)
                    y4 = r4 * np.sin(theta2)
                    
                    # Dibujar el sector en la región
                    sector = plt.Polygon([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 
                                        fill=True, alpha=0.5, color='blue')
                    ax1.add_patch(sector)
                    patches.append(sector)
                    
                    # Calcular el valor de la función en el centro del sector
                    r_center = (r1 + r2 + r3 + r4) / 4
                    theta_center = (theta1 + theta2) / 2
                    f_value = f(r_center, theta_center)
                    
                    # Coordenadas del centro del sector
                    x_center = r_center * np.cos(theta_center)
                    y_center = r_center * np.sin(theta_center)
                    
                    # Dibujar el prisma en 3D
                    x_corners = [x1, x2, x3, x4]
                    y_corners = [y1, y2, y3, y4]
                    z_bottom = np.zeros(4)
                    z_top = np.ones(4) * f_value
                    
                    # Caras del prisma
                    verts = [
                        list(zip(x_corners, y_corners, z_bottom)),  # Base inferior
                        list(zip(x_corners, y_corners, z_top)),     # Base superior
                        list(zip([x1, x2, x2, x1], [y1, y2, y2, y1], [z_bottom[0], z_bottom[1], z_top[1], z_top[0]])),  # Cara 1
                        list(zip([x2, x3, x3, x2], [y2, y3, y3, y2], [z_bottom[1], z_bottom[2], z_top[2], z_top[1]])),  # Cara 2
                        list(zip([x3, x4, x4, x3], [y3, y4, y4, y3], [z_bottom[2], z_bottom[3], z_top[3], z_top[2]])),  # Cara 3
                        list(zip([x4, x1, x1, x4], [y4, y1, y1, y4], [z_bottom[3], z_bottom[0], z_top[0], z_top[3]]))   # Cara 4
                    ]
                    
                    # Dibujar el prisma
                    collection = ax2.add_collection3d(plt.art3d.Poly3DCollection(
                        verts, alpha=0.5, color='blue'))
                    bars.append(collection)
                    
                    # Actualizar el resultado numérico
                    dr1 = r_vals1[j + 1] - r_vals1[j]
                    dr2 = r_vals2[j + 1] - r_vals2[j]
                    area_element = r_center * ((dr1 + dr2) / 2) * dtheta
                    self.numerical_result += area_element
                
                # Actualizar la etiqueta de resultados
                total_sectors = (n_divisions - 1) * (n_divisions - 1)
                current_sector = (i - 1) // (n_divisions - 1) * (n_divisions - 1) + i_theta + 1
                self.result_label.config(text=f"Integral de r dr dθ sobre un cardioide r = a(1 + cos(θ))\n\n"
                                            f"Valor exacto: {exact_value:.6f}\n\n"
                                            f"Aproximación numérica: {self.numerical_result:.6f}\n\n"
                                            f"Error: {abs(self.numerical_result - exact_value):.6f}\n\n"
                                            f"Progreso: {current_sector}/{total_sectors} sectores")
            
            return patches + bars
        
        # Crear la animación
        self.anim = animation.FuncAnimation(
            self.fig, animate, init_func=init, frames=(n_divisions-1)**2 + 1,
            interval=100/self.speed_var.get(), blit=False
        )
        
        # Ajustar la figura
        self.fig.tight_layout()
    
    def create_paraboloid_integration_animation(self):
        """Crea una animación del proceso de integración para un paraboloide"""
        # Configurar la figura
        ax1 = self.fig.add_subplot(121, aspect='equal')
        ax2 = self.fig.add_subplot(122, projection='3d')
        
        # Parámetros
        R = 1.0  # Radio del círculo
        n_divisions = self.divisions_var.get()
        
        # Crear una malla de puntos en coordenadas polares
        r = np.linspace(0, R, n_divisions)
        theta = np.linspace(0, 2*np.pi, n_divisions)
        dr = R / (n_divisions - 1)
        dtheta = 2*np.pi / (n_divisions - 1)
        
        # Función a integrar (volumen bajo el paraboloide)
        def f(r, theta):
            return (4 - r**2) * r  # (4 - r²) * r (jacobiano)
        
        # Calcular el valor exacto
        exact_value = 2 * np.pi
        
        # Inicializar los gráficos
        patches = []
        bars = []
        
        # Inicializar el resultado numérico
        self.numerical_result = 0.0
        
        # Función de inicialización
        def init():
            ax1.clear()
            ax2.clear()
            
            # Configurar los ejes
            ax1.set_xlim(-R-0.5, R+0.5)
            ax1.set_ylim(-R-0.5, R+0.5)
            ax1.grid(True)
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_title('Región de Integración')
            
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            ax2.set_zlabel('z = 4 - x² - y²')
            ax2.set_title('Función a Integrar')
            
            # Dibujar el círculo completo
            circle = plt.Circle((0, 0), R, fill=False, color='blue', linestyle='--')
            ax1.add_patch(circle)
            
            # Dibujar la función completa
            r_grid, theta_grid = np.meshgrid(r, theta)
            x_grid = r_grid * np.cos(theta_grid)
            y_grid = r_grid * np.sin(theta_grid)
            z_grid = 4 - x_grid**2 - y_grid**2
            
            ax2.plot_surface(x_grid, y_grid, z_grid, cmap='coolwarm', alpha=0.3)
            
            # Reiniciar el resultado numérico
            self.numerical_result = 0.0
            
            # Actualizar la etiqueta de resultados
            self.result_label.config(text=f"Integral de (4 - r²)·r dr dθ sobre un círculo de radio {R}\n\n"
                                        f"Valor exacto: {exact_value:.6f}\n\n"
                                        f"Aproximación numérica: {self.numerical_result:.6f}\n\n"
                                        f"Error: {abs(self.numerical_result - exact_value):.6f}")
            
            return []
        
        # Función de animación
        def animate(i):
            if i == 0:
                init()
                return []
            
            # Índices para r y theta
            i_r = (i - 1) // (n_divisions - 1)
            i_theta = (i - 1) % (n_divisions - 1)
            
            if i_r < n_divisions - 1 and i_theta < n_divisions - 1:
                # Coordenadas del sector
                r1 = r[i_r]
                r2 = r[i_r + 1]
                theta1 = theta[i_theta]
                theta2 = theta[i_theta + 1]
                
                # Vértices del sector en coordenadas cartesianas
                x1 = r1 * np.cos(theta1)
                y1 = r1 * np.sin(theta1)
                x2 = r2 * np.cos(theta1)
                y2 = r2 * np.sin(theta1)
                x3 = r2 * np.cos(theta2)
                y3 = r2 * np.sin(theta2)
                x4 = r1 * np.cos(theta2)
                y4 = r1 * np.sin(theta2)
                
                # Dibujar el sector en la región
                sector = plt.Polygon([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 
                                    fill=True, alpha=0.5, color='blue')
                ax1.add_patch(sector)
                patches.append(sector)
                
                # Calcular el valor de la función en el centro del sector
                r_center = (r1 + r2) / 2
                theta_center = (theta1 + theta2) / 2
                x_center = r_center * np.cos(theta_center)
                y_center = r_center * np.sin(theta_center)
                z_center = 4 - x_center**2 - y_center**2
                
                # Calcular el valor del integrando
                f_value = (4 - r_center**2) * r_center
                
                # Dibujar el prisma en 3D
                x_corners = [x1, x2, x3, x4]
                y_corners = [y1, y2, y3, y4]
                z_corners = [4 - x1**2 - y1**2, 4 - x2**2 - y2**2, 4 - x3**2 - y3**2, 4 - x4**2 - y4**2]
                z_bottom = np.zeros(4)
                
                # Caras del prisma
                verts = [
                    list(zip(x_corners, y_corners, z_bottom)),  # Base inferior
                    list(zip(x_corners, y_corners, z_corners)),  # Base superior (paraboloide)
                    list(zip([x1, x2, x2, x1], [y1, y2, y2, y1], [z_bottom[0], z_bottom[1], z_corners[1], z_corners[0]])),  # Cara 1
                    list(zip([x2, x3, x3, x2], [y2, y3, y3, y2], [z_bottom[1], z_bottom[2], z_corners[2], z_corners[1]])),  # Cara 2
                    list(zip([x3, x4, x4, x3], [y3, y4, y4, y3], [z_bottom[2], z_bottom[3], z_corners[3], z_corners[2]])),  # Cara 3
                    list(zip([x4, x1, x1, x4], [y4, y1, y1, y4], [z_bottom[3], z_bottom[0], z_corners[0], z_corners[3]]))   # Cara 4
                ]
                
                # Dibujar el prisma
                collection = ax2.add_collection3d(plt.art3d.Poly3DCollection(
                    verts, alpha=0.5, color='blue'))
                bars.append(collection)
                
                # Actualizar el resultado numérico
                volume_element = f_value * dr * dtheta
                self.numerical_result += volume_element
                
                # Actualizar la etiqueta de resultados
                self.result_label.config(text=f"Integral de (4 - r²)·r dr dθ sobre un círculo de radio {R}\n\n"
                                            f"Valor exacto: {exact_value:.6f}\n\n"
                                            f"Aproximación numérica: {self.numerical_result:.6f}\n\n"
                                            f"Error: {abs(self.numerical_result - exact_value):.6f}\n\n"
                                            f"Progreso: {i}/{(n_divisions-1)**2} sectores")
            
            return patches + bars
        
        # Crear la animación
        self.anim = animation.FuncAnimation(
            self.fig, animate, init_func=init, frames=(n_divisions-1)**2 + 1,
            interval=100/self.speed_var.get(), blit=False
        )
        
        # Ajustar la figura
        self.fig.tight_layout()
