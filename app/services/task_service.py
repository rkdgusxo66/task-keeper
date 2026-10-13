from sqlalchemy.orm import Session, selectinload

from app.models import Tag, Task


def list_tasks(db: Session) -> list[Task]:
    # 태그를 즉시 로딩해 직렬화 시 할 일마다 태그 쿼리가 실행되는 N+1을 막습니다.
    return db.query(Task).options(selectinload(Task.tags)).all()


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, title: str, tag_names: list[str]) -> Task:
    tags: list[Tag] = []
    for name in tag_names:
        tag = db.query(Tag).filter(Tag.name == name).first()
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
        tags.append(tag)

    task = Task(title=title, tags=tags)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
