# Cross Save Game Manager

## CrossSaveGameManager

S'encarrega de sinconitzar les partides guardades entre el `local_game` i el `remote_game`.

Atributs de la classe:

- local_game: instancia de un `SaveGameManager`
- remote_game: instancia de un `RemoteSaveGameManager`
- last_sync_date: data de la última vegada que es va sincronitzar el `local_game`

Métodes:

- CrossSaveGameManager(local_path, remote_path, host, user, password, last_sync_date=None):
  - Crea la instancia de `local_game`.
  - Crea la instancia de `remote_game`.
  - Calcula el valor de `last_sync_date` si no ens el passen.  # TODO: com ho fem? algun fitxer a la carpeta on deixar-ho guardat??
- sync():
  - Si el `last_sync_date`, `local_game`, o `remote_game` estan a `None` falla.
  - Crida el `remote_game.get_new_saves()`
  - Crida el `local_game.get_new_saves()`
  - Podem tindre 3 situacions:
    - Versio remota és la més recent:
      - TODO
    - Versio local es la més recent:
      - TODO
    - Les dos versions tenen fitxers nous (conflicte)
      - TODO

notes:

Lo seu seria que sempre s'agafin TOTS els fitxers remots i es posin al local (si el local no es mes recent). Llavors al tancar el joc es pujen els fixers i s'actuaitza la data. Amb aixo no fara falta ni data, pero amb la data detectarem conflictes.

## SaveGameManager

S'encarrega de gestionar la pujada o descarrega de fitxers de partides guardades situades al `path`

Atributs de la classe:

- path: ruta absoluta a la carpeta on hi ha les partides guardades
- saves: llista de instancies de `SaveGame` creades a partir dels fitxers situats al `path`
- backups_path: ruta absoluta a la carpeta on es guardaran els backups dels fitxers que es s'actualitzen.

Métodes:

- SaveGameManager(path, backups_path=None):

  - Guarda el valor de `path`. Revisa que el directori existeixi. Si no exiteix falla.
  - Guarda el valor de `backups_path`. Si no s'ha passat valor el calcula  el calcula amb el `path` + `.backups`. Revisa que el directori existeixi. Si no existeix el crea.
  - Crida el metode `update_saves_list`.
- update_saves_list():

  - Actualitza la llista de `saves`.
  - Les instancies que hi havia es perden i s'en creen de noves en base als fitxers que hi hagi en aquest moment al `path`.
- add_save(SaveGame):

  - Crea un fitxer  al `path` amb el `content` del `SaveGame` que es passa per parametre.
  - Si ja existia un fitxer amb el mateix `filename` es fa un backup del fitxer antic (metode `backup` del `SaveGame` passant el `backups_path` com a parametre) i es crea un fitxer nou.
- get_new_saves(date):

  - Retorna una llista de instancies de `SaveGame` amb els registres de `saves` que el seu `last_write_date` es igual o posterior a la data passada per parametre.

## RemoteSaveGameManager(SaveGameManager)

S'encarrega de gestionar la pujada o descarrega de fitxers de partides guardades situades al `path` de un servidor
remot (`host`) al qual ens hi podem conectar per scp i ssh amb el `user` i `password` proporcionats.

Atributs de la classe:

- host
- user
- password

Métodes:

- RemoteSaveGameManager(host, user, password, path, backups_path=None):
  - Intenta conectarse per ssh al `host` amb el `user` i `password` passats. Si no es pot conectar falla.
  - Guarda el valor de `path`. Revisa que el directori existeixi en el servidor remote. Si no exiteix falla.
  - Guarda el valor de `backups_path`. Si no s'ha passat valor el calcula  el calcula amb el `path` + `.backups`. Revisa que el directori existeixi en el servidor remote. Si no existeix el crea.
  - Crida el metode `update_saves_list`.

## SaveGame

Representa una partida guardada.

Atributs de la classe:

- path: ruta abslotua al fitxer que representa la partida guardada
- filename: nom del fitxer (la última part del `path`)
- last_write_date: float que representa els segons desde "epoch" de la ultima vegada que es va modificar self.path

Métodes:

- get_content():

  - Retorna el contingut del fitxer (els bytes).
- backup(dst_path, copy=False):

  - Es fa un backup del fitxer a la carpeta `dst_path`.
  - Es pot fer de dos maneres: fent una copia o moguent el fitxer directament. Dependrà el valor del paràmetre `copy`.
  - Adicionalment es modifica el nom del fitxer per afegir el prefix "csgm_backup_YYYYMMDDHHMMSS_"
  - Retorna el path del backup
