
import pulp

# Shared data
facilities = ['F1', 'F2', 'F3']
customers = ['C1', 'C2', 'C3', 'C4', 'C5']

cost = {
    ('F1', 'C1'): 2, ('F1', 'C2'): 4, ('F1', 'C3'): 3, ('F1', 'C4'): 6, ('F1', 'C5'): 9,
    ('F2', 'C1'): 6, ('F2', 'C2'): 2, ('F2', 'C3'): 5, ('F2', 'C4'): 2, ('F2', 'C5'): 4,
    ('F3', 'C1'): 7, ('F3', 'C2'): 5, ('F3', 'C3'): 2, ('F3', 'C4'): 4, ('F3', 'C5'): 3,
}
emissions = {
    ('F1', 'C1'): 20, ('F1', 'C2'): 25, ('F1', 'C3'): 15, ('F1', 'C4'): 30, ('F1', 'C5'): 35,
    ('F2', 'C1'): 40, ('F2', 'C2'): 18, ('F2', 'C3'): 28, ('F2', 'C4'): 16, ('F2', 'C5'): 20,
    ('F3', 'C1'): 50, ('F3', 'C2'): 30, ('F3', 'C3'): 12, ('F3', 'C4'): 22, ('F3', 'C5'): 18,
}
capacity = {'F1': 150, 'F2': 130, 'F3': 140}
demand = {'C1': 80, 'C2': 65, 'C3': 70, 'C4': 55, 'C5': 90}
job_capacity = {'F1': 50, 'F2': 45, 'F3': 40}


def print_solution(model, x, y, jobs):
    print(f"Status: {pulp.LpStatus[model.status]}")
    print(f"Total Cost: {pulp.value(pulp.lpSum(cost[i,j]*x[i,j] for i in facilities for j in customers))}")
    print(f"Total Emissions: {pulp.value(pulp.lpSum(emissions[i,j]*x[i,j] for i in facilities for j in customers))}")
    print(f"Total Jobs Created: {pulp.value(pulp.lpSum(jobs[i] for i in facilities))}")
    print("Facility Plan:")
    for i in facilities:
        print(f"  {i}: Open = {y[i].varValue}, Jobs = {jobs[i].varValue}")
    print("Transport Plan:")
    for i in facilities:
        for j in customers:
            if x[i, j].varValue > 0:
                print(f"  Transport from {i} to {j}: {x[i, j].varValue}")
    print("\n" + "-"*50 + "\n")


