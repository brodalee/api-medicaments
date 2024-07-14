def french_boolean_to_real_boolean(fake_boolean: str) -> bool:
    if fake_boolean.lower() == 'oui':
        return True

    return False


def translate_generic_group_type(code_type: int) -> str:
    types = ["princeps", "générique", "génériques par complémentarité posologique", "générique substituable"]
    return types[code_type]
