
activating the venv 
  > located in tasktracker folder
  > making sure terminal is set to cmd
  > from backend folder ( be in cmd ) -> tasktracker\Scripts\activate.bat

git 
  > my repo is inside tasktrackerAPI 
  > git add * | git commit -m "message" | git push

django app
  > creating an app
    > setting the views and url
    > connecting the apps urls to the main django url.


# postman tests 
https://.postman.co/workspace/My-Workspace~4757bf4a-2b3d-455d-8a45-89cb1c49b210/collection/40152220-160a1fde-7a09-4626-abba-3b24855d8060?action=share&creator=40152220




# testing

pytest to run 

| Category                 | Test Name                                 | What it Checks                                                                                                                                                                         |
| ------------------------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🧑‍💻 **Authentication** | `test_auth_required`                      | Ensures unauthenticated users cannot access protected endpoints (`401 Unauthorized`).                                                                                                  |
| 🧱 **Create Task**       | `test_create_task`                        | Confirms that an authenticated user can create a task successfully (`201 Created`). Verifies the new task’s title and creator.                                                         |
| 📋 **List Tasks**        | `test_list_tasks`                         | Checks that the API returns all tasks created by the current user with `GET /api/tasks/`.                                                                                              |
| 🔍 **Retrieve Task**     | `test_retrieve_task`                      | Ensures a user can fetch a single task by its ID using `GET /api/tasks/<id>/`.                                                                                                         |
| ✏️ **Partial Update**    | `test_update_task`                        | Verifies that the `PATCH /api/tasks/<id>/` endpoint updates specific fields (e.g. task title).                                                                                         |
| 🧩 **Full Update**       | `test_full_update_task`                   | Confirms that `PUT /api/tasks/<id>/` replaces the task’s content with new data and updates its state, description, and category.                                                       |
| ❌ **Delete Task**        | `test_delete_task`                        | Validates that `DELETE /api/tasks/<id>/` removes the task and returns `204 No Content`.                                                                                                |
| ⏰ **Validation**         | `test_due_date_cannot_be_before_creation` | *(Currently expects success)* Ensures that the model can handle due dates before creation gracefully. Can be updated to expect a `400 Bad Request` once strict validation is enforced. |
