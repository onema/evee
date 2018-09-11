#
# This file is part of the onema.io evee Package.
# For the full copyright and license information,
# please view the LICENSE file that was distributed
# with this source code.
#
# @author Juan Manuel Torres <software@onema.io>
#
from abc import ABC
from abc import abstractmethod


class AbstractEventSubscriber(ABC):

    @staticmethod
    @abstractmethod
    def get_subscribed_events():
        """
        Get all the subscribed events
        :return:
        """
