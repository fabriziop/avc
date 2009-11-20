#!/bin/bash
# .+
#
# .context    : Application View Controller
# .title      : Publish AVC web site
# .kind	      : command shell
# .author     : Fabrizio Pollastri <pollastri@inrim.it>
# .site	      : Torino - Italy
# .creation   :	15-Nov-2007
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

# import parameters
source common.sh

# computed parameters
SOURCE_ROOT="$NAME-$VERSION"


#### build web site
echo -n "publishing web site ..."
rsh fabrizio@serzot rm -rf /var/www/avc/*
scp ${SOURCE_ROOT}_site.tbz fabrizio@serzot:/var/www/avc
rsh fabrizio@serzot "cd /var/www/avc; tar -jxvf ${SOURCE_ROOT}_site.tbz; rm ${SOURCE_ROOT}_site.tbz"
echo "Done"

#### END
