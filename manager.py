import os
import shutil
import zipfile

class Manager():
    
    def __init__(self, connection):

        self.connection = connection
        self.path = connection.folder
        self.disk = connection.disk


    def listdir(self, print_list = True):

        dirlist = []

        n = 0
        for i in self.disk.listdir(self.path):
            dirlist.append(i.name)
            if print_list:
                print(f'{n}) {i.name}')
            n += 1

        if not dirlist:
            print("There are no files in the current directory")

        return dirlist
    
    
    def mkdir(self, dirname):

        try:
            self.disk.mkdir(f'{self.path}{dirname}/')
        except:
            print(f'Unable to make new directory "{dirname}"')


    def get_dir_by_number(self, n):
        dirlist = self.listdir(False)
        return dirlist[n]


    def remdir(self, dirnum):
            
        try:
            print(f'Removing : {self.path}{self.get_dir_by_number(dirnum)}/')
            self.disk.remove(f'{self.path}{self.get_dir_by_number(dirnum)}/')
        except:
            print(f'Unable to remove this directory')


    def changedir(self, dirname):

        try:
            if dirname == "..":               
                self.path = self.path.rstrip("//")
                self.path = self.path[0:self.path.rfind("/") + 1]
            else: 
                self.path += f'{self.get_dir_by_number(int(dirname))}/'

        except:
            print(f'Unable to change directory to "{dirname}"')


    def start_project(self, project_name):

        new_pr = f'./project_{project_name}.zip'
        try:
            zfile = zipfile.ZipFile(new_pr, 'w')
            zfile.close()

            self.disk.upload(new_pr, f'{self.path}project_{project_name}.zip')
            os.remove(new_pr)

        except Exception as e:
            print(e)
            return False
        

    def download(self):

        self.disk.download(self.active_project_path, f'{self.active_project_pcpath}{self.active_project}')
        zfile = zipfile.ZipFile(f'{self.active_project_pcpath}\\{self.active_project}', 'r')

        if not os.path.exists(self.active_project_pcpath_project_folder):
            os.mkdir(self.active_project_pcpath_project_folder)

        zfile.extractall(self.active_project_pcpath_project_folder)
        zfile.close()
        os.remove(f'{self.active_project_pcpath}\\{self.active_project}')


    def save(self):
        
        try:
            print('Saving the project...')

            with zipfile.ZipFile(f'{self.active_project_pcpath}{self.active_project}.zip', 'w') as zfile:
                for root, dirs, files in os.walk(f'{self.active_project_pcpath_project_folder}'):
                    for file in files:
                        zfile.write(os.path.join(root, file),
                                    os.path.relpath(os.path.join(root, file), self.active_project_pcpath_project_folder),
                                    compress_type=zipfile.ZIP_DEFLATED)

        except Exception as e:
            print(e)
            return False
        
        try:
            self.disk.remove(self.active_project_path)
        except Exception as e:
            print(e)
            return False
        
        try:
            self.disk.upload(f'{self.active_project_pcpath}{self.active_project}.zip', f'{self.path}{self.active_project}')
        except Exception as e:
            print(e)
            return False
        
        try:
            os.remove(f'{self.active_project_pcpath}{self.active_project}.zip')
        except Exception as e:
            print(e)
            return False
        
        return True
        

    def deploy(self, pc_path, n):

        try:

            if not pc_path: 
                pc_path = './projects/' 
                if not os.path.exists(pc_path):
                    os.mkdir(pc_path)

            self.active_project = self.get_dir_by_number(int(n))
            self.active_project_path = f'{self.path}{self.active_project}'
            self.active_project_pcpath = pc_path
            self.active_project_pcpath_project_folder = f'{pc_path}{self.active_project[0:self.active_project.rfind(".")]}'

            if not self.active_project.startswith('project_'):
                print('This is not a project')
                return
            
            self.download()

        except Exception as e:
            print('Unable to deploy this project')
            print(e)
            return

        while True:

            cmd = input(f'[Active] {self.active_project_path} >')

            if cmd == 's':
                self.save()
            
            elif cmd == 'sw':
                self.save()
                print('Wrapping the project...')
                return
            
            elif cmd == 'wrap':
                print('Wrapping project without saving...')
                return
            
            elif cmd == 'wrem':
                saved = self.save()
                print('Removing project folder from PC...')

                try:
                    if saved:
                        shutil.rmtree(os.path.join(os.path.abspath(os.path.dirname(__file__)), self.active_project_pcpath_project_folder))
                        print('Wrapping project...')

                except Exception as e:
                    print('Unable to remove project folder from PC')
                    print(e)
                    return

                finally: 
                    return
                
            elif cmd == 'help':
                print('s    - save active project to YaDisk')
                print('sw   - save and wrap active project')
                print('wrap - wrap active project without saving')
                print('wrem - save and wrap active project with removing project folder on PC')

    def start_process(self):

        print('Enter "help" to get command list')

        while True:

            self.listdir()
            self.act = input(f'{self.path}>')

            if self.act == 'mkdir': 
                dirname = input('Name of new directory >')
                self.mkdir(dirname)

            elif self.act == 'rem': 
                dirnum = int(input('Item to remove >'))
                self.remdir(dirnum)

            elif self.act == 'cd':
                dirnum = input('Which directory change to >')
                self.changedir(dirnum)

            elif self.act == 'start':
                project_name = input('Name of new project >')
                self.start_project(project_name)

            elif self.act == 'dep':
                project_num = input('Which project to deploy >')
                pc_path = input('The path where deploy >')                
                self.deploy(pc_path, project_num)

            elif self.act == 'help':
                print('mkdir - create a directory')
                print('rem   - remove directory or anything')
                print('cd    - change directory. Enter ".." to select the previous directory')
                print('start - start new project')
                print('dep   - deploy project on PC')
                print('ext   - exit the program')
                print('# When prompted to select a directory or project, enter the number of this')

            elif self.act == 'ext':
                return