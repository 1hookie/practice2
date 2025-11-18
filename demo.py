#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования обработки ошибок
"""

from config import ConfigManager, ConfigError


def test_scenarios():
    """Тестирование различных сценариев конфигурации"""
    
    print("Демонстрация обработки ошибок конфигурации")
    print("=" * 50)
    
    # Тест 1: Корректная конфигурация
    print("\n1. Тест корректной конфигурации:")
    try:
        config_manager = ConfigManager('config.csv')
        config = config_manager.load_config()
        config_manager.display_config()
        print("✅ Конфигурация загружена успешно")
    except ConfigError as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 2: Несуществующий файл
    print("\n2. Тест несуществующего файла:")
    try:
        config_manager = ConfigManager('nonexistent.csv')
        config = config_manager.load_config()
    except ConfigError as e:
        print(f"✅ Обработана ожидаемая ошибка: {e}")
    
    # Тест 3: Неверный формат CSV
    print("\n3. Тест неверного формата CSV:")
    try:
        config_manager = ConfigManager('bad_config.csv')
        config = config_manager.load_config()
    except ConfigError as e:
        print(f"✅ Обработана ожидаемая ошибка: {e}")


if __name__ == "__main__":
    test_scenarios()