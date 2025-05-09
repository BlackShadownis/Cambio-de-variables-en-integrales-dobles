import numpy as np
import matplotlib.pyplot as plt

def plot_region(ax, r_func, theta_range, title):
    """
    Dibuja una región en coordenadas polares
    
    Args:
        ax: Eje de matplotlib
        r_func: Función que define el radio en términos de theta
        theta_range: Tupla con el rango de theta
        title: Título del gráfico
    """
    # Crear valores para theta
    theta = np.linspace(theta_range[0], theta_range[1], 200)
    
    # Calcular r
    r = np.array([r_func(t) for t in theta])
    
    # Convertir a coordenadas cartesianas
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Dibujar la curva
    ax.plot(x, y, 'b-')
    
    # Rellenar la región
    ax.fill(x, y, alpha=0.3)
    
    # Configurar los ejes
    r_max = np.max(r)
    ax.set_xlim(-r_max * 1.2, r_max * 1.2)
    ax.set_ylim(-r_max * 1.2, r_max * 1.2)
    ax.grid(True)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)

def plot_surface(ax, r_func, z_func, theta_range, title):
    """
    Dibuja una superficie en coordenadas polares
    
    Args:
        ax: Eje de matplotlib
        r_func: Función que define el radio en términos de theta
        z_func: Función que define la altura en términos de r y theta
        theta_range: Tupla con el rango de theta
        title: Título del gráfico
    """
    # Crear una malla de puntos en coordenadas polares
    theta = np.linspace(theta_range[0], theta_range[1], 50)
    
    # Encontrar el valor máximo de r
    r_max = 0
    for t in theta:
        r_val = r_func(t)
        if r_val > r_max:
            r_max = r_val
    
    # Crear valores para r
    r = np.linspace(0, r_max, 50)
    
    # Crear la malla
    R, Theta = np.meshgrid(r, theta)
    
    # Convertir a coordenadas cartesianas
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    
    # Calcular Z
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = z_func(R[i, j], Theta[i, j])
    
    # Crear una máscara para mostrar solo dentro de la región
    mask = R <= np.array([r_func(t) for t in Theta[0, :]])
    
    # Dibujar la superficie
    surf = ax.plot_surface(
        X, Y, Z,
        cmap='viridis', alpha=0.8
    )
    
    # Configurar los ejes
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title)
