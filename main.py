import tkinter as tk
from tkinter import ttk
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import integrate
import sympy as sp

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.app import IntegralesApp

def main():
    """Función principal que inicia la aplicación"""
    root = tk.Tk()
    root.title("Integrales Dobles con Cambio de Variables")
    root.geometry("1200x800")
    
    # Crear la aplicación
    app = IntegralesApp(root)
    
    # Iniciar el bucle principal
    root.mainloop()

def explicar_teoria():
    print("TEORÍA DE CAMBIO DE VARIABLES EN INTEGRALES DOBLES")
    print("--------------------------------------------------")
    print("En coordenadas cartesianas, una integral doble se expresa como:")
    print("∫∫_R f(x,y) dA = ∫_a^b ∫_c^d f(x,y) dy dx")
    print("\nEn coordenadas polares, usamos la transformación:")
    print("x = r·cos(θ), y = r·sin(θ)")
    print("El jacobiano de esta transformación es |J| = r")
    print("Por lo tanto, la integral se convierte en:")
    print("∫∫_R f(x,y) dA = ∫_α^β ∫_0^h(θ) f(r·cos(θ), r·sin(θ)) · r dr dθ")
    print("\nEste cambio es especialmente útil cuando la región de integración")
    print("o la función tienen simetría circular o radial.\n")

