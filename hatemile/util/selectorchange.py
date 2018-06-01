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


class SelectorChange:
    """
    The SelectorChange class store the selector that be attribute change.
    """

    def __init__(
        self,
        selector=None,
        attribute=None,
        value_for_attribute=None
    ):
        """
        Inicializes a new object with the values pre-defineds.
        @param selector: The selector.
        @type selector: str
        @param attribute: The attribute.
        @type attribute: str
        @param value_for_attribute: The value of the attribute.
        @type value_for_attribute: str
        """

        self.selector = selector
        self.attribute = attribute
        self.value_for_attribute = value_for_attribute

    def get_selector(self):
        """
        Returns the selector.
        @return: The selector.
        @rtype: str
        """

        return self.selector

    def get_attribute(self):
        """
        Returns the attribute.
        @return: The attribute.
        @rtype: str
        """

        return self.attribute

    def get_value_for_attribute(self):
        """
        Returns the value of the attribute.
        @return: The value of the attribute.
        @rtype: str
        """

        return self.value_for_attribute
