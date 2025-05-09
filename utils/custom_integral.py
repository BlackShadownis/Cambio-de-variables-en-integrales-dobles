import numpy as np
import sympy as sp
from scipy import integrate

def parse_expression(expr_str, variables):
    """
    Parsea una expresión matemática en string a una función evaluable

    Args:
        expr_str: String con la expresión matemática
        variables: Lista de nombres de variables en la expresión

    Returns:
        Función evaluable
    """
    # Reemplazar funciones matemáticas comunes por sus equivalentes en numpy
    expr_str = expr_str.replace('sin', 'np.sin')
    expr_str = expr_str.replace('cos', 'np.cos')
    expr_str = expr_str.replace('tan', 'np.tan')
    expr_str = expr_str.replace('exp', 'np.exp')
    expr_str = expr_str.replace('log', 'np.log')
    expr_str = expr_str.replace('sqrt', 'np.sqrt')
    expr_str = expr_str.replace('pi', 'np.pi')
    expr_str = expr_str.replace('e', 'np.e')

    # Crear una función lambda que evalúe la expresión
    var_str = ', '.join(variables)
    func_str = f"lambda {var_str}: {expr_str}"

    return eval(func_str)

def evaluate_double_integral(func_str, coord_system, limits, variable_limits=False):
    """
    Evalúa una integral doble numérica y simbólicamente si es posible

    Args:
        func_str: String con la función a integrar
        coord_system: Sistema de coordenadas ('cartesianas' o 'polares')
        limits: Diccionario con los límites de integración
        variable_limits: Booleano que indica si los límites son variables

    Returns:
        result: Resultado numérico
        error: Error estimado
        symbolic_result: Resultado simbólico (None si no se puede calcular)
    """
    if coord_system == 'cartesianas':
        if variable_limits:
            x_lower = limits['x_lower']
            x_upper = limits['x_upper']
            y_lower_expr = limits['y_lower_expr']
            y_upper_expr = limits['y_upper_expr']
            
            # Definir la función para integración numérica
            def integrand(y, x):
                return eval(func_str)
            
            # Integración numérica
            result, error = integrate.dblquad(
                integrand,
                x_lower, x_upper,
                lambda x: eval(y_lower_expr),
                lambda x: eval(y_upper_expr)
            )
            
            # Integración simbólica
            try:
                x, y = sp.symbols('x y')
                expr = sp.sympify(func_str)
                symbolic_result = sp.integrate(
                    sp.integrate(expr, (y, sp.sympify(y_lower_expr), sp.sympify(y_upper_expr))), 
                    (x, x_lower, x_upper)
                )
            except:
                symbolic_result = None
            
        else:
            x_lower = limits['x_lower']
            x_upper = limits['x_upper']
            y_lower = limits['y_lower']
            y_upper = limits['y_upper']
            
            # Definir la función para integración numérica
            def integrand(y, x):
                return eval(func_str)
            
            # Integración numérica
            result, error = integrate.dblquad(
                integrand,
                x_lower, x_upper,
                lambda x: y_lower,
                lambda x: y_upper
            )
            
            # Integración simbólica
            try:
                x, y = sp.symbols('x y')
                expr = sp.sympify(func_str)
                symbolic_result = sp.integrate(
                    sp.integrate(expr, (y, y_lower, y_upper)), 
                    (x, x_lower, x_upper)
                )
            except:
                symbolic_result = None

    elif coord_system == 'polares':
        # Reemplazar theta por t para evitar problemas
        func_str_mod = func_str.replace('theta', 't')
        
        r_lower = limits['r_lower']
        theta_lower = limits['theta_lower']
        theta_upper = limits['theta_upper']
        
        if variable_limits:
            r_upper_expr = limits['r_upper_expr'].replace('theta', 't')
            
            # Definir la función para integración numérica
            def integrand(t, r):
                # El jacobiano en coordenadas polares es r
                return eval(func_str_mod) * r
            
            # Integración numérica
            result, error = integrate.dblquad(
                integrand,
                theta_lower, theta_upper,
                lambda t: r_lower,
                lambda t: eval(r_upper_expr)
            )
            
            # La integración simbólica con límites variables es más compleja
            symbolic_result = None
            
        else:
            r_upper = limits['r_upper']
            
            # Definir la función para integración numérica
            def integrand(t, r):
                # El jacobiano en coordenadas polares es r
                return eval(func_str_mod) * r
            
            # Integración numérica
            result, error = integrate.dblquad(
                integrand,
                theta_lower, theta_upper,
                lambda t: r_lower,
                lambda t: r_upper
            )
            
            # Integración simbólica
            try:
                r, theta = sp.symbols('r theta')
                expr = sp.sympify(func_str) * r  # No olvidar el jacobiano
                symbolic_result = sp.integrate(
                    sp.integrate(expr, (r, r_lower, r_upper)), 
                    (theta, theta_lower, theta_upper)
                )
            except:
                symbolic_result = None

    return result, error, symbolic_result

def get_integration_limits(coord_system, limits_vars, variable_limits):
    """
    Obtiene los límites de integración a partir de las variables de la interfaz

    Args:
        coord_system: Sistema de coordenadas ('cartesianas' o 'polares')
        limits_vars: Diccionario con las variables de los límites
        variable_limits: Booleano que indica si los límites son variables

    Returns:
        limits: Diccionario con los límites de integración
    """
    limits = {}

    if coord_system == 'cartesianas':
        limits['x_lower'] = float(limits_vars["x_lower"].get())
        limits['x_upper'] = float(limits_vars["x_upper"].get())
        
        if variable_limits:
            limits['y_lower_expr'] = limits_vars["y_lower_expr"].get()
            limits['y_upper_expr'] = limits_vars["y_upper_expr"].get()
        else:
            limits['y_lower'] = float(limits_vars["y_lower"].get())
            limits['y_upper'] = float(limits_vars["y_upper"].get())

    elif coord_system == 'polares':
        limits['r_lower'] = float(limits_vars["r_lower"].get())
        
        theta_lower_str = limits_vars["theta_lower"].get()
        theta_upper_str = limits_vars["theta_upper"].get()
        
        # Convertir expresiones de límites a valores numéricos
        limits['theta_lower'] = eval(theta_lower_str.replace('pi', 'np.pi'))
        limits['theta_upper'] = eval(theta_upper_str.replace('pi', 'np.pi'))
        
        if variable_limits:
            limits['r_upper_expr'] = limits_vars["r_upper_expr"].get()
        else:
            limits['r_upper'] = float(limits_vars["r_upper"].get())

    return limits
