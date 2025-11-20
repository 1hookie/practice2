class PlantUMLVisualizer:
    def __init__(self):
        self.plantuml_code = ""
    
    def generate_plantuml(self, graph: dict, root_package: str, title: str = "Граф зависимостей"):
        """Генерирует PlantUML код для графа зависимостей"""
        
        self.plantuml_code = f"""@startuml
title {title}
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle

' Стили для пакетов
skinparam node {{
    backgroundColor White
    borderColor Black
    fontSize 12
}}

' Корневой пакет
node "{root_package}" as root #LightBlue

"""
        
        # Добавляем все пакеты
        all_packages = set()
        for package, dependencies in graph.items():
            all_packages.add(package)
            all_packages.update(dependencies)
        
        for package in sorted(all_packages):
            if package != root_package:
                self.plantuml_code += f'node "{package}" as {self._sanitize_id(package)}\n'
        
        self.plantuml_code += "\n"
        
        # Добавляем зависимости
        for package, dependencies in graph.items():
            for dep in dependencies:
                if package == root_package:
                    self.plantuml_code += f'root --> {self._sanitize_id(dep)}\n'
                else:
                    self.plantuml_code += f'{self._sanitize_id(package)} --> {self._sanitize_id(dep)}\n'
        
        self.plantuml_code += "@enduml"
        return self.plantuml_code
    
    def _sanitize_id(self, package_name: str) -> str:
        """Создает валидный идентификатор для PlantUML"""
        return package_name.replace(':', '_').replace('.', '_').replace('-', '_')
    
    def save_to_file(self, filename: str):
        """Сохраняет PlantUML код в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.plantuml_code)
        print(f"PlantUML код сохранен в: {filename}")
    
    def display_plantuml_code(self):
        """Выводит PlantUML код на экран"""
        print("\n" + "="*60)
        print("PLANTUML КОД:")
        print("="*60)
        print(self.plantuml_code)
        print("="*60)