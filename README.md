# MiniTAC Compiler

An Interactive Python-Based Compiler with Code Optimization and Visualization

## Overview

MiniTAC Compiler is a Python-based educational compiler designed to demonstrate the internal working of a compiler through different stages of compilation. It transforms source code into Three-Address Code (TAC), applies multiple optimization techniques, performs control-flow and liveness analysis, eliminates unnecessary instructions, and executes the optimized code.

The project features an interactive **Streamlit dashboard** that provides visual representations of each compiler phase. Users can explore tokens, Abstract Syntax Trees, intermediate code, optimization results, control-flow graphs, and program execution outputs.

The primary goal is to make compiler design concepts easier to understand through practical implementation and interactive visualization.

## Features

- **Lexical Analysis:** Converts source code into tokens by identifying keywords, identifiers, operators, and constants.
- **Syntax Analysis:** Validates program structure and generates an Abstract Syntax Tree (AST).
- **TAC Generation:** Translates the AST into Three-Address Code.
- **Code Optimization:** Implements constant folding, constant propagation, algebraic simplification, copy propagation, and common subexpression elimination.
- **Control Flow Graph:** Divides instructions into basic blocks and represents program execution paths.
- **Liveness Analysis:** Determines which variables are required during program execution.
- **Dead Code Elimination:** Removes unnecessary temporary instructions.
- **Program Execution:** Executes optimized TAC and displays the final output.
- **Code Complexity Analyzer:** Evaluates program structure using metrics such as AST nodes, branches, loops, and cyclomatic complexity.
- **Optimization Analysis:** Displays instruction reduction and optimization savings.
- **Learn Mode:** Provides explanations of individual compiler phases through an interactive learning interface.
- **Interactive Dashboard:** Visualizes the complete compilation pipeline through a user-friendly interface.
- **Error Handling:** Identifies lexical and syntax errors and displays relevant error locations.

## Compiler Architecture

MiniTAC follows a structured compilation pipeline:

```text
             SOURCE CODE
                  |
                  v
          LEXICAL ANALYSIS
                  |
                  v
          SYNTAX ANALYSIS
                  |
                  v
        ABSTRACT SYNTAX TREE
                  |
                  v
       THREE-ADDRESS CODE
                  |
                  v
          CODE OPTIMIZATION
                  |
                  v
        CONTROL FLOW GRAPH
                  |
                  v
          LIVENESS ANALYSIS
                  |
                  v
       DEAD CODE ELIMINATION
                  |
                  v
          FINAL OPTIMIZED TAC
                  |
                  v
          PROGRAM EXECUTION
                  |
                  v
            PROGRAM OUTPUT
```

## Compiler Modules

### 1. Lexical Analysis
The lexer reads the source program and converts it into a sequence of tokens. It identifies keywords, identifiers, numerical values, operators, and symbols.

### 2. Syntax Analysis
The parser checks whether the token sequence follows the language grammar and constructs an Abstract Syntax Tree (AST).

### 3. Three-Address Code Generation
The AST is converted into intermediate instructions called Three-Address Code, where complex expressions are divided into simpler operations.

### 4. Code Optimization
The optimizer improves the generated intermediate code using different optimization techniques to reduce unnecessary computations.

### 5. Control Flow Graph
The CFG represents program execution using basic blocks, successors, and predecessors. It helps analyze conditional statements and loops.

### 6. Liveness Analysis
Liveness analysis identifies variables that may be needed in future instructions. It uses iterative dataflow analysis to calculate USE, DEF, LIVE IN, and LIVE OUT sets.

### 7. Dead Code Elimination
The DCE module uses liveness information to identify and remove unnecessary temporary assignments while preserving required instructions and program output.

### 8. Program Execution
The final optimized TAC is executed using the compiler's execution engine. The output is displayed directly on the dashboard.

## Optimization Techniques

The project implements the following optimization techniques:

| Optimization | Description |
|---|---|
| Constant Folding | Evaluates constant expressions during compilation. |
| Constant Propagation | Replaces variables with known constant values. |
| Algebraic Simplification | Simplifies expressions using algebraic identities. |
| Copy Propagation | Replaces copied variables with their original values. |
| Common Subexpression Elimination | Avoids repeated calculations of identical expressions. |
| Dead Code Elimination | Removes unnecessary temporary computations. |

## Dashboard Modules

The Streamlit dashboard provides different sections for exploring the compilation process.

| Module | Functionality |
|---|---|
| Words | Displays tokens generated by lexical analysis. |
| Structure | Visualizes the Abstract Syntax Tree. |
| Instructions | Displays generated Three-Address Code. |
| Cleanup | Shows optimization techniques and results. |
| Sections | Visualizes the Control Flow Graph. |
| Usage | Displays Liveness Analysis results. |
| Trim | Shows Dead Code Elimination results. |
| Insights | Displays complexity and optimization statistics. |
| Learn Mode | Explains the different compiler phases. |
| Program Output | Displays the result of executing optimized TAC. |

## Technology Stack

**Programming Language**
- Python

**Frontend and Visualization**
- Streamlit
- HTML
- CSS

**Compiler Design Concepts**
- Lexical Analysis
- Syntax Analysis
- Abstract Syntax Tree
- Three-Address Code
- Code Optimization
- Control Flow Graph
- Liveness Analysis
- Dead Code Elimination

**Testing**
- Pytest

## Project Structure

```text
MiniTAC-Compiler/
│
├── app.py
│
├── lexer.py
├── parser.py
├── tac.py
├── optimizer.py
├── cfg.py
├── dataflow.py
├── dce.py
├── compiler.py
│
├── tests/
│   ├── test_lexer_tokens.py
│   ├── test_parser_ast.py
│   ├── test_tac_generation.py
│   ├── test_optimization.py
│   ├── test_control_flow_graph.py
│   ├── test_liveness_analysis.py
│   ├── test_dead_code_elimination.py
│   └── test_compiler_pipeline.py
│
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd MiniTAC-Compiler
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If script execution is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

## How to Run the Project

### Step 1: Activate the Virtual Environment

Open the terminal inside the project directory:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2: Start the Streamlit Application

```bash
streamlit run app.py
```

### Step 3: Open the Dashboard

Open your browser and navigate to:

```text
http://localhost:8501
```

The MiniTAC Compiler dashboard will appear, allowing you to enter source code, compile programs, explore different compiler stages, and view execution results.

## Sample Input Program

Try the following program in the source code editor:

```text
a = 10;
b = 20;
c = a + b;
d = c * 2;

if (d > 50) {
    result = d + 5;
} else {
    result = d - 5;
}

print(result);
```

### Expected Program Output

```text
65
```

This example demonstrates variable assignments, arithmetic expressions, conditional statements, and program output.

## Running Tests

The project includes automated test cases to verify individual compiler modules and the complete compilation pipeline.

Run all tests using:

```bash
pytest -v
```

The test suite covers:

- Lexer token generation
- Parser and AST construction
- TAC generation
- Code optimization
- Control Flow Graph construction
- Liveness Analysis
- Dead Code Elimination
- Complete compiler pipeline

## Project Objective

The objective of MiniTAC Compiler is to provide hands-on experience with compiler design, intermediate code generation, optimization algorithms, and program execution.

By combining compiler implementation with an interactive dashboard, the project demonstrates how source code is analyzed, transformed, optimized, and executed step by step.

## Future Enhancements

- Interactive step-by-step compiler execution.
- Source code to TAC mapping.
- Advanced semantic analysis and type checking.
- Assembly code generation.
- Register allocation.
- Interactive compiler debugging.

## Author

**Abhi Raksha**


LinkedIn: [Abhi Raksha](https://www.linkedin.com/in/abhi-raksha-9b3b80369/)