def calcular_areas_volumenes():
    print("\n=== APLICACIÓN 1: CÁLCULO DE ÁREAS Y VOLÚMENES ===")
    print("------------------------------------------------")
    
    # Ejemplo 1: Área de un cardioide
    print("\nEjemplo 1.1: Área de un cardioide r = a(1 + cos(θ))")
    
    # Parámetros
    a = 2.0  # Parámetro del cardioide
    
    # En coordenadas polares, el área es ∫∫ r dr dθ
    def integrando_area(r, theta):
        return r  # Solo el jacobiano para calcular el área
    
    # Función que define el cardioide
    def r_cardioide(theta):
        return a * (1 + np.cos(theta))
    
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
    
    print(f"Área del cardioide (numérica): {area_numerica:.6f}")
    print(f"Área del cardioide (simbólica): {float(area_simbolica):.6f}")
    print(f"Fórmula exacta: 6πa² = {6*np.pi*a**2:.6f}")
    
    # Visualización del cardioide
    plt.figure(figsize=(10, 5))
    
    # En coordenadas polares
    ax1 = plt.subplot(121, projection='polar')
    theta_vals = np.linspace(0, 2*np.pi, 200)
    r_vals = r_cardioide(theta_vals)
    ax1.plot(theta_vals, r_vals)
    ax1.fill(theta_vals, r_vals, alpha=0.3)
    ax1.set_title('Cardioide r = a(1 + cos(θ))')
    
    # En coordenadas cartesianas
    ax2 = plt.subplot(122)
    x = r_vals * np.cos(theta_vals)
    y = r_vals * np.sin(theta_vals)
    ax2.plot(x, y)
    ax2.fill(x, y, alpha=0.3)
    ax2.set_aspect('equal')
    ax2.grid(True)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('Cardioide en coordenadas cartesianas')
    
    plt.tight_layout()
    plt.savefig('cardioide.png')
    print("Gráfico guardado como 'cardioide.png'")
    
    # Ejemplo 2: Volumen bajo una superficie
    print("\nEjemplo 1.2: Volumen bajo la superficie z = 4 - x² - y² sobre un círculo de radio 1")
    
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
    
    print(f"Volumen bajo la superficie (numérico): {volumen:.6f}")
    print(f"Volumen bajo la superficie (simbólico): {float(vol_simbolico):.6f}")
    print(f"Fórmula exacta: 2π = {2*np.pi:.6f}")
    
    # Visualización
    fig = plt.figure(figsize=(12, 5))
    
    # Región de integración
    ax1 = fig.add_subplot(121)
    circle = plt.Circle((0, 0), 1, fill=True, alpha=0.3)
    ax1.add_patch(circle)
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.2, 1.2)
    ax1.set_aspect('equal')
    ax1.grid(True)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('Región de integración: círculo de radio 1')
    
    # Superficie
    ax2 = fig.add_subplot(122, projection='3d')
    r = np.linspace(0, 1, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    r, theta = np.meshgrid(r, theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = 4 - x**2 - y**2
    
    surf = ax2.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.8)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')
    ax2.set_title('Superficie z = 4 - x² - y²')
    
    plt.tight_layout()
    plt.savefig('volumen_paraboloide.png')
    print("Gráfico guardado como 'volumen_paraboloide.png'")

def calcular_momentos_inercia():
    print("\n=== APLICACIÓN 2: CÁLCULO DE MOMENTOS DE INERCIA ===")
    print("--------------------------------------------------")
    
    # Ejemplo: Momento de inercia de un disco con densidad variable
    print("\nEjemplo 2.1: Momento de inercia de un disco con densidad ρ(r) = ρ₀(1 - r²/R²)")
    
    # Parámetros
    R = 5.0  # Radio del disco en cm
    rho_0 = 3.0  # Densidad en el centro en g/cm³
    
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
    
    print(f"Radio del disco: {R} cm")
    print(f"Densidad en el centro: {rho_0} g/cm³")
    print(f"Momento de inercia (numérico): {momento:.4f} g·cm²")
    print(f"Momento de inercia (teórico): {teorico:.4f} g·cm²")
    print(f"Error relativo: {abs(momento-teorico)/teorico*100:.8f}%\n")
    
    # Visualización
    fig = plt.figure(figsize=(15, 5))
    
    # Distribución de densidad en 2D
    ax1 = fig.add_subplot(131)
    r_vals = np.linspace(0, R, 100)
    theta_vals = np.linspace(0, 2*np.pi, 100)
    r_grid, theta_grid = np.meshgrid(r_vals, theta_vals)
    x_grid = r_grid * np.cos(theta_grid)
    y_grid = r_grid * np.sin(theta_grid)
    z_grid = densidad(r_grid)
    
    contour = ax1.contourf(x_grid, y_grid, z_grid, cmap='viridis', levels=20)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x (cm)')
    ax1.set_ylabel('y (cm)')
    ax1.set_title('Distribución de densidad ρ(r)')
    plt.colorbar(contour, ax=ax1, label='Densidad (g/cm³)')
    
    # Perfil de densidad
    ax2 = fig.add_subplot(132)
    ax2.plot(r_vals, densidad(r_vals))
    ax2.set_xlabel('r (cm)')
    ax2.set_ylabel('ρ(r) (g/cm³)')
    ax2.set_title('Perfil de densidad')
    ax2.grid(True)
    
    # Representación 3D de la densidad
    ax3 = fig.add_subplot(133, projection='3d')
    surf = ax3.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', alpha=0.8)
    ax3.set_xlabel('x (cm)')
    ax3.set_ylabel('y (cm)')
    ax3.set_zlabel('ρ(r) (g/cm³)')
    ax3.set_title('Densidad variable')
    
    plt.tight_layout()
    plt.savefig('momento_inercia.png')
    print("Gráfico guardado como 'momento_inercia.png'")
    
    # Ejemplo 2: Momento de inercia de una placa con forma de cardioide
    print("\nEjemplo 2.2: Momento de inercia de una placa con forma de cardioide r = a(1 + cos(θ))")
    
    # Parámetros
    a = 2.0  # Parámetro del cardioide
    rho = 1.0  # Densidad uniforme
    
    # Función que define el cardioide
    def r_cardioide(theta):
        return a * (1 + np.cos(theta))
    
    # Momento de inercia respecto al origen
    def integrando_momento_cardioide(r, theta):
        return rho * r**2 * r  # Densidad * r² * jacobiano
    
    # Integración numérica
    momento_cardioide, error = integrate.dblquad(
        integrando_momento_cardioide,
        0, 2*np.pi,  # límites de theta
        lambda theta: 0, r_cardioide  # límites de r
    )
    
    print(f"Parámetro del cardioide: a = {a}")
    print(f"Densidad: {rho} g/cm³")
    print(f"Momento de inercia respecto al origen: {momento_cardioide:.4f} g·cm²")
    
    # Visualización
    plt.figure(figsize=(10, 5))
    
    # En coordenadas polares
    ax1 = plt.subplot(121, projection='polar')
    theta_vals = np.linspace(0, 2*np.pi, 200)
    r_vals = r_cardioide(theta_vals)
    ax1.plot(theta_vals, r_vals)
    ax1.fill(theta_vals, r_vals, alpha=0.3)
    ax1.set_title('Cardioide r = a(1 + cos(θ))')
    
    # En coordenadas cartesianas
    ax2 = plt.subplot(122)
    x = r_vals * np.cos(theta_vals)
    y = r_vals * np.sin(theta_vals)
    ax2.plot(x, y)
    ax2.fill(x, y, alpha=0.3)
    ax2.set_aspect('equal')
    ax2.grid(True)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('Cardioide en coordenadas cartesianas')
    
    plt.tight_layout()
    plt.savefig('momento_cardioide.png')
    print("Gráfico guardado como 'momento_cardioide.png'")

def calcular_valores_promedio():
    print("\n=== APLICACIÓN 3: CÁLCULO DE VALORES PROMEDIO ===")
    print("----------------------------------------------")
    
    # Ejemplo 1: Valor promedio de temperatura en un disco
    print("\nEjemplo 3.1: Valor promedio de temperatura T(x,y) = T₀(1 - r²/R²) en un disco")
    
    # Parámetros
    R = 10.0  # Radio del disco en cm
    T_0 = 100.0  # Temperatura en el centro en °C
    
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
    
    print(f"Radio del disco: {R} cm")
    print(f"Temperatura en el centro: {T_0} °C")
    print(f"Temperatura promedio (numérica): {temp_avg:.4f} °C")
    print(f"Temperatura promedio (teórica): {teorico:.4f} °C")
    print(f"Error relativo: {abs(temp_avg-teorico)/teorico*100:.8f}%\n")
    
    # Visualización
    fig = plt.figure(figsize=(12, 5))
    
    # Distribución de temperatura en 2D
    ax1 = fig.add_subplot(121)
    r_vals = np.linspace(0, R, 100)
    theta_vals = np.linspace(0, 2*np.pi, 100)
    r_grid, theta_grid = np.meshgrid(r_vals, theta_vals)
    x_grid = r_grid * np.cos(theta_grid)
    y_grid = r_grid * np.sin(theta_grid)
    z_grid = temperatura(r_grid)
    
    contour = ax1.contourf(x_grid, y_grid, z_grid, cmap='hot', levels=20)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x (cm)')
    ax1.set_ylabel('y (cm)')
    ax1.set_title('Distribución de temperatura T(r)')
    plt.colorbar(contour, ax=ax1, label='Temperatura (°C)')
    
    # Perfil de temperatura
    ax2 = fig.add_subplot(122)
    ax2.plot(r_vals, temperatura(r_vals))
    ax2.axhline(y=temp_avg, color='r', linestyle='--', label=f'Promedio: {temp_avg:.1f} °C')
    ax2.set_xlabel('r (cm)')
    ax2.set_ylabel('T(r) (°C)')
    ax2.set_title('Perfil de temperatura')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('temperatura_promedio.png')
    print("Gráfico guardado como 'temperatura_promedio.png'")
    
    # Ejemplo 2: Valor promedio de una función sobre un cardioide
    print("\nEjemplo 3.2: Valor promedio de f(r,θ) = r·cos(θ) sobre un cardioide r = a(1 + cos(θ))")
    
    # Parámetros
    a = 2.0  # Parámetro del cardioide
    
    # Función a promediar: f(r,θ) = r·cos(θ) = x
    def f_polar(r, theta):
        return r * np.cos(theta) * r  # f * jacobiano
    
    # Función que define el cardioide
    def r_cardioide(theta):
        return a * (1 + np.cos(theta))
    
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
    
    print(f"Parámetro del cardioide: a = {a}")
    print(f"Valor promedio de f(r,θ) = r·cos(θ): {f_avg:.4f}")
    print(f"Área del cardioide: {denom_card:.4f}")
    
    # Visualización
    plt.figure(figsize=(12, 5))
    
    # Región en coordenadas cartesianas
    ax1 = plt.subplot(121)
    theta_vals = np.linspace(0, 2*np.pi, 200)
    r_vals = r_cardioide(theta_vals)
    x = r_vals * np.cos(theta_vals)
    y = r_vals * np.sin(theta_vals)
    
    # Crear una malla para visualizar la función
    x_grid = np.linspace(-4, 4, 100)
    y_grid = np.linspace(-4, 4, 100)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = X  # La función es f(x,y) = x
    
    # Dibujar el contorno
    ax1.contourf(X, Y, Z, cmap='coolwarm', levels=20)
    ax1.plot(x, y, 'k-', linewidth=2)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('f(x,y) = x sobre el cardioide')
    
    # Visualización 3D
    ax2 = plt.subplot(122, projection='3d')
    
    # Convertir a coordenadas cartesianas para visualización
    r_grid, theta_grid = np.meshgrid(np.linspace(0, 3*a, 50), np.linspace(0, 2*np.pi, 50))
    x_grid = r_grid * np.cos(theta_grid)
    y_grid = r_grid * np.sin(theta_grid)
    z_grid = x_grid  # La función es f(x,y) = x
    
    # Crear una máscara para mostrar solo dentro del cardioide
    mask = r_grid <= r_cardioide(theta_grid)
    
    # Dibujar la superficie
    surf = ax2.plot_surface(
        x_grid * mask, y_grid * mask, z_grid * mask, 
        cmap='coolwarm', alpha=0.8
    )
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('f(x,y) = x')
    ax2.set_title(f'Valor promedio: {f_avg:.4f}')
    
    plt.tight_layout()
    plt.savefig('promedio_cardioide.png')
    print("Gráfico guardado como 'promedio_cardioide.png'")

if __name__ == "__main__":
    main()
