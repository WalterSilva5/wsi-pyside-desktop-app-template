# 14 — Build e Empacotamento

Gerar um executável standalone (`.exe` no Windows, `.app` no macOS, binário no Linux) é feito com **PyInstaller**.

## Por que PyInstaller?

- **Maduro** e suportado pelo time do Qt via `pyside6-deploy`.
- Gera **um único arquivo** (ou pasta com dependências).
- **Cross-platform** — você builda o executável na plataforma alvo.
- **Não precisa** de Python instalado no computador do usuário final.

## Instalação

```bash
uv add --dev pyinstaller

# ou
pip install pyinstaller
```

## Build simples

```bash
uv run pyinstaller main.py \
    --name "MeuApp" \
    --windowed \
    --onefile \
    --add-data "resources;resources"
```

**Explicação das flags:**
- `--name` — nome do executável gerado
- `--windowed` — não abre janela de console (só janela Qt)
- `--onefile` — gera um único `.exe` (vs pasta com dlls)
- `--add-data "resources;resources"` — inclui a pasta `resources/` dentro do bundle (no macOS/Linux use `:` em vez de `;`)

O executável sai em `dist/MeuApp.exe`.

## Arquivo `.spec` recomendado

Para builds repetíveis, use um arquivo `.spec`. Crie `build/MeuApp.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../resources', 'resources'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Reduza o tamanho excluindo módulos não usados
        'tkinter',
        'unittest',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MeuApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,            # Comprime com UPX (se instalado)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # --windowed
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../resources/icons/app.ico',
)
```

Depois basta:

```bash
uv run pyinstaller build/MeuApp.spec
```

## Incluindo `resources/`

O `ConfigService` e `ThemeService` carregam arquivos de `resources/` relativos ao `__file__`. Após o bundle, `__file__` aponta para dentro do `.exe` — o PyInstaller expõe `sys._MEIPASS` para isso.

**Se você encontrar problemas** com arquivos não encontrados, ajuste o método `_find_styles_path` em `src/services/theme_service.py:43` para tratar também o caso `_MEIPASS`:

```python
def _find_styles_path(self) -> Path:
    import sys
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "resources" / "styles"
    # ... fallbacks anteriores
```

## Reduzindo tamanho do `.exe`

- **`--onedir`** em vez de `--onefile`: pasta em vez de .exe monolítico, mas startup é 2-3× mais rápido.
- **Excluir módulos não usados** via `excludes` no `.spec`.
- **UPX**: `pip install upx` e adicione `upx=True` no `.spec` — comprime ~30%.
- **Não empacotar `tests/`, `docs/`, `.venv/`**: PyInstaller ignora por padrão, mas confira.

Tamanho típico de um app PySide6 minimal: **~60-80 MB** onefile, **~50-70 MB** onedir.

## `pyside6-deploy` (alternativa)

O Qt oferece seu próprio empacotador:

```bash
pyside6-deploy main.py
```

Vantagens:
- Integrado com Qt.
- Lida bem com plugins Qt que PyInstaller às vezes esquece.

Desvantagens:
- Menos flexível que PyInstaller.
- Gera bundles maiores.

Para a maioria dos casos, **PyInstaller é suficiente**. Use `pyside6-deploy` só se encontrar problemas específicos.

## Ícones da aplicação

Gere o `.ico` (Windows) ou `.icns` (macOS) a partir de um PNG:

```bash
# Windows (Pillow)
python -c "from PIL import Image; Image.open('icon.png').save('icon.ico')"

# macOS
sips -s format icns icon.png --out icon.icns
```

Adicione ao `.spec`:

```python
icon='resources/icons/app.ico',
```

E ao criar o `QApplication`:

```python
from PySide6.QtGui import QIcon
app.setWindowIcon(QIcon("resources/icons/app.png"))
```

## Versionamento do executável (Windows)

Crie `build/file_version_info.txt`:

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'WSI'),
        StringStruct('FileDescription', 'Meu App'),
        StringStruct('FileVersion', '1.0.0'),
        StringStruct('InternalName', 'MeuApp'),
        StringStruct('OriginalFilename', 'MeuApp.exe'),
        StringStruct('ProductName', 'Meu App'),
        StringStruct('ProductVersion', '1.0.0'),
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
```

E no `.spec`:

```python
exe = EXE(
    ...
    version='file_version_info.txt',
)
```

## Assinatura de código

**Windows**: use `signtool` com um certificado de code signing (caro, ~$300/ano). Sem assinatura, o Windows SmartScreen vai reclamar no primeiro launch.

**macOS**: use `codesign` com um certificado Apple Developer. Sem assinatura, o Gatekeeper bloqueia o app.

Ambos são além do escopo deste template — veja a documentação específica da plataforma.

## CI/CD

Exemplo de build automático via GitHub Actions em `.github/workflows/build.yml`:

```yaml
name: Build
on:
  release:
    types: [created]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv add --dev pyinstaller
      - run: uv run pyinstaller build/MeuApp.spec
      - uses: actions/upload-release-asset@v1
        with:
          upload_url: ${{ github.event.release.upload_url }}
          asset_path: dist/MeuApp.exe
          asset_name: MeuApp-windows.exe
```

Replique para `macos-latest` e `ubuntu-latest` para builds multi-plataforma.

## Próximos passos

Você terminou a documentação! Volte para o [índice](README.md) e explore o que mais te interessar.

Se encontrar algo faltando ou errado, abra uma issue no repositório.
