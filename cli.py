import sys
import argparse
from config import ConfigManager
from maven_parser import MavenParser
from dependency_graph import DependencyGraph
from test_repository import TestRepository


def main():
    parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей - Этап 3')
    parser.add_argument('--config', default='config.csv', help='Конфигурационный файл')
    parser.add_argument('--depth', type=int, default=3, help='Глубина обхода')
    
    args = parser.parse_args()
    config_manager = ConfigManager(args.config)
    
    try:
        config = config_manager.load_config()
        config_manager.display_config()
        
        dependency_graph = None
        test_repo = None
        
        if config['test_repo_mode']:
            print(f"\nРЕЖИМ ТЕСТИРОВАНИЯ")
            print(f"Файл: {config['repository_url']}")
            test_repo = TestRepository(config['repository_url'])
            test_repo.load_test_repository()
            dependency_graph = DependencyGraph(test_repository=test_repo)
        else:
            print(f"\nРЕЖИМ MAVEN")
            print(f"Репозиторий: {config['repository_url']}")
            maven_parser = MavenParser(config['repository_url'])
            dependency_graph = DependencyGraph(maven_parser=maven_parser)
        
        print(f"\nПостроение графа:")
        print(f"Пакет: {config['package_name']}")
        print(f"Фильтр: '{config['filter_substring']}'")
        print("-" * 40)
        
        graph_data = dependency_graph.build_dependency_graph_bfs(
            root_package=config['package_name'],
            filter_substring=config['filter_substring'],
            max_depth=args.depth
        )
        
        dependency_graph.display_dependency_info(
            root_package=config['package_name'],
            filter_substring=config['filter_substring']
        )
        
        print(f"\nСтатистика:")
        print(f"  Пакетов: {graph_data['total_packages']}")
        print(f"  Режим: {'Тестовый' if config['test_repo_mode'] else 'Maven'}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()