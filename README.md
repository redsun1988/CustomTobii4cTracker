# CustomTobii4cTracker README

## English

### Overview

**CustomTobii4cTracker** is an unofficial Python package that provides a simple API for tracking gaze position on the screen using the Tobii 4C eye tracker. With this package, you can easily subscribe to gaze center updates and integrate gaze-based interactions into your applications.

### Features

- **Easy-to-use API** for accessing gaze data from Tobii 4C
- **Event-driven**: Subscribe to real-time gaze center updates
- **Direct access** to the current gaze center coordinates at any time

### Installation

```bash
pip install CustomTobii4cTracker
```

### Usage Example

```python
from CustomTobii4cTracker import Tobii4cTracker
from typing import Tuple

def on_center_change(center: Tuple[float, float]):
    print(f"\rCenter changed to: {center}", end="")

main = Tobii4cTracker(target_color=(0, 191, 255))
main.on_center_updated.subscribe(on_center_change)
await main.start_monitoring()

# Get the current gaze center at any moment
current_center = main.find_center()
print(f"Current gaze center: {current_center}")
```

### API Reference

#### Tobii4cTracker

- **Parameters:**
  - `target_color` (tuple): RGB color for target highlight (e.g., `(0, 191, 255)`)

- **Events:**
  - `on_center_updated`: Subscribe to receive gaze center position as `(x, y)` coordinates (floats, in screen pixels or relative units)

- **Methods:**
  - `start_monitoring()`: Start tracking gaze position (asynchronous)
  - `find_center() -> Tuple[float, float]`: Returns the current gaze center coordinates as a tuple `(x, y)` in **absolute monitor coordinates**

### Requirements

- Python 3.10+
- Tobii 4C eye tracker
- Tobii software/drivers installed

### Disclaimer

This package is **unofficial** and not affiliated with Tobii. Use at your own risk.

## Русский

### Описание

**CustomTobii4cTracker** — неофициальный Python-пакет, предоставляющий простой API для отслеживания положения взгляда на экране с помощью трекера Tobii 4C. С помощью этого пакета вы можете легко подписаться на события обновления центра взгляда и интегрировать взаимодействие на основе взгляда в свои приложения.

### Возможности

- **Простой API** для получения данных о взгляде с Tobii 4C
- **Событийная модель**: подписка на обновления центра взгляда в реальном времени
- **Прямой доступ** к текущим координатам центра взгляда в любой момент

### Установка

```bash
pip install CustomTobii4cTracker
```

### Пример использования

```python
from CustomTobii4cTracker import Tobii4cTracker
from typing import Tuple

def on_center_change(center: Tuple[float, float]):
    print(f"\rCenter changed to: {center}", end="")

main = Tobii4cTracker(target_color=(0, 191, 255))
main.on_center_updated.subscribe(on_center_change)
await main.start_monitoring()

# Получить текущие координаты центра взгляда в любой момент
current_center = main.find_center()
print(f"Current gaze center: {current_center}")
```

### Описание API

#### Tobii4cTracker

- **Параметры:**
  - `target_color` (кортеж): RGB-цвет для выделения цели (например, `(0, 191, 255)`)

- **События:**
  - `on_center_updated`: подписка на получение координат центра взгляда `(x, y)` (float, в пикселях экрана или относительных единицах)

- **Методы:**
  - `start_monitoring()`: запуск отслеживания положения взгляда (асинхронно)
  - `find_center() -> Tuple[float, float]`: возвращает текущие координаты центра взгляда в виде кортежа `(x, y)` в **абсолютных координатах монитора**

### Требования

- Python 3.10+
- Трекер Tobii 4C
- Установленное ПО/драйверы Tobii

### Дисклеймер

Этот пакет **неофициальный** и не связан с компанией Tobii. Используйте на свой страх и риск.

Happy coding! / Удачной разработки!