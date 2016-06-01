import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.composite.validators import composite_group2json

class CompositePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'composite')

    # IValidators
    def get_validators(self):
        return {"composite_group2json": composite_group2json}
