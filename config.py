import csv
import os
from typing import Dict, Any


class ConfigError(Exception):
    """Базовое исключение для ошибок конфигурации"""
    pass


class ConfigFileNotFoundError(ConfigError):
    """Ошибка: файл конфигурации не найден"""
    pass


class ConfigParameterError(ConfigError):
    """Ошибка: неверный параметр конфигурации"""
    pass


class ConfigManager:
    """Менеджер конфигурации приложения"""
    
    # Обязательные параметры конфигурации
    REQUIRED_PARAMETERS = {
        'package_name': str,
        'repository_url': str,
        'test_repo_mode': bool,
        'filter_substring': str
    }
    
    def __init__(self, config_file: str = 'config.csv'):
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
    
    def load_config(self) -> Dict[str, Any]:
        """
        Загружает конфигурацию из CSV-файла
        
        Returns:
            Dict[str, Any]: Словарь с параметрами конфигурации
            
        Raises:
            ConfigFileNotFoundError: Если файл конфигурации не найден
            ConfigParameterError: Если параметры конфигурации неверны
        """
        if not os.path.exists(self.config_file):
            raise ConfigFileNotFoundError(
                f"Конфигурационный файл '{self.config_file}' не найден"
            )
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                config_data = {}
                
                for row in reader:
                    parameter = row['parameter'].strip()
                    value = row['value'].strip()
                    config_data[parameter] = value
                
                self._validate_config(config_data)
                self.config = self._parse_config_values(config_data)
                return self.config
                
        except csv.Error as e:
            raise ConfigError(f"Ошибка чтения CSV файла: {e}")
        except KeyError as e:
            raise ConfigError(f"Неверный формат CSV файла: отсутствует ключ {e}")
        except Exception as e:
            raise ConfigError(f"Неожиданная ошибка при загрузке конфигурации: {e}")
    
    def _validate_config(self, config_data: Dict[str, str]) -> None:
        """
        Проверяет корректность загруженной конфигурации
        
        Args:
            config_data: Словарь с параметрами конфигурации
            
        Raises:
            ConfigParameterError: Если параметры конфигурации неверны
        """
        # Проверка наличия всех обязательных параметров
        missing_params = set(self.REQUIRED_PARAMETERS.keys()) - set(config_data.keys())
        if missing_params:
            raise ConfigParameterError(
                f"Отсутствуют обязательные параметры: {', '.join(missing_params)}"
            )
        
        # Проверка на лишние параметры
        extra_params = set(config_data.keys()) - set(self.REQUIRED_PARAMETERS.keys())
        if extra_params:
            print(f"Предупреждение: обнаружены неизвестные параметры: {', '.join(extra_params)}")
    
    def _parse_config_values(self, config_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Преобразует строковые значения конфигурации в соответствующие типы
        
        Args:
            config_data: Словарь с параметрами конфигурации в строковом формате
            
        Returns:
            Dict[str, Any]: Словарь с преобразованными значениями
            
        Raises:
            ConfigParameterError: Если преобразование типа невозможно
        """
        parsed_config = {}
        
        for param, value in config_data.items():
            if param in self.REQUIRED_PARAMETERS:
                expected_type = self.REQUIRED_PARAMETERS[param]
                
                try:
                    if expected_type == bool:
                        # Преобразование строки в булево значение
                        if value.lower() in ('true', '1', 'yes', 'y'):
                            parsed_config[param] = True
                        elif value.lower() in ('false', '0', 'no', 'n'):
                            parsed_config[param] = False
                        else:
                            raise ValueError(f"Недопустимое булево значение: {value}")
                    else:
                        # Преобразование в другие типы
                        parsed_config[param] = expected_type(value)
                        
                except (ValueError, TypeError) as e:
                    raise ConfigParameterError(
                        f"Неверное значение параметра '{param}': {value}. Ожидается тип {expected_type.__name__}"
                    )
        
        return parsed_config
    
    def display_config(self) -> None:
        """Выводит текущую конфигурацию в формате ключ-значение"""
        if not self.config:
            print("Конфигурация не загружена")
            return
        
        print("Текущая конфигурация:")
        print("-" * 40)
        for key, value in self.config.items():
            print(f"{key}: {value} ({type(value).__name__})")
        print("-" * 40)