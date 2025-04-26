# Dolar Scraper

Scraper para obtener cotizaciones de dólares (Oficial, Blue, MEP) desde [dolarito.ar](https://www.dolarito.ar/)

## 🛠️ Estructura del proyecto

├── dollars/
│   ├── __init__.py
│   ├── base.py         # Clase base
│   ├── oficial.py      # Dólar Oficial
│   ├── blue.py         # Dólar Blue
│   └── mep.py          # Dólar MEP
├── scraper.py          # Lógica principal
├── factory.py          # Patrón Factory
├── config/
│   └── logger.py       # Configuración de logs
├── tests/              # Tests unitarios
└── main.py             # Ejemplo de uso

## Instalacion

### Clonar repositorio

```bash

git clone [url-del-repositorio]
cd dolar-scraper
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## 💻 Uso basico

```python

from scraper import DolaritoScraper

scraper = DolaritoScraper()
cotizaciones = scraper.get_rates()

print(f"🔵 Oficial: ${cotizaciones['oficial'].buy} / ${cotizaciones['oficial'].sell}")
print(f"🔵 Blue: ${cotizaciones['blue'].buy} / ${cotizaciones['blue'].sell}")
print(f"🔵 MEP: ${cotizaciones['mep'].sell} (solo venta)")
```

## 📊Ejemplo de salida

🕒 2023-11-20 15:30:00
═══════════════════════════
  💵 COTIZACIONES DÓLAR  
═══════════════════════════
• OFICIAL: Compra $350.00 | Venta $355.00
• BLUE:    Compra $720.00 | Venta $730.00
• MEP:               Venta $680.00
═══════════════════════════

## 🧪 Ejecutar tests

```bash
pytest tests/
```

## 📦 Dependencias

Python 3.8+
beautifulsoup4
requests
pytest (para testing)

## Licencia

Ing. Agustín Palau
