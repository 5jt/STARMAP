#!/usr/bin/env python3
"""
Extract star data from Yale Bright Star Catalog (BSC5) for STARMAP book table.

Reads the existing table to get Yale numbers and row metadata,
looks up all stars in BSC5, and outputs a corrected table.
"""

import re
from pathlib import Path


def parse_bsc5_catalog(catalog_path):
    """Parse BSC5 catalog file into a dictionary keyed by HR number."""
    stars = {}
    with open(catalog_path, 'r', encoding='latin-1') as f:
        for line in f:
            if len(line) < 107:
                continue
            try:
                hr = int(line[0:4].strip())
            except ValueError:
                continue

            # J2000 coordinates (bytes 76-90, 0-indexed: 75-89)
            try:
                ra_h = line[75:77].strip()
                ra_m = line[77:79].strip()
                ra_s = line[79:83].strip()
                de_sign = line[83:84]
                de_d = line[84:86].strip()
                de_m = line[86:88].strip()

                if not ra_h or not de_d:
                    continue

                ra_h = int(ra_h)
                ra_m = int(ra_m)
                ra_s = float(ra_s)
                de_d = int(de_d)
                de_m = int(de_m)
            except (ValueError, IndexError):
                continue

            # Visual magnitude (bytes 103-107, 0-indexed: 102-106)
            try:
                vmag = float(line[102:107].strip())
            except (ValueError, IndexError):
                vmag = None

            # Parallax (bytes 162-166, 0-indexed: 161-165)
            try:
                parallax = float(line[161:166].strip())
            except (ValueError, IndexError):
                parallax = None

            # Extract Bayer name from bytes 5-14
            bayer_name = line[4:14].strip()

            stars[hr] = {
                'hr': hr,
                'bayer_name': bayer_name,
                'ra_h': ra_h,
                'ra_m': ra_m,
                'ra_s': ra_s,
                'de_sign': de_sign,
                'de_d': de_d,
                'de_m': de_m,
                'vmag': vmag,
                'parallax': parallax
            }

    return stars


def parse_book_table(starmap_path, yale_251_300_path):
    """Parse existing star table to get row metadata and Yale numbers."""
    rows = {}

    with open(starmap_path, 'r', encoding='utf-8') as f:
        content = f.read()

    in_table = False
    for line in content.split('\n'):
        if 'Popular Name' in line and 'Bayer' in line:
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith('```'):
            break
        if not line.strip():
            continue

        # Parse: [Popular Name (up to ~17 chars)] seq_num [greek] constellation [yale_num] ...
        # Handle rows with/without popular names, with/without Greek letters

        # First try to extract sequence number - it's always there
        # Greek letter is either a Greek character (α-ω) or a single uppercase letter (A-Z)
        # Constellation is 2-3 uppercase letters
        # Some rows have no Greek letter (e.g., Pleiades "PLE")
        match = re.search(r'(\d+)\s+([α-ω]|[A-Z](?=\s))?\s*([A-Z]{2,3})\s+(\d+)', line)
        if not match:
            continue

        seq = int(match.group(1))
        greek = match.group(2).strip() if match.group(2) else ''
        constellation = match.group(3)
        yale_str = match.group(4)

        # Extract popular name (everything before the sequence number)
        seq_pos = line.find(str(seq))
        popular_name = line[:seq_pos].strip() if seq_pos > 0 else ''

        # Get Yale number if present
        yale_num = int(yale_str) if yale_str else None

        rows[seq] = {
            'seq': seq,
            'popular_name': popular_name,
            'greek': greek,
            'constellation': constellation,
            'yale_num': yale_num
        }

    # Load Yale numbers for rows 251-300
    with open(yale_251_300_path, 'r') as f:
        new_yales = [int(line.strip()) for line in f if line.strip()]

    for i, yale in enumerate(new_yales):
        seq = 251 + i
        if seq in rows:
            rows[seq]['yale_num'] = yale
            rows[seq]['use_bsc5_bayer'] = True  # Flag to get Bayer from BSC5
        else:
            # Row might be incomplete in original - create minimal entry
            rows[seq] = {
                'seq': seq,
                'popular_name': '',
                'greek': '',
                'constellation': '',
                'yale_num': yale,
                'use_bsc5_bayer': True
            }

    return rows


