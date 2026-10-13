from sqlalchemy import event


def test_list_tasks_query_count_is_constant(client, db_session):
    for i in range(5):
        client.post("/tasks", json={"title": f"할 일 {i}", "tags": [f"태그{i}"]})
    db_session.expire_all()  # 세션에 캐시된 태그를 비워 실제 조회 쿼리를 발생시킵니다.

    statements = []
    engine = db_session.get_bind()
    listener = lambda *args: statements.append(args[2])  # noqa: E731
    event.listen(engine, "before_cursor_execute", listener)
    try:
        res = client.get("/tasks")
    finally:
        event.remove(engine, "before_cursor_execute", listener)

    assert res.status_code == 200
    assert all(t["tags"] for t in res.json())
    # 할 일 조회 1회 + 태그 일괄 조회 1회
    assert len(statements) == 2, statements
