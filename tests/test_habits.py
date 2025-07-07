def test_create_and_get_habit_success(client, user_factory):
    user = user_factory()
    client.post("/auth/register", json=user)
    login_resp = client.post("/auth/login", json=user)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    habit_data = {
        "title": "Drink Water",
        "description": "Drink 8 glasses per day",
        "icon": "💧",
        "color": "#00BFFF",
        "group": "health",            
        "type": "daily",           
        "ikigai_category": None,  
        "goal": {
            "period": "day",
            "type": "quantity", 
            "target": 8,      
            "unit": "glasses"
        },
        "task_days": ["mon", "tue", "wed"],
        "reminders": ["08:00"],
    }
    resp = client.post("/habits/", json=habit_data, headers=headers)
    assert resp.status_code == 201
    habit_id = resp.json()["_id"]

    # Get
    resp = client.get(f"/habits/{habit_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Drink Water"
