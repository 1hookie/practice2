#!/usr/bin/env python3
"""
Инструмент визуализации графа зависимостей
Этап 2: Получение данных о зависимостях Maven-пакетов
"""

import sys
import argparse
from config import ConfigFileNotFoundError, ConfigManager, ConfigError
from practice2.maven_parser import MavenParser, MavenError


def main():
    """Основная функция приложения"""
    parser = argparse.ArgumentParser(
        description='Инструмент визуализации графа зависимостей - Этап 2'
    )
    parser.add_argument(
        '--config', 
        default='config.csv',
        help='Путь к конфигурационному файлу (по умолчанию: config.csv)'
    )
    
    args = parser.parse_args()
    
    # Создаем менеджер конфигурации
    config_manager = ConfigManager(args.config)
    
    try:
        # Загружаем конфигурацию
        config = config_manager.load_config()
        
        # Выводим конфигурацию
        config_manager.display_config()
        
        # Создаем парсер Maven
        maven_parser = MavenParser(config['repository_url'])
        
        print(f"\nАнализ пакета: {config['package_name']}")
        print("-" * 40)
        
        # Получаем прямые зависимости
        dependencies = maven_parser.get_direct_dependencies(config['package_name'])
        
        # Выводим зависимости на экран
        maven_parser.display_dependencies(dependencies)
        
    except ConfigFileNotFoundError as e:
        print(f"Ошибка: {e}")
        print("Создайте файл config.csv с необходимыми параметрами.")
        sys.exit(1)
        
    except ConfigParameterError as e:
        print(f"Ошибка конфигурации: {e}")
        sys.exit(1)
        
    except MavenError as e:
        print(f"Ошибка при работе с Maven: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()