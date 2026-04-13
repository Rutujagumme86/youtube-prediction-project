import mysql.connector

def insert_data(like_count, comment_count, duration, predicted_views):
    conn = mysql.connector.connect(
        host="metro.proxy.rlwy.net",
        user="root",
        password="nFndttoviVvwlACQOHCniUEwlAXruqHR",
        database="railway",
        port=44942
    )
    
    print("Connected to DB")
    cursor = conn.cursor()
    
    query = """
    INSERT INTO predictions 
    (like_count, comment_count, duration, predicted_views)
    VALUES (%s, %s, %s, %s)
    """
    
    cursor.execute(query, (like_count, comment_count, duration, predicted_views))
    
    conn.commit()
    conn.close()






