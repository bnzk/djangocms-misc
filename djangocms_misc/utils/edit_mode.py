

def is_edit_mode(toolbar):
    if (getattr(toolbar, 'edit_mode', None)  # cms pre 3.6
        or getattr(toolbar, 'edit_mode_active', None)  # cms 3.6+
    ):
        return True
    return False


def is_edit_or_build_mode(toolbar):
    if (getattr(toolbar, 'edit_mode', None)  # cms pre 3.6
        or getattr(toolbar, 'edit_mode_active', None)  # noqa cms 3.6+
        or getattr(toolbar, 'build_mode', None)  # noqa
        or getattr(toolbar, 'build_mode_active', None)  # noqa
    ):
        return True
    return False
