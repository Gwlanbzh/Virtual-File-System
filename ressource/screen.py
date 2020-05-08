""" Module de contrôle du terminal

    Utilisation :

        import screen

        screen.clear()
            pour effacer tous les caractères de l'écran

        screen.setpos(i, j)
            pour positionner le curseur du terminal en position (i, j)
            Le nombre de lignes du terminal est défini par screen.ROWS.
            Le nombre de colonnes du terminal est défini par screen.COLS.
            0 <= i < screen.ROWS
            0 <= j < screen.COLS
            Par exemple :
                screen.setpos(6, 10) écrit les caractères `\x1b[7;11W`

        screen.write(text)
            pour écrire le str text dans le terminal
            Pour des raisons de performance, les caractères ne sont pas
            envoyés au terminal mais mis dans une mémoire tampon
            (buffer en anglais).
            Le contenu du buffer est envoyé vers le terminal par
            la fonction screen.flush().

        screen.flush()
            pour vider le buffer d'écriture

        screen.write(screen.BLUE)
            permet ensuite d'écrire en bleu
            screen.BLUE est défini comme étant égal à '\x1b[38;5;12m'

        screen.write(screen.BLUEBG)
            permet ensuite d'écrire sur un fond bleu

        screen.write(screen.ITALIC)
            permet ensuite d'écrire en italique

        screen.write(screen.DEFAULT)
            restaure les valeurs par défaut du mode d'écriture

        screen.hidecursor()
            pour cacher le curseur du terminal
            Équivalent à screen.write('\x1b[?25l')

        screen.showcursor()
            pour rendre visible le curseur du terminal

        settings = screen.savescreen()
            pour mémoriser la configuration actuelle du terminal
            et configurer le terminal en mode graphisme :
                pas d'écho, pas de scroll, lecture caractère par caractère.
            Cette fonction est à exécuter au début du programme.

        screen.restorescreen(settings)
            pour restaurer la configuration sauvegardée.
            Si le programme s'interrompt en raison d'une erreur,
            cette fonction ne sera pas exécuter et le terminal
            peut ainsi se retrouver dans un état non souhaitable.
            Dans ce cas, exécuter la commande reset pour restaurer
            le terminal.

        ch = screen.getch()
            Lit un unique caractère ou bien une séquence d'échappement
            sur l'entrée standard

            Lors de l'appui sur certaines touches spéciales, la fonction
            ne retourne pas un unique caractère, mais une suite de caractères
            qui débute par le caractère ÉCHAPPEMENT (\x1b) :

            Flèche vers le haut   : '\x1b[A'
            Flèche vers le bas    : '\x1b[B'
            Flèche vers la gauche : '\x1b[D'
            Flèche vers la droite : '\x1b[C'
            Page vers le haut     : '\x1b[5~'
            Page vers le bas      : '\x1b[6~'
            Touche SUPPR          : '\x1b[3~'

    Constantes prédéfinies :

        screen.ROWS             nombre de lignes du terminal
        screen.COLORS           nombre de colonnes du terminal

        Séquences d'échappement pour modifier les propriétés du curseur

        En envoyant la séquence de caractères '\x1b[38;5;12m'
        les caractères envoyés ensuites seront écrits en bleu.
        Plutôt que de devoir écrire screen.write('\x1b[38;5;12m')
        le module définit la constante screen.BLUE = '\x1b[38;5;12m'
        de sorte que l'on peut écrire plus clairement
        screen.write(screen.BLUE)

        Couleurs prédéfinies :

            screen.DEFAULT          Couleur par défaut du terminal
            screen.RED              Rouge
            screen.GREEN            Vert
            screen.YELLOW           Jaune
            screen.BLUE             Bleu
            screen.MAGENTA          Magenta
            screen.CYAN             Cyan
            screen.WHITE            Blanc
            screen.LIGHTGRAY        Gris clair
            screen.DARKGRAY         Gris foncé

            screen.REDBG            Fond rouge
            screen.GREENBG          Fond vert
            screen.YELLOWBG         Fond jaune
            screen.BLUEBG           Fond bleu
            screen.MAGENTABG        Fond magenta
            screen.CYANBG           Fond cyan
            screen.WHITEBG          Fond blanc
            screen.LIGHTGRAYBG      Fond gris clair
            screen.DARKGRAYBG       Fond gris foncé

        Outre la couleur, il est possible de modifier d'autres
        attributs du curseur.
        Par exemple en envoyant la séquence de caractères '\x1b[1m'
        les caractères envoyés ensuites seront écrits en gras.
        screen.BOLD est défini comme étant égal à '\x1b[1m'.

        Constantes d'attributs prédéfinies :

            screen.BOLD             Gras
            screen.FAINT            Faible
            screen.ITALIC           Italique
            screen.UNDERLINE        Souligné
            screen.BLINK            Clignotant
            screen.REVERSEVIDEO     Inverse vidéo
            screen.CROSSED          Barré
            screen.NOFAINT          Supprime l'attribut faible
            screen.NOITALIC         Supprime l'attribut italique
            screen.NOUNDERLINE      Supprime l'attribut souligné
            screen.NOBLINK          Supprime l'attribut clignotant
            screen.NOREVERSEVIDEO   Supprime l'attribut inverse vidéo
            screen.NOCROSSED        Supprime l'attribut barré

        Séquences d'échappement retournées par la fonction screen.getch
        lors de la frappe de touches spéciales :

        screen.KEYBACKSPACE         Touche Retour arrière
        screen.KEYUP                Flèche vers le haut
        screen.KEYDOWN              Flèche vers le bas
        screen.KEYLEFT              Flèche gauche
        screen.KEYRIGHT             Flèche droite
        screen.KEYPAGEUP            Touche Page vers le haut
        screen.KEYPAGEDOWN          Touche Page vers le bas
        screen.KEYSUPPR             Touche Suppression

        Par exemple avec l'instruction ch = screen.getch()
        si l'utilisateur appuie sur la flèche gauche,
        la variable ch vaudra screen.KEYLEFT.
        screen.KEYLEFT est égal au str '\x1b[D' mais en utilisant
        screen.KEYLEFT vous n'avez pas besoin de vous en préocupper.

    La fin du module contient un mini exemple d'utilisation des
    fonctions. Pour tester l'exemple, exécuter dans un terminal
    la commande : python screen.py
"""


