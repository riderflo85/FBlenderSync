FR = (
    ('Drb-App-Key', 'Clé publique de votre application Dropbox.'),
    ('Drb-App-Secret', 'Clé secrète de votre application Dropbox.'),
    ('Pref-Header-Inputs', 'Entrez vous clés secrètes que vous pouvez retrouvez sur votre compte Dropbox.'),
    ('Local-Storage-Folder', 'Dossier dans lequel sera téléchargé vos fichiers de votre cloud.'),
    ('Bt-Label-Login', 'Connexion à l\'API Dropbox.'),
    ('Bt-Save-Settings', 'Enregistrer'),
    ('FB-Success-Write-Pref', 'Enregistrement du profil avec succès !'),
    ('Ms-Not-Token', 'Application Dropbox pas encore connectée.'),
    ('Ms-Valide-Token', 'Votre token est encore valide.'),
    ('Ms-Token-Expires-In', 'Expiration du token le'),
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
