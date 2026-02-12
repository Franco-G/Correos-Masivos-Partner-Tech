from tkinter import ttk

class UIStyles:
    # Colores Corporativos
    AZUL_OSCURO = "#0021a4"
    AZUL_MEDIO = "#243a92"
    AZUL_ELECTRICO = "#1e53dd"
    BLANCO = "#ffffff"
    FONDO = "#f4f6f9"
    GRIS_TEXTO = "#333333"

    @staticmethod
    def apply(root):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(".", background=UIStyles.FONDO, font=("Segoe UI", 10))
        style.configure("TFrame", background=UIStyles.FONDO)
        style.configure("TLabelframe", background=UIStyles.FONDO, bordercolor=UIStyles.AZUL_MEDIO)
        style.configure("TLabelframe.Label", background=UIStyles.FONDO, foreground=UIStyles.AZUL_OSCURO, font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", background=UIStyles.FONDO, foreground=UIStyles.GRIS_TEXTO)
        style.configure("Header.TLabel", background=UIStyles.AZUL_OSCURO, foreground=UIStyles.BLANCO, font=("Orbitron", 18, "bold"))
        style.configure("Bold.TLabel", font=("Segoe UI", 10, "bold"), foreground=UIStyles.AZUL_OSCURO)
        
        style.configure("Action.TButton", background=UIStyles.AZUL_ELECTRICO, foreground=UIStyles.BLANCO, font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("Action.TButton", background=[('active', UIStyles.AZUL_MEDIO), ('disabled', '#cccccc')])
        
        return style
