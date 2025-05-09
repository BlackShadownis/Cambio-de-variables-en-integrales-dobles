import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.animation as animation
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class AnimationTab:
    """Pestaña para animaciones de transformación entre sistemas de coordenadas"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de animaciones"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Animaciones")
        
        # Título
        title_label = ttk.Label(self.frame, text="Animaciones de Transformación de Coordenadas", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Marco principal con dos columnas
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Marco para controles (izquierda)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, expand=False)
        
        # Selector de animación
        ttk.Label(controls_frame, text="Seleccione una animación:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.animation_var = tk.StringVar(value="cartesian_to_polar")
        animations = ttk.Combobox(controls_frame, textvariable=self.animation_var, 
                                values=["cartesian_to_polar", "polar_to_cartesian", "grid_transformation"])
        animations.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        animations.bind("<<ComboboxSelected>>", self.update_animation)
        
        # Marco para parámetros
        params_frame = ttk.LabelFrame(controls_frame, text="Parámetros")
        params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Velocidad de la animación
        ttk.Label(params_frame, text="Velocidad:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(params_frame, from_=0.1, to=2.0, orient=tk.HORIZONTAL, 
                              variable=self.speed_var, length=200)
        speed_scale.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.speed_label = ttk.Label(params_frame, text="1.0")
        self.speed_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        speed_scale.bind("<Motion>", self.update_speed_label)
        
        # Número de puntos
        ttk.Label(params_frame, text="Puntos:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.points_var = tk.IntVar(value=10)
        points_scale = ttk.Scale(params_frame, from_=5, to=20, orient=tk.HORIZONTAL, 
                               variable=self.points_var, length=200)
        points_scale.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.points_label = ttk.Label(params_frame, text="10")
        self.points_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        points_scale.bind("<Motion>", self.update_points_label)
        
        # Botones de control
        controls_buttons_frame = ttk.Frame(controls_frame)
        controls_buttons_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        self.play_button = ttk.Button(controls_buttons_frame, text="Reproducir", command=self.play_animation)
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.pause_button = ttk.Button(controls_buttons_frame, text="Pausar", command=self.pause_animation)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reset_button = ttk.Button(controls_buttons_frame, text="Reiniciar", command=self.reset_animation)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Marco para explicación
        explanation_frame = ttk.LabelFrame(controls_frame, text="Explicación")
        explanation_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        self.explanation_text = tk.Text(explanation_frame, wrap=tk.WORD, height=10, width=30)
        self.explanation_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
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
    
    def update_speed_label(self, event=None):
        """Actualiza la etiqueta de velocidad"""
        value = self.speed_var.get()
        self.speed_label.config(text=f"{value:.1f}")
    
    def update_points_label(self, event=None):
        """Actualiza la etiqueta de puntos"""
        value = self.points_var.get()
        self.points_label.config(text=f"{value}")
    
    def update_animation(self, event=None):
        """Actualiza la animación seleccionada"""
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
        
        # Obtener el tipo de animación
        animation_type = self.animation_var.get()
        
        if animation_type == "cartesian_to_polar":
            self.create_cartesian_to_polar_animation()
        elif animation_type == "polar_to_cartesian":
            self.create_polar_to_cartesian_animation()
        elif animation_type == "grid_transformation":
            self.create_grid_transformation_animation()
        
        # Agregar la figura al marco
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(self.canvas, self.viz_frame)
        toolbar.update()
    
    def create_cartesian_to_polar_animation(self):
        """Crea una animación de transformación de coordenadas cartesianas a polares"""
        # Configurar la figura
        ax1 = self.fig.add_subplot(121, aspect='equal')
        ax2 = self.fig.add_subplot(122, projection='polar')
        
        # Número de puntos
        n_points = self.points_var.get()
        
        # Generar puntos aleatorios en coordenadas cartesianas
        np.random.seed(42)  # Para reproducibilidad
        x = np.random.uniform(-5, 5, n_points)
        y = np.random.uniform(-5, 5, n_points)
        
        # Convertir a coordenadas polares
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # Inicializar los gráficos
        points_cart, = ax1.plot([], [], 'bo', markersize=8)
        points_polar, = ax2.plot([], [], 'ro', markersize=8)
        
        # Configurar los ejes
        ax1.set_xlim(-6, 6)
        ax1.set_ylim(-6, 6)
        ax1.grid(True)
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title('Coordenadas Cartesianas')
        
        ax2.set_title('Coordenadas Polares')
        
        # Función de inicialización
        def init():
            points_cart.set_data([], [])
            points_polar.set_data([], [])
            return points_cart, points_polar
        
        # Función de animación
        def animate(i):
            # Interpolar entre coordenadas cartesianas y polares
            t = min(1.0, i / 50.0)  # Normalizar entre 0 y 1
            
            # Actualizar los puntos
            points_cart.set_data(x[:i+1], y[:i+1])
            points_polar.set_data(theta[:i+1], r[:i+1])
            
            return points_cart, points_polar
        
        # Crear la animación
        self.anim = animation.FuncAnimation(
            self.fig, animate, init_func=init, frames=n_points,
            interval=100/self.speed_var.get(), blit=True
        )
        
        # Ajustar la figura
        self.fig.tight_layout()
        
        # Actualizar la explicación
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, """
Transformación de Coordenadas Cartesianas a Polares