def parse_bsc5_bayer(bayer_name):
    """Parse BSC5 bayer name like 'Zet Pup' or '21Alp Sco' into (greek, constellation)."""
    # Greek letter abbreviations to Unicode
    abbrev_to_greek = {
        'Alp': 'α', 'Bet': 'β', 'Gam': 'γ', 'Del': 'δ', 'Eps': 'ε',
        'Zet': 'ζ', 'Eta': 'η', 'The': 'θ', 'Iot': 'ι', 'Kap': 'κ',
        'Lam': 'λ', 'Mu': 'μ', 'Nu': 'ν', 'Xi': 'ξ', 'Omi': 'ο',
        'Pi': 'π', 'Rho': 'ρ', 'Sig': 'σ', 'Tau': 'τ', 'Ups': 'υ',
        'Phi': 'φ', 'Chi': 'χ', 'Psi': 'ψ', 'Ome': 'ω'
    }

    # Constellation abbreviation mappings (BSC5 mixed case to book uppercase)
    const_map = {
        'And': 'AND', 'Aql': 'AQL', 'Aqr': 'AQR', 'Ara': 'ARA', 'Ari': 'ARI',
        'Aur': 'AUR', 'Boo': 'BOO', 'Cap': 'CAP', 'Car': 'CAR', 'Cas': 'CAS',
        'Cen': 'CEN', 'Cep': 'CEP', 'Cet': 'CET', 'CMa': 'CMA', 'CMi': 'CMI',
        'Cnc': 'CNC', 'Col': 'COL', 'CrB': 'CRB', 'Cru': 'CRU', 'Crv': 'CRV',
        'CVn': 'CVN', 'Cyg': 'CYG', 'Del': 'DEL', 'Dor': 'DOR', 'Dra': 'DRA',
        'Eri': 'ERI', 'Gem': 'GEM', 'Gru': 'GRU', 'Her': 'HER', 'Hya': 'HYA',
        'Hyi': 'HYI', 'Ind': 'IND', 'Leo': 'LEO', 'Lep': 'LEP', 'Lib': 'LIB',
        'Lup': 'LUP', 'Lyn': 'LYN', 'Lyr': 'LYR', 'Mus': 'MUS', 'Oph': 'OPH',
        'Ori': 'ORI', 'Pav': 'PAV', 'Peg': 'PEG', 'Per': 'PER', 'Phe': 'PHE',
        'Pic': 'PIC', 'Psc': 'PSC', 'PsA': 'PSA', 'Pup': 'PUP', 'Sco': 'SCO',
        'Scl': 'SCL', 'Sgr': 'SGR', 'Tau': 'TAU', 'TrA': 'TRA', 'Tri': 'TRI',
        'Tuc': 'TUC', 'UMa': 'UMA', 'UMi': 'UMI', 'Vel': 'VEL', 'Vir': 'VIR'
    }

    if not bayer_name:
        return '', ''

    # Try to parse: optional number, Greek abbrev, optional number, constellation
    match = re.match(r'\d*([A-Z][a-z]{1,2})\d?\s*([A-Z][a-zA-Z]{1,2})', bayer_name)
    if match:
        greek_abbrev = match.group(1)
        const_abbrev = match.group(2)
        greek = abbrev_to_greek.get(greek_abbrev, '')
        const = const_map.get(const_abbrev, const_abbrev.upper())
        return greek, const

    return '', ''


def format_dec_value(sign, value):
    """Format declination component with APL high minus for negative."""
    if sign == '-':
        return f"¯{value}"
    return str(value)


def format_magnitude(vmag):
    """Format magnitude with APL high minus for negative."""
    if vmag is None:
        return ""
    if vmag < 0:
        return f"¯{abs(vmag):.2f}"
    return f"{vmag:.2f}"


def format_parallax(parallax):
    """Format parallax with APL high minus for negative."""
    if parallax is None or parallax == 0:
        return ".000"
    if parallax < 0:
        return f"¯.{abs(int(parallax * 1000)):03d}"
    return f".{int(parallax * 1000):03d}"


def format_table_row(row, star):
    """Format a single table row matching book format."""
    # Popular Name: 17 chars, left-aligned
    # For rows 251-300, we don't have reliable popular names
    if row.get('use_bsc5_bayer'):
        name = ''.ljust(17)
    else:
        name = row['popular_name'][:17].ljust(17)

    # Sequence: 3 chars, right-aligned
    seq = str(row['seq']).rjust(3)

    # Greek letter + constellation
    # For rows 251-300, get Bayer designation from BSC5
    if row.get('use_bsc5_bayer'):
        greek, const = parse_bsc5_bayer(star.get('bayer_name', ''))
        greek = greek if greek else ' '
        const = const if const else '   '
    else:
        greek = row['greek'] if row['greek'] else ' '
        const = row['constellation']

    # Yale number: 5 chars, right-aligned
    yale = str(row['yale_num']).rjust(5)

    # RA: hours (4 chars), minutes (4 chars), seconds (4 chars, rounded to int)
    ra_h = str(star['ra_h']).rjust(5)
    ra_m = str(star['ra_m']).rjust(4)
    ra_s = str(int(round(star['ra_s']))).rjust(4)

    # Dec: degrees (6 chars with sign), minutes (4 chars with sign)
    de_sign = star['de_sign']
    deg_str = format_dec_value(de_sign, star['de_d']).rjust(6)
    min_str = format_dec_value(de_sign, star['de_m']).rjust(4)

    # Magnitude: 9 chars
    mag_str = format_magnitude(star['vmag']).rjust(9)

    # Parallax
    prlx_str = format_parallax(star['parallax'])

    return f"{name}{seq}  {greek} {const}{yale}{ra_h}{ra_m}{ra_s}{deg_str}{min_str}{mag_str}  {prlx_str}"


