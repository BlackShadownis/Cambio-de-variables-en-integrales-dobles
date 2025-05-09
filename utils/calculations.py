import numpy as np
import sympy as sp
from scipy import integrate

def calculate_area(r_func, theta_limits):
    """
    Calcula el área de una región en coordenadas polares
    
    Args:
        r_func: Función que define el radio en términos de theta
        theta_limits: Tupla con los límites de integración para theta
    
    Returns:
        area: Área numérica
        area_symbolic: Área simbólica (None si no se puede calcular)
    """
    # Integración numérica
    def integrand(theta):
        r = r_func(theta)
        return 0.5 * r**2
    
    area, error = integrate.quad(integrand, theta_limits[0], theta_limits[1])
    
    # Integración simbólica
    try:
        theta = sp.symbols('theta')
        r_sym = r_func(theta)
        area_symbolic = sp.integrate(0.5 * r_sym**2, (theta, theta_limits[0], theta_limits[1]))
    except:
        area_symbolic = None
    
    return area, area_symbolic

def calculate_volume(r_func, z_func, theta_limits):
    """
    Calcula el volumen bajo una superficie en coordenadas polares
    
    Args:
        r_func: Función que define el radio en términos de theta
        z_func: Función que define la altura en términos de r y theta
        theta_limits: Tupla con los límites de integración para theta
    
    Returns:
        volume: Volumen numérico
        volume_symbolic: Volumen simbólico (None si no se puede calcular)
    """
    # Integración numérica
    def integrand(r, theta):
        z = z_func(r, theta)
        return z * r
    
    volume, error = integrate.dblquad(
        integrand,
        theta_limits[0], theta_limits[1],  # límites de theta
        lambda theta: 0, lambda theta: r_func(theta)  # límites de r
    )
    
    # Integración simbólica
    try:
        r, theta = sp.symbols('r theta')
        z_sym = z_func(r, theta)
        volume_symbolic = sp.integrate(
            sp.integrate(z_sym * r, (r, 0, r_func(theta))),
            (theta, theta_limits[0], theta_limits[1])
        )
    except:
        volume_symbolic = None
    
    return volume, volume_symbolic