Esta animación muestra cómo los puntos en coordenadas cartesianas (x, y) se transforman a coordenadas polares (r, θ).

La transformación está dada por:
r = √(x² + y²)
θ = arctan(y/x)

Donde:
- r es la distancia desde el origen al punto
- θ es el ángulo medido desde el eje x positivo

Esta transformación es útil para integrales dobles sobre regiones con simetría circular o radial.
        """)
    
    def create_polar_to_cartesian_animation(self):
        """Crea una animación de transformación de coordenadas polares a cartesianas"""
        # Configurar la figura
        ax1 = self.fig.add_subplot(121, projection='polar')
        ax2 = self.fig.add_subplot(122, aspect='equal')
        
        # Número de puntos
        n_points = self.points_var.get()
        
        # Generar puntos aleatorios en coordenadas polares
        np.random.seed(42)  # Para reproducibilidad
        r = np.random.uniform(0, 5, n_points)
        theta = np.random.uniform(0, 2*np.pi, n_points)
        
        # Convertir a coordenadas cartesianas
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Inicializar los gráficos
        points_polar, = ax1.plot([], [], 'ro', markersize=8)
        points_cart, = ax2.plot([], [], 'bo', markersize=8)
        
        # Configurar los ejes
        ax1.set_title('Coordenadas Polares')
        
        ax2.set_xlim(-6, 6)
        ax2.set_ylim(-6, 6)
        ax2.grid(True)
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_title('Coordenadas Cartesianas')
        
        # Función de inicialización
        def init():
            points_polar.set_data([], [])
            points_cart.set_data([], [])
            return points_polar, points_cart
        
        # Función de animación
        def animate(i):
            # Interpolar entre coordenadas polares y cartesianas
            t = min(1.0, i / 50.0)  # Normalizar entre 0 y 1
            
            # Actualizar los puntos
            points_polar.set_data(theta[:i+1], r[:i+1])
            points_cart.set_data(x[:i+1], y[:i+1])
            
            return points_polar, points_cart
        
        # Crear la animación
        self.anim = animation.FuncAnimation(
            self.fig, animate, init_func=init, frames=n_points,
            interval=100/self.speed_var.get(), blit=True
        )
        
        # Ajustar la figura
        self.fig.tight_layout()
        
        # Actualizar la explicación
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, """
Transformación de Coordenadas Polares a Cartesianas

Esta animación muestra cómo los puntos en coordenadas polares (r, θ) se transforman a coordenadas cartesianas (x, y).

La transformación está dada por:
x = r·cos(θ)
y = r·sin(θ)

Donde:
- r es la distancia desde el origen al punto
- θ es el ángulo medido desde el eje x positivo

