# View for leaderboard
def display_leaderboard(leaderboard_data):
    """
    Menampilkan tabel leaderboard top players
    
    Args:
        leaderboard_data (list): List of dict berisi data pemain
        
    Returns:
        None
    """
    print("\n" + "="*90)
    print("🏆 LEADERBOARD - TOP PLAYERS 🏆".center(90))
    print("="*90)
    
    if not leaderboard_data or not isinstance(leaderboard_data, list):
        print("Belum ada data pemain di leaderboard.")
        print("="*90)
        input("\nTekan Enter untuk kembali...")
        return
    
    # Header tabel
    print(f"Rank   {'Username':<18} {'Class':<13} {'Floor':<8} {'Score':<10} {'Title':<15}")
    print("-"*90)
    
    # Data pemain
    for idx, player in enumerate(leaderboard_data, start=1):
        if not isinstance(player, dict):
            continue
        
        username = str(player.get('username', 'Unknown'))[:17]
        class_name = str(player.get('class_name', 'N/A'))[:12]
        floor = player.get('floor', 0)
        score = player.get('score', 0)
        title = str(player.get('title', 'N/A'))[:14]
        
        # Medal untuk top 3, spasi manual untuk yang lain
        if idx == 1:
            print(f"🥇     {username:<18} {class_name:<13} {floor:<8} {score:<10} {title:<15}")
        elif idx == 2:
            print(f"🥈     {username:<18} {class_name:<13} {floor:<8} {score:<10} {title:<15}")
        elif idx == 3:
            print(f"🥉     {username:<18} {class_name:<13} {floor:<8} {score:<10} {title:<15}")
        else:
            print(f"{idx}.     {username:<18} {class_name:<13} {floor:<8} {score:<10} {title:<15}")
    
    print("="*90)
    input("\nTekan Enter untuk kembali...")