import tkinter as tk
from tkinter import ttk
import webbrowser
import sys
import os

# Asegurarse de que podemos importar desde subdirectorios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class HelpTab:
    """Pestaña de ayuda y contacto"""
    
    def __init__(self, notebook):
        """Inicializa la pestaña de ayuda"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Ayuda")
        
        # Título
        title_label = ttk.Label(self.frame, text="Ayuda y Contacto", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Marco principal
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Información de contacto
        contact_frame = ttk.LabelFrame(main_frame, text="Información de Contacto")
        contact_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # WhatsApp
        whatsapp_frame = ttk.Frame(contact_frame)
        whatsapp_frame.pack(fill=tk.X, padx=20, pady=10)
        
        whatsapp_icon = ttk.Label(whatsapp_frame, text="📱")
        whatsapp_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        whatsapp_label = ttk.Label(whatsapp_frame, text="WhatsApp:", font=("Arial", 11, "bold"))
        whatsapp_label.pack(side=tk.LEFT, padx=(0, 10))
        
        whatsapp_number = ttk.Label(whatsapp_frame, text="+57 3106014652")
        whatsapp_number.pack(side=tk.LEFT)
        
        # Correo electrónico
        email_frame = ttk.Frame(contact_frame)
        email_frame.pack(fill=tk.X, padx=20, pady=10)
        
        email_icon = ttk.Label(email_frame, text="✉️")
        email_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        email_label = ttk.Label(email_frame, text="Correo Electrónico:", font=("Arial", 11, "bold"))
        email_label.pack(side=tk.LEFT, padx=(0, 10))
        
        email_address = ttk.Label(email_frame, text="dylanjaredbautistasierra03@gmail.com")
        email_address.pack(side=tk.LEFT)
        
        # GitHub
        github_frame = ttk.Frame(contact_frame)
        github_frame.pack(fill=tk.X, padx=20, pady=10)
        
        github_icon = ttk.Label(github_frame, text="🌐")
        github_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        github_label = ttk.Label(github_frame, text="Repositorio GitHub:", font=("Arial", 11, "bold"))
        github_label.pack(side=tk.LEFT, padx=(0, 10))
        
        github_link = ttk.Label(github_frame, text="https://github.com/BlackShadownis/Cambio-de-variables-en-integrales-dobles.git", 
                              foreground="blue", cursor="hand2")
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: self.open_url("https://github.com/BlackShadownis/Cambio-de-variables-en-integrales-dobles.git"))
        
        # Instrucciones de uso
        instructions_frame = ttk.LabelFrame(main_frame, text="Instrucciones de Uso")
        instructions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        instructions_text = tk.Text(instructions_frame, wrap=tk.WORD, height=15, width=60)
        instructions_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(instructions_text, command=instructions_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        instructions_text.config(yscrollcommand=scrollbar.set)
        
        # Contenido de las instrucciones
        instructions = """
INSTRUCCIONES DE USO

Este software está diseñado para ayudar a comprender y visualizar integrales dobles, con énfasis en el cambio de variables a coordenadas polares.

1. PESTAÑA DE INTRODUCCIÓN
   - Familiarízate con los conceptos teóricos básicos
   - Explora las visualizaciones de coordenadas cartesianas y polares

2. PESTAÑA DE TRANSFORMACIÓN
   - Selecciona diferentes curvas (cardioide, círculo, lemniscata, espiral)
   - Ajusta los parámetros para ver cómo cambian las curvas
   - Observa cómo se calculan las áreas usando coordenadas polares

3. PESTAÑA DE ÁREAS Y VOLÚMENES
   - Explora ejemplos de cálculo de áreas y volúmenes
   - Visualiza las regiones de integración y las superficies

4. PESTAÑA DE MOMENTOS DE INERCIA
   - Calcula momentos de inercia para diferentes distribuciones de masa
   - Visualiza cómo varía la densidad en diferentes regiones

5. PESTAÑA DE VALORES PROMEDIO
   - Calcula valores promedio de funciones sobre regiones
   - Visualiza la distribución de valores sobre la región

6. PESTAÑA DE INTEGRALES PERSONALIZADAS
   - Define tus propias funciones para integrar
   - Establece límites de integración personalizados
   - Visualiza la región de integración y la función

CONSEJOS:
- Puedes ajustar los parámetros en cada pestaña para explorar diferentes casos, ( no necesitas comprender calculo diferencial para usar el software)
- Utiliza las herramientas de zoom y desplazamiento en los gráficos
- Compara los resultados numéricos con los valores teóricos

Si tienes alguna pregunta o problema, no dudes en contactarnos usando la información proporcionada.
        """
        
        instructions_text.insert(tk.END, instructions)
        instructions_text.config(state=tk.DISABLED)  # Hacer el texto de solo lectura
    
    def open_url(self, url):
        """Abre una URL en el navegador predeterminado"""
        webbrowser.open_new(url)