def solve_weighted_aggregation(alpha_cost=1, alpha_jobs=1000):
    print("Weighted Aggregation")
    model = pulp.LpProblem("Weighted_Aggregation", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", [(i, j) for i in facilities for j in customers], lowBound=0)
    y = pulp.LpVariable.dicts("y", facilities, cat="Binary")
    jobs = pulp.LpVariable.dicts("jobs", facilities, lowBound=0)

    model += alpha_cost * pulp.lpSum(cost[i,j]*x[i,j] for i in facilities for j in customers) - alpha_jobs * pulp.lpSum(jobs[i] for i in facilities)

    for j in customers:
        model += pulp.lpSum(x[i,j] for i in facilities) == demand[j]

    for i in facilities:
        model += pulp.lpSum(x[i,j] for j in customers) <= capacity[i]*y[i]
        model += jobs[i] <= job_capacity[i]*y[i]

    model.solve()
    print_solution(model, x, y, jobs)


def solve_epsilon_constrained(epsilon=6160):
    print("Epsilon-Constrained Model")
    model = pulp.LpProblem("Epsilon_Constrained", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", [(i, j) for i in facilities for j in customers], lowBound=0)
    y = pulp.LpVariable.dicts("y", facilities, cat="Binary")
    jobs = pulp.LpVariable.dicts("jobs", facilities, lowBound=0)

    model += pulp.lpSum(cost[i,j]*x[i,j] for i in facilities for j in customers)

    for j in customers:
        model += pulp.lpSum(x[i,j] for i in facilities) == demand[j]
    for i in facilities:
        model += pulp.lpSum(x[i,j] for j in customers) <= capacity[i]*y[i]
        model += jobs[i] <= job_capacity[i]*y[i]

    model += pulp.lpSum(emissions[i,j]*x[i,j] for i in facilities for j in customers) <= epsilon

    model.solve()
    print_solution(model, x, y, jobs)


def solve_lexicographic():
    print("Lexicographic Optimization")
    # Phase 1 - Maximize jobs
    model1 = pulp.LpProblem("Lexico_Phase1", pulp.LpMaximize)
    x1 = pulp.LpVariable.dicts("x", [(i, j) for i in facilities for j in customers], lowBound=0)
    y1 = pulp.LpVariable.dicts("y", facilities, cat="Binary")
    jobs1 = pulp.LpVariable.dicts("jobs", facilities, lowBound=0)

    model1 += pulp.lpSum(jobs1[i] for i in facilities)

    for j in customers:
        model1 += pulp.lpSum(x1[i,j] for i in facilities) == demand[j]
    for i in facilities:
        model1 += pulp.lpSum(x1[i,j] for j in customers) <= capacity[i]*y1[i]
        model1 += jobs1[i] <= job_capacity[i]*y1[i]

    model1.solve()

    max_jobs = pulp.value(pulp.lpSum(jobs1[i] for i in facilities))

    # Phase 2 - Minimize cost with fixed jobs
    model2 = pulp.LpProblem("Lexico_Phase2", pulp.LpMinimize)
    x2 = pulp.LpVariable.dicts("x", [(i, j) for i in facilities for j in customers], lowBound=0)
    y2 = pulp.LpVariable.dicts("y", facilities, cat="Binary")
    jobs2 = pulp.LpVariable.dicts("jobs", facilities, lowBound=0)

    model2 += pulp.lpSum(cost[i,j]*x2[i,j] for i in facilities for j in customers)

    for j in customers:
        model2 += pulp.lpSum(x2[i,j] for i in facilities) == demand[j]
    for i in facilities:
        model2 += pulp.lpSum(x2[i,j] for j in customers) <= capacity[i]*y2[i]
        model2 += jobs2[i] <= job_capacity[i]*y2[i]

    model2 += pulp.lpSum(jobs2[i] for i in facilities) >= max_jobs

    model2.solve()
    print_solution(model2, x2, y2, jobs2)


def solve_goal_programming(cost_goal=830, emissions_goal=6160, job_goal=135):
    print("Goal Programming")
    model = pulp.LpProblem("Goal_Programming", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", [(i, j) for i in facilities for j in customers], lowBound=0)
    y = pulp.LpVariable.dicts("y", facilities, cat="Binary")
    jobs = pulp.LpVariable.dicts("jobs", facilities, lowBound=0)
    d_cost = pulp.LpVariable("dev_cost", lowBound=0)
    d_emissions = pulp.LpVariable("dev_emissions", lowBound=0)
    d_jobs = pulp.LpVariable("dev_jobs", lowBound=0)

    model += d_cost + d_emissions + d_jobs

    for j in customers:
        model += pulp.lpSum(x[i,j] for i in facilities) == demand[j]
    for i in facilities:
        model += pulp.lpSum(x[i,j] for j in customers) <= capacity[i]*y[i]
        model += jobs[i] <= job_capacity[i]*y[i]

    model += pulp.lpSum(cost[i,j]*x[i,j] for i in facilities for j in customers) - cost_goal <= d_cost
    model += emissions_goal - pulp.lpSum(emissions[i,j]*x[i,j] for i in facilities for j in customers) <= d_emissions
    model += job_goal - pulp.lpSum(jobs[i] for i in facilities) <= d_jobs

    model.solve()
    print_solution(model, x, y, jobs)


if __name__ == "__main__":
    solve_weighted_aggregation()
    solve_epsilon_constrained()
    solve_lexicographic()
    solve_goal_programming()
