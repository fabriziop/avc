#!/bin/sh
# .+
#
# .context    : Application View Controller
# .title      : Build AVC web site tar
# .kind	      : command shell
# .author     : Fabrizio Pollastri <pollastri@inrim.it>
# .site	      : Torino - Italy
# .creation   :	30-Oct-2007
# .copyright  :	(c) 2007 Fabrizio Pollastri
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
VERSION="0.6.0"

# computed parameters
SOURCE_ROOT="$NAME-$VERSION"
SRCDIR=`pwd`
TMPDIR=`mktemp -d`

#### build web site tar
echo -n "building web site tar ..."
pushd $TMPDIR &> /dev/null
touch robots.txt
cp -rdp $SRCDIR/{COPYING,copyright,examples,doc/favicon.ico,html,images} .
rm examples/avc
mkdir dist
cp -dp $SRCDIR/{old/avc-*.tar.gz,dist/${NAME}-${VERSION}.tar.gz} dist
mkdir doc
cp -dp $SRCDIR/doc/user_manual.pdf doc
tar -jcvf $SRCDIR/${SOURCE_ROOT}_site.tbz .
echo tar -jcvf $SRCDIR/${SOURCE_ROOT}_site.tbz .
popd &> /dev/null
rm -rf $TMPDIR
echo "Done"

#### END

