from dataclasses import dataclass, field
from typing import Optional

import xml.etree.ElementTree as ElementTree


#-------------------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------------------

@dataclass
class GameFile(object):
    name: str
    hashes: dict[str, str] = field(default_factory=dict)
    size: int = 0
    status: Optional[str] = None


@dataclass
class Game(object):
    name: str
    files: list[GameFile] = field(default_factory=list)


class DatFile(object):
    def __init__(self, filename: str):
        self._games: list[Game] = []
        self._load(filename)

    #---------------------------------------------------------------------------
    # Public Methods
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # Private Methods
    #---------------------------------------------------------------------------

    def _load(self, filename: str):
        for child in ElementTree.parse(filename).getroot():
            if child.tag == 'header':
                self._name = child.findall('name')[0].text
                self._description = child.findall('description')[0].text
                self._version = child.findall('version')[0].text
            elif child.tag == 'game':
                game = Game(child.attrib['name'])

                for entry in child:
                    if entry.tag == 'rom':
                        game_file = GameFile(entry.attrib['name'])

                        for attrib, value in entry.attrib.items():
                            if attrib in ['crc', 'md5', 'sha1']:
                                game_file.hashes[attrib] = value.lower()
                            elif attrib in ['name', 'serial']:
                                pass
                            elif attrib == 'status':
                                game_file.status = value
                            elif attrib == 'size':
                                game_file.size = int(value)
                            else:
                                print('WARNING: Unknown attribute {}'.format(attrib))

                        game.files.append(game_file)

                self._games.append(game)

        print(self._games[0])
