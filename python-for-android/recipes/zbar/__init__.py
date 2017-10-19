from os.path import join
from pythonforandroid.recipe import PythonRecipe


class ZBarRecipe(PythonRecipe):

    version = '0.10'

    url = 'https://github.com/ZBar/ZBar/archive/{version}.zip'

    call_hostpython_via_targetpython = False

    depends = ['hostpython2', 'python2', 'setuptools', 'libzbar']

    def get_build_dir(self, arch):
        zbar_dir = super(ZBarRecipe, self).get_build_dir(arch)
        zbar_python_dir = join(zbar_dir, 'python')
        return zbar_python_dir


recipe = ZBarRecipe()
