# Controller for leaderboard
from utils.database import db, cursor

def get_leaderboard(limit=10):
    """
    Mengambil data leaderboard dari database
    Args:
        limit (int): Jumlah maksimal data yang ditampilkan
    Returns:
        list: Data leaderboard berisi username, class_name, floor, score, title
    """
    try:
        query = """
            SELECT 
                u.username,
                c.class_name,
                c.floor,
                c.score,
                c.title,
                c.exp,
                c.gold
            FROM characters c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.score DESC, c.floor DESC, c.exp DESC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        leaderboard_data = cursor.fetchall()
        return leaderboard_data
    
    except Exception as e:
        print(f"⚠️ Terjadi kesalahan saat mengambil data leaderboard: {e}")
        return []

def update_player_score(character_id, score_gained):
    """
    Menambah score pemain setelah menyelesaikan quest atau mengalahkan boss
    Args:
        character_id (int): ID karakter
        score_gained (int): Score yang didapat
    """
    try:
        cursor.execute(
            "UPDATE characters SET score = score + %s WHERE id = %s",
            (score_gained, character_id)
        )
        db.commit()
        print(f"✨ Score bertambah +{score_gained}!")
    
    except Exception as e:
        db.rollback()
        print(f"⚠️ Gagal update score: {e}")