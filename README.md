# BBM103: Python Programming Projects

A collection of projects developed for the **Introduction to Programming Laboratory I (BBM103)** course. These projects focus on algorithms, recursion, and data manipulation using Python.

## 🛠️ Tech Stack
* **Language:** Python 3.9 
* **IDE:** PyCharm
* **Key Libraries:** `re` (Regex), `collections`, `ast`, `locale`

## 📂 Projects Overview

### 1. Text Analyzer (Assignment 2)
A command-line tool that performs statistical analysis on text files.
* **Features:** Calculates word count, sentence count, letter frequency, and identifies longest/shortest words. Handles punctuation exclusion and English locale formatting.
* **Key Concepts:** Regular Expressions (Regex), String manipulation, File I/O.
* **Usage:** `python text_analyzer.py <input_file> <output_file>`

### 2. Database System (Assignment 3)
An in-memory database simulation supporting SQL-like commands stored in Python dictionaries.
* **Features:** Supports `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `COUNT`, and `JOIN` operations. Uses `ast.literal_eval` to parse dictionary-like conditions from text inputs.
* **Key Concepts:** Dictionary data structures, dynamic query parsing, error handling.
* **Usage:** `python database.py <input_file>`

### 3. Route Finder (Assignment 4)
A recursive pathfinding program that navigates a grid with obstacles ("sinkholes").
* **Features:** Finds the optimal path with the minimum cost using a recursive Depth-First Search (DFS) approach. Calculates movement costs based on neighbor proximity (horizontal/vertical vs. diagonal).
* **Key Concepts:** Recursion, Backtracking algorithm, Matrix traversal.
* **Usage:** `python route_finder.py <input_file> <output_file>`