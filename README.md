# Tergum

Software für das sichern von Dateien, bzw. diese zu Synchronisieren.


## Projekt Struktur
```
.
|
+-- modules
|   +-- module_dir
|       |-- module.py
|       |-- data.json / settings.json
|       |-- otherfiles...
|   
|-- main.py
|-- module_dir.py
|-- data.json
```

Ein Modul stellt ein "Tab" und die dazu gehörigen Einstellungen dar. Es stellt z.B. das synchronisieren von Verzeichnissen dar.

Modul Code bleibt im `module_dir`. Alle modulrelevanten Einstellungen oder Daten werden in der `data.json` oder `settings.json` gespeichert.

`module_dir.py` beinhaltet Prozeduren, die helfen, vom Code in den Modulen auf die Dateien in den `module_dir`'s zu zugreifen.
