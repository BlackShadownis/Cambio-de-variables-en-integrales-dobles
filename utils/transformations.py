import numpy as np

def cartesian_to_polar(x, y):
    """
    Convierte coordenadas cartesianas a polares
    
    Args:
        x: Coordenada x
        y: Coordenada y
    
    Returns:
        r: Radio
        theta: Ángulo en radianes
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta

def polar_to_cartesian(r, theta):
    """
    Convierte coordenadas polares a cartesianas
    
    Args:
        r: Radio
        theta: Ángulo en radianes
    
    Returns:
        x: Coordenada x
        y: Coordenada y
    """
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def jacobian_polar():
    """
    Devuelve el jacobiano de la transformación de coordenadas polares
    
    Returns:
        jacobian: Función que calcula el jacobiano
    """
    def jacobian(r, theta):
        return r
    
    return jacobian
