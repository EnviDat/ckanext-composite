import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.composite import validators, helpers

class CompositePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'composite')

    # IValidators
    def get_validators(self):
        return { "composite_group2json": validators.composite_group2json ,
                 "composite_group2json_output": validators.composite_group2json_output,
                 "composite_repeating_group2json":validators.composite_repeating_group2json }

    # ITemplateHelpers
    def get_helpers(self):
        return { 'composite_get_as_dict': helpers.composite_get_as_dict,
                 'composite_get_value_dict': helpers.composite_get_value_dict,
                 'composite_get_label_dict': helpers.composite_get_label_dict,
                 'composite_get_choices_dict': helpers.composite_get_choices_dict,
                 'composite_get_name_list': helpers.composite_get_name_list,
                 'composite_repeating_get_value_dict_list': helpers.composite_repeating_get_value_dict_list,
                 'composite_is_mail': helpers.composite_is_mail }
