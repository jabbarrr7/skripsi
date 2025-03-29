<<<<<<< HEAD
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
=======
import numpy as np
import random

class GeneticScheduler:
    def __init__(self, tasks, teachers, subjects, rooms, timeslots):
        self.tasks = tasks
        self.teachers = teachers
        self.subjects = subjects
        self.rooms = rooms
        self.timeslots = timeslots
        self.population_size = 50
        self.mutation_rate = 0.1
        self.generations = 100

        # Dosen dengan keahlian yang sesuai untuk mata kuliah tertentu
        self.teacher_skills = {teacher: random.sample(subjects, k=random.randint(1, len(subjects))) for teacher in teachers}

    def create_chromosome(self):
        """Membuat satu individu (jadwal acak)"""
        return [
            (
                task, 
                random.choice(self.teachers),
                random.choice(self.subjects),
                random.choice(self.rooms),
                random.choice(self.timeslots)
            ) 
            for task in self.tasks
        ]

    def fitness(self, chromosome):
        """Menghitung skor fitness berdasarkan seberapa baik jadwal"""
        score = 0

        # 1. Tidak ada dosen yang bentrok mengajar di dua tempat sekaligus
        teacher_schedule = {}
        for task, teacher, subject, room, timeslot in chromosome:
            if (teacher, timeslot) in teacher_schedule:
                score -= 10  # Penalti jika bentrok
            else:
                teacher_schedule[(teacher, timeslot)] = True

        # 2. Tidak ada ruangan yang dipakai bersamaan
        room_schedule = {}
        for task, teacher, subject, room, timeslot in chromosome:
            if (room, timeslot) in room_schedule:
                score -= 10  # Penalti jika ruangan bentrok
            else:
                room_schedule[(room, timeslot)] = True

        # 3. Bonus jika tugas sesuai kompetensi dosen
        for task, teacher, subject, room, timeslot in chromosome:
            if subject in self.teacher_skills[teacher]:
                score += 5  # Reward jika sesuai keahlian

        return score

    def select_parents(self, population, fitness_scores):
        """Seleksi orang tua dengan metode roulette wheel"""
        total_fitness = sum(fitness_scores)
        probabilities = [f / total_fitness for f in fitness_scores]
        selected = np.random.choice(population, size=2, p=probabilities)
        return selected[0], selected[1]

    def crossover(self, parent1, parent2):
        """Two-Point Crossover"""
        point1, point2 = sorted(np.random.randint(0, len(parent1), 2))
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        return child1, child2

    def mutate(self, chromosome):
        """Mutasi dengan mengganti ruangan atau waktu"""
        for i in range(len(chromosome)):
            if np.random.rand() < self.mutation_rate:
                task, teacher, subject, room, timeslot = chromosome[i]
                new_room = random.choice(self.rooms)
                new_timeslot = random.choice(self.timeslots)
                chromosome[i] = (task, teacher, subject, new_room, new_timeslot)
        return chromosome

    def evolve(self):
        """Menjalankan algoritma genetika"""
        population = [self.create_chromosome() for _ in range(self.population_size)]
        
        for _ in range(self.generations):
            fitness_scores = [self.fitness(chrom) for chrom in population]
            new_population = []

            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))

            population = new_population

        # Ambil solusi terbaik
        best_chromosome = max(population, key=self.fitness)
        return best_chromosome
>>>>>>> 5fbeba9 (Inisialisasi proyek optimasi penjadwalan)
