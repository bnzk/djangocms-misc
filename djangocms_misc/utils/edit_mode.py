

def is_edit_mode(toolbar):
    if (getattr(toolbar, 'edit_mode', None) or  # cms pre 3.6
        getattr(toolbar, 'edit_mode_active', None)  # cms 3.6+
    ):
        return True
    return False


def is_edit_or_build_mode(toolbar):
    if (getattr(toolbar, 'edit_mode', None) or  # cms pre 3.6
        getattr(toolbar, 'edit_mode_active', None) or  # cms 3.6+
        getattr(toolbar, 'build_mode', None) or
        getattr(toolbar, 'build_mode_active', None)
    ):
        return True
    return False
