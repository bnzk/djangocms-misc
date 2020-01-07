# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model, get_permission_codename
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from cms.utils.urlutils import admin_reverse
from cms.toolbar_pool import toolbar_pool
from cms.cms_toolbars import BasicToolbar, ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK

from djangocms_misc.utils.edit_mode import is_edit_or_build_mode

USER_MENU_IDENTIFIER = 'user-menu'
CLIPBOARD_MENU_IDENTIFIER = 'clipboard-menu'


toolbar_pool.unregister(BasicToolbar)


@toolbar_pool.register
class AlternateBasicToolbar(BasicToolbar):

    def populate(self):
        # still dont know why this if!?
        if not self.page:
            self.init_from_request()
            self.clipboard = self.request.toolbar.user_settings.clipboard
            self.add_user_menu()
            self.add_admin_menu()
            self.add_clipboard_menu()
            self.add_language_menu()

    def add_user_menu(self):
        # menu
        self.user_menu = self.toolbar.get_or_create_menu(
            USER_MENU_IDENTIFIER,
            _('User'),
            position=0,
        )
        # buttons / items
        self.user_menu.add_sideframe_item(
            _("Change Password"),
            url=admin_reverse('password_change'),
        )
        self.user_menu.add_sideframe_item(
            _('User settings'),
            url=admin_reverse('cms_usersettings_change'),
        )
        self.add_logout_button(self.user_menu)

    def add_admin_menu(self):
        # menu
        self.admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER,
            _('Administration'),
            position=1,
        )
        # buttons / items (pages are added automagically, in PageToolbar!)
        if 'filer' in settings.INSTALLED_APPS:
            self.admin_menu.add_sideframe_item(
                _('Files'),
                url=admin_reverse('filer_folder_changelist')
            )
        # in between
        self.add_more_admin_menu_items()
        # end
        self.admin_menu.add_break(ADMINISTRATION_BREAK, position=199)
        self.add_user_group_button(self.admin_menu, position=200)
        self.admin_menu.add_sideframe_item(
            _('Administration'),
            url=admin_reverse('index'),
            position=200
        )

    # override
    def add_more_admin_menu_items(self):
        pass

    def add_user_group_button(self, parent, position=200):
        User = get_user_model()
        if User in admin.site._registry:
            opts = User._meta
            if self.request.user.has_perm(
                    '%s.%s' % (opts.app_label, get_permission_codename('change', opts))):
                user_group_changelist_url = admin_reverse(
                    'app_list', args=(opts.app_label, ))
                parent.add_sideframe_item(
                    _('Users & Groups'),
                    url=user_group_changelist_url,
                    position=position
                )

    def add_clipboard_menu(self):
        # menu
        self.clipboard_menu = self.toolbar.get_or_create_menu(
            CLIPBOARD_MENU_IDENTIFIER,
            _('Clipboard'),
            position=-1,
        )
        # buttons / items
        # if self.toolbar.edit_mode or getattr(self.toolbar, 'build_mode', None):
        # new, testing for preventing a recursion error!
        if (is_edit_or_build_mode(self)
            and getattr(self.request, 'current_page', None)
        ):
            # True if the clipboard exists and there's plugins in it.
            if getattr(self, 'get_clipboard_plugins', None):
                # cms up to 4.4.6
                if getattr(self, 'clipboard_plugin_prevent_recursion', None):
                    # recursive loop, when empty clipboard?!
                    clipboard_is_bound = False
                else:
                    self.clipboard_plugin_prevent_recursion = True
                    clipboard_is_bound = self.get_clipboard_plugins().exists()
            else:
                clipboard_is_bound = self.toolbar.clipboard_plugin
            self.clipboard_menu.add_link_item(
                _('Clipboard...'),
                url='#',
                extra_classes=['cms-clipboard-trigger'],
                disabled=not clipboard_is_bound,
            )
            self.clipboard_menu.add_link_item(
                _('Clear clipboard'),
                url='#',
                extra_classes=['cms-clipboard-empty'],
                disabled=not clipboard_is_bound,
            )
