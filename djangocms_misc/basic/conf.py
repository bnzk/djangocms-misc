from appconf import AppConf


# TODO: dont need a that complex one for default
class UntranslatedPlaceholderConf(AppConf):
    GET_FROM_PAGE_CONTENT = {
        'video_id': {
            'placeholders': ('Inhalt',),
            'plugins': {
                'YoutubeVideoPlugin': ['video_id'],
            }
        },
        'image': {
            'placeholders': ('Inhalt', ),
            'plugins': {
                'ImagePlugin': ('image', 'preview_image'),
                'HeaderPlugin': ('image', ),
            }
        },
        'text': {
            'placeholders': ('Inhalt',),
            'plugins': {
                'ImagePlugin': ('image', 'preview_image'),
                'HeaderPlugin': ('image',),
            }
        },
    }

    class Meta:
        prefix = 'djangocms_misc'
