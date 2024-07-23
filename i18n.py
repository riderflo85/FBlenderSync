FR = (
    ('Drb-App-Key', 'Clé publique de votre application Dropbox.'),
    ('Drb-App-Secret', 'Clé secrète de votre application Dropbox.'),
    ('Pref-Header-Inputs', 'Entrez vous clés secrètes que vous pouvez retrouvez sur votre compte Dropbox.'),
    ('Pref-Download-Mode', 'Mode de téléchargement des fichiers cloud.'),
    ('Local-Storage-Folder', 'Dossier dans lequel sera téléchargé vos fichiers de votre cloud.'),
    ('Bt-Label-Login', 'Connexion à l\'API Dropbox.'),
    ('Bt-Save-Settings', 'Enregistrer'),
    ('FB-Success-Write-Pref', 'Enregistrement du profil avec succès !'),
    ('Ms-Not-Token', 'Application Dropbox pas encore connectée.'),
    ('Ms-Valide-Token', 'Votre token est encore valide.'),
    ('Ms-Expired-Token', 'Votre token est expiré.'),
    ('Ms-Token-Expires-In', 'Expiration du token le'),
    ('Ms-Token-Expires-Out', 'Votre token a expiré le'),
    ('FMRI-DRB-desc', 'Le fichier est plus récent sur Dropbox.'),
    ('FMRI-Local-desc', 'Le fichier est plus récent sur cet ordinateur.'),
    ('FMRI-MissingLocal-desc', 'Le fichier n\'est pas présent sur cet ordinateur.'),
    ('DM-Store-name', 'Téléchargé.'),
    ('DM-Store-desc', 'Le ficher sera téléchargé.'),
    ('DM-StoreOpen-name', 'Téléchargé et ouvert.'),
    ('DM-StoreOpen-desc', 'Le ficher sera téléchargé et ouvert.'),
)

EN = (
    ('FMRI-DRB-desc', 'The file is more recent on Dropbox.'),
    ('FMRI-Local-desc', 'The file is more recent on this computer.'),
    ('FMRI-MissingLocal-desc', 'The file is not present on this computer.'),
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
