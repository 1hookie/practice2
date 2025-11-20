import argparse
from config import ConfigManager
from maven_parser import MavenParser
from dependency_graph import DependencyGraph
from test_repository import TestRepository
from visualizer import PlantUMLVisualizer

def main():
    parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей - Этап 5')
    parser.add_argument('--config', default='config.csv', help='Конфигурационный файл')
    parser.add_argument('--depth', type=int, default=3, help='Глубина обхода')
    parser.add_argument('--reverse', help='Обратные зависимости для пакета')
    parser.add_argument('--visualize', action='store_true', help='Сгенерировать PlantUML визуализацию')
    parser.add_argument('--output', help='Файл для сохранения PlantUML кода')
    
    args = parser.parse_args()
    config_manager = ConfigManager(args.config)
    
    try:
        config = config_manager.load_config()
        config_manager.display_config()
        
        dependency_graph = None
        test_repo = None
        
        if config['test_repo_mode']:
            print(f"\nРЕЖИМ ТЕСТИРОВАНИЯ")
            test_repo = TestRepository(config['repository_url'])
            test_repo.load_test_repository()
            dependency_graph = DependencyGraph(test_repository=test_repo)
        else:
            print(f"\nРЕЖИМ MAVEN")
            maven_parser = MavenParser(config['repository_url'])
            dependency_graph = DependencyGraph(maven_parser=maven_parser)
        
        print(f"\nПостроение графа:")
        print(f"Пакет: {config['package_name']}")
        print("-" * 40)
        
        graph_data = dependency_graph.build_dependency_graph_bfs(
            root_package=config['package_name'],
            filter_substring=config['filter_substring'],
            max_depth=args.depth
        )
        
        # Визуализация
        if args.visualize:
            visualizer, plantuml_code = dependency_graph.generate_plantuml_visualization(
                config['package_name']
            )
            visualizer.display_plantuml_code()
            
            if args.output:
                visualizer.save_to_file(args.output)
        
        # Обратные зависимости
        elif args.reverse:
            dependency_graph.display_reverse_dependencies(args.reverse)
        
        # Обычный вывод
        else:
            dependency_graph.display_dependency_info(
                root_package=config['package_name'],
                filter_substring=config['filter_substring']
            )
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()