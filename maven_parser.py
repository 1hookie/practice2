import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import re


class MavenError(Exception):
    """Базовое исключение для ошибок Maven"""
    pass


class MavenRepositoryError(MavenError):
    """Ошибка доступа к репозиторию Maven"""
    pass


class MavenPackageError(MavenError):
    """Ошибка поиска пакета"""
    pass


class MavenParser:
    """Парсер для извлечения зависимостей из Maven-пакетов"""
    
    # Основные Maven-репозитории
    MAVEN_CENTRAL = "https://repo1.maven.org/maven2"
    MAVEN_GOOGLE = "https://maven.google.com"
    
    def __init__(self, repository_url: str = None):
        self.repository_url = repository_url or self.MAVEN_CENTRAL
        self.dependencies_cache = {}
    
    def extract_dependencies_from_pom(self, pom_content: str):
        """Извлекает зависимости из POM-файла"""
        try:
            namespaces = {'ns': 'http://maven.apache.org/POM/4.0.0'}
            root = ET.fromstring(pom_content)
            
            dependencies = []
            
            for dep in root.findall('.//ns:dependencies/ns:dependency', namespaces):
                group_id_elem = dep.find('ns:groupId', namespaces)
                artifact_id_elem = dep.find('ns:artifactId', namespaces)
                version_elem = dep.find('ns:version', namespaces)
                
                if group_id_elem is not None and artifact_id_elem is not None:
                    version = version_elem.text if version_elem is not None else 'LATEST'
                    
                    # Пропускаем зависимости без версии (кроме BOM)
                    if version == 'UNKNOWN':
                        continue
                        
                    dependency = {
                        'group_id': group_id_elem.text,
                        'artifact_id': artifact_id_elem.text,
                        'version': version,
                        'scope': 'compile'
                    }
                    dependencies.append(dependency)
            
            return dependencies
            
        except ET.ParseError as e:
            raise MavenError(f"Ошибка парсинга POM: {e}")

    def parse_maven_identifier(self, package_name: str) -> Dict[str, str]:
        """
        Парсит идентификатор Maven-пакета в формате groupId:artifactId:version
        
        Args:
            package_name: Имя пакета в формате "groupId:artifactId:version"
            
        Returns:
            Dict с компонентами пакета
            
        Raises:
            MavenPackageError: Если формат неверный
        """
        parts = package_name.split(':')
        if len(parts) != 3:
            raise MavenPackageError(
                f"Неверный формат пакета: {package_name}. "
                f"Ожидается: groupId:artifactId:version"
            )
        
        return {
            'group_id': parts[0],
            'artifact_id': parts[1],
            'version': parts[2]
        }
    
    def build_pom_url(self, group_id: str, artifact_id: str, version: str) -> str:
        """
        Строит URL для POM-файла в Maven-репозитории
        
        Args:
            group_id: Group ID пакета
            artifact_id: Artifact ID пакета  
            version: Версия пакета
            
        Returns:
            URL POM-файла
        """
        group_path = group_id.replace('.', '/')
        return f"{self.repository_url}/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    
    def build_metadata_url(self, group_id: str, artifact_id: str) -> str:
        """
        Строит URL для metadata-файла в Maven-репозитории
        
        Args:
            group_id: Group ID пакета
            artifact_id: Artifact ID пакета
            
        Returns:
            URL metadata-файла
        """
        group_path = group_id.replace('.', '/')
        return f"{self.repository_url}/{group_path}/{artifact_id}/maven-metadata.xml"
    
    def fetch_xml_content(self, url: str) -> str:
        """
        Загружает XML-контент по URL
        
        Args:
            url: URL для загрузки
            
        Returns:
            XML-контент как строка
            
        Raises:
            MavenRepositoryError: Если не удалось загрузить
        """
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return response.read().decode('utf-8')
                else:
                    raise MavenRepositoryError(
                        f"Не удалось загрузить {url}. Статус: {response.status}"
                    )
        except urllib.error.URLError as e:
            raise MavenRepositoryError(f"Ошибка сети при загрузке {url}: {e}")
        except Exception as e:
            raise MavenRepositoryError(f"Неожиданная ошибка при загрузке {url}: {e}")
    
    def extract_dependencies_from_pom(self, pom_content: str) -> List[Dict[str, str]]:
        """
        Извлекает зависимости из POM-файла
        
        Args:
            pom_content: Содержимое POM-файла
            
        Returns:
            Список зависимостей
        """
        try:
            # Регистрируем namespace для правильного парсинга
            namespaces = {
                'ns': 'http://maven.apache.org/POM/4.0.0'
            }
            
            root = ET.fromstring(pom_content)
            
            dependencies = []
            
            # Ищем секцию dependencies
            for dep in root.findall('.//ns:dependencies/ns:dependency', namespaces):
                group_id_elem = dep.find('ns:groupId', namespaces)
                artifact_id_elem = dep.find('ns:artifactId', namespaces)
                version_elem = dep.find('ns:version', namespaces)
                scope_elem = dep.find('ns:scope', namespaces)
                
                if group_id_elem is not None and artifact_id_elem is not None:
                    dependency = {
                        'group_id': group_id_elem.text,
                        'artifact_id': artifact_id_elem.text,
                        'version': version_elem.text if version_elem is not None else 'UNKNOWN',
                        'scope': scope_elem.text if scope_elem is not None else 'compile'
                    }
                    dependencies.append(dependency)
            
            return dependencies
            
        except ET.ParseError as e:
            raise MavenError(f"Ошибка парсинга POM: {e}")
    
    def get_direct_dependencies(self, package_name: str) -> List[Dict[str, str]]:
        """
        Получает прямые зависимости пакета
        
        Args:
            package_name: Имя пакета в формате "groupId:artifactId:version"
            
        Returns:
            Список прямых зависимостей
            
        Raises:
            MavenError: Если не удалось получить зависимости
        """
        if package_name in self.dependencies_cache:
            return self.dependencies_cache[package_name]
        
        try:
            # Парсим идентификатор пакета
            package_info = self.parse_maven_identifier(package_name)
            group_id = package_info['group_id']
            artifact_id = package_info['artifact_id']
            version = package_info['version']
            
            print(f"Поиск зависимостей для: {group_id}:{artifact_id}:{version}")
            
            # Строим URL для POM-файла
            pom_url = self.build_pom_url(group_id, artifact_id, version)
            print(f"POM URL: {pom_url}")
            
            # Загружаем и парсим POM
            pom_content = self.fetch_xml_content(pom_url)
            dependencies = self.extract_dependencies_from_pom(pom_content)
            
            # Кэшируем результат
            self.dependencies_cache[package_name] = dependencies
            
            return dependencies
            
        except MavenError:
            raise
        except Exception as e:
            raise MavenError(f"Неожиданная ошибка при получении зависимостей: {e}")
    
    def display_dependencies(self, dependencies: List[Dict[str, str]]) -> None:
        """
        Выводит зависимости в читаемом формате
        
        Args:
            dependencies: Список зависимостей
        """
        if not dependencies:
            print("Прямые зависимости не найдены")
            return
        
        print("\nПрямые зависимости:")
        print("=" * 60)
        for i, dep in enumerate(dependencies, 1):
            print(f"{i}. {dep['group_id']}:{dep['artifact_id']}:{dep['version']} "
                  f"[scope: {dep['scope']}]")
        print("=" * 60)
        print(f"Всего найдено зависимостей: {len(dependencies)}")