import svglib
from reportlab.graphics import renderPM
import os

def create_svg_content():
    # SVG код схемы с 5 вертикальными блоками
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="700" xmlns="http://www.w3.org/2000/svg">
  <!-- Фон -->
  <rect width="100%" height="100%" fill="#f4f6f9"/>
  
  <!-- Заголовок -->
  <text x="300" y="40" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle" fill="#2c3e50">
    Ключевые принципы системы госзакупок
  </text>

  <!-- Блок 1: Соблюдение правовых норм -->
  <g transform="translate(100, 70)">
    <rect x="0" y="0" width="400" height="80" rx="8" ry="8" fill="#ffffff" stroke="#3498db" stroke-width="2" filter="drop-shadow(2px 2px 2px rgba(0,0,0,0.1))"/>
    <circle cx="40" cy="40" r="25" fill="#ebf5fb" stroke="#3498db" stroke-width="2"/>
    <!-- Иконка весов/закона -->
    <path d="M30,35 L50,35 M40,35 L40,25 M40,45 L30,55 M40,45 L50,55" stroke="#2980b9" stroke-width="2" fill="none"/>
    
    <text x="80" y="35" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#2c3e50">Соблюдение</text>
    <text x="80" y="55" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#2c3e50">правовых норм</text>
  </g>

  <!-- Блок 2: Конкурентность -->
  <g transform="translate(100, 170)">
    <rect x="0" y="0" width="400" height="80" rx="8" ry="8" fill="#ffffff" stroke="#2ecc71" stroke-width="2" filter="drop-shadow(2px 2px 2px rgba(0,0,0,0.1))"/>
    <circle cx="40" cy="40" r="25" fill="#eafaf1" stroke="#2ecc71" stroke-width="2"/>
    <!-- Иконка конкуренции (медали) -->
    <circle cx="30" cy="35" r="8" fill="none" stroke="#27ae60" stroke-width="2"/>
    <circle cx="50" cy="35" r="8" fill="none" stroke="#27ae60" stroke-width="2"/>
    <circle cx="40" cy="45" r="8" fill="none" stroke="#27ae60" stroke-width="2"/>
    
    <text x="80" y="45" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#2c3e50">Конкурентность</text>
  </g>

  <!-- Блок 3: Открытость -->
  <g transform="translate(100, 270)">
    <rect x="0" y="0" width="400" height="80" rx="8" ry="8" fill="#ffffff" stroke="#f39c12" stroke-width="2" filter="drop-shadow(2px 2px 2px rgba(0,0,0,0.1))"/>
    <circle cx="40" cy="40" r="25" fill="#fef5e7" stroke="#f39c12" stroke-width="2"/>
    <!-- Иконка открытости (дверь/свет) -->
    <path d="M35,25 L45,25 L45,55 L35,55 Z" fill="none" stroke="#d35400" stroke-width="2"/>
    <line x1="45" y1="40" x2="55" y2="40" stroke="#d35400" stroke-width="2"/>
    
    <text x="80" y="45" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#2c3e50">Открытость</text>
  </g>

  <!-- Блок 4: Прозрачность -->
  <g transform="translate(100, 370)">
    <rect x="0" y="0" width="400" height="80" rx="8" ry="8" fill="#ffffff" stroke="#9b59b6" stroke-width="2" filter="drop-shadow(2px 2px 2px rgba(0,0,0,0.1))"/>
    <circle cx="40" cy="40" r="25" fill="#f5eef8" stroke="#9b59b6" stroke-width="2"/>
    <!-- Иконка прозрачности (глаз/лупа) -->
    <circle cx="40" cy="35" r="10" fill="none" stroke="#8e44ad" stroke-width="2"/>
    <line x1="47" y1="42" x2="55" y2="50" stroke="#8e44ad" stroke-width="2"/>
    
    <text x="80" y="45" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#2c3e50">Прозрачность</text>
  </g>

  <!-- Блок 5: Контролируемость -->
  <g transform="translate(100, 470)">
    <rect x="0" y="0" width="400" height="80" rx="8" ry="8" fill="#ffffff" stroke="#e74c3c" stroke-width="2" filter="drop-shadow(2px 2px 2px rgba(0,0,0,0.1))"/>
    <circle cx="40" cy="40" r="25" fill="#fdedec" stroke="#e74c3c" stroke-width="2"/>
    <!-- Иконка контроля (галочка/щит) -->
    <path d="M30,40 L38,50 L50,30" fill="none" stroke="#c0392b" stroke-width="3"/>
    
    <text x="80" y="45" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#2c3e50">Контролируемость</text>
  </g>

  <!-- Связующая линия слева -->
  <line x1="80" y1="110" x2="80" y2="510" stroke="#bdc3c7" stroke-width="2" stroke-dasharray="5,5"/>
  
  <!-- Подпись снизу -->
  <text x="300" y="580" font-family="Arial, sans-serif" font-size="14" fill="#7f8c8d" text-anchor="middle">
    Фундаментальные основы контрактной системы РФ
  </text>
</svg>
"""
    return svg_content

def main():
    svg_filename = "temp_principles.svg"
    png_filename = "principles_scheme.png"
    
    print(f"Генерация файла {svg_filename}...")
    with open(svg_filename, "w", encoding="utf-8") as f:
        f.write(create_svg_content())
    print("SVG файл создан.")

    print(f"Конвертация {svg_filename} в {png_filename}...")
    try:
        drawing = svglib.svg2rlg(svg_filename)
        renderPM.drawToFile(drawing, png_filename, fmt="PNG", dpi=300)
        
        print(f"Успешно! Файл сохранен как {png_filename}")
        print(f"Полный путь: {os.path.abspath(png_filename)}")
        
        # Удаляем временный SVG
        os.remove(svg_filename)
        
    except Exception as e:
        print(f"Произошла ошибка при конвертации: {e}")
        print("Совет: Убедитесь, что установлены последние версии библиотек:")
        print("pip install --upgrade svglib reportlab")
        print("\nАльтернатива: Откройте созданный SVG файл в браузере и сделайте скриншот.")

if __name__ == "__main__":
    main()