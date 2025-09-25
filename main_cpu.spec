import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files,copy_metadata

base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
block_cipher = None
datas=[]
datas += (
    collect_data_files("paddlex") +
    copy_metadata("ftfy") +
    copy_metadata("imagesize") +
    copy_metadata("lxml") +
    copy_metadata("opencv-contrib-python") +
    copy_metadata("openpyxl") +
    copy_metadata("premailer") +
    copy_metadata("pyclipper") +
    copy_metadata("pypdfium2") +
    copy_metadata("scikit-learn") +
    copy_metadata("shapely") +
    copy_metadata("tokenizers") +
    copy_metadata("einops") +
    copy_metadata("jinja2") +
    copy_metadata("regex") +
    copy_metadata("tiktoken")
)


# === 加入 images 文件夹（全部图片） ===
images_path = os.path.join(base_dir, 'images')
if os.path.exists(images_path):
    datas.append((images_path, 'images'))

# === 加入 weights 文件夹（全部模板） ===
weights_path = os.path.join(base_dir, 'weights')
if os.path.exists(weights_path):
    datas.append((weights_path, 'weights'))    

# === 加入 DLL 文件 ===
binaries = []


# 虚拟环境 site-packages 路径
site_packages = os.path.join(sys.prefix, "Lib", "site-packages")


# ====== 1. PaddleOCR DLL ======
paddle_dlls = [
    "mkldnn.dll","mklml.dll"
]

paddle_libs_dir = os.path.join(site_packages, "paddle", "libs")
for dll_name in paddle_dlls:
    dll_path = os.path.join(paddle_libs_dir, dll_name)
    if os.path.exists(dll_path):
        binaries.append((dll_path, '.'))
        print("[已加入 Paddle DLL]", dll_path)
    else:
        print("⚠️ 没找到 Paddle DLL:", dll_path)

# === 加入自定义 DLL ===
dll1_path = os.path.join(base_dir, 'Dll1.dll')
if os.path.exists(dll1_path):
    binaries.append((dll1_path, '.'))

a = Analysis(
    ['main.py'],
    pathex=[base_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=[],
    excludes=[],
    hookspath=[],
    runtime_hooks=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='rc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
    single_file=True,
    uac_admin=True
 )
#pyinstaller --clean main_cpu.spec 
