import ast
import inspect
import subprocess
import sys
from typing import List, Dict, Any

class CodeEvolutionEngine:
    def __init__(self):
        self.function_library = {}
        self.test_cases = {}
        self.performance_metrics = {}
        self.code_generation_attempts = 0
        
    def evolve_function(self, function_name: str, requirements: str) -> str:
        """Evolve a function to meet requirements"""
        self.code_generation_attempts += 1
        
        if function_name in self.function_library:
            current_code = self.function_library[function_name]
            mutated_code = self.mutate_code(current_code, requirements)
        else:
            mutated_code = self.generate_initial_code(function_name, requirements)
        
        # Test the new code
        if self.test_function(mutated_code, function_name):
            self.function_library[function_name] = mutated_code
            print(f"✓ Evolution successful for {function_name}")
            return mutated_code
        else:
            # Try again with different mutation
            return self.evolve_function(function_name, requirements)
    
    def generate_initial_code(self, function_name: str, requirements: str) -> str:
        """Generate initial code based on requirements"""
        if "sort" in requirements.lower():
            return f"""
def {function_name}(items):
    \"\"\"Sort a list of items\"\"\"
    return sorted(items)
"""
        elif "search" in requirements.lower():
            return f"""
def {function_name}(items, target):
    \"\"\"Search for target in items\"\"\"
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1
"""
        else:
            # Generic function template
            return f"""
def {function_name}(*args, **kwargs):
    \"\"\"{requirements}\"\"\"
    # TODO: Implement functionality
    return args[0] if args else None
"""
    
    def mutate_code(self, code: str, requirements: str) -> str:
        """Mutate existing code to improve it"""
        tree = ast.parse(code)
        
        # Simple mutations: add conditions, change operations, add error handling
        mutations = [
            self.add_condition_check,
            self.add_error_handling,
            self.optimize_loop,
            self.add_logging
        ]
        
        mutation = random.choice(mutations)
        try:
            mutated_tree = mutation(tree)
            return ast.unparse(mutated_tree)
        except:
            return code  # Return original if mutation fails
    
    def add_error_handling(self, tree):
        """Add try-except blocks to function"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Wrap function body in try-except
                try_body = node.body
                except_body = [
                    ast.Pass()  # Simple recovery
                ]
                
                node.body = [
                    ast.Try(
                        body=try_body,
                        handlers=[
                            ast.ExceptHandler(
                                type=ast.Name(id="Exception", ctx=ast.Load()),
                                name=None,
                                body=except_body
                            )
                        ],
                        orelse=[],
                        finalbody=[]
                    )
                ]
        return tree
    
    def test_function(self, code: str, function_name: str) -> bool:
        """Test if the function works correctly"""
        try:
            # Execute the code in a safe environment
            local_env = {}
            exec(code, {}, local_env)
            
            func = local_env[function_name]
            
            # Run basic tests
            if "sort" in function_name.lower():
                result = func([3, 1, 2])
                return result == [1, 2, 3]
            elif "search" in function_name.lower():
                result = func([1, 2, 3], 2)
                return result == 1
            else:
                # Generic test - just see if it runs without error
                func()
                return True
                
        except Exception as e:
            print(f"Test failed: {e}")
            return False

# Example of evolving a sorting function
if __name__ == "__main__":
    engine = CodeEvolutionEngine()
    
    print("=== Evolving a Sort Function ===")
    sort_code = engine.evolve_function(
        "smart_sort", 
        "Sort lists efficiently with error handling"
    )
    print(f"Evolved code:\n{sort_code}")
    
    print(f"\n=== Evolution Stats ===")
    print(f"Attempts: {engine.code_generation_attempts}")
    print(f"Functions in library: {len(engine.function_library)}")
