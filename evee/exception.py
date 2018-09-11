#
# This file is part of the onema.io evee Package.
# For the full copyright and license information,
# please view the LICENSE file that was distributed
# with this source code.
#
# @author Juan Manuel Torres <software@onema.io>
#


class EventDispatcherError(Exception):
    pass


class LogicError(EventDispatcherError):
    pass


class BadMethodCallError(LogicError):
    pass
