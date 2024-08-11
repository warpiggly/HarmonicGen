import random
from deap import base, creator, tools
from music21 import chord, stream, midi, note
import pygame
import imput_module
import subprocess

# Ejecutar input_module.py en paralelo
subprocess.Popen(['python', 'input_module.py'])


# Define escalas disponibles
scales = {
    'C Major': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'G Major': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    'D Major': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    'A Major': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    'E Major': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    'B Major': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
    'F# Major': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
    'Db Major': ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
    'Ab Major': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
    'Eb Major': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
    'Bb Major': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
    'F Major': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],

    'A Minor': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    'E Minor': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
    'B Minor': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
    'F# Minor': ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'],
    'C# Minor': ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'],
    'G# Minor': ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#'],
    'D# Minor': ['D#', 'E#', 'F#', 'G#', 'A#', 'B', 'C#'],
    'B# Minor': ['B#', 'C#', 'D#', 'E#', 'F#', 'G#', 'A#'],
    'D Minor': ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'],
    'G Minor': ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'],
    'C Minor': ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'],
    'F Minor': ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb']
}

# Selección de la escala
selected_scale =input("Escribe la escala que quiere en notacion inglesa y despues Si es Minor o Major con un espacio:")  # Cambia esta variable para seleccionar la escala

def generate_chord(scale_notes):
    # Genera una triada aleatoria en la escala seleccionada
    root = random.choice(scale_notes)
    third = random.choice([n for n in scale_notes if n != root])
    fifth = random.choice([n for n in scale_notes if n not in [root, third]])
    return chord.Chord([note.Note(root + '4'), note.Note(third + '4'), note.Note(fifth + '4')])

def create_chord_labels(scale_name):
    scale_notes = scales[scale_name]
    # Crea una lista de etiquetas para los acordes
    chord_options = [generate_chord(scale_notes) for _ in range(10)]  # Genera 10 acordes diferentes
    return ['-'.join(n.name for n in c.pitches) for c in chord_options]

# Crea las etiquetas de los acordes según la escala seleccionada
chord_labels = create_chord_labels(selected_scale)

# Configuración del algoritmo genético
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def create_individual():
    return random.sample(chord_labels, 4)  # Genera 4 acordes aleatorios

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función de evaluación personalizada (inicialmente aleatoria)
def evaluate(individual):
    print(f"Evaluando: {' - '.join(individual)}")
    score = int(input("Evalúa esta secuencia del 1 al 5: "))
    
    imput_module.save_to_csv(score)
    
    return (score,)
    


toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

def play_chord_sequence(chord_labels):
    midi_stream = stream.Stream()
    
    for label in chord_labels:
        note_names = label.split('-')
        ch = chord.Chord([note.Note(n) for n in note_names])
        midi_stream.append(ch)
    
    mf = midi.translate.music21ObjectToMidiFile(midi_stream)
    mf.open('output.mid', 'wb')
    mf.write()
    mf.close()

    # Reproduce el archivo MIDI
    pygame.mixer.init()
    pygame.mixer.music.load('output.mid')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # Espera hasta que la reproducción termine
        pygame.time.Clock().tick(10)

# Ejecuta el algoritmo genético
population = toolbox.population(n=5)  # Tamaño de la población
generations = 3  # Número de generaciones

for gen in range(generations):
    for individual in population:
        play_chord_sequence(individual)
        individual.fitness.values = toolbox.evaluate(individual)
    
    population = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, population))
    
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    population[:] = offspring
    
    