def test_extraction(rows, bsc5_stars):
    """Test that extraction from BSC5 works correctly.

    Uses BSC5 as authoritative source. Small discrepancies with the 1978 book
    are attributed to catalog improvements, though this is untested.
    """
    # Test cases: verify Yale numbers map correctly and BSC5 has data
    test_cases = [
        # (seq, expected_yale, expected_ra_h)
        (1, 15, 0),        # ALPHERATZ - first star
        (27, 5340, 14),    # ARCTURUS
        (81, 2491, 6),     # SIRIUS
        (250, 8728, 22),   # FOMALHAUT - last before gap
        (251, 595, 2),     # First row from yale-numbers-251-300.txt (α Psc)
        (300, 4301, 11),   # Last row from yale-numbers-251-300.txt
        (332, 5107, 13),   # Last star (ζ VIR)
    ]

    print("Testing extraction:")
    all_pass = True
    for seq, expected_yale, expected_ra_h in test_cases:
        row = rows.get(seq)
        if not row:
            print(f"  FAIL: Row {seq} not found")
            all_pass = False
            continue

        yale = row['yale_num']
        if yale != expected_yale:
            print(f"  FAIL: Row {seq} Yale number: expected {expected_yale}, got {yale}")
            all_pass = False
            continue

        star = bsc5_stars.get(yale)
        if not star:
            print(f"  FAIL: Yale {yale} not found in BSC5")
            all_pass = False
            continue

        if star['ra_h'] != expected_ra_h:
            print(f"  FAIL: Row {seq} RA hours: expected {expected_ra_h}, got {star['ra_h']}")
            all_pass = False
            continue

        print(f"  PASS: Row {seq} - Yale {yale}, RA {star['ra_h']}h {star['ra_m']}m")

    return all_pass


def main():
    base_dir = Path(__file__).parent.parent
    catalog_path = base_dir / 'yale-catalog' / 'ybsc5'
    starmap_path = base_dir / 'book' / 'markdown' / 'starmap.md'
    yale_251_300_path = base_dir / 'book' / 'markdown' / 'yale-numbers-251-300.txt'
    output_path = base_dir / 'yale-catalog' / 'star_table_new.txt'

    print("Loading BSC5 catalog...")
    bsc5_stars = parse_bsc5_catalog(catalog_path)
    print(f"Loaded {len(bsc5_stars)} stars from BSC5")

    print("\nParsing book table...")
    rows = parse_book_table(starmap_path, yale_251_300_path)
    print(f"Found {len(rows)} rows")

    # Check for missing Yale numbers
    missing_yale = [seq for seq, row in rows.items() if row['yale_num'] is None]
    if missing_yale:
        print(f"WARNING: Rows without Yale numbers: {missing_yale}")
        return

    # Check all Yale numbers exist in BSC5
    missing_in_bsc5 = [row['yale_num'] for row in rows.values() if row['yale_num'] not in bsc5_stars]
    if missing_in_bsc5:
        print(f"WARNING: Yale numbers not found in BSC5: {missing_in_bsc5}")
        return

    print("\n" + "="*60)
    if not test_extraction(rows, bsc5_stars):
        print("\nTests failed - stopping")
        return
    print("="*60)

    print("\nGenerating output table...")
    lines = []
    lines.append("Popular Name        Bayer  Yale   Right Asc.     Decl.     Mag.  Prlx")
    lines.append("                            No.   Hr Min Sec   Deg Min           Secs")
    lines.append("")

    for seq in sorted(rows.keys()):
        row = rows[seq]
        star = bsc5_stars[row['yale_num']]
        lines.append(format_table_row(row, star))

    output = '\n'.join(lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Output written to {output_path}")
    print(f"Total rows: {len(rows)}")

    # Show a few sample rows
    print("\nSample output (first 5 rows):")
    for line in lines[3:8]:
        print(f"  {line}")


if __name__ == '__main__':
    main()
