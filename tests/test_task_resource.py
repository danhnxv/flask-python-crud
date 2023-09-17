from app.models import Task


# ============================  GET tasks test cases ============================
def test_get_tasks(client, database):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    response_data = response.json
    assert "data" in response_data


def test_get_tasks_with_provided_title(client, database):
    # Create and add multiple tasks to the database
    tasks = [
        Task(id="01", title="Task 1", description="Description 1"),
        Task(id="02", title="Task 2", description="Description 2"),
        Task(id="03", title="Task 3", description="Description 3"),
    ]

    # Add each task to the session and commit them
    for task in tasks:
        database.session.add(task)

    database.session.commit()

    title_to_filter = "Task 2"

    response = client.get(f"/api/tasks?title={title_to_filter}")

    assert response.status_code == 200
    response_data = response.json

    assert "data" in response_data

    # Assert that the response data contains tasks with the specified title
    data = response_data["data"]
    assert isinstance(data, list)

    filtered_tasks = [task for task in data if task["title"] == title_to_filter]
    assert len(filtered_tasks) > 0


def test_get_tasks(client, database):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    response_data = response.json
    assert "data" in response_data


def test_get_tasks_with_provided_title_not_exist(client, database):
    title_to_filter = "Task 111"

    response = client.get(f"/api/tasks?title={title_to_filter}")

    assert response.status_code == 200
    response_data = response.json

    assert "data" in response_data

    # Assert that the response data contains tasks with the specified title
    data = response_data["data"]
    assert len(data) == 0


def test_get_tasks_with_provided_completed(client, database):
    tasks = [
        Task(id="04", title="Task 4", completed=True),
        Task(id="05", title="Task 5"),
        Task(id="06", title="Task 6", completed=True),
    ]

    # Add each task to the session and commit them
    for task in tasks:
        database.session.add(task)

    database.session.commit()
    database.session.add(task)
    database.session.commit()
    title_to_filter = "true"

    response = client.get(f"/api/tasks?completed={title_to_filter}")

    assert response.status_code == 200
    response_data = response.json

    assert "data" in response_data

    # Assert that the response data contains tasks with the specified completed value
    data = response_data["data"]
    assert isinstance(data, list)

    # Check that all items in the response have completed set to True
    for item in data:
        assert item["completed"] is True


# ============================ POST task test cases ============================
def test_create_new_task_success(client, database):
    # Define the task data you want to post as a dictionary
    new_task_data = {"title": "test title", "description": "test description"}

    # Send a POST request to create the new task
    response = client.post("/api/tasks", json=new_task_data)

    # Check the response status code
    assert response.status_code == 201

    # Parse the response JSON
    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task created successfully"

    # Check the response data to ensure the new task was created correctly
    assert "data" in response_data

    new_task = response_data["data"]
    assert new_task["title"] == new_task_data["title"]
    assert new_task["description"] == new_task_data["description"]
    assert new_task["completed"] == False


def test_create_task_without_title(client, database):
    new_task_data = {"description": "test create task"}

    # Send a POST request to create the new task
    response = client.post("/api/tasks", json=new_task_data)

    # Check the response status code
    assert response.status_code == 400

    # Parse the response JSON
    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Missing required fields: title"


def test_create_existing_task(client, database):
    # Create a task in the database
    task = Task(id="test", title="test create task")
    database.session.add(task)
    database.session.commit()

    response = client.post(
        "/api/tasks",
        json={
            "title": "test create task",
        },
    )

    # Parse the response JSON
    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task already exists"

    assert response.status_code == 400


def test_create_existing_task(client, database):
    initial_task_data = {
        "title": "test",
    }
    response = client.post("/api/tasks", json=initial_task_data)

    assert response.status_code == 201

    response = client.post("/api/tasks", json=initial_task_data)

    # Parse the response JSON
    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task already exists"

    assert response.status_code == 400


# ============================ PUT task test cases ============================
def test_update_task_success(client, database):
    # Create a task in the database
    task = Task(id="1", title="test")
    database.session.add(task)
    database.session.commit()

    response = client.put(
        f"/api/tasks/{task.id}",
        json={
            "title": "updated task",
            "description": "Updated description",
            "completed": True,
        },
    )

    assert response.status_code == 200

    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task updated successfully"

    # Query the database for the updated task
    updated_task = database.session.get(Task, task.id)

    # Assert that the task was updated with the expected attributes
    assert updated_task.title == "updated task"
    assert updated_task.description == "Updated description"
    assert updated_task.completed == True


def test_update_task_not_existing(client, database):
    response = client.put(
        f"/api/tasks/2",
        json={
            "title": "updated task not existing",
        },
    )

    assert response.status_code == 404

    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task not found"


def test_update_task_with_existing_title(client, database):
    # Create a task in the database
    task = Task(id="3", title="exiting title")
    database.session.add(task)
    database.session.commit()
    response = client.put(
        f"/api/tasks/1",
        json={
            "title": "exiting title",
        },
    )

    assert response.status_code == 400

    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task with title 'exiting title' already exists"


# ============================ DELETE task test case ============================
def test_delete_task_success(client, database):
    response = client.delete(f"/api/tasks/1")

    assert response.status_code == 200

    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task deleted successfully"


def test_delete_task_not_existing(client, database):
    response = client.delete(f"/api/tasks/10")

    assert response.status_code == 404

    response_data = response.json

    # Check if the response contains the expected message
    assert "message" in response_data
    assert response_data["message"] == "Task not found"
