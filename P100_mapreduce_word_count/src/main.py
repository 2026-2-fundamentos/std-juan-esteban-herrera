import glob
import os.path
import shutil
import string
import time

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data")
INPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "temp", "input")
OUTPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "temp", "output")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER, "submission")

# La carpeta input/ debe existir y estar vacia.
# -----------------------------------------------------------------------------

if os.path.exists(INPUT_FOLDER):
    for file in glob.glob(f"{INPUT_FOLDER}/*"):
        os.remove(file)
else:
    os.makedirs(INPUT_FOLDER)



# Genera copias de los archivos en raw/
# -----------------------------------------------------------------------------

n = 1000

for file in glob.glob(f"{DATA_FOLDER}/*"):

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    for i in range(1, n + 1):

        raw_filename_with_extension = os.path.basename(file)

        raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

        new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

        with open(f"{INPUT_FOLDER}/{new_filename}", "w", encoding="utf-8") as f2:
            f2.write(text)


# Lectura de los archivos
# -----------------------------------------------------------------------------

start_time = time.time()

sequence = []
files = glob.glob(f"{INPUT_FOLDER}/*")
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            sequence.append((file, line))


# Mapper
# -----------------------------------------------------------------------------

pairs_sequence = []
for _, line in sequence:
    line = line.lower()
    line = line.translate(str.maketrans("", "", string.punctuation))
    line = line.replace("\n", "")
    words = line.split()
    pairs_sequence.extend([(word, 1) for word in words])



# Shuffle and sort
# -----------------------------------------------------------------------------

pairs_sequence = sorted(pairs_sequence)


# Reducer
# -----------------------------------------------------------------------------

result = []
for key, value in pairs_sequence:
    if result and result[-1][0] == key:
        result[-1] = (key, result[-1][1] + value)
    else:
        result.append((key, value))




# La carpeta de salida debe estar vacia
# -----------------------------------------------------------------------------

if os.path.exists(OUTPUT_FOLDER):
    for file in glob.glob(f"{OUTPUT_FOLDER}/*"):
        os.remove(file)
else:
    os.makedirs(OUTPUT_FOLDER)


# Archivo con el conteo
# -----------------------------------------------------------------------------

with open(f"{OUTPUT_FOLDER}/part-00000", "w", encoding="utf-8") as f:
    for key, value in result:
        f.write(f"{key}\t{value}\n")



# Marcador de éxito
# -----------------------------------------------------------------------------

with open(f"{OUTPUT_FOLDER}/_SUCCESS", "w", encoding="utf-8") as f:
    f.write("")



# Copia el resultado desde HDFS simulado al disco local
# -----------------------------------------------------------------------------

if os.path.exists(SUBMISSION_FOLDER):
    for file in glob.glob(f"{SUBMISSION_FOLDER}/*"):
        os.remove(file)
else:
    os.makedirs(SUBMISSION_FOLDER)

for file in glob.glob(f"{OUTPUT_FOLDER}/*"):
    shutil.copy2(file, SUBMISSION_FOLDER)



# Reporte de tiempo de ejecución
# -----------------------------------------------------------------------------

end_time = time.time()
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")