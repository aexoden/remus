# remus

Remus is a basic tool for managing emulator data files, including games (disk
or ROM images) and other accessory files.

## Configuration

Remus requires a configuration file named remus.json to be present in the
current working directory. (This limitation will be removed at some point.) The
configuration file should be a standard JSON file with the following format:

```json
{
    "paths": {
        "dats": "/path/to/dat/files",
        "library": "/path/to/library",
    },
    "systems": {
        "system_code": {
            "dats": ["system_dat_file.dat", "system_dat_file_2.dat"]
        }
    }
}
```

Relative paths are considered relative to the configuration file (which for the
moment must be in the current working directory). DAT files for a system should
be located in the configured DAT file directory. The system code is the short
version of the system name that will be used in the library. (For example, "a26"
for the Atari 2600 or "psx" for the Sony PlayStation. The program itself does
not care what the codes are, and these are just potential examples.)
