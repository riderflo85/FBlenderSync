FR = (
    ('Drb-App-Key', 'Clé publique de votre application Dropbox.'),
    ('Drb-App-Secret', 'Clé secrète de votre application Dropbox.'),
    ('Pref-Header-Inputs', 'Entrez vous clés secrètes que vous pouvez retrouvez sur votre compte Dropbox.'),
    ('Local-Storage-Folder', 'Dossier dans lequel sera téléchargé vos fichiers de votre cloud.'),
    ('Bl-Label-Login', 'Connexion à l\'API Dropbox.'),
)


def get_label(tag: str) -> str:
    """Return the text matching with tag.

    Args:
        tag (str): dict tag to find text.

    Returns:
        str: text label.
    """
    label = 'Label not found'
    for translate in FR:
        if tag in translate:
            label = translate[1]
    
    return label