Esta transformación es útil para convertir integrales en coordenadas polares de vuelta a coordenadas cartesianas.
        """)
    
    def create_grid_transformation_animation(self):
        """Crea una animación de transformación de una malla de coordenadas"""
        # Configurar la figura
        ax = self.fig.add_subplot(111, aspect='equal')
        
        # Crear una malla de puntos en coordenadas polares
        r = np.linspace(0, 5, 6)
        theta = np.linspace(0, 2*np.pi, 13)[:-1]  # Excluir el último para evitar duplicados
        
        r_grid, theta_grid = np.meshgrid(r, theta)
        x_grid = r_grid * np.cos(theta_grid)
        y_grid = r_grid * np.sin(theta_grid)
        
        # Inicializar los gráficos
        lines_r = []
        lines_theta = []
        
        # Líneas de radio constante (círculos)
        for i in range(len(r)):
            line, = ax.plot([], [], 'b-', alpha=0.5)
            lines_r.append(line)
        
        # Líneas de ángulo constante (radios)
        for i in range(len(theta)):
            line, = ax.plot([], [], 'r-', alpha=0.5)
            lines_theta.append(line)
        
        # Puntos de la malla
        points, = ax.plot([], [], 'ko', markersize=3)
        
        # Configurar los ejes
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Transformación de Malla de Coordenadas')
        
        # Función de inicialización
        def init():
            for line in lines_r + lines_theta:
                line.set_data([], [])
            points.set_data([], [])
            return lines_r + lines_theta + [points]
        
        # Función de animación
        def animate(i):
            t = i / 100.0  # Parámetro de interpolación
            
            # Interpolar entre una malla cartesiana y una malla polar
            if t < 0.5:
                # De cartesiana a polar
                t_norm = t / 0.5  # Normalizar entre 0 y 1
                
                # Malla cartesiana
                x_cart = np.linspace(-5, 5, 6)
                y_cart = np.linspace(-5, 5, 6)
                
                # Interpolar las líneas de radio constante (horizontales a círculos)
                for j, line in enumerate(lines_r):
                    circle_x = r[j] * np.cos(np.linspace(0, 2*np.pi, 100))
                    circle_y = r[j] * np.sin(np.linspace(0, 2*np.pi, 100))
                    
                    # Interpolar de línea horizontal a círculo
                    if j == 0:  # El origen es un caso especial
                        line_x = np.zeros(100)
                        line_y = np.zeros(100)
                    else:
                        line_x = np.linspace(-5, 5, 100)
                        line_y = np.ones(100) * (y_cart[j] - 2.5)
                    
                    x = (1 - t_norm) * line_x + t_norm * circle_x
                    y = (1 - t_norm) * line_y + t_norm * circle_y
                    
                    line.set_data(x, y)
                
                # Interpolar las líneas de ángulo constante (verticales a radios)
                for j, line in enumerate(lines_theta):
                    radius_x = np.linspace(0, 5, 100) * np.cos(theta[j])
                    radius_y = np.linspace(0, 5, 100) * np.sin(theta[j])
                    
                    # Interpolar de línea vertical a radio
                    line_x = np.ones(100) * (x_cart[j % 6] - 2.5)
                    line_y = np.linspace(-5, 5, 100)
                    
                    x = (1 - t_norm) * line_x + t_norm * radius_x
                    y = (1 - t_norm) * line_y + t_norm * radius_y
                    
                    line.set_data(x, y)
                
                # Interpolar los puntos de la malla
                x_points = (1 - t_norm) * (x_grid * 0 + np.linspace(-5, 5, 6)[np.newaxis, :].repeat(12, axis=0)) + t_norm * x_grid
                y_points = (1 - t_norm) * (y_grid * 0 + np.linspace(-5, 5, 6)[np.newaxis, :].repeat(12, axis=0).T.flatten().reshape(12, 6)) + t_norm * y_grid
                
                points.set_data(x_points.flatten(), y_points.flatten())
                
            else:
                # De polar a cartesiana
                t_norm = (t - 0.5) / 0.5  # Normalizar entre 0 y 1
                
                # Malla cartesiana
                x_cart = np.linspace(-5, 5, 6)
                y_cart = np.linspace(-5, 5, 6)
                
                # Interpolar las líneas de radio constante (círculos a horizontales)
                for j, line in enumerate(lines_r):
                    circle_x = r[j] * np.cos(np.linspace(0, 2*np.pi, 100))
                    circle_y = r[j] * np.sin(np.linspace(0, 2*np.pi, 100))
                    
                    # Interpolar de círculo a línea horizontal
                    if j == 0:  # El origen es un caso especial
                        line_x = np.zeros(100)
                        line_y = np.zeros(100)
                    else:
                        line_x = np.linspace(-5, 5, 100)
                        line_y = np.ones(100) * (y_cart[j] - 2.5)
                    
                    x = (1 - t_norm) * circle_x + t_norm * line_x
                    y = (1 - t_norm) * circle_y + t_norm * line_y
                    
                    line.set_data(x, y)
                
                # Interpolar las líneas de ángulo constante (radios a verticales)
                for j, line in enumerate(lines_theta):
                    radius_x = np.linspace(0, 5, 100) * np.cos(theta[j])
                    radius_y = np.linspace(0, 5, 100) * np.sin(theta[j])
                    
                    # Interpolar de radio a línea vertical
                    line_x = np.ones(100) * (x_cart[j % 6] - 2.5)
                    line_y = np.linspace(-5, 5, 100)
                    
                    x = (1 - t_norm) * radius_x + t_norm * line_x
                    y = (1 - t_norm) * radius_y + t_norm * line_y
                    
                    line.set_data(x, y)
                
                # Interpolar los puntos de la malla
                x_points = (1 - t_norm) * x_grid + t_norm * (x_grid * 0 + np.linspace(-5, 5, 6)[np.newaxis, :].repeat(12, axis=0))
                y_points = (1 - t_norm) * y_grid + t_norm * (y_grid * 0 + np.linspace(-5, 5, 6)[np.newaxis, :].repeat(12, axis=0).T.flatten().reshape(12, 6))
                
                points.set_data(x_points.flatten(), y_points.flatten())
            
            return lines_r + lines_theta + [points]
        
        # Crear la animación
        self.anim = animation.FuncAnimation(
            self.fig, animate, init_func=init, frames=200,
            interval=20/self.speed_var.get(), blit=True
        )
        
        # Ajustar la figura
        self.fig.tight_layout()
        
        # Actualizar la explicación
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, """
Transformación de Malla de Coordenadas

Esta animación muestra cómo una malla de coordenadas cartesianas se transforma en una malla de coordenadas polares y viceversa.

En coordenadas cartesianas:
- Las líneas horizontales tienen y constante
- Las líneas verticales tienen x constante

En coordenadas polares:
- Los círculos tienen r constante
- Las líneas radiales tienen θ constante

Esta visualización ayuda a entender cómo cambia el elemento de área dA = dx dy a dA = r dr dθ en la transformación.
        """)