import sys
import os
import termios


#  CONSTANTES _________________________________________________________________

# Nombre de lignes (ROWS) et nombre de colonnes (COLS) du terminal
ROWS, COLS = map(int, os.popen("stty size", "r").read().split())

DEFAULT = "\x1b[0m"
RED = "\x1b[38;5;9m"
GREEN = "\x1b[38;5;10m"
YELLOW = "\x1b[38;5;11m"
BLUE = "\x1b[38;5;12m"
MAGENTA = "\x1b[38;5;13m"
CYAN = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
LIGHTGRAY = "\x1b[38;5;7m"
DARKGRAY = "\x1b[38;5;8m"
ORANGE = "\x1b[38:5:208m"

REDBG = "\x1b[48;5;9m"
GREENBG = "\x1b[48;5;10m"
YELLOWBG = "\x1b[48;5;11m"
BLUEBG = "\x1b[48;5;12m"
MAGENTABG = "\x1b[48;5;13m"
CYANBG = "\x1b[48;5;14m"
WHITEBG = "\x1b[348;5;15m"
LIGHTGRAYBG = "\x1b[48;5;7m"
DARKGRAYBG = "\x1b[48;5;8m"

# Codes ANSI des attributs du curseur
BOLD = "\x1b[1m"
FAINT = "\x1b[2m"
ITALIC = "\x1b[3m"
UNDERLINE = "\x1b[4m"
BLINK = "\x1b[5m"
REVERSEVIDEO = "\x1b[7m"
CROSSED = "\x1b[9m"
NOFAINT = "\x1b[22m"
NOITALIC = "\x1b[23m"
NOUNDERLINE = "\x1b[24m"
NOBLINK = "\x1b[25m"
NOREVERSEVIDEO = "\x1b[27m"
NOCROSSED = "\x1b[29m"

