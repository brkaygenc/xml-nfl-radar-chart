from src.database.queries import search_players

def main():
    # Search for QBs
    print("\nSearching for QBs (Mahomes, Allen):")
    qbs = search_players("mahomes", "qb") + search_players("allen", "qb")
    for qb in qbs:
        print(f"{qb['name']} ({qb['team']}) - ID: {qb['id']}")
    
    # Search for WRs
    print("\nSearching for WRs (Hill, Jefferson):")
    wrs = search_players("hill", "wr") + search_players("jefferson", "wr")
    for wr in wrs:
        print(f"{wr['name']} ({wr['team']}) - ID: {wr['id']}")
    
    # Search for RBs
    print("\nSearching for RBs (McCaffrey, Taylor):")
    rbs = search_players("mccaffrey", "rb") + search_players("taylor", "rb")
    for rb in rbs:
        print(f"{rb['name']} ({rb['team']}) - ID: {rb['id']}")

if __name__ == '__main__':
    main() 