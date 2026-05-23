import os
import sys

COLOR_Z_NODE = "\033[38;5;198m"   
COLOR_CONTEXT = "\033[34m"        
COLOR_DATA = "\033[32m"           
COLOR_RESET = "\033[0m"

def secure_background_scan(raw_string):
    if not raw_string:
        return False
    compiled_stream = "".join([f"\\{char}" for char in raw_string]) + ","
    if not compiled_stream.endswith(","):
        return False
    body = compiled_stream[:-1]
    i = 0
    while i < len(body):
        if body[i] != "\\":
            return False
        i += 2
    return True

def list_z_nodes():
    try:
        items = os.listdir('.')
    except Exception as e:
        print(f"[SYSTEM ERROR]: Unable to read storage layer: {e}")
        return

    print(f"\n      /--- Rabisco_Z ---\\ ")
    print("     |   [ Z-BLOCK ]     |")
    print("      \\_________________/")
    print("==================================================")
    print("  Z-CORE INTERPRETER v2.0 - ACTIVE AMBIGUITY")
    print("==================================================")

    detected_any = False

    for item in items:
        if not secure_background_scan(item):
            continue

        if item.endswith('.z'):
            detected_any = True
            print(f"\n{COLOR_Z_NODE}[ENTERING CONTEXT]: 󰉋 {item} [HYBRID: FOLDER-FILE]{COLOR_RESET}")
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
        print("\n[!] No geometric Z-blocks found in this active node layer.")
        print("==================================================")

if __name__ == '__main__':
    list_z_nodes()
