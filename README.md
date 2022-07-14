# Tergum

Software für das sichern von Dateien, bzw. diese zu Synchronisieren.


## Projekt Struktur
```
.
|
+-- modules
|   +-- module_dir
|       |-- module.py
|       |-- test.py
|       |-- data.json / settings.json
|       |-- otherfiles...
|   
|-- main.py
|-- load_from_module.py
|-- dev.py
|-- data.json
```

Ein Modul stellt ein "Tab" und die dazu gehörigen Einstellungen dar. Es stellt z.B. das synchronisieren von Verzeichnissen dar.

Modul Code bleibt im `modules/module_dir`. Alle modulrelevanten Einstellungen oder Daten werden in der `data.json` oder `settings.json` gespeichert.

Die Datei `load_from_module.py` beinhaltet die Imports der einzellnen module. Sowie eine Funktion die die QWidget's zurück gibt. 

`dev.py` beinhaltet eine CLI zum testen von bestimmten Szenarien. Erstellt automatisch leere Module etc. . Kann die tests.py der Module ansteuern.
