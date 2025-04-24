# Dólar Scraper

Este proyecto realiza web scraping de la página [dolarito.ar](https://www.dolarito.ar/) para obtener las cotizaciones del:

- Dólar Oficial
- Dólar Blue
- Dólar MEP

Obtiene los valores de **compra** y **venta**, y los muestra por consola utilizando `logging`.

---

## 📁 Estructura del Proyecto

```
dolar_scraper/
├── main.py                  # Script principal para ejecutar el scraper
├── scraper.py               # Contiene la clase DolarScraper que hace el scraping
├── utils/
│   └── logger.py            # Configuración de logging
├── tests/
│   └── test_scraper.py      # Tests unitarios usando pytest
├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Archivos a ignorar por Git
└── README.md                # Este archivo
```

---

## 🚀 Cómo ejecutar

1. Cloná el proyecto o descargá el zip.
2. Instalá las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutá el scraper:

```bash
python main.py
```

---

## 🧪 Cómo testear

Usamos `pytest` para correr los tests unitarios.

```bash
pytest
```

---

## 🧠 Detalles técnicos

El scraper busca las cotizaciones dentro de las siguientes secciones del HTML:

- `ul#quotation-oficial-desktop`
- `ul#quotation-informal-desktop`
- `ul#quotation-mep-desktop`

Y extrae los valores dentro de etiquetas con clases específicas:

- `"chakra-text css-1hexnl9"`: contiene los textos "Comprá a:" o "Vendé a:"
- `"chakra-skeleton css-ahyunb"` seguido de un `p`:
  - `"chakra-text css-12u0t8b"` para el valor de **compra**
  - `"chakra-text css-113t1jt"` para el valor de **venta**

---

## 🛠 Dependencias

- `requests`
- `beautifulsoup4`
- `pytest`

---

## ✍️ Autor

Hecho por pedido especial de un usuario de ChatGPT. ¡Gracias por la idea!