import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize

# 1. Parámetros Matemáticos de Saturación (Techo, Velocidad de saturación)
# TV satura lento pero tiene un techo alto. Social satura rápido.
canales = {'TV': {'alpha': 500, 'lambda': 0.02, 'color': '#2C3E50'},
           'Radio': {'alpha': 200, 'lambda': 0.05, 'color': '#E74C3C'},
           'Social Media': {'alpha': 600, 'lambda': 0.08, 'color': '#3498DB'}}

# Función de ventas (Curva exponencial de rendimientos decrecientes)
def ventas_canal(inversion, alpha, lam):
    return alpha * (1 - np.exp(-lam * inversion))

# Función objetivo a minimizar (Scipy minimiza, así que invertimos el signo para maximizar)
def objetivo_ventas(presupuestos):
    tv, radio, social = presupuestos
    v_tv = ventas_canal(tv, canales['TV']['alpha'], canales['TV']['lambda'])
    v_radio = ventas_canal(radio, canales['Radio']['alpha'], canales['Radio']['lambda'])
    v_social = ventas_canal(social, canales['Social Media']['alpha'], canales['Social Media']['lambda'])
    return -(v_tv + v_radio + v_social)

# 2. Motor de Optimización Matemática
presupuesto_total = 100 # $100k
restricciones = ({'type': 'eq', 'fun': lambda x: np.sum(x) - presupuesto_total})
limites = ((0, presupuesto_total), (0, presupuesto_total), (0, presupuesto_total))
presupuesto_inicial = [33.3, 33.3, 33.3] # Punto de partida

resultado = minimize(objetivo_ventas, presupuesto_inicial, method='SLSQP', bounds=limites, constraints=restricciones)
optimo_tv, optimo_radio, optimo_social = resultado.x
ventas_maximas = -resultado.fun

# 3. Diseño Visual "Agency-Grade"
sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: Curvas de Saturación (El "Por qué")
x_vals = np.linspace(0, 100, 200)
for nombre, params in canales.items():
    y_vals = ventas_canal(x_vals, params['alpha'], params['lambda'])
    ax1.plot(x_vals, y_vals, label=nombre, color=params['color'], linewidth=3)
    
ax1.axvline(x=optimo_tv, color=canales['TV']['color'], linestyle='--', alpha=0.5)
ax1.axvline(x=optimo_radio, color=canales['Radio']['color'], linestyle='--', alpha=0.5)
ax1.axvline(x=optimo_social, color=canales['Social Media']['color'], linestyle='--', alpha=0.5)

ax1.set_title('Análisis de Saturación (Rendimientos Decrecientes)', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Inversión ($k)', fontsize=12)
ax1.set_ylabel('Ventas Generadas ($k)', fontsize=12)
ax1.legend(title="Canales")

# Panel 2: Distribución Óptima (El "Qué hacer")
nombres = ['TV', 'Radio', 'Social Media']
valores = [optimo_tv, optimo_radio, optimo_social]
colores = [canales['TV']['color'], canales['Radio']['color'], canales['Social Media']['color']]

barras = ax2.bar(nombres, valores, color=colores, edgecolor='none', alpha=0.9, width=0.6)
ax2.set_title(f'Distribución Óptima de Presupuesto\nROAS Proyectado: ${(ventas_maximas/presupuesto_total):.2f}x', fontsize=14, fontweight='bold', pad=15)
ax2.set_ylabel('Inversión Asignada ($k)', fontsize=12)

# Añadir etiquetas de datos en las barras
for barra in barras:
    yval = barra.get_height()
    ax2.text(barra.get_x() + barra.get_width()/2, yval + 1, f'${yval:.1f}k', ha='center', va='bottom', fontweight='bold', fontsize=11)

sns.despine(left=True)
plt.tight_layout()

# Exportar para GitHub
plt.savefig('Marketing_Mix_Optimization_Pro.png', dpi=300, bbox_inches='tight')
print("¡Panel de optimización avanzado generado con éxito!")