from cms.models import Page
from cms.test_utils.testcases import CMSTestCase
from cms.utils.urlutils import admin_reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client, modify_settings
from django.utils.http import urlencode

from djangocms_misc.tests.test_app.cms_plugins import TestPlugin


@modify_settings(INSTALLED_APPS={
    'append': 'djangocms_misc.autopublisher',
})
class AutoPublisherTestCase(TestCase):
    password = "123"
    def setUp(self):
        super().setUp()
        self.client = Client()
        # self._admin_user = self.get_superuser()
        self._admin_user = User.objects.create_superuser(username='admin', email=None, password=self.password)

    def tearDown(self):
        pass

    def test_save_page(self):
        from cms import api as cms_api
        page = cms_api.create_page('test', 'base.html', 'en', reverse_id='what')
        page.publish('en')
        page.reverse_id = 'lucky'
        title_obj = page.get_title_obj('en')
        title_obj.title = 'dummy'
        title_obj.save()
        self.assertEqual(page.publisher_is_draft, True)
        # public_obj = page.get_public_object()
        # TODO: this isnt working yet!? normaly, a page is saved with a title. works via frontend, though!?
        # so when using the cms via frontend it works.
        # self.assertEqual(public_obj.reverse_id, 'lucky')

    def test_save_title(self):
        from cms import api as cms_api
        page = cms_api.create_page('test', 'base.html', 'en')
        page.publish('en')
        title = page.get_title_obj('en')
        title.title = 'another'
        title.save()
        self.assertEqual(page.publisher_is_draft, True)
        self.assertEqual(page.get_public_object().get_title_obj('en').title, 'another')
        pass

    def test_add_save_plugin(self):
        from cms import api as cms_api
        page = cms_api.create_page('test', 'base.html', 'en')
        page.publish('en')
        placeholder = page.placeholders.get(slot='translated_placeholder')
        plugin = cms_api.add_plugin(placeholder, TestPlugin, 'en', field1='teststring')
        # public_obj = page.get_public_object()
        response = self.client.get(page.get_absolute_url())
        self.assertRegexpMatches(str(response.content), "teststring")
        plugin.field1 = "another test"
        plugin.save()
        # TODO: inconsistency, publish should not be needed, but appearently, dirty state is not applied when saving
        # a plugin with save() only.
        page.publish('en')
        response = self.client.get(page.get_absolute_url())
        self.assertRegexpMatches(str(response.content), "another test")

    def test_move_plugin(self):
        from cms import api as cms_api
        page = cms_api.create_page('test', 'base.html', 'en')
        page.publish('en')
        placeholder = page.placeholders.get(slot='translated_placeholder')
        plugin1 = cms_api.add_plugin(placeholder, TestPlugin, 'en', field1='teststring')
        plugin2 = cms_api.add_plugin(placeholder, TestPlugin, 'en', field1='teststring2')
        uri = self.get_move_plugin_uri(
            plugin1,
            page,
            'en',
        )
        data = {
            'plugin_id': plugin1.id,
            'target_language': 'en',
            'placeholder_id': placeholder.id,
            'plugin_order': [plugin2.id, plugin1.id, ],
        }
        # with self.login_user_context(self._admin_user):
        #     response = self.client.post(uri, data)
        #     self.assertEqual(response.status_code, 200)
        self.client.force_login(self._admin_user)
        response = self.client.post(uri, data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(page.get_absolute_url())
        # helps debugging, when plugin output might have change slightly!
        # print(response.content)
        self.assertContains(response, '''<div>
    testplugin content: teststring2
</div><div>
    testplugin content: teststring
</div>
''')

    def get_admin_url(self, model, action, *args):
        opts = model._meta
        url_name = f"{opts.app_label}_{opts.model_name}_{action}"
        return admin_reverse(url_name, args=args)

    def get_move_plugin_uri(self, plugin, container=None, language=None):
        container = container or Page
        language = language or 'en'

        if plugin.page:
            path = plugin.page.get_absolute_url(language) or f'/{language}/'
        else:
            path = f'/{language}/'

        endpoint = self.get_admin_url(container, 'move_plugin')
        endpoint += '?' + urlencode({'cms_path': path})
        return endpoint

    def test_move_page(self):
        pass

    def test_save_static_placeholder_plugin(self):
        pass

    def test_move_static_placeholder_plugin(self):
        pass
