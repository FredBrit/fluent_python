import os
import svglib
from reportlab.graphics import renderPM

# --- ИСПРАВЛЕНИЕ ИМПОРТА ДЛЯ НОВЫХ ВЕРСИЙ SVGLIB ---
svg2rlg = None

# Попытка найти функцию разными способами
try:
    # Способ 1: Прямой импорт из подмодуля (часто работает в 1.5+)
    from svglib import svg_lib
    svg2rlg = svg_lib.svg2rlg
except ImportError:
    try:
        # Способ 2: Старый способ (для старых версий)
        from svglib.svg_lib import svg2rlg
    except ImportError:
        pass

# Если не нашли ни одним способом, пробуем взять из корневого модуля (редко, но бывает)
if svg2rlg is None and hasattr(svglib, 'svg2rlg'):
    svg2rlg = svglib.svg2rlg

if svg2rlg is None:
    print("ОШИБКА: Не удалось найти функцию svg2rlg в установленной версии svglib.")
    print("Мы все равно создадим SVG файл, который вы сможете открыть в браузере.")
    print("Для конвертации в PNG попробуйте откатить версию: pip install svglib==1.5.1")

# --- СОДЕРЖИМОЕ SVG ---
svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f4f6f9"/>
  
  <!-- Заголовок -->
  <text x="450" y="50" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="#2c3e50">
    Ключевые направления развития системы госзакупок
  </text>

  <!-- Блок 1: Актуализация НПА -->
  <g transform="translate(50, 100)">
    <rect x="0" y="0" width="250" height="300" rx="10" ry="10" fill="#ffffff" stroke="#3498db" stroke-width="2" filter="drop-shadow(3px 3px 2px rgba(0,0,0,0.2))"/>
    <circle cx="125" cy="60" r="40" fill="#ebf5fb" stroke="#3498db" stroke-width="2"/>
    <!-- Иконка документа -->
    <path d="M105,45 L145,45 L145,75 L105,75 Z" fill="none" stroke="#2980b9" stroke-width="3"/>
    <line x1="110" y1="55" x2="140" y2="55" stroke="#2980b9" stroke-width="2"/>
    <line x1="110" y1="65" x2="140" y2="65" stroke="#2980b9" stroke-width="2"/>
    
    <text x="125" y="130" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#2c3e50">Актуализация</text>
    <text x="125" y="155" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#2c3e50">НПА</text>
    
    <text x="125" y="190" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">Обновление нормативной</text>
    <text x="125" y="210" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">базы в соответствии с</text>
    <text x="125" y="230" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">текущими требованиями</text>
    <text x="125" y="250" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">и лучшими практиками</text>
  </g>

  <!-- Блок 2: Цифровая инфраструктура -->
  <g transform="translate(325, 100)">
    <rect x="0" y="0" width="250" height="300" rx="10" ry="10" fill="#ffffff" stroke="#2ecc71" stroke-width="2" filter="drop-shadow(3px 3px 2px rgba(0,0,0,0.2))"/>
    <circle cx="125" cy="60" r="40" fill="#eafaf1" stroke="#2ecc71" stroke-width="2"/>
    <!-- Иконка сети -->
    <circle cx="125" cy="60" r="15" fill="none" stroke="#27ae60" stroke-width="3"/>
    <line x1="125" y1="45" x2="125" y2="30" stroke="#27ae60" stroke-width="2"/>
    <line x1="125" y1="75" x2="125" y2="90" stroke="#27ae60" stroke-width="2"/>
    <line x1="110" y1="60" x2="95" y2="60" stroke="#27ae60" stroke-width="2"/>
    <line x1="140" y1="60" x2="155" y2="60" stroke="#27ae60" stroke-width="2"/>

    <text x="125" y="130" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#2c3e50">Зрелая цифровая</text>
    <text x="125" y="155" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#2c3e50">инфраструктура</text>
    
    <text x="125" y="190" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">Единая платформа,</text>
    <text x="125" y="210" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">открытые API и защита</text>
    <text x="125" y="230" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">данных, интеграция</text>
    <text x="125" y="250" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">сервисов</text>
  </g>

  <!-- Блок 3: Квалификация -->
  <g transform="translate(600, 100)">
    <rect x="0" y="0" width="250" height="300" rx="10" ry="10" fill="#ffffff" stroke="#f39c12" stroke-width="2" filter="drop-shadow(3px 3px 2px rgba(0,0,0,0.2))"/>
    <circle cx="125" cy="60" r="40" fill="#fef5e7" stroke="#f39c12" stroke-width="2"/>
    <!-- Иконка человека/роста -->
    <circle cx="125" cy="50" r="12" fill="#d35400"/>
    <path d="M110,85 Q125,65 140,85" fill="none" stroke="#d35400" stroke-width="3"/>
    <path d="M125,85 L125,100 M110,100 L140,100" stroke="#d35400" stroke-width="2"/>

    <text x="125" y="130" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#2c3e50">Систематическое</text>
    <text x="125" y="155" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#2c3e50">повышение</text>
    <text x="125" y="175" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#2c3e50">квалификации</text>
    
    <text x="125" y="210" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">Обучение сотрудников,</text>
    <text x="125" y="230" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">центры компетенций,</text>
    <text x="125" y="250" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#555">партнерство с вузами</text>
  </g>

  <!-- Связующая линия снизу -->
  <path d="M175,420 L725,420 L725,440 L175,440 Z" fill="#34495e"/>
  <text x="450" y="435" font-family="Arial, sans-serif" font-size="16" fill="white" text-anchor="middle" font-weight="bold">ЕДИНАЯ СТРАТЕГИЯ РАЗВИТИЯ</text>
</svg>
"""

def main():
    svg_filename = "temp_scheme.svg"
    png_filename = "procurement_scheme.png"
    
    # 1. СОХРАНЯЕМ SVG ФАЙЛ (Это произойдет гарантированно)
    print(f"Сохранение SVG файла: {svg_filename}...")
    try:
        with open(svg_filename, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"УСПЕХ: SVG файл создан по пути: {os.path.abspath(svg_filename)}")
        print("Вы можете открыть этот файл в любом браузере (Chrome, Edge).")
    except Exception as e:
        print(f"Критическая ошибка при сохранении SVG: {e}")
        return

    # 2. ПЫТАЕМСЯ КОНВЕРТИРОВАТЬ В PNG
    if svg2rlg is None:
        print("\n[ПРЕДУПРЕЖДЕНИЕ] Конвертация в PNG пропущена из-за проблемы с библиотекой svglib.")
        print("Используйте созданный SVG файл или сделайте скриншот из браузера.")
        return

    print(f"\nПопытка конвертации в PNG: {png_filename}...")
    try:
        drawing = svg2rlg(svg_filename)
        renderPM.drawToFile(drawing, png_filename, fmt="PNG", dpi=300)
        print(f"УСПЕХ: PNG файл создан по пути: {os.path.abspath(png_filename)}")
    except Exception as e:
        print(f"Ошибка при конвертации в PNG: {e}")
        print("Но SVG файл уже сохранен! Откройте temp_scheme.svg в браузере.")

if __name__ == "__main__":
    main()