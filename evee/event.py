#
# This file is part of the onema.io evee Package.
# For the full copyright and license information,
# please view the LICENSE file that was distributed
# with this source code.
#
# @author Juan Manuel Torres <software@onema.io>
#


class Event(object):
    def __init__(self):
        self.__propagation_stopped = False

    def is_propagation_stopped(self) -> bool:
        return self.__propagation_stopped

    def stop_propagation(self):
        self.__propagation_stopped = True
