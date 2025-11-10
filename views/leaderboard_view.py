# View for leaderboard
def display_leaderboard(leaderboard_data, player_rank_info=None):
    """
    Menampilkan leaderboard ke layar
    Args:
        leaderboard_data (list): Data leaderboard dari controller
        player_rank_info (dict, optional): Info ranking pemain saat ini
    """
    print("\n" + "="*70)
    print("🏆 LEADERBOARD - TOP PLAYERS 🏆".center(70))
    print("="*70)
    
    if not leaderboard_data:
        print("Belum ada data pemain di leaderboard.")
        print("="*70)
        return
    
    # Header tabel
    print(f"{'Rank':<6} {'Username':<15} {'Class':<12} {'Floor':<7} {'Score':<10} {'Title':<15}")
    print("-"*70)
    
    # Data pemain
    for idx, player in enumerate(leaderboard_data, start=1):
        # Medal untuk top 3
        medal = ""
        if idx == 1:
            medal = "🥇"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}."
        
        print(f"{medal:<6} {player['username']:<15} {player['class_name']:<12} "
              f"{player['floor']:<7} {player['score']:<10} {player['title']:<15}")
    
    print("="*70)
    
    input("\nTekan Enter untuk kembali...")