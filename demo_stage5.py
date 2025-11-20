from test_repository import TestRepository
from dependency_graph import DependencyGraph
import sys


def demonstrate_visualization():
    print("ДЕМОНСТРАЦИЯ ЭТАПА 5 - ВИЗУАЛИЗАЦИЯ")
    print("=" * 50)
    
    # Тест 1: Простой граф
    print("\n1. Визуализация простого графа (A):")
    test_repo1 = TestRepository('test_repo_simple.txt')
    test_repo1.load_test_repository()
    graph1 = DependencyGraph(test_repository=test_repo1)
    graph1.build_dependency_graph_bfs('A', max_depth=3)
    
    visualizer1, code1 = graph1.generate_plantuml_visualization('A', "Простой граф зависимостей")
    visualizer1.display_plantuml_code()
    visualizer1.save_to_file('visualization_simple.puml')
    
    # Тест 2: Граф с циклами
    print("\n2. Визуализация графа с циклами (A):")
    test_repo2 = TestRepository('test_repo_cycles.txt')
    test_repo2.load_test_repository()
    graph2 = DependencyGraph(test_repository=test_repo2)
    graph2.build_dependency_graph_bfs('A', max_depth=3)
    
    visualizer2, code2 = graph2.generate_plantuml_visualization('A', "Граф с циклическими зависимостями")
    visualizer2.display_plantuml_code()
    visualizer2.save_to_file('visualization_cycles.puml')
    
    # Тест 3: Сложный граф
    print("\n3. Визуализация сложного графа (A):")
    test_repo3 = TestRepository('test_repo_complex.txt')
    test_repo3.load_test_repository()
    graph3 = DependencyGraph(test_repository=test_repo3)
    graph3.build_dependency_graph_bfs('A', max_depth=3)
    
    visualizer3, code3 = graph3.generate_plantuml_visualization('A', "Сложный граф зависимостей")
    visualizer3.display_plantuml_code()
    visualizer3.save_to_file('visualization_complex.puml')

def main():
    try:
        demonstrate_visualization()
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()