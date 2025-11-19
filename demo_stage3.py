from test_repository import TestRepository
from dependency_graph import DependencyGraph


def demonstrate_test_repository():
    print("ДЕМОНСТРАЦИЯ ЭТАПА 3")
    print("=" * 50)
    
    print("\n1. Простой граф:")
    test_repo = TestRepository('test_repo_simple.txt')
    test_repo.load_test_repository()
    graph = DependencyGraph(test_repository=test_repo)
    graph.build_dependency_graph_bfs('A', max_depth=5)
    graph.display_dependency_info('A')
    
    print("\n2. Граф с циклами:")
    test_repo2 = TestRepository('test_repo_cycles.txt')
    test_repo2.load_test_repository()
    graph2 = DependencyGraph(test_repository=test_repo2)
    graph2.build_dependency_graph_bfs('A', max_depth=5)
    graph2.display_dependency_info('A')
    
    print("\n3. С фильтрацией:")
    graph3 = DependencyGraph(test_repository=test_repo)
    graph3.build_dependency_graph_bfs('A', filter_substring="B", max_depth=5)
    graph3.display_dependency_info('A', "B")


if __name__ == "__main__":
    demonstrate_test_repository()