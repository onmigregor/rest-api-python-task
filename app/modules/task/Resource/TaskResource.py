class TaskResource:
    @staticmethod
    def serialize(task):
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "due_date": task.due_date,
            "priority": task.priority.value if hasattr(task.priority, "value") else task.priority,
            "category": {
                "id": task.category.id,
                "name": task.category.name
            } if hasattr(task, "category") and task.category else None,
            "created_by": {
                "id": task.creator.id,
                "name": getattr(task.creator, "name", None)
            } if hasattr(task, "creator") and task.creator else None,
            "assigned_to": {
                "id": task.assignee.id,
                "name": getattr(task.assignee, "name", None)
            } if hasattr(task, "assignee") and task.assignee else task.assigned_to,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }
