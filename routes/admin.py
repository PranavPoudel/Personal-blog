from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from database import get_db
from auth import verify_token

router = APIRouter(tags=["Admin"])

@router.get ("/dashboard")
async def Admin(token: str = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor()

    query ="SELECT * FROM articles"
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    finally:
        conn.close()
    query_response = cursor.fetchall()
    if not query_response:
        raise HTTPException(status_code=404, detail="NO Data in DB")
    
    query_result = []
    for q in query_response:
        value = {
            "id": q[0],
            "title" : q[1],
            "content": q[2],
            "published_date": q[3],
            "visits": q[4]
        }
        query_result.append(value)
    conn.close()
    return query_result

