from sqlalchemy.orm import Session
from ..Validators import taskValidator

class TaskDTO:
    def __init__(self, task_data, user_id: int, db: Session):
        self.task_data = task_data
        self.user_id = user_id
        self.db = db
        
    def prepare_for_create(self):
        """Prepara los datos para la creación de una tarea"""
        # Validar categoría
        taskValidator.TaskValidator.validate_category(self.db, self.task_data.category_id)
        # Autoasignar si no es admin
        self.task_data = taskValidator.TaskValidator.auto_assign_if_not_admin(self.db, self.user_id, self.task_data)
        # Validar usuario asignado
        taskValidator.TaskValidator.validate_assigned_user(self.db, self.task_data.assigned_to)
        return self.task_data
    
    def prepare_for_update(self):
        """Prepara los datos para la actualización de una tarea"""
        # Validar categoría si se proporciona
        if hasattr(self.task_data, 'category_id') and self.task_data.category_id is not None:
            taskValidator.TaskValidator.validate_category(self.db, self.task_data.category_id)
        # Autoasignar si no es admin
        self.task_data = taskValidator.TaskValidator.auto_assign_if_not_admin(self.db, self.user_id, self.task_data)
        # Validar usuario asignado si se proporciona
        if hasattr(self.task_data, 'assigned_to') and self.task_data.assigned_to is not None:
            taskValidator.TaskValidator.validate_assigned_user(self.db, self.task_data.assigned_to)
        return self.task_data
