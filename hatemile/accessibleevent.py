# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module of AccessibleEvent interface.
"""


class AccessibleEvent:
    """
    The AccessibleEvent interface fixes accessibility problems associated with
    JavaScript events in elements.
    """

    def fix_drop(self, element):
        """
        Provide a solution for the element that has drop events.

        :param element: The element with drop event.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_drag(self, element):
        """
        Provide a solution for the element that has drag events.

        :param element: The element with drag event.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_drags_and_drops(self):
        """
        Provide a solution for elements that has Drag-and-Drop events.
        """

        pass

    def fix_hover(self, element):
        """
        Provide a solution for the element that has inaccessible hover events.

        :param element: The element with hover event.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_hovers(self):
        """
        Provide a solution for elements that has inaccessible hover events.
        """

        pass

    def fix_active(self, element):
        """
        Provide a solution for the element that has inaccessible active events.

        :param element: The element with active event.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_actives(self):
        """
        Provide a solution for elements that has inaccessible active events.
        """

        pass
