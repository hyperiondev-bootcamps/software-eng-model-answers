# Model-View-Controller (MVC) Responsibilities

## 1. Overview
The **Model-View-Controller (MVC)** architectural pattern separates an application into three distinct layers. This separation of concerns ensures that code is organised, easy to maintain, and simple to test.

In the **Task Manager Application**, the responsibilities are divided as follows:

---

## 2. Component Responsibilities

### 🔹 Model (`TaskModel` & `Task`)
* **Role**: Manages the application data and business rules.
* **Key Responsibilities**:
  * Stores the in-memory collection of tasks (`tasks` list).
  * Encapsulates the attributes of individual tasks (ID, title, description, completion status).
  * Performs CRUD operations on the task data (`create`, `get_all`, `update`, `delete`).
  * Handles file persistence by reading from and writing to the storage file (`tasks.json` / `tasks.txt`).
* **Rule**: The Model does **not** know anything about the user interface (it never calls `print()` or `input()`).

---

### 🔹 View (`TaskView`)
* **Role**: Handles all user interface presentation and input collection.
* **Key Responsibilities**:
  * Displays the main menu options to the user.
  * Prompts the user for input (e.g., asking for task title, description, or task ID).
  * Formats and prints task records to the terminal for reading.
  * Shows feedback messages to the user (e.g., success notices, validation warnings, error alerts).
* **Rule**: The View only focuses on input and output; it does not process business logic or save directly to files.

---

### 🔹 Controller (`TaskController`)
* **Role**: Acts as the coordinator or intermediary between the View and the Model.
* **Key Responsibilities**:
  * Controls the main application loop (`run`).
  * Receives user choices from the View.
  * Decides what action needs to be taken and delegates work:
    * Requests input via the View.
    * Calls the appropriate method on the Model.
    * Passes the Model's results back to the View to display to the user.
* **Rule**: The Controller keeps the View and Model decoupled so neither needs to know about the internal details of the other.

---

## 3. Step-by-Step Data Flow: Creating a Task

Here is how data flows through the MVC components when a user adds a new task:

1. **User Request**: The user selects the "Add Task" option from the console menu presented by the `TaskView`.
2. **Collect Input**: The `TaskView` prompts the user for the task title and description, and passes these inputs to the `TaskController`.
3. **Delegate to Model**: The `TaskController` receives the title and description, validates that they are not empty, and calls `TaskModel.create(title, description)`.
4. **Data Persistence**: The `TaskModel` instantiates a new `Task` object, assigns it a unique ID, appends it to its internal list, and writes the updated list to `tasks.json`.
5. **Confirmation to Controller**: The `TaskModel` confirms that the task was successfully created and saved by returning the new `Task` object.
6. **Display Feedback**: The `TaskController` instructs the `TaskView` to display a confirmation message (e.g., `"Task 'Buy Groceries' created successfully!"`) to the user.

