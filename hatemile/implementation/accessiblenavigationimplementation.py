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
Module of AccessibleNavigationImplementation class.
"""

import os
import re
from xml.dom import minidom
from hatemile.accessiblenavigation import AccessibleNavigation
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.idgenerator import IDGenerator


class AccessibleNavigationImplementation(AccessibleNavigation):
    """
    The AccessibleNavigationImplementation class is official implementation of
    AccessibleNavigation interface.
    """

    def __init__(
        self,
        parser,
        configure,
        skipper_file_name=None,
        user_agent=None
    ):
        """
        Initializes a new object that manipulate the accessibility of the
        navigation of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        :param skipper_file_name: The file path of skippers configuration.
        :type skipper_file_name: str
        :param user_agent: The user agent of the user.
        :type user_agent: str
        """

        self.parser = parser
        self.id_generator = IDGenerator('navigation')
        self.id_container_shortcuts = 'container-shortcuts'
        self.id_container_skippers = 'container-skippers'
        self.id_container_heading = 'container-heading'
        self.id_text_shortcuts = 'text-shortcuts'
        self.id_text_heading = 'text-heading'
        self.class_skipper_anchor = 'skipper-anchor'
        self.class_heading_anchor = 'heading-anchor'
        self.class_long_description_link = 'longdescription-link'
        self.data_access_key = 'data-shortcutdescriptionfor'
        self.data_anchor_for = 'data-anchorfor'
        self.data_heading_anchor_for = 'data-headinganchorfor'
        self.data_heading_level = 'data-headinglevel'
        self.data_long_description_for_image = 'data-longdescriptionfor'
        self.text_shortcuts = configure.get_parameter('text-shortcuts')
        self.text_heading = configure.get_parameter('text-heading')
        self.standart_prefix = configure.get_parameter(
            'text-standart-shortcut-prefix'
        )
        self.prefix_long_description_link = configure.get_parameter(
            'prefix-longdescription'
        )
        self.suffix_long_description_link = configure.get_parameter(
            'suffix-longdescription'
        )
        self.skippers = AccessibleNavigationImplementation._get_skippers(
            skipper_file_name
        )
        self.list_shortcuts_added = False
        self.list_skippers_added = False
        self.validate_heading = False
        self.valid_heading = False
        self.list_skippers = None
        self.list_shortcuts = None

        if user_agent is not None:
            user_agent = user_agent.lower()
            opera = 'opera' in user_agent
            mac = 'mac' in user_agent
            konqueror = 'konqueror' in user_agent
            spoofer = 'spoofer' in user_agent
            safari = 'applewebkit' in user_agent
            windows = 'windows' in user_agent
            chrome = 'chrome' in user_agent
            firefox = re.match(
                '.*firefox/[2-9]|minefield/3.*',
                user_agent
            ) is not None
            internet_explorer = (
                ('msie' in user_agent)
                or ('trident' in user_agent)
            )

            if opera:
                self.prefix = 'SHIFT + ESC'
            elif chrome and mac and (not spoofer):
                self.prefix = 'CTRL + OPTION'
            elif safari and (not windows) and (not spoofer):
                self.prefix = 'CTRL + ALT'
            elif (not windows) and (safari or mac or konqueror):
                self.prefix = 'CTRL'
            elif firefox:
                self.prefix = 'ALT + SHIFT'
            elif chrome or internet_explorer:
                self.prefix = 'ALT'
            else:
                self.prefix = self.standart_prefix
        else:
            self.prefix = self.standart_prefix

    @staticmethod
    def _get_skippers(file_name=None):
        """
        Returns the skippers of configuration.

        :param file_name: The file path of skippers configuration.
        :type file_name: str
        :return: The skippers of configuration.
        :rtype: list(dict(str, str))
        """

        skippers = []
        if file_name is None:
            file_name = os.path.join(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
            )), 'skippers.xml')
        xmldoc = minidom.parse(file_name)
        skippers_xml = xmldoc.getElementsByTagName(
            'skippers'
        )[0].getElementsByTagName('skipper')
        for skipper_xml in skippers_xml:
            skippers.append({
                'selector': skipper_xml.attributes['selector'].value,
                'description': skipper_xml.attributes['description'].value,
                'shortcut': skipper_xml.attributes['shortcut'].value
            })
        return skippers

    def _get_description(self, element):
        """
        Returns the description of element.

        :param element: The element with description.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The description of element.
        :rtype: str
        """

        description = None
        if element.has_attribute('title'):
            description = element.get_attribute('title')
        elif element.has_attribute('aria-label'):
            description = element.get_attribute('aria-label')
        elif element.has_attribute('alt'):
            description = element.get_attribute('alt')
        elif element.has_attribute('label'):
            description = element.get_attribute('label')
        elif (
            (element.has_attribute('aria-labelledby'))
            or (element.has_attribute('aria-describedby'))
        ):
            if element.has_attribute('aria-labelledby'):
                description_ids = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-labelledby').strip()
                )
            else:
                description_ids = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-describedby').strip()
                )
            for description_id in description_ids:
                element_description = self.parser.find(
                    '#' + description_id
                ).first_result()
                if element_description is not None:
                    description = element_description.get_text_content()
                    break
        elif (
            (element.get_tag_name() == 'INPUT')
            and (element.has_attribute('type'))
        ):
            type_attribute = element.get_attribute('type').lower()
            if (
                (
                    (type_attribute == 'button')
                    or (type_attribute == 'submit')
                    or (type_attribute == 'reset')
                )
                and (element.has_attribute('value'))
            ):
                description = element.get_attribute('value')
        if not bool(description):
            description = element.get_text_content()
        return re.sub('[ \n\r\t]+', ' ', description.strip())

    def _generate_list_shortcuts(self):
        """
        Generate the list of shortcuts of page.

        :return: The list of shortcuts of page.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        container = self.parser.find(
            '#' + self.id_container_shortcuts
        ).first_result()
        html_list = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.id_container_shortcuts)

                text_container = self.parser.create_element('span')
                text_container.set_attribute('id', self.id_text_shortcuts)
                text_container.append_text(self.text_shortcuts)

                container.append_element(text_container)
                local.append_element(container)
        if container is not None:
            html_list = self.parser.find(container).find_children(
                'ul'
            ).first_result()
            if html_list is None:
                html_list = self.parser.create_element('ul')
                container.append_element(html_list)
        self.list_shortcuts_added = True

        return html_list

    def _generate_list_skippers(self):
        """
        Generate the list of skippers of page.

        :return: The list of skippers of page.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        container = self.parser.find(
            '#' + self.id_container_skippers
        ).first_result()
        html_list = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.id_container_skippers)
                local.get_first_element_child().insert_before(container)
        if container is not None:
            html_list = self.parser.find(container).find_children(
                'ul'
            ).first_result()
            if html_list is None:
                html_list = self.parser.create_element('ul')
                container.append_element(html_list)
        self.list_skippers_added = True

        return html_list

    def _generate_list_heading(self):
        """
        Generate the list of heading links of page.

        :return: The list of heading links of page.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        container = self.parser.find(
            '#' + self.id_container_heading
        ).first_result()
        html_list = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.id_container_heading)

                text_container = self.parser.create_element('span')
                text_container.set_attribute('id', self.id_text_heading)
                text_container.append_text(self.text_heading)

                container.append_element(text_container)
                local.append_element(container)
        if container is not None:
            html_list = self.parser.find(container).find_children(
                'ol'
            ).first_result()
            if html_list is None:
                html_list = self.parser.create_element('ol')
                container.append_element(html_list)
        return html_list

    def _get_heading_level(self, element):
        """
        Returns the level of heading.

        :param element: The heading.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The level of heading.
        :rtype: int
        """

        tag = element.get_tag_name()
        if tag == 'H1':
            return 1
        elif tag == 'H2':
            return 2
        elif tag == 'H3':
            return 3
        elif tag == 'H4':
            return 4
        elif tag == 'H5':
            return 5
        elif tag == 'H6':
            return 6
        return -1

    def _is_valid_heading(self):
        """
        Inform if the headings of page are sintatic correct.

        :return: True if the headings of page are sintatic correct or false if
                 not.
        :rtype: bool
        """

        elements = self.parser.find('h1,h2,h3,h4,h5,h6').list_results()
        last_level = 0
        count_main_heading = 0
        self.validate_heading = True
        for element in elements:
            level = self._get_heading_level(element)
            if level == 1:
                if count_main_heading == 1:
                    return False
                else:
                    count_main_heading = 1
            if (level - last_level) > 1:
                return False
            last_level = level
        return True

    def _generate_anchor_for(self, element, data_attribute, anchor_class):
        """
        Generate an anchor for the element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param data_attribute: The name of attribute that links the element
                               with the anchor.
        :type data_attribute: str
        :param anchor_class: The HTML class of anchor.
        :type anchor_class: str
        :return: The anchor.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self.id_generator.generate_id(element)
        if self.parser.find(
            '[' + data_attribute + '="' + element.get_attribute('id') + '"]'
        ).first_result() is None:
            if element.get_tag_name() == 'A':
                anchor = element
            else:
                anchor = self.parser.create_element('a')
                self.id_generator.generate_id(anchor)
                anchor.set_attribute('class', anchor_class)
                element.insert_before(anchor)
            if not anchor.has_attribute('name'):
                anchor.set_attribute('name', anchor.get_attribute('id'))
            anchor.set_attribute(data_attribute, element.get_attribute('id'))
        return anchor

    def _free_shortcut(self, shortcut):
        """
        Replace the shortcut of elements, that has the shortcut passed.

        :param shortcut: The shortcut.
        :type shortcut: str
        """

        alpha_numbers = '1234567890abcdefghijklmnopqrstuvwxyz'
        elements = self.parser.find('[accesskey]').list_results()
        found = False
        for element in elements:
            shortcuts = element.get_attribute('accesskey').lower()
            if CommonFunctions.in_list(shortcuts, shortcut):
                for key in alpha_numbers:
                    found = True
                    for element_with_shortcuts in elements:
                        shortcuts = element_with_shortcuts.get_attribute(
                            'accesskey'
                        ).lower()
                        if CommonFunctions.in_list(shortcuts, key):
                            found = False
                            break
                    if found:
                        element.set_attribute('accesskey', key)
                        break
                if found:
                    break

    def fix_shortcut(self, element):
        if element.has_attribute('accesskey'):
            description = self._get_description(element)
            if not element.has_attribute('title'):
                element.set_attribute('title', description)

            if not self.list_shortcuts_added:
                self.list_shortcuts = self._generate_list_shortcuts()

            if self.list_shortcuts is not None:
                keys = re.split(
                    '[ \n\t\r]+',
                    element.get_attribute('accesskey')
                )
                for key in keys:
                    key = key.upper()
                    if self.parser.find(self.list_shortcuts).find_children(
                        '[' + self.data_access_key + '="' + key + '"]'
                    ).first_result() is None:
                        item = self.parser.create_element('li')
                        item.set_attribute(self.data_access_key, key)
                        item.append_text(
                            self.prefix
                            + ' + '
                            + key
                            + ': '
                            + description
                        )
                        self.list_shortcuts.append_element(item)

    def fix_shortcuts(self):
        elements = self.parser.find('[accesskey]').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.fix_shortcut(element)

    def fix_skipper(self, element, skipper):
        if not self.list_skippers_added:
            self.list_skippers = self._generate_list_skippers()
        if self.list_skippers is not None:
            anchor = self._generate_anchor_for(
                element,
                self.data_anchor_for,
                self.class_skipper_anchor
            )
            if anchor is not None:
                item_link = self.parser.create_element('li')
                link = self.parser.create_element('a')
                link.set_attribute('href', '#' + anchor.get_attribute('name'))
                link.append_text(skipper['description'])

                shortcuts = skipper['shortcut']
                if shortcuts:
                    shortcut = shortcuts[0]
                    if shortcut != '':
                        self._free_shortcut(shortcut)
                        link.set_attribute('accesskey', shortcut)
                self.id_generator.generate_id(link)

                item_link.append_element(link)
                self.list_skippers.append_element(item_link)

    def fix_skippers(self):
        for skipper in self.skippers:
            elements = self.parser.find(skipper['selector']).list_results()
            for element in elements:
                if CommonFunctions.is_valid_element(element):
                    self.fix_skipper(element, skipper)

    def fix_heading(self, element):
        if not self.validate_heading:
            self.valid_heading = self._is_valid_heading()
        if self.valid_heading:
            anchor = self._generate_anchor_for(
                element,
                self.data_heading_anchor_for,
                self.class_heading_anchor
            )
            if anchor is not None:
                list_element = None
                level = self._get_heading_level(element)
                if level == 1:
                    list_element = self._generate_list_heading()
                else:
                    super_item = self.parser.find(
                        '#'
                        + self.id_container_heading
                    ).find_descendants(
                        '['
                        + self.data_heading_level
                        + '="'
                        + str(level - 1)
                        + '"]'
                    ).last_result()
                    if super_item is not None:
                        list_element = self.parser.find(
                            super_item
                        ).find_children('ol').first_result()
                        if list_element is None:
                            list_element = self.parser.create_element('ol')
                            super_item.append_element(list_element)
                if list_element is not None:
                    item = self.parser.create_element('li')
                    item.set_attribute(self.data_heading_level, str(level))

                    link = self.parser.create_element('a')
                    link.set_attribute(
                        'href',
                        '#' + anchor.get_attribute('name')
                    )
                    link.append_text(element.get_text_content())

                    item.append_element(link)
                    list_element.append_element(item)

    def fix_headings(self):
        elements = self.parser.find('h1,h2,h3,h4,h5,h6').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.fix_heading(element)

    def fix_long_description(self, element):
        if element.has_attribute('longdesc'):
            self.id_generator.generate_id(element)
            id_element = element.get_attribute('id')
            if self.parser.find(
                '['
                + self.data_long_description_for_image
                + '="'
                + id_element
                + '"]'
            ).first_result() is None:
                if element.has_attribute('alt'):
                    text = (
                        self.prefix_long_description_link
                        + ' '
                        + element.get_attribute('alt')
                        + ' '
                        + self.suffix_long_description_link
                    )
                else:
                    text = (
                        self.prefix_long_description_link
                        + ' '
                        + self.suffix_long_description_link
                    )
                anchor = self.parser.create_element('a')
                anchor.set_attribute('href', element.get_attribute('longdesc'))
                anchor.set_attribute('target', '_blank')
                anchor.set_attribute(
                    self.data_long_description_for_image,
                    id_element
                )
                anchor.set_attribute('class', self.class_long_description_link)
                anchor.append_text(text.strip())
                element.insert_after(anchor)

    def fix_long_descriptions(self):
        elements = self.parser.find('[longdesc]').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.fix_long_description(element)
