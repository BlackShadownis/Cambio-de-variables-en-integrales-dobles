import tkinter as tk
from tkinter import ttk
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class CreditsTab:
    """Pestaña de créditos"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de créditos"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Créditos")
        
        # Título
        title_label = ttk.Label(self.frame, text="Créditos", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Marco principal
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Logo o imagen (placeholder)
        logo_frame = ttk.Frame(main_frame)
        logo_frame.pack(pady=20)
        
        logo_label = ttk.Label(logo_frame, text="🧮 Integrales Dobles 📊", 
                             font=("Arial", 24, "bold"))
        logo_label.pack()
        
        subtitle_label = ttk.Label(logo_frame, text="Software Educativo", 
                                 font=("Arial", 14))
        subtitle_label.pack(pady=5)
        
        # Desarrolladores
        developers_frame = ttk.LabelFrame(main_frame, text="Desarrolladores")
        developers_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Desarrollador 1
        dev1_frame = ttk.Frame(developers_frame)
        dev1_frame.pack(fill=tk.X, padx=20, pady=10)
        
        dev1_icon = ttk.Label(dev1_frame, text="👨‍💻")
        dev1_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        dev1_name = ttk.Label(dev1_frame, text="Dylan Jared Bautista Sierra", 
                            font=("Arial", 11, "bold"))
        dev1_name.pack(side=tk.LEFT)
        
        # Desarrollador 2
        dev2_frame = ttk.Frame(developers_frame)
        dev2_frame.pack(fill=tk.X, padx=20, pady=10)
        
        dev2_icon = ttk.Label(dev2_frame, text="👨‍💻")
        dev2_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        dev2_name = ttk.Label(dev2_frame, text="Daniel Alejandro Arevalo Guecha", 
                            font=("Arial", 11, "bold"))
        dev2_name.pack(side=tk.LEFT)
        
        # Desarrollador 3
        dev3_frame = ttk.Frame(developers_frame)
        dev3_frame.pack(fill=tk.X, padx=20, pady=10)
        
        dev3_icon = ttk.Label(dev3_frame, text="👨‍💻")
        dev3_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        dev3_name = ttk.Label(dev3_frame, text="Juan Marco Parada Carpio", 
                            font=("Arial", 11, "bold"))
        dev3_name.pack(side=tk.LEFT)
        
        # Docente
        teacher_frame = ttk.LabelFrame(main_frame, text="Docente")
        teacher_frame.pack(fill=tk.X, padx=20, pady=10)
        
        teacher_info_frame = ttk.Frame(teacher_frame)
        teacher_info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        teacher_icon = ttk.Label(teacher_info_frame, text="👨‍🏫")
        teacher_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        teacher_name = ttk.Label(teacher_info_frame, text="ING. Darwin Orlando Cardozo Sarmiento", 
                               font=("Arial", 11, "bold"))
        teacher_name.pack(side=tk.LEFT)
        
        # Información institucional
        institution_frame = ttk.Frame(main_frame)
        institution_frame.pack(fill=tk.X, padx=20, pady=20)
        
        institution_label = ttk.Label(institution_frame, 
                                    text="Fundación De Estudios Superiores Comfanorte", 
                                    font=("Arial", 12, "bold"))
        institution_label.pack()
        
        department_label = ttk.Label(institution_frame, 
                                   text="Ingeniería de Software", 
                                   font=("Arial", 11))
        department_label.pack()
        
        year_label = ttk.Label(institution_frame, 
                             text="2025", 
                             font=("Arial", 11))
        year_label.pack(pady=5)
        
        # Pie de página
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        footer_label = ttk.Label(footer_frame, 
                               text="Desarrollado con ❤️ para estudiantes de cálculo multivariable", 
                               font=("Arial", 10, "italic"))
        footer_label.pack()
