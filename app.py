import random
from deap import base, creator, tools
from music21 import chord, stream, midi, note 
import pygame
import imput_module
import subprocess
import librosa 
import numpy as np 
# Ejecutar input_module.py en paralelo , para ejecutatr los otros archivos de la aplicacion.



def main_menu():
    
    while True:
        
        print ("Este es el menu principal , elige una opcion")
        print ("1 - Analizar una cancion:")
        print ("2 - codigo genetico")
        print ("3 - Salir")
        
        
        choice= input("Ingresa un numero aqui:")
        
        if  choice == "1":
            print ("Este es el punto para entender la tonalidad ")
            #Librosa puede cargar la canción y convertirla en un array de frecuencias que podemos analizar.
            def load_audio(file_phat):
                y, sr = librosa.load(file_phat)
                return y, sr
            #La transformada de Fourier nos permitirá analizar las frecuencias presentes en la canción.
            def get_fourier_transform(y,sr):
                chroma_stft=librosa.feature.chroma_stft(y=y, sr=sr)
                return np.mean(chroma_stft , axis=1)
            def  estimate_key(chromagram):
                major_profile = np.array([
                    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],  # C major
                    [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # C# major
                    [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],  #"D major":   D E F# G A B C#
                    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],  #"D# major":  D# F G G# A# C D
                    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],  #"E major":   E F# G# A B C# D#
                    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],  #"F major":   F G A A# C D E
                    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # "F# major":  F# G# A# B C# D# F
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],  # "G major":   G A B C D E F#
                    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  #"G# major": G# A# C C# D# F G
                    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  #"A major":   A B C# D E F# G#
                    [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],  #"A# major":  A# C D D# F G A
                    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],  # "B major":   B C# D# E F# G# A#
                ])

                minor_profile = np.array([
                    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],  #     "C minor":  C D D# F G G# A#
                    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],  #     "C# minor": C# D# E F# G# A B
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],  #     "D minor":  D E F G A A# C
                    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],  #     "D# minor": D# F F# G# A# B C#
                    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],  #     "E minor":  E F# G A B C D
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],  #    "F minor":   F G G# A# C C# D#
                    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],  #    "F# minor":  F# G# A B C# D E
                    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],  #    "G minor":   G A A# C D D# F
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],  #     "G# minor": G# A# B C# D# E F#
                    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],  #    "A minor":   A B C D E F G
                    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],  #     "A# minor": A# C C# D# F F# G#
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],  #    "B minor":     B C# D E F# G A
                ])
            
                        # Similaridad con perfiles mayores y menores
                major_similarity = np.dot(chromagram, major_profile)
                minor_similarity = np.dot(chromagram, minor_profile)

                if np.max(major_similarity) > np.max(minor_similarity):
                    key_index = np.argmax(major_similarity)
                    return f"{['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][key_index]} Major"
                else:
                    key_index = np.argmax(minor_similarity)
                    return f"{['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][key_index]} Minor"
                
            def find_song_key(file_path):
                y, sr = load_audio(file_path)
                chromagram = get_fourier_transform(y, sr)
                song_key = estimate_key(chromagram)
                return song_key

            # Ejemplo de uso:
            # Solicitar al usuario que ingrese la ruta del archivo
            file_path = input("Por favor, ingresa la ruta completa del archivo de audio(incluyendo la extensión, como .wav o .mp3): ")

            # Encontrar y mostrar la tonalidad de la canción
            key = find_song_key(file_path)
            if key:
                print(f"La tonalidad de la canción es: {key}")
            else:
                print("No se pudo determinar la tonalidad de la canción.")
            
        
        elif choice == "2":
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
                
        elif choice == "3":
            print ("Saliendo de el proyecto") 
            break
            
        else:
            print ("Este numero no existe")       
            
if __name__ == "__main__":
    main_menu()
    
    

