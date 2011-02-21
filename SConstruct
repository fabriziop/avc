# .+
#
# .context    : Application View Controller
# .title      : Build AVC distibutions
# .kind	      : scons configuration
# .author     : Fabrizio Pollastri <f.pollastri@inrim.it>
# .site	      : Torino - Italy
# .creation   :	13-Jan-2011
# .copyright  :	(c) 2011 Fabrizio Pollastri
# .license    : GNU General Public License (see below)
#
# This file is part of "AVC, Application View Controller".
#
# AVC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# AVC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# .-

## import required modules
from glob import glob
import re

## parameters
NAME = 'avc'
# read version string, author name, author e-mail from file src/avccore.py
ftext = open('src/avccore.py').read()
VERSION = re.search('__version__\s+=\s+\'(\d+\.\d+\.\d+)\'',ftext).group(1)
AUTHOR = re.search('__author__ = \'([a-zA-Z]+\s+[a-zA-Z]+)\s+',ftext).group(1)
AUTHOR_EMAIL = re.search('__author__ = .*?<(.*?)>',ftext).group(1)

## define environment
env = Environment()

## build highlighted syntax examples
for source in Glob('examples/*_spin*.py'):
  env.Command('wml/'+source.name+'.html',source, \
  'source-highlight -n -i $SOURCE -o $TARGET')

## build html pages from wml files
# wml files scanner function
def wml_scan(node, env, path):
  return re.findall(r'\#include\s*[\'\"]([\w\.\/]*)',node.get_text_contents())
# build
env.Requires(Glob('html/*.html'),'html/common.css')
for source in Glob('wml/*.wml'):
  env.Command('html/${SOURCE.filebase}.html',[source] + ['wml/common.wml.h'], \
  'wml -o ../html/${TARGET.filebase}.html ${SOURCE.file}',chdir='wml', \
  source_scanner=Scanner(wml_scan))

## build user manual pdf
env.Command('doc/user_manual.pdf','doc/user_manual.odt', \
  ['ooffice -invisible &','odt2pdf $SOURCE'])

## build python source distribution
# get dependences from file 'MANIFEST.in'
ftext = open('MANIFEST.in').read()
sources = []
# include file
for row in map(glob,re.findall('include\s+(.*?)\n',ftext)):
  sources += row
# exclude file
for row in map(glob,re.findall('exclude\s+(.*?)\n',ftext)):
  for fname in row:
    sources.remove(fname)
# add non MANIFEST.in dependencies
sources += glob('src/*.py')
# build
sdist_target = 'dist/' + NAME + '-' + VERSION + '.tar.gz'
sdist = env.Command(sdist_target,sources,'python setup.py -q sdist')

## build web site tar
env['TARFLAGS'] = '-jc --exclude=examples/avc --xform "s/old/dist/"'
tar_target = NAME + '-' + VERSION + '_site.tbz'
env.Tar(tar_target,Split('COPYING.FDL COPYING.GPL copyright'))
env.Tar(tar_target,Split('examples html images old'))
env.Tar(tar_target,Split('doc/favicon.ico doc/user_manual.pdf'))
env.Tar(tar_target,sdist_target)

#### END
