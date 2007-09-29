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
VERSION="0.3.0"

# computed parameters
SOURCE_ROOT="$NAME-$VERSION"


#### build web site tar
echo -n "building web site tar ..."
cat <<-EOF > site_file_list
COPYING
copyright
examples
dist/${NAME}-${VERSION}.tar.gz
html
images
EOF
tar -T site_file_list -jcvf ${SOURCE_ROOT}_site.tbz
rm site_file_list
echo "Done"

#### END

