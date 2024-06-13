#!/bin/bash

# Create by Florent Grenaille
# Create a .zip archive for install addon with Blender settings UI !

FILES=(__init__.py preference.py profiles.py statics.py i18n.py mixins.py menu.py history.py)
FOLDERS=(server helpers settings)
EXCLUDED_FILES=()

SOURCE_CODE_PATH=code
ARCHIVE_PATH=fblender_sync
ARCHIVE_NAME=fblender_sync.zip


function remove-archive {
    rm -rf $ARCHIVE_PATH
    rm $ARCHIVE_NAME
}


function create-archive {
    mkdir $ARCHIVE_PATH

    for file in "${FILES[@]}"
    do
        cp $SOURCE_CODE_PATH/$file $ARCHIVE_PATH
    done

    for folder in "${FOLDERS[@]}"
    do
        cp -r $SOURCE_CODE_PATH/$folder $ARCHIVE_PATH
    done

    for ex_file in "${EXCLUDED_FILES[@]}"
    do
        rm $ARCHIVE_PATH/$ex_file
    done

    zip -r "$ARCHIVE_NAME" "$ARCHIVE_PATH"
    rm -rf $ARCHIVE_PATH
}


cd ..

if test -f "$ARCHIVE_NAME"; then
    remove-archive
fi

create-archive
