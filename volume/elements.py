#  This file is part of AIVolume.

#  AIVolume is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  AIVolume is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AIVolume.  If not, see <http://www.gnu.org/licenses/>.

class AreaROI:

    def __init__(self):
        self.key = None
        self.voxelsize = None
        self.index = None
        self.flags = None
        self.image = None
        self.linelist= None
        self.linewidths = None
        self.sections = []
        self.length = None
        self.diameter = None
        self.volume = None
        self.b4channel = None
        self.xstart = None
        self.xend = None

