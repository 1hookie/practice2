from test_repository import TestRepository
from dependency_graph import DependencyGraph


def demonstrate_reverse_dependencies():
    print("ДЕМОНСТРАЦИЯ ЭТАПА 4 - ОБРАТНЫЕ ЗАВИСИМОСТИ")
    print("=" * 50)
    
    test_repo = TestRepository('test_repo_complex.txt')
    test_repo.load_test_repository()
    
    graph = DependencyGraph(test_repository=test_repo)
    graph.build_dependency_graph_bfs('A', max_depth=4)
    
    print("\n1. Обратные зависимости для B:")
    graph.display_reverse_dependencies('B')
    
    print("\n2. Обратные зависимости для C:")
    graph.display_reverse_dependencies('C')
    
    print("\n3. Обратные зависимости для E:")
    graph.display_reverse_dependencies('E')
    
    print("\n4. Обратные зависимости для I:")
    graph.display_reverse_dependencies('I')

    graph.display_graph_structure()


if __name__ == "__main__":
    demonstrate_reverse_dependencies()