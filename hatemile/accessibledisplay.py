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
Module of AccessibleDisplay interface.
"""


class AccessibleDisplay:
    """
    The AccessibleDisplay interface improve accessibility, showing
    informations.
    """

    def fix_shortcut(self, element):
        """
        Display the shortcuts of element.

        :param element: The element with shortcuts.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_shortcuts(self):
        """
        Display the shortcuts of elements.
        """

        pass
