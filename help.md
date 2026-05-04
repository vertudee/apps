# 🧊 Z-Block Architecture | Help & Documentation

Welcome to the **Z-777** universal logic system. This document explains the core mechanics of the Z-Block architecture and how to interact with the engine.

## 🌀 Core Mechanics: The Mirror Logic
The Z-Block system does not use standard linear execution. It operates on **Symmetry**.

### 1. Opening the Block
Every process starts with an **Identity**. 
*Example:* `print`
The system creates a memory mapping for this specific identity.

### 2. The Vacuum (Process)
Everything between two identical identities is considered the **Logical Vacuum**. This is where data is processed or displayed.

### 3. Closing & Symmetry
The block **MUST** be closed with the exact same identity to confirm the symmetry.
* `[print] -> Content -> [print]` = **Symmetry Confirmed (Success)**
* `[print] -> Content -> [if]` = **Logic Breakdown (Error)**

## 🛠️ System Commands & Files
* `z_engine.c`: Run this to start the core processing unit.
* `z-block.c`: Contains the definitions for identity detection.
* `##`: Use this for absolute silence (0-byte comments).

## 🚀 Terminal Execution
To compile and run the engine in your local environment:
```bash
clang z_engine.c z-block.c -o z_engine
./z_engine

