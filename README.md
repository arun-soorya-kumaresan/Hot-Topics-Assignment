# Multi-Objective Optimization for Sustainable Supply Chain Design

This repository contains the Python implementation of four multi-objective optimization models for designing a sustainable supply chain network. The models are applied to a hypothetical case with three facilities and five customers, considering trade-offs between **economic cost**, **environmental emissions**, and **social impact (job creation)**.

## 📌 Objectives

The goal is to support data-driven decision-making in supply chain design by balancing:

- 💰 Economic Efficiency (Cost Minimization)
- 🌱 Environmental Sustainability (Emission Reduction)
- 🧑‍🤝‍🧑 Social Responsibility (Job Creation)

## 📊 Optimization Methods Implemented

1. **Weighted Aggregation**  
   All objectives are combined into a single function using weighted coefficients.

2. **ε-Constrained Optimization**  
   Cost is minimized while keeping emissions and social impact within user-defined bounds.

3. **Lexicographic Optimization**  
   Objectives are prioritized in a strict hierarchy (e.g., Social > Cost > Emissions).

4. **Goal Programming**  
   The model minimizes deviations from target values set for each objective.

## 🧮 Tools Used

- Python 3  
- PuLP (Linear Programming Solver)  
- CBC MILP Solver (default backend)

## 🗂 File Structure

- `multi_objective_optimization_supply_chain.py` – Core implementation of all four models
- No external dataset is used; all parameters are hardcoded for demonstration

## 🧠 Insights

Each method demonstrates a unique strategy for balancing conflicting sustainability goals. The code is structured to help compare outcomes across methods and understand their implications in real-world ESG-driven supply chain planning.

## 📎 Report Link

The detailed assignment report discusses the model design, mathematical formulations, outputs, and recommendations. A PDF version of the report is attached in the submission.

## 📬 Contact

For any questions or collaboration ideas, feel free to reach out via GitHub or email.
