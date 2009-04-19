#!/bin/bash
# .+
#
# .context    : Application View Controller
# .title      : Build AVC distibutions
# .kind	      : command shell
# .author     : Fabrizio Pollastri <f.pollastri@inrim.it>
# .site	      : Torino - Italy
# .creation   :	15-Oct-2007
# .copyright  :	(c) 2007-2009 Fabrizio Pollastri
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

# parameters
NAME="avc"
VERSION="0.7.1"
MANTAINER_ADDRESS="f.pollastri@inrim.it"

SECTION="python"
PRIORITY="optional"
DEPENDS="python (>=2.2)"
DESCRIPTION="live connection among widgets and application variables"

# computed parameters
ROOT=`pwd`
SOURCE_ROOT="$NAME-$VERSION"
TAR="$NAME-$VERSION.tar.gz"

# cleanup
rm -rf dist

# build python source distribution
echo -n "building python distribution ... "
python setup.py -q sdist
echo "Done"

# expand tar
echo "building Debian distribution ..."
pushd dist > /dev/null
tar zxvf $TAR > /dev/null

# rename source dir according debian standards
mv $SOURCE_ROOT python-$SOURCE_ROOT

# goto source directory
pushd python-$SOURCE_ROOT > /dev/null

# initial debianization
dh_make -s -c GPL -e $MANTAINER_ADDRESS -f ../$TAR

# remove unwanted files
rm debian/dirs debian/*.{ex,EX} debian/README.Debian

# copy debian changelog,control,copyright,dirs,docs,rules files
cp $ROOT/copyright $ROOT/deb/{changelog,control,docs,rules} debian
chmod +x debian/rules

# build debian package
dpkg-buildpackage -tc -kpollastri

# clean up dpkg-deb working directories
popd > /dev/null
rm -rf python-$SOURCE_ROOT
echo "Debian distribution done"

#### END
