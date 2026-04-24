import os
import subprocess
import time

# Ensure we are working inside the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MiniMake:
    def __init__(self):
        # target -> {'deps': [list of deps], 'cmd': "command string"}
        self.rules = {}

    def add_rule(self, target, deps, cmd):
        self.rules[target] = {
            'deps': deps,
            'cmd': cmd
        }

    def get_mtime(self, path):
        """Get the modification time of a file. Returns 0 if file doesn't exist."""
        if not os.path.exists(path):
            return 0
        return os.path.getmtime(path)

    def build(self, target):
        """
        Build a specific target.
        This is a recursive function that ensures all dependencies are built first.
        """
        print(f"[*] Checking target: {target}")

        # If target isn't in rules, it must be a source file (leaf node)
        if target not in self.rules:
            if os.path.exists(target):
                return
            else:
                raise Exception(f"Error: No rule to make target '{target}' and file not found.")

        rule = self.rules[target]
        
        # 1. Build all dependencies first (Post-order traversal of DAG)
        for dep in rule['deps']:
            self.build(dep)

        # 2. Check if we actually need to build this target
        target_mtime = self.get_mtime(target)
        
        needs_build = False
        if target_mtime == 0:
            print(f"    - Target '{target}' does not exist. Building...")
            needs_build = True
        else:
            for dep in rule['deps']:
                if self.get_mtime(dep) > target_mtime:
                    print(f"    - Dependency '{dep}' is newer than '{target}'. Rebuilding...")
                    needs_build = True
                    break

        # 3. Execute command if needed
        if needs_build:
            print(f"    [EXEC] {rule['cmd']}")
            subprocess.run(rule['cmd'], shell=True, check=True)
        else:
            print(f"    - Target '{target}' is up to date.")

# --- LAB DEMONSTRATION ---
if __name__ == "__main__":
    mm = MiniMake()

    # Define a simple build pipeline:
    # hello.c -> hello.o -> hello.exe
    
    # Let's simulate some files
    with open("hello.c", "w") as f:
        f.write("#include <stdio.h>\nint main() { printf(\"Hello, Mini-Make!\\n\"); return 0; }\n")

    mm.add_rule("hello.o", ["hello.c"], "gcc -c hello.c -o hello.o")
    mm.add_rule("hello.exe", ["hello.o"], "gcc hello.o -o hello.exe")

    print("--- FIRST BUILD ---")
    mm.build("hello.exe")

    print("\n--- SECOND BUILD (Should be up to date) ---")
    mm.build("hello.exe")

    print("\n--- MODIFYING SOURCE ---")
    time.sleep(1.1) # Ensure timestamp changes
    with open("hello.c", "a") as f:
        f.write("// modified\n")
    
    print("\n--- THIRD BUILD (Should rebuild everything) ---")
    mm.build("hello.exe")
