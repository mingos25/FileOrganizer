import argparse
import os
import fnmatch
import shutil
from os import path
import csv
import numpy as np


# metodo che crea la sotto-cartella se non esiste e sposta il file nella sotto-cartella
def move_file_create_folder(a_file, name_folder, type_name):
    file_size = os.path.getsize('files/' + a_file)
    if not os.path.exists('files/' + name_folder):
        os.mkdir('files/' + name_folder)
    shutil.move('files/' + a_file, 'files/' + name_folder + '/' + a_file)
    # stampa in console i dettagli del file
    print(os.path.splitext(a_file)[0] + ' type:' + type_name + ' size:' + str(file_size) + 'B')
    print("file spostato!")
    data = np.array([os.path.splitext(a_file)[0], type_name, str(file_size)])
    # inserisce i dati del file nel csv
    with open("files/recap.csv", "a") as csv_modify:
        writer = csv.writer(csv_modify)
        writer.writerow(data)
        csv_modify.close()


def main():
    # creo la CLI con argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--Output", help="Show Output")
    arg = parser.parse_args()

    # se l'utente ha inserito il nome del file
    if arg.Output:
        file = arg.Output
        # controlla se esiste il csv recap
        if not path.isfile('files/recap.csv'):
            # se non esiste, viene creato e viene inserito la prima riga: l'header
            data_header = ["name", "type", "size(B)"]
            with open("files/recap.csv", "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(data_header)
                csv_file.close()

        # controlla se è un file o una cartella, se è un file entra nel blocco if
        if path.isfile('files/' + file):
            # if innestati per poter spostare il file nella giusta sotto-cartella in base al suo tipo
            if fnmatch.fnmatch(arg.Output, '*.mp3'):
                move_file_create_folder(arg.Output, 'audio', 'audio')
            if fnmatch.fnmatch(arg.Output, '*.txt') or fnmatch.fnmatch(arg.Output, '*.odt'):
                move_file_create_folder(arg.Output, 'docs', 'doc')
            if fnmatch.fnmatch(arg.Output, '*.png') or fnmatch.fnmatch(arg.Output, '*.jpeg') or fnmatch.fnmatch(
                    arg.Output,
                    '*.jpg'):
                move_file_create_folder(arg.Output, 'images', 'image')
        else:
            # se il file non esiste avviserà l'utente
            print("Il file non esiste")

    # per avviare la cli scrivi python3 addfile.py -o nome file


if __name__ == "__main__":
    main()
