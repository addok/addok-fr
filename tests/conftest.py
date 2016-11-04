def pytest_configure():
    from addok import hooks
    import addok_fr
    hooks.register(addok_fr)
