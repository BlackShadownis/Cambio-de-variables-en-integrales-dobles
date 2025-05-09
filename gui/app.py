import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar las pestañas
from gui.tabs.intro_tab import IntroTab
from gui.tabs.transformation_tab import TransformationTab
from gui.tabs.custom_integral_tab import CustomIntegralTab
from gui.tabs.areas_volumes_tab import AreasVolumesTab
from gui.tabs.moments_tab import MomentsTab
from gui.tabs.average_values_tab import AverageValuesTab
from gui.tabs.animation_tab import AnimationTab
from gui.tabs.integration_steps_tab import IntegrationStepsTab

class IntegralesApp:
    """Clase principal de la aplicación de integrales dobles"""
    
    def __init__(self, root):
        """Inicializa la aplicación principal"""
        self.root = root
        
        # Crear un notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.intro_tab = IntroTab(self.notebook)
        self.transformation_tab = TransformationTab(self.notebook)
        self.areas_volumes_tab = AreasVolumesTab(self.notebook)
        self.moments_tab = MomentsTab(self.notebook)
        self.average_values_tab = AverageValuesTab(self.notebook)
        self.custom_integral_tab = CustomIntegralTab(self.notebook)
        self.animation_tab = AnimationTab(self.notebook)
        self.integration_steps_tab = IntegrationStepsTab(self.notebook)
        
        # Configurar estilo
        self.configure_style()
    
    def configure_style(self):
        """Configura el estilo de la aplicación"""
        style = ttk.Style()
        
        # Configurar el estilo de los botones
        style.configure('TButton', font=('Arial', 11))
        
        # Configurar el estilo de las etiquetas
        style.configure('TLabel', font=('Arial', 11))
        
        # Configurar el estilo de los marcos
        style.configure('TFrame', background='#f0f0f0')
        
        # Configurar el estilo de las pestañas
        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'))
