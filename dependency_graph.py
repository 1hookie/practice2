from collections import deque
from maven_parser import MavenParser
from test_repository import TestRepository


class DependencyGraph:
    def __init__(self, maven_parser=None, test_repository=None):
        self.maven_parser = maven_parser
        self.test_repository = test_repository
        self.graph = {}
        self.visited = set()
    
    def build_dependency_graph_bfs(self, root_package: str, filter_substring: str = "", max_depth: int = 10):
        self.graph = {}
        self.visited = set()
        
        print(f"BFS построение графа для: {root_package}")
        print(f"Фильтр: '{filter_substring}', Глубина: {max_depth}")
        
        queue = deque([(root_package, 0)])
        self.visited.add(root_package)
        
        while queue:
            current_package, depth = queue.popleft()
            
            if depth >= max_depth:
                continue
            
            if self.test_repository:
                dependencies = self.test_repository.get_dependencies(current_package)
            else:
                dependencies_data = self.maven_parser.get_direct_dependencies(current_package)
                dependencies = [f"{dep['group_id']}:{dep['artifact_id']}:{dep['version']}" for dep in dependencies_data]
            
            filtered_dependencies = []
            for dep in dependencies:
                if filter_substring and filter_substring in dep:
                    continue
                filtered_dependencies.append(dep)
            
            self.graph[current_package] = filtered_dependencies
            
            for dep in filtered_dependencies:
                if dep not in self.visited:
                    self.visited.add(dep)
                    queue.append((dep, depth + 1))
        
        return {
            'graph': self.graph,
            'total_packages': len(self.graph),
            'root_package': root_package
        }
    
    def detect_cycles(self):
        visited = set()
        recursion_stack = set()
        cycles = []
        
        def dfs_cycle_detection(node: str, path: list):
            if node in recursion_stack:
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                if cycle not in cycles:
                    cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            recursion_stack.add(node)
            path.append(node)
            
            if node in self.graph:
                for neighbor in self.graph[node]:
                    dfs_cycle_detection(neighbor, path.copy())
            
            recursion_stack.remove(node)
            path.pop()
        
        for node in self.graph:
            if node not in visited:
                dfs_cycle_detection(node, [])
        
        return cycles
    
    def get_all_dependencies_recursive(self, package: str, visited=None, depth=0):
        if visited is None:
            visited = set()
        
        if package in visited:
            return set()
        
        visited.add(package)
        all_dependencies = set()
        
        if package in self.graph:
            for dep in self.graph[package]:
                all_dependencies.add(dep)
                transitive_deps = self.get_all_dependencies_recursive(dep, visited.copy(), depth + 1)
                all_dependencies.update(transitive_deps)
        
        return all_dependencies
    
    def display_dependency_info(self, root_package: str, filter_substring: str = ""):
        print(f"\nАнализ зависимостей для: {root_package}")
        if filter_substring:
            print(f"Фильтр: '{filter_substring}'")
        print("=" * 50)
        
        direct_deps = self.graph.get(root_package, [])
        print(f"Прямые зависимости ({len(direct_deps)}):")
        for i, dep in enumerate(direct_deps, 1):
            print(f"  {i}. {dep}")
        
        all_deps = self.get_all_dependencies_recursive(root_package)
        print(f"\nВсе зависимости ({len(all_deps)}):")
        for i, dep in enumerate(sorted(all_deps), 1):
            print(f"  {i}. {dep}")
        
        cycles = self.detect_cycles()
        if cycles:
            print(f"\nОбнаружены циклические зависимости ({len(cycles)}):")
            for i, cycle in enumerate(cycles, 1):
                print(f"  Цикл {i}: {' -> '.join(cycle)}")
        else:
            print(f"\nЦиклические зависимости не обнаружены")
        
        print("=" * 50)