class TestRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.graph = {}
    
    def load_test_repository(self):
        self.graph = {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                package, dependencies_str = line.split(':', 1)
                package = package.strip()
                dependencies = [dep.strip() for dep in dependencies_str.split(',') if dep.strip()]
                self.graph[package] = dependencies
        return self.graph
    
    def get_dependencies(self, package: str):
        return self.graph.get(package, [])