# Touches spéciales
KEYBACKSPACE = "\x7f"
KEYUP = "\x1b[A"
KEYDOWN = "\x1b[B"
KEYLEFT = "\x1b[D"
KEYRIGHT = "\x1b[C"
KEYPAGEUP = "\x1b[5~"
KEYPAGEDOWN = "\x1b[6~"
KEYSUPPR = "\x1b[3~"

SPECIALKEYS = (
    KEYBACKSPACE,
    KEYUP,
    KEYDOWN,
    KEYLEFT,
    KEYRIGHT,
    KEYPAGEUP,
    KEYPAGEDOWN,
    KEYSUPPR,
)


#  FONCTIONS __________________________________________________________________


def getch() -> str:
    """ Lit un caractère ou une séquence d'échappement sur l'entrée standard

        Lors de l'appui sur certaines touches spéciales, la fonction
        ne retourne pas un unique caractère, mais une suite de caractères
        qui débute par le caractère ÉCHAPPEMENT (\x1b) :

        Flèche vers le haut   : '\x1b[A'
        Flèche vers le bas    : '\x1b[B'
        Flèche vers la gauche : '\x1b[D'
        Flèche vers la droite : '\x1b[C'
        Page vers le haut     : '\x1b[5~'
        Page vers le bas      : '\x1b[6~'
        Touche SUPPR          : '\x1b[3~'
    """
    while True:
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            sequences = [
                KEYUP,
                KEYDOWN,
                KEYLEFT,
                KEYRIGHT,
                KEYPAGEUP,
                KEYPAGEDOWN,
                KEYSUPPR,
            ]
            sequences = [x[1:] for x in sequences]
            chs = ch
            while len(sequences) > 0:
                ch = sys.stdin.read(1)
                sequences = [x[1:] for x in sequences if x.startswith(ch)]
                chs = chs + ch
                if len(sequences) == 1 and len(sequences[0]) == 0:
                    return chs
        else:
            return ch


def write(text: str) -> None:
    sys.stdout.write(text)


def flush() -> None:
    sys.stdout.flush()


def clear() -> None:
    """ Efface tous les caractères affichés dans le terminal.
    """
    write("\x1b[2J")


def setpos(i: int, j: int) -> None:
    """ Positionne le curseur sur la i-ième ligne et la j-ième colonne.
        Les lignes et les colonnes sont numérotés à partir de 0.
        La dernière ligne est ROWS - 1.
        La dernière colonne a COLS - 1.
    """
    write("\x1b[" + str(i + 1) + ";" + str(j + 1) + "H")


def hidecursor() -> None:
    """ Rend le curseur invisible
    """
    write("\x1b[?25l")


def showcursor() -> None:
    """ Rend le curseur visible
    """
    write("\x1b[?25h")


def savescreen() -> None:
    """ Sauvegarde l'affichage actuel du terminal afin
        qu'il puisse être restauré par la fonction restorescreen.
        Configure le terminal en mode graphisme :
            pas d'écho, pas de scroll, lecture caractère par caractère.
    """
    write("\x1b[?1049h\x1b[H")
    flush()
    settings = termios.tcgetattr(0)
    new_settings = settings.copy()
    new_settings[3] &= ~termios.ICANON
    new_settings[3] &= ~termios.ECHO
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    return settings


def restorescreen(settings: list) -> None:
    """ Restaure l'affichage du terminal sauvegardé par
        la fonction restorescreen.
    """
    termios.tcsetattr(0, termios.TCSANOW, settings)
    write("\x1b[?1049l")
    flush()


# PROGRAMME PRINCIPAL _________________________________________________________

if __name__ == "__main__":

    settings = savescreen()
    hidecursor()
    clear()

    while True:
        setpos(10, 10)
        write("Appuyer sur une des touches r, g, b ou q")
        flush()
        ch = getch()
        if ch == "r":
            write(RED)
        elif ch == "g":
            write(GREEN)
        elif ch == "b":
            write(BLUE)
        elif ch == "q":
            break

    showcursor()
    restorescreen(settings)
