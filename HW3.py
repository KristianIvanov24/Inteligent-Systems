import random

def create_population(size, num_items):
    population = []
    for _ in range(size):
        individual = [random.randint(0, 1) for _ in range(num_items)]
        population.append(individual)
    return population

def calculate_value_weight(individual, items):
    total_value = 0
    total_weight = 0
    for i, selected in enumerate(individual):
        if selected == 1:
            total_value += items[i][1]
            total_weight += items[i][0]
    return total_value, total_weight

def fitness(individual, items, max_weight):
    total_value, total_weight = calculate_value_weight(individual, items)
    if total_weight > max_weight:
        return 0
    return total_value

def selection(population, fitnesses):
    selected = []
    for _ in range(len(population)):
        idx1, idx2 = random.sample(range(len(population)), 2)
        selected.append(population[idx1] if fitnesses[idx1] > fitnesses[idx2] else population[idx2])
    return selected

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

def genetic_algorithm(max_weight, items, population_size, generations):
    num_items = len(items)
    population = create_population(population_size, num_items)
    best_overall_value = 0

    for generation in range(generations):
        fitnesses = [fitness(individual, items, max_weight) for individual in population]
        best_individual = max(population, key=lambda x: fitness(x, items, max_weight))
        best_value, _ = calculate_value_weight(best_individual, items)

        print(f"Generation {generation + 1}: Best value = {best_value}")

        best_overall_value = max(best_overall_value, best_value)

        selected = selection(population, fitnesses)
        children = []
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                child1 = crossover(selected[i], selected[i + 1])
                child2 = crossover(selected[i + 1], selected[i])
                children.extend([mutation(child1, 0.1), mutation(child2, 0.1)])

        population = children

    return best_overall_value

# Input
max_weight, num_items = map(int, input().split())
items = [tuple(map(int, input().split())) for _ in range(num_items)]

# Output
result = genetic_algorithm(max_weight, items, population_size=20, generations=10)
print("Best value:", result)
