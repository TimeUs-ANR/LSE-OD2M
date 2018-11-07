# XML2TXT

Transformation vers un texte brut structuré de fichiers XML générés par ABBY FineReader (http://fr7.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml) contenant les transcriptions des volumes des *Ouvriers des Deux Mondes*.

## Installation
Le script nécessite l'installation des libraries python 3.* suivantes (de préférence dans un environnement virtuel) :
- `bs4`
- `lxml=>4.2.5`

## Utilisation
Le script transforme un fichier XML à la fois.

### Exemple 1:
```
~$ python3 -i abbyy-file.xml
```

>> un fichier abbyy-file.txt sera créé dans le même répertoire que le fichier d'entrée.

### Exemple 2:
```
~$ python3 -i abby-file.xml -o filename
```

>> un fichier filename.txt sera créé à l'emplacement indiqué, par rapport à xml2txt.py.

