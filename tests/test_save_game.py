import pytest
import os
import shutil
from save_game import SaveGame
from datetime import datetime


class TestSaveGame(object):

    @pytest.fixture
    def setup_and_teardown(self):
        # SetUp:
        # - Ens asegurem que els fixtures comencen en l'estat correcte
        # - Retornem un diccionari amb els fixtures disponibles
        self.base_path = os.path.join(os.path.dirname(__file__), "fixtures", "test_save_game")
        self.base_backup_path = os.path.join(self.base_path, "backup_test_save_game")
        files = ['file1.txt', 'file2.csv', 'img_test.png']
        files_data = {}
        for file in files:
            assert os.path.exists(os.path.join(self.base_path, file))
            assert os.path.exists(os.path.join(self.base_backup_path, file))
            path = os.path.join(self.base_path, file)
            f1 = open(path, "rb")
            content = f1.read()
            f2 = open(os.path.join(self.base_backup_path, file), "rb")
            assert content == f2.read()
            files_data[file] = {'path': path, 'content': content}

        # Test
        yield files_data

        # TearDown
        # - Sobreescrivim els fixtures amb el contingut de la carpeta backup
        for file in files:
            assert os.path.exists(os.path.join(self.base_backup_path, file))
            f1_path = os.path.join(self.base_path, file)
            f2_path = os.path.join(self.base_backup_path, file)
            shutil.copy2(f2_path, f1_path)

    def test_last_write_date(self, setup_and_teardown):
        sg = SaveGame(setup_and_teardown['file1.txt']['path'])
        ultima_modificacio_original = sg.last_write_date
        assert ultima_modificacio_original > 0
        ultima_modificacio_sense_haver_editat = sg.last_write_date
        assert ultima_modificacio_sense_haver_editat == ultima_modificacio_original
        fw = open(setup_and_teardown['file1.txt']['path'], "w")
        fw.write("pastanaga bullida")
        fw.close()
        ultima_modificacio_havent_editat = sg.last_write_date
        assert ultima_modificacio_havent_editat > ultima_modificacio_original

    def test_backup_without_copy(self, setup_and_teardown):
        backup_dir = os.path.join(self.base_path, "test_backup")
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        os.makedirs(backup_dir)

        sg = SaveGame(setup_and_teardown['file1.txt']['path'])

        # Al fer un backup amb sense el copy no existeix el fitxer original i s'ha modificat el SaveGame
        backup_path = sg.backup(backup_dir, copy=False)
        timestamp = datetime.now().strftime("%Y%m%d%H")
        assert f"csgm_backup_{timestamp}" in backup_path
        assert backup_path.endswith(sg.filename)
        assert os.path.exists(backup_path)
        assert sg.path == backup_path
        assert not os.path.exists(setup_and_teardown['file1.txt']['path'])
        f1 = open(sg.path, "rb")
        assert f1.read() == setup_and_teardown['file1.txt']['content']
        f1.close()
        shutil.rmtree(backup_dir)

    def test_backup_without_copy_png_file(self, setup_and_teardown):
        backup_dir = os.path.join(self.base_path, "test_backup")
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        os.makedirs(backup_dir)

        sg = SaveGame(setup_and_teardown['img_test.png']['path'])

        # Al fer un backup amb sense el copy no existeix el fitxer original i s'ha modificat el SaveGame
        backup_path = sg.backup(backup_dir, copy=False)
        timestamp = datetime.now().strftime("%Y%m%d%H")
        assert f"csgm_backup_{timestamp}" in backup_path
        assert backup_path.endswith(sg.filename)
        assert os.path.exists(backup_path)
        assert sg.path == backup_path
        assert not os.path.exists(setup_and_teardown['img_test.png']['path'])
        f1 = open(sg.path, "rb")
        assert f1.read() == setup_and_teardown['img_test.png']['content']
        f1.close()
        shutil.rmtree(backup_dir)

    def test_backup_with_copy(self, setup_and_teardown):
        backup_dir = os.path.join(self.base_path, "test_backup")
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        os.makedirs(backup_dir)

        sg = SaveGame(setup_and_teardown['file1.txt']['path'])

        # Al fer un backup amb el copy continua existint el fitxer original i no s'ha modificat el SaveGame
        backup_path = sg.backup(backup_dir, copy=True)
        timestamp = datetime.now().strftime("%Y%m%d%H")
        assert f"csgm_backup_{timestamp}" in backup_path
        assert backup_path.endswith(sg.filename)
        assert os.path.exists(backup_path)
        assert sg.path == setup_and_teardown['file1.txt']['path']
        assert os.path.exists(sg.path)
        f1 = open(sg.path, "rb")
        content = f1.read()
        f2 = open(backup_path, "rb")
        assert content == f2.read()
        assert content == setup_and_teardown['file1.txt']['content']
        f1.close()
        f2.close()
        shutil.rmtree(backup_dir)

    def test_get_content(self, setup_and_teardown):
        expected_hard_coded_vals = {
            'file1.txt': """ç
ñ
à
;
-
@
%
$

""",
            'file2.csv': """1;2;3;4
5;6;7;8"""
        }
        for fname, vals in setup_and_teardown.items():
            sg = SaveGame(vals['path'])
            res = sg.get_content()
            assert res == vals['content']
            if fname in expected_hard_coded_vals:
                assert res == expected_hard_coded_vals[fname].encode()
