# XML2TXT

Transformation vers un texte brut structuré de fichiers XML générés par ABBY FineReader (http://fr7.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml) contenant les transcriptions des volumes des *Ouvriers des Deux Mondes*.

## Installation
Le script nécessite l'installation des libraries python 3.* suivantes (de préférence dans un environnement virtuel) :
- `bs4`
- `beautifulsoup4=>4.6.3`
- `lxml=>4.2.5`
- `termcolor=>1.1.0`
- `StringDist=>1.0.9`

## Utilisation
Le script transforme un seul fichier XML à la fois.

### Exemple 1:
```
~$ python3 main.py -i abbyy-file.xml
```

> un fichier *abbyy-file\_out.xml* et un fichier *abby-file\_guard.xml* seront créés dans le même répertoire que le fichier d'entrée.

### Exemple 2:
```
~$ python3 main.py -i abby-file.xml -o filename
```

> un fichier *filename\_out.xml* et un fichier *filename\_guard.xml* seront créés à l'emplacement indiqué, par rapport à xml2txt.py.

