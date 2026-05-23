import os
import sys
import shutil

def build_package():
    print("[Z-BUILDER]: Starting global architecture setup...")

    root_dir = "zblock-core"
    sub_dir = os.path.join(root_dir, "zblock_core")

    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)
        print("  ├── Cleaned old directory structure.")

    os.makedirs(sub_dir)
    print(f"  ├── Created directory tree: {sub_dir}")

    readme_content = """# Z-Block Core
Advanced geometric syntax interpreter with active ambiguity and background purity checking.
Developed by @vertudee.
"""

    setup_content = """from setuptools import setup

setup(
    name="zblock-core",
    version="2.0.0",
    author="vertudee",
    description="A secure geometric syntax interpreter handling hybrid file-folder contexts.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vertudee/apps",
    packages=["zblock_core"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "z-core=zblock_core.interpreter:list_z_nodes",
        ],
    },
)
"""

    init_content = "from .interpreter import list_z_nodes\n"

    interpreter_content = """import os
import sys

COLOR_Z_NODE = "\\033[38;5;198m"   
COLOR_CONTEXT = "\\033[34m"        
COLOR_DATA = "\\033[32m"           
COLOR_RESET = "\\033[0m"

def secure_background_scan(raw_string):
    if not raw_string:
        return False
    compiled_stream = "".join([f"\\\\{char}" for char in raw_string]) + ","
    if not compiled_stream.endswith(","):
        return False
    body = compiled_stream[:-1]
    i = 0
    while i < len(body):
        if body[i] != "\\\\":
            return False
        i += 2
    return True

def list_z_nodes():
    try:
        items = os.listdir('.')
    except Exception as e:
        print(f"[SYSTEM ERROR]: Unable to read storage layer: {e}")
        return

    print(f"\\n      /--- Rabisco_Z ---\\\\ ")
    print("     |   [ Z-BLOCK ]     |")
    print("      \\\\_________________/")
    print("==================================================")
    print("  Z-CORE INTERPRETER v2.0 - ACTIVE AMBIGUITY")
    print("==================================================")

    detected_any = False

    for item in items:
        if not secure_background_scan(item):
            continue

        if item.endswith('.z'):
            detected_any = True
            print(f"\\n{COLOR_Z_NODE}[ENTERING CONTEXT]: 󰉋 {item} [HYBRID: FOLDER-FILE]{COLOR_RESET}")
            print(f"{COLOR_CONTEXT} ↳ Metadata Detected: [STATE] Active Ambiguity{COLOR_RESET}")
            
            if os.path.isdir(item):
                try:
                    sub_nodes = os.listdir(item)
                    if sub_nodes:
                        print(f"{COLOR_CONTEXT} ┌── [BLOCK: NODE_DIRECTORY_LIST]{COLOR_RESET}")
                        for node in sub_nodes:
                            if secure_background_scan(node):
                                print(f"{COLOR_CONTEXT} │   ├── Node Read: • {COLOR_DATA}{node}{COLOR_RESET} >> [Packed Data]")
                        print(f"{COLOR_CONTEXT} └── [END OF BLOCK]{COLOR_RESET}")
                    else:
                        print(f"{COLOR_CONTEXT} └── [EMPTY GEOMETRIC BLOCK]{COLOR_RESET}")
                except Exception:
                    pass
            print("==================================================")

    if not detected_any:
        print("\\n[!] No geometric Z-blocks found in this active node layer.")
        print("==================================================")

if __name__ == '__main__':
    list_z_nodes()
"""

    with open(os.path.join(root_dir, "README.md"), "w") as f: f.write(readme_content)
    with open(os.path.join(root_dir, "setup.py"), "w") as f: f.write(setup_content)
    with open(os.path.join(root_dir, "LICENSE"), "w") as f: f.write("MIT License")
    with open(os.path.join(sub_dir, "__init__.py"), "w") as f: f.write(init_content)
    with open(os.path.join(sub_dir, "interpreter.py"), "w") as f: f.write(interpreter_content)

    print("[SUCCESS]: Package structural deployment complete with proper naming rules.")

if __name__ == "__main__":
    build_package()

