# Registry schema

`design/registry.yaml` is the list of every named thing in the game. Skills reference things by ID, never by display name.

## ID prefixes

| Prefix | Thing | Example |
|---|---|---|
| `P` | Pillar | `P1` |
| `MECH` | Mechanic or verb | `MECH-dash` |
| `ZON` | Zone, level or room | `ZON-sunken-crypt` |
| `CHR` | Player or NPC character | `CHR-warden` |
| `ENM` | Enemy | `ENM-ogre` |
| `ITM` | Item | `ITM-iron-key` |
| `WPN` | Weapon | `WPN-short-sword` |
| `CUR` | Currency | `CUR-gold` |
| `QST` | Quest | `QST-0007` |
| `PUZ` | Puzzle | `PUZ-vault-door` |
| `FAC` | Faction | `FAC-ashen-order` |
| `SHOP` | Shop or vendor | `SHOP-blacksmith` |
| `SKL` | Skill, spell or ability | `SKL-fireball` |

IDs are lowercase after the prefix, hyphen separated, and never change. If something is renamed, change the display name and keep the ID. If it is removed, set `status: deprecated`.

## Entry format

```yaml
entries:
  - id: ENM-ogre
    name: Ogre
    status: canon          # proposed | approved | canon | deprecated
    source: PROP-0012      # proposal that introduced it
    file: gdd/04-characters.md#ogre
    refs: [ZON-sunken-crypt, WPN-club]   # things this entry depends on
    tags: [tank, melee]
```

## Rules checked by `validate_registry.py`

1. IDs are unique.
2. Every ID uses a known prefix.
3. `status` is one of the four allowed values.
4. Every ID in `refs` exists in the registry.
5. No `canon` entry refs a `proposed` or `deprecated` entry.
6. `canon` entries have a `file` field.
