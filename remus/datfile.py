import re
import subprocess

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
    region: str = 'Unknown'
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

    def match(self, filename: str) -> Optional[GameFile]:
        hashes = self._hash_basic(filename)

        for game in self._games:
            for game_file in game.files:
                match_count = 0

                for algorithm, hash in hashes.items():
                    if game_file.hashes[algorithm] == hash:
                        match_count += 1

                if match_count == 3:
                    return game_file
                elif match_count > 0:
                    print(f'WARNING: {filename} partially matched {game_file.name} from {game.name}')

                    for algorithm, hash in hashes.items():
                        print(f' {algorithm:5} "{hash}" "{game_file.hashes[algorithm]}"')

        return None

    #---------------------------------------------------------------------------
    # Private Methods
    #---------------------------------------------------------------------------

    def _hash_basic(self, filename: str):
        return {
            'crc': subprocess.check_output(['crc32', filename]).decode('utf-8').strip(),
            'md5': subprocess.check_output(['md5sum', filename]).decode('utf-8').strip().split(' ')[0],
            'sha1': subprocess.check_output(['sha1sum', filename]).decode('utf-8').strip().split(' ')[0],
        }

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

                        for tag in re.findall(r'\(([^\)]*)\)', game_file.name):
                            if 'USA' in tag:
                                game_file.region = 'USA'
                            elif 'Japan' in tag:
                                game_file.region = 'Japan'
                            elif 'Europe' in tag or 'Germany' in tag or 'France' in tag or 'Spain' in tag:
                                game_file.region = 'Europe'

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
