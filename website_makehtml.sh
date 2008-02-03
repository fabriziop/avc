#!/bin/sh
# .+
#
# .context    : Application View Controller
# .title      : Build AVC web site html files
# .kind	      : command shell
# .author     : Fabrizio Pollastri <pollastri@inrim.it>
# .site	      : Torino - Italy
# .creation   :	11-Jan-2008
# .copyright  :	(c) 2008 Fabrizio Pollastri
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


# build highlighted example source code for "quick start pages"
echo "making html highlighted source code ..."
pushd examples &> /dev/null
source-highlight -n *_spin*.py
mv *_spin*.py.html ../wml
popd &> /dev/null

# build html with WML
echo "making html from wml ..."
pushd wml &> /dev/null
wmk
popd &> /dev/null

#### END

