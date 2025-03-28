import numpy as np
import random

class GeneticScheduler:
    def __init__(self, num_classes, num_teachers, num_rooms, num_timeslots, population_size=100, generations=500):
        self.num_classes = num_classes
        self.num_teachers = num_teachers
        self.num_rooms = num_rooms
        self.num_timeslots = num_timeslots
        self.population_size = population_size
        self.generations = generations

    def initialize_population(self):
        return [np.random.randint(0, self.num_timeslots, (self.num_classes,)) for _ in range(self.population_size)]

    def fitness(self, schedule):
        # Evaluasi fitness berdasarkan konflik (misal: bentrok jadwal guru atau ruangan)
        conflicts = 0
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if schedule[i] == schedule[j]:
                    conflicts += 1
        return 1 / (1 + conflicts)

    def crossover(self, parent1, parent2):
        point = random.randint(0, len(parent1) - 1)
        child = np.concatenate((parent1[:point], parent2[point:]))
        return child

    def mutate(self, schedule):
        if random.random() < 0.1:  # 10% chance mutation
            idx = random.randint(0, len(schedule) - 1)
            schedule[idx] = random.randint(0, self.num_timeslots - 1)
        return schedule

    def evolve(self):
        population = self.initialize_population()
        for _ in range(self.generations):
            sorted_population = sorted(population, key=lambda x: self.fitness(x), reverse=True)
            new_population = sorted_population[:10]  # Elitism: Keep best 10

            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(sorted_population[:50], 2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        best_schedule = sorted(population, key=lambda x: self.fitness(x), reverse=True)[0]
        return best_schedule
