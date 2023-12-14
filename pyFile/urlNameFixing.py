from os import path

def nameFixing(filePath):
    
    turkish_to_ascii = {
        'ı': 'i',
        'ö': 'o',
        'ü': 'u',
        'ğ': 'g',
        'ş': 's',
        'ç': 'c',
        'İ': 'I',
        'Ö': 'O',
        'Ü': 'U',
        'Ğ': 'G',
        'Ş': 'S',
        'Ç': 'C'
    }

    filePath = filePath.split("\\")[-1].lower().strip()

    fileName, uzanti = path.splitext(filePath)

    forbidden_symbols = [' ', '/', '.', '..', '\\', '?', '=', '&']
    non_ascii_characters = [chr(i) for i in range(128, 256)] + list(turkish_to_ascii.keys())
    invalid_characters = forbidden_symbols + non_ascii_characters

    for character in fileName:

        if character in invalid_characters:

            if character in turkish_to_ascii.keys():

                fileName = fileName.replace(character,turkish_to_ascii.get(character))
            
            else:

                fileName = fileName.replace(character,"_")

    return f"{fileName}{uzanti}"