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

from hatemile.util.commonfunctions import CommonFunctions
from hatemile.accessibleform import AccessibleForm
import re


class AccessibleFormImplementation(AccessibleForm):
    """
    The AccessibleFormImplementation class is official implementation of
    AccessibleForm interface.
    """

    def __init__(self, parser, configure):
        """
        Initializes a new object that manipulate the accessibility of the forms
        of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        """

        self.parser = parser
        self.data_label_prefix_required_field = 'data-prefixrequiredfield'
        self.data_label_suffix_required_field = 'data-suffixrequiredfield'
        self.data_label_prefix_range_min_field = 'data-prefixvalueminfield'
        self.data_label_suffix_range_min_field = 'data-suffixvalueminfield'
        self.data_label_prefix_range_max_field = 'data-prefixvaluemaxfield'
        self.data_label_suffix_range_max_field = 'data-suffixvaluemaxfield'
        self.data_label_prefix_autocomplete_field = (
            'data-prefixautocompletefield'
        )
        self.data_label_suffix_autocomplete_field = (
            'data-suffixautocompletefield'
        )
        self.data_ignore = 'data-ignoreaccessibilityfix'
        self.prefix_id = configure.get_parameter('prefix-generated-ids')
        self.prefix_required_field = configure.get_parameter(
            'prefix-required-field'
        )
        self.suffix_required_field = configure.get_parameter(
            'suffix-required-field'
        )
        self.prefix_range_min_field = configure.get_parameter(
            'prefix-range-min-field'
        )
        self.suffix_range_min_field = configure.get_parameter(
            'suffix-range-min-field'
        )
        self.prefix_range_max_field = configure.get_parameter(
            'prefix-range-max-field'
        )
        self.suffix_range_max_field = configure.get_parameter(
            'suffix-range-max-field'
        )
        self.prefix_autocomplete_field = configure.get_parameter(
            'prefix-autocomplete-field'
        )
        self.suffix_autocomplete_field = configure.get_parameter(
            'suffix-autocomplete-field'
        )
        self.text_autocomplete_value_both = configure.get_parameter(
            'text-autocomplete-value-both'
        )
        self.text_autocomplete_value_list = configure.get_parameter(
            'text-autocomplete-value-list'
        )
        self.text_autocomplete_value_inline = configure.get_parameter(
            'text-autocomplete-value-inline'
        )
        self.text_autocomplete_value_none = configure.get_parameter(
            'text-autocomplete-value-none'
        )

    def _add_prefix_suffix(
        self,
        label,
        field,
        prefix,
        suffix,
        data_prefix,
        data_suffix
    ):
        """
        Display in label the information of field.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @param prefix: The prefix.
        @type prefix: str
        @param suffix: The suffix.
        @type suffix: str
        @param data_prefix: The name of prefix attribute.
        @type data_prefix: str
        @param data_suffix: The name of suffix attribute.
        @type data_suffix: str
        """

        contentLabel = field.get_attribute('aria-label')
        if prefix != '':
            label.set_attribute(data_prefix, prefix)
            if prefix not in contentLabel:
                contentLabel = prefix + ' ' + contentLabel
        if suffix != '':
            label.set_attribute(data_suffix, suffix)
            if suffix not in contentLabel:
                contentLabel = contentLabel + ' ' + suffix
        field.set_attribute('aria-label', contentLabel)

    def _fix_label_required_field(self, label, required_field):
        """
        Display in label the information if the field is required.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param required_field: The required field.
        @type required_field: L{hatemile.util.HTMLDOMElement}
        """

        if (
            (
                (required_field.has_attribute('required'))
                or (
                    (required_field.has_attribute('aria-required'))
                    and (required_field.get_attribute(
                        'aria-required'
                    ).lower() == 'true')
                )
            )
            and (required_field.has_attribute('aria-label'))
            and (not label.has_attribute(
                self.data_label_prefix_required_field
            ))
            and (not label.has_attribute(
                self.data_label_suffix_required_field
            ))
        ):
            self._add_prefix_suffix(
                label,
                required_field,
                self.prefix_required_field,
                self.suffix_required_field,
                self.data_label_prefix_required_field,
                self.data_label_suffix_required_field
            )

    def _fix_label_range_field(self, label, range_field):
        """
        Display in label the information of range of field.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param range_field: The range field.
        @type range_field: L{hatemile.util.HTMLDOMElement}
        """

        if range_field.has_attribute('aria-label'):
            if (
                (
                    range_field.has_attribute('min')
                    or range_field.has_attribute('aria-valuemin')
                )
                and (not label.has_attribute(
                    self.data_label_prefix_range_min_field
                ))
                and (not label.has_attribute(
                    self.data_label_suffix_range_min_field
                ))
            ):
                if range_field.has_attribute('min'):
                    value = range_field.get_attribute('min')
                else:
                    value = range_field.get_attribute('aria-valuemin')
                self._add_prefix_suffix(
                    label,
                    range_field,
                    re.sub(
                        '{{value}}',
                        value,
                        self.prefix_range_min_field
                    ),
                    re.sub(
                        '{{value}}',
                        value,
                        self.suffix_range_min_field
                    ),
                    self.data_label_prefix_range_min_field,
                    self.data_label_suffix_range_min_field
                )
            if (
                (
                    range_field.has_attribute('max')
                    or range_field.has_attribute('aria-valuemax')
                )
                and (not label.has_attribute(
                    self.data_label_prefix_range_max_field
                ))
                and (not label.has_attribute(
                    self.data_label_suffix_range_max_field
                ))
            ):
                if range_field.has_attribute('max'):
                    value = range_field.get_attribute('max')
                else:
                    value = range_field.get_attribute('aria-valuemax')
                self._add_prefix_suffix(
                    label,
                    range_field,
                    re.sub(
                        '{{value}}',
                        value,
                        self.prefix_range_max_field
                    ),
                    re.sub(
                        '{{value}}',
                        value,
                        self.suffix_range_max_field
                    ),
                    self.data_label_prefix_range_max_field,
                    self.data_label_suffix_range_max_field
                )

    def _fix_label_autocomplete_field(self, label, autocomplete_field):
        """
        Display in label the information if the field has autocomplete.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param autocomplete_field: The autocomplete field.
        @type autocomplete_field: L{hatemile.util.HTMLDOMElement}
        """

        prefixAutoCompleteFieldModified = ''
        suffixAutoCompleteFieldModified = ''
        if (
            (autocomplete_field.has_attribute('aria-label'))
            and (not label.has_attribute(
                self.data_label_prefix_autocomplete_field
            ))
            and (not label.has_attribute(
                self.data_label_suffix_autocomplete_field
            ))
        ):
            ariaAutocomplete = self._get_aria_autocomplete(autocomplete_field)
            if ariaAutocomplete is not None:
                if ariaAutocomplete == 'both':
                    if self.prefix_autocomplete_field != '':
                        prefixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.text_autocomplete_value_both,
                            self.prefix_autocomplete_field
                        )
                    if self.suffix_autocomplete_field != '':
                        suffixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.text_autocomplete_value_both,
                            self.suffix_autocomplete_field
                        )
                elif ariaAutocomplete == 'none':
                    if self.prefix_autocomplete_field != '':
                        prefixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.text_autocomplete_value_none,
                            self.prefix_autocomplete_field
                        )
                    if self.suffix_autocomplete_field != '':
                        suffixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.text_autocomplete_value_none,
                            self.suffix_autocomplete_field
                        )
                elif ariaAutocomplete == 'list':
                    if self.prefix_autocomplete_field != '':
                        prefixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.text_autocomplete_value_list,
                            self.prefix_autocomplete_field
                        )
                    if self.suffix_autocomplete_field != '':
                        suffixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.text_autocomplete_value_list,
                            self.suffix_autocomplete_field
                        )
                self._add_prefix_suffix(
                    label,
                    autocomplete_field,
                    prefixAutoCompleteFieldModified,
                    suffixAutoCompleteFieldModified,
                    self.data_label_prefix_autocomplete_field,
                    self.data_label_suffix_autocomplete_field
                )

    def _get_aria_autocomplete(self, field):
        """
        Returns the appropriate value for attribute aria-autocomplete of field.
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @return: The ARIA value of field.
        @rtype: str
        """

        tagName = field.get_tag_name()
        inputType = None
        if field.has_attribute('type'):
            inputType = field.get_attribute('type').lower()
        if (
            (tagName == 'TEXTAREA')
            or (
                (tagName == 'INPUT')
                and (not (
                    ('button' == inputType)
                    or ('submit' == inputType)
                    or ('reset' == inputType)
                    or ('image' == inputType)
                    or ('file' == inputType)
                    or ('checkbox' == inputType)
                    or ('radio' == inputType)
                    or ('hidden' == inputType)
                ))
            )
        ):
            value = None
            if field.has_attribute('autocomplete'):
                value = field.get_attribute('autocomplete').lower()
            else:
                form = self.parser.find(field).find_ancestors(
                    'form'
                ).first_result()
                if (form is None) and (field.has_attribute('form')):
                    form = self.parser.find(
                        '#' + field.get_attribute('form')
                    ).first_result()
                if (form is not None) and (form.has_attribute('autocomplete')):
                    value = form.get_attribute('autocomplete').lower()
            if 'on' == value:
                return 'both'
            elif (
                (field.has_attribute('list'))
                and (self.parser.find(
                    'datalist[id="' + field.get_attribute('list') + '"]'
                ).first_result() is not None)
            ):
                return 'list'
            elif 'off' == value:
                return 'none'
        return None

    def _get_labels(self, field):
        """
        Returns the labels of field.
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @return: The labels of field.
        @rtype: array.L{hatemile.util.HTMLDOMElement}
        """

        labels = None
        if field.has_attribute('id'):
            labels = self.parser.find(
                'label[for="' + field.get_attribute('id') + '"]'
            ).list_results()
        if (labels is None) or (len(labels) == 0):
            labels = self.parser.find(field).find_ancestors(
                'label'
            ).list_results()
        return labels

    def fix_required_field(self, required_field):
        if required_field.has_attribute('required'):
            required_field.set_attribute('aria-required', 'true')

            labels = self._get_labels(required_field)
            for label in labels:
                self._fix_label_required_field(label, required_field)

    def fix_required_fields(self):
        requiredFields = self.parser.find('[required]').list_results()
        for requiredField in requiredFields:
            if not requiredField.has_attribute(self.data_ignore):
                self.fix_required_field(requiredField)

    def fix_range_field(self, range_field):
        if range_field.has_attribute('min'):
            range_field.set_attribute(
                'aria-valuemin',
                range_field.get_attribute('min')
            )
        if range_field.has_attribute('max'):
            range_field.set_attribute(
                'aria-valuemax',
                range_field.get_attribute('max')
            )
        labels = self._get_labels(range_field)
        for label in labels:
            self._fix_label_range_field(label, range_field)

    def fix_range_fields(self):
        rangeFields = self.parser.find('[min],[max]').list_results()
        for rangeField in rangeFields:
            if not rangeField.has_attribute(self.data_ignore):
                self.fix_range_field(rangeField)

    def fix_autocomplete_field(self, autocomplete_field):
        ariaAutoComplete = self._get_aria_autocomplete(autocomplete_field)
        if ariaAutoComplete is not None:
            autocomplete_field.set_attribute(
                'aria-autocomplete',
                ariaAutoComplete
            )

            labels = self._get_labels(autocomplete_field)
            for label in labels:
                self._fix_label_autocomplete_field(label, autocomplete_field)

    def fix_autocomplete_fields(self):
        elements = self.parser.find(
            'input[autocomplete],textarea[autocomplete],'
            + 'form[autocomplete] input,form[autocomplete] textarea,'
            + '[list],[form]'
        ).list_results()
        for element in elements:
            if not element.has_attribute(self.data_ignore):
                self.fix_autocomplete_field(element)

    def fix_label(self, label):
        if label.get_tag_name() == 'LABEL':
            if label.has_attribute('for'):
                field = self.parser.find(
                    '#' + label.get_attribute('for')
                ).first_result()
            else:
                field = self.parser.find(label).find_descendants(
                    'input,select,textarea'
                ).first_result()

                if field is not None:
                    CommonFunctions.generate_id(field, self.prefix_id)
                    label.set_attribute('for', field.get_attribute('id'))
            if field is not None:
                if not field.has_attribute('aria-label'):
                    field.set_attribute(
                        'aria-label',
                        re.sub(
                            '[ \n\r\t]+',
                            ' ',
                            label.get_text_content().strip()
                        )
                    )

                self._fix_label_required_field(label, field)
                self._fix_label_range_field(label, field)
                self._fix_label_autocomplete_field(label, field)

                CommonFunctions.generate_id(label, self.prefix_id)
                field.set_attribute(
                    'aria-labelledby',
                    CommonFunctions.increase_in_list(
                        field.get_attribute('aria-labelledby'),
                        label.get_attribute('id')
                    )
                )

    def fix_labels(self):
        labels = self.parser.find('label').list_results()
        for label in labels:
            if not label.has_attribute(self.data_ignore):
                self.fix_label(label)
