# Definición de estilos basados en la paleta de colores proporcionada
COLORS = {
    "primary": {
        "turquesa": "#00B4D8",
        "dorado": "#E6B012",
    },
    "secondary": {
        "azul_marino": "#003A5D",
        "azul_medio": "#0077B6",
    },
    "neutral": {
        "blanco": "#FFFFFF",
        "gris": "#A3A3A3",
    },
    "functional": {
        "verde": "#4CAF50",
        "rojo": "#F44336",
    },
    
}

# Estilos compartidos
STYLES = {
    "base": {
        "width": "100%",
        "min_height": "100vh",
        "background_color": COLORS["neutral"]["blanco"],
        "font_family": "'Poppins', sans-serif",
    },
    "container": {
        "max_width": "1200px",
        "margin": "0 auto",
        "padding": "0 1rem",
    },
    "section": {
        "padding": "4rem 0",
    },
    "heading": {
        "color": COLORS["secondary"]["azul_marino"],
        "font_weight": "bold",
        "margin_bottom": "1.5rem",
    },
    "heading_primary": {
        "color": COLORS["primary"]["turquesa"],
        "font_size": "2.5rem",
        "font_weight": "bold",
        "text_align": "center",
        "margin_bottom": "1rem",
    },
    "heading_secondary": {
        "color": COLORS["secondary"]["azul_marino"],
        "font_size": "2rem",
        "font_weight": "bold",
        "margin_bottom": "1rem",
    },
    "paragraph": {
        "color": COLORS["secondary"]["azul_marino"],
        "font_size": "1rem",
        "line_height": "1.6",
        "margin_bottom": "1rem",
    },
    "button_primary": {
        "background_color": COLORS["primary"]["turquesa"],
        "color": COLORS["neutral"]["blanco"],
        "padding": "0.75rem 1.5rem",
        "border_radius": "0.375rem",
        "font_weight": "bold",
        "border": "none",
        "cursor": "pointer",
        "transition": "all 0.3s ease",
        "_hover": {
            "background_color": "#0EAAA9",  # Versión un poco más oscura del turquesa
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
        }
    },
    "button_secondary": {
        "background_color": COLORS["primary"]["dorado"],
        "color": COLORS["neutral"]["blanco"],
        "padding": "0.75rem 1.5rem",
        "border_radius": "0.375rem",
        "font_weight": "bold",
        "border": "none",
        "cursor": "pointer",
        "transition": "all 0.3s ease",
        "_hover": {
            "background_color": "#D4A000",  # Versión un poco más oscura del dorado
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
        }
    },
    "card": {
        "background_color": COLORS["neutral"]["blanco"],
        "border_radius": "0.5rem",
        "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "padding": "2rem",
        "transition": "all 0.3s ease",
        "_hover": {
            "transform": "translateY(-5px)",
            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.1)",
        }
    },
    "icon": {
        "color": COLORS["primary"]["turquesa"],
        "font_size": "2rem",
        "margin_bottom": "1rem",
    },
    
    
    # Estilos específicos para el login
    "login": {
        "container": {
            "position": "absolute",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "height": "80%",
            "background_size": "cover",
            "background_position": "center",
            "border_radius": "30px",
            "margin_top": "20px",
            "box_shadow": "0 15px 35px rgba(0, 0, 0, 0.5)",
            "background": "url('/Proyecto_Odontomara/assets/images/background.jpg') no-repeat"
        },
        "form_panel": {
            "height": "100%",
            "border": "5px double transparent",
            "border_radius": "30px",
            "justify_content": "center",
            "align_items": "center",
            "overflow": "hidden",
            "display": "flex",
            "background": f"linear-gradient(rgba({COLORS['secondary']['azul_marino'].replace('#', '')}, 0.8), rgba({COLORS['primary']['turquesa'].replace('#', '')}, 0.6))",
            "backdrop_filter": "blur(20px)",
            "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.3)",
        },
        "input": {
            "border_radius": "15px",
            "padding": "5px",
            "height": "2.5em",
            "border": f"2px solid {COLORS['primary']['turquesa']}",
            "box_shadow": f"0 0 10px {COLORS['primary']['turquesa']}",
            "font_size": "1.3em",
        },
        "button": {
            "width": "80%",
            "height": "60px",
            # "bg": COLORS["primary"]["turquesa"],
            "color": COLORS["neutral"]["blanco"],
            "background": f"linear-gradient(135deg, {COLORS['primary']['turquesa']} 0%, {COLORS['secondary']['azul_medio']} 50%, {COLORS['secondary']['azul_marino']} 100%)",
            "border_radius": "30px",
            "font_weight": "bold",
            "transition": "all 0.2s ease-in-out",
            "margin_top": "25px",
            "_hover": {
                "transform": "translateY(-1px)",
                "box_shadow": f"0px 1px 10px {COLORS["primary"]["dorado"]}",
                # "bg": COLORS["primary"]["dorado"],
                "background": f"linear-gradient(135deg, {COLORS['secondary']['azul_marino']} 0%, {COLORS['secondary']['azul_medio']} 50%, {COLORS['primary']['turquesa']} 100%)",
            },
        },
        
        "background": {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "width": "100%",
            "height": "100%",
            "background": f"linear-gradient(135deg, {COLORS['secondary']['azul_marino']} 0%, {COLORS['secondary']['azul_medio']} 100%)",
            "z_index": "-2",
        }
    },
    
    
    # Estilos para el template
   "template": {
       "box_shadow_style":{ "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"},
        
        "template_content_style": {
              "padding": "1em",
              "margin_bottom": "2em",
              "min_height": "90vh",
         },
        
        "template_page_style": {
            "padding_top": ["1em", "1em", "2em"],
            "padding_x": ["auto", "auto", "2em"],
        }
   }
        
    
    
    
    
}
