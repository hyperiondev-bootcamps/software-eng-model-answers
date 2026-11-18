# CRUD Matrix for Task Manager Application

## 1. CRUD Matrix Table

Modeled directly after the course design specifications (Page 16):

| Entity | Create | Read | Update | Delete |
| :--- | :---: | :---: | :---: | :---: |
| **Task** | **X** | **X** | **X** | **X** |

---

## 2. Operation Breakdown

The table below explains what each CRUD operation does in plain English within the Task Manager application:

| Operation | Action | Description | Application Example |
| :--- | :--- | :--- | :--- |
| **Create (C)** | Add new task | Instantiates a new `Task` record with a title, description, unique ID, and default incomplete status, then saves it to `tasks.json`. | Adding a new item: `Task(id=4, title="Submit assignment", description="Upload files to dashboard")`. |
| **Read (R)** | View tasks | Retrieves task records from memory or the storage file to view all tasks or look up a single task by its ID. | Listing all active tasks in a formatted table in the console, or finding task details for ID `2`. |
| **Update (U)** | Edit existing task | Modifies the attributes of an existing task (such as updating its title, changing its description, or marking it as completed). | Toggling `is_completed` from `False` to `True` for task ID `1`, or correcting a typo in a task title. |
| **Delete (D)** | Remove task | Removes an existing task record from the task list by matching its unique ID, and persists the changes to file. | Deleting completed or cancelled task ID `3` from the system. |
