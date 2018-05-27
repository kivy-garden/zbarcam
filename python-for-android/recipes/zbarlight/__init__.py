import os
from pythonforandroid.recipe import PythonRecipe


class ZbarLightRecipe(PythonRecipe):
    version = '1.2'
    url = 'https://github.com/Polyconseil/zbarlight/archive/{version}.tar.gz'
    depends = [
        ('python2', 'python3crystax'), 'setuptools', 'libzbar']
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        # TODO: python 3 support
        env = super(ZbarLightRecipe, self).get_recipe_env(arch, with_flags_in_cc)
        libzbar = self.get_recipe('libzbar', self.ctx)
        libzbar_dir = libzbar.get_build_dir(arch.arch)
        env['PYTHON_ROOT'] = self.ctx.get_python_install_dir()
        env['CFLAGS'] += ' -I' + os.path.join(libzbar_dir, 'include')
        env['CFLAGS'] += ' -I' + env['PYTHON_ROOT'] + '/include/python2.7'
        # TODO
        env['LDSHARED'] = env['CC'] + \
            ' -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions'
        # TODO: hardcoded Python version
        env['LDFLAGS'] += " -landroid -lpython2.7 -lzbar"
        return env


recipe = ZbarLightRecipe()
