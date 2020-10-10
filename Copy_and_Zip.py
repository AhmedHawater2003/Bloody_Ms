import subprocess
import shutil
import os
import time
client_zip_name = "BLOODY MS - MR-Tamer"
FolderName = "BLOODY MS"
#@@@@@@@@@@@@@
new_folder_path = f"D:/Ahmed_Programing_Things/PythonAndOthersRelated/BLOODY MS/Clients/{FolderName}"
#@@@@@@@@@@@@@
things_inside = os.listdir()
things_inside.remove("Copy_and_Zip.py")
things_inside.remove("LKG.exe")



files = list(filter(lambda x : x.endswith("py") or x.endswith("exe") or x.endswith("ico") , things_inside))
folders = list(filter(lambda x : not x.endswith("py") and  not x.endswith("exe") and not x.endswith("ico") , things_inside))

def CopyMove():
    os.mkdir(new_folder_path)
    for i in folders:
        copy_name = i + "_copy"
        shutil.copytree(i , copy_name)
        shutil.move(copy_name , new_folder_path)

    for i in files:
        copy_name = i.split(".")
        oo = copy_name[-1]
        pp = copy_name[0]
        pp = pp + "_copy"
        copy_name = pp + "." + oo
        shutil.copy(i, copy_name)
        shutil.move(copy_name, new_folder_path)

def Rename():
    os.chdir(new_folder_path)
    for i in os.listdir():
        os.rename(i , i.replace("_copy", ""))

def ToExe():
    os.chdir(new_folder_path)
    subprocess.run('pyinstaller login_page.py --onefile -w -i "controllericon.ico" ', shell = True)


def Clean():
    os.chdir(new_folder_path)
    shutil.copy("dist/login_page.exe","BLOODY MS.exe")
    shutil.rmtree("dist")
    shutil.rmtree("build")
    shutil.rmtree("__pycache__")
    for i in os.listdir(new_folder_path):
        if i.endswith("py") or i.endswith("spec"):
            os.remove(i)
        # @@@@@@@@@@@@@
    os.chdir("D:/Ahmed_Programing_Things/PythonAndOthersRelated/BLOODY MS/Clients")
    shutil.make_archive(client_zip_name, 'zip', new_folder_path)
    shutil.rmtree(f"D:/Ahmed_Programing_Things/PythonAndOthersRelated/BLOODY MS/Clients/{FolderName}")
        # @@@@@@@@@@@@@  


CopyMove()
Rename()
ToExe()
Clean()

# subprocess.Popen('pyinstaller login_page.py --onefile -w', shell = True)
print('done')
