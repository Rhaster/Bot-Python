# plik.spec

# Importy
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

# Konfiguracja dla test.py
a = Analysis(['test.py'],
             pathex=[r'C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Bot\\test.py'],
             binaries=[],
             # reszta konfiguracji
             )
pyzA = PYZ(a.pure)
exeA = EXE(pyzA,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + collect_data_files(r'', r'C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Bot\\test.py'),
          a.dependencies,
          name=os.path.join('dist', 'test.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=1 )

# Konfiguracja dla Debbug.py
b = Analysis(['Debbug.py'],
             pathex=[r'C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Bot\\Debbug.py'],
             binaries=[],
             # reszta konfiguracji
             )
pyzB = PYZ(b.pure)
exeB = EXE(pyzB,
          b.scripts,
          b.binaries,
          b.zipfiles,
          b.datas + collect_data_files(r'', r'C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Bot\\test.py'),
          b.dependencies,
          name=os.path.join('dist', 'Debbug.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=1 )

# Konfiguracja dla bilkom.py
c = Analysis(['bilkom.py'],
             pathex=[r'C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Bot\\bilkom.py'],
             binaries=[],
             # reszta konfiguracji
             )
pyzC = PYZ(c.pure)
exeC = EXE(pyzC,
          c.scripts,
          c.binaries,
          c.zipfiles,
          c.datas + collect_data_files(r'',r'C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Bot\\bilkom.py'),
          c.dependencies,
          name=os.path.join('dist', 'bilkom.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=1 )

# Kolekcja plików
coll = COLLECT(exeA, exeB, exeC,
               a.binaries,
               a.zipfiles,
               a.datas,
               b.binaries,
               b.zipfiles,
               b.datas,
               c.binaries,
               c.zipfiles,
               c.datas,
               # reszta konfiguracji
               )