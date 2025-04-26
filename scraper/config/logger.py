import logging
import sys
from pathlib import Path

def setup_logger(name: str = 'dolar_scraper', log_file: str = 'scraper.log') -> logging.Logger:
    """
    Configura un logger con salida a consola y archivo
    
    Args:
        name: Nombre del logger
        log_file: Ruta del archivo de logs
        
    Returns:
        Logger configurado
    """
    # Crear directorio de logs si no existe
    log_path = Path('logs')
    log_path.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Formato común
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Handler para archivo
    file_handler = logging.FileHandler(log_path / log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger