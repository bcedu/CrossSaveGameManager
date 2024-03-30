from datetime import datetime
import os
import shutil


class SaveGame(object):
    path: str  # ruta abslotua al fitxer que representa la partida guardada
    filename: str  # nom del fitxer (la ultima aprt del path)

    @property
    def last_write_date(self) -> float:
        """
        :return:
            Retorna un float que representa els segons desde "epoch" de la ultima vegada que es va modificar self.path.
        """
        return os.path.getmtime(self.path)

    def __init__(self, path: str, filename: str = None):
        self.path = path
        if not os.path.exists(path):
            raise Exception(f"The given path ({path}) does not exists!")

        if filename:
            self.filename = filename
        else:
            self.filename = os.path.basename(path)

    def get_content(self) -> bytes:
        """
        :return:
            Retorna els bytes que representen el contingut de self.path.
        """
        with open(self.path, "rb") as f:
            res = f.read()
        return res

    def backup(self, dst_path: str, copy: bool = False) -> str:
        """
        :param dst_path: ruta completa a la carpeta on es guarda el backup.
        :param copy: boolea per indicar si es copia o es mou el fitxer.
        :return:
            Es fa un backup del fitxer a la carpeta `path`.
            Es pot fer de dos maneres: fent una copia o moguent el fitxer directament. Dependrà el valor del paràmetre `copy`.
            Adicionalment es modifica el nom del fitxer per afegir el prefix "csgm_backup_YYYYMMDDHHMMSS_"

            Retorna el nou path del backup
        """
        if not os.path.exists(dst_path):
            raise Exception(f"The given path {dst_path} does not exists!")
        if not os.path.isdir(dst_path):
            raise Exception(f"The given path {dst_path} is not a directory!")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_path = f"{dst_path}/csgm_backup_{timestamp}_{self.filename}"
        if copy:
            shutil.copy2(self.path, new_path)
        else:
            os.replace(self.path, new_path)
            self.path = new_path
        return new_path
