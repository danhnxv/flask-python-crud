from werkzeug.exceptions import BadRequest
from flask_restful import Resource, reqparse, abort
from app.models import Task
from app import db
import hashlib
import uuid
from flask import request


class TaskResource(Resource):
    def get(self):
        try:
            title = request.args.get("title")
            completed = request.args.get("completed")

            # Initialize the query without any filters
            query = Task.query

            if title is not None:
                query = query.filter(Task.title.ilike(f"%{title}%"))

            if completed is not None:
                completed_bool = completed.lower() == "true"
                query = query.filter_by(completed=completed_bool)

            # Execute the query and retrieve tasks
            tasks = query.all()

            serialized_tasks = [task.serialize for task in tasks]
            return {"data": serialized_tasks}, 200
        except Exception as err:
            print(err)
            abort(500, message="Server Error", statusCode=500, error=str(err))

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str, required=True)
            parser.add_argument("description", type=str)
            args = parser.parse_args()

            # Generate a unique ID (e.g., using uuid)
            unique_id = str(uuid.uuid4())

            # Hash the ID using SHA-256
            hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()

            # Check if a task with the same title already exists
            existing_task = Task.query.filter_by(title=args["title"]).first()
            if existing_task:
                return {
                    "message": "Task already exists",
                }, 400

            new_task = Task(
                id=hashed_id,
                title=args["title"],
                description=args["description"],
            )
            db.session.add(new_task)
            db.session.commit()

            # Create a dictionary representing the serialized task data
            serialized_task = {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "completed": new_task.completed,
            }

            # Return the serialized task data along with the success message
            return {
                "message": "Task created successfully",
                "data": serialized_task,  # Include the task data in the response
            }, 201
        except BadRequest as e:
            missing_fields = [field for field in e.data["message"].keys()]
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            return {"message": error_message}, 400

        except Exception as err:
            print(err)
            db.session.rollback()
            abort(500, message="Server Error", statusCode=500, error=str(err))


class TaskUpdateResource(Resource):
    def put(self, task_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str)
            parser.add_argument("description", type=str)
            parser.add_argument("completed", type=str)
            args = parser.parse_args()

            # Check if task not found
            existing_task = db.session.get(Task, task_id)
            if not existing_task:
                return {"message": f"Task not found"}, 404

            # Check if the new title already exists in the database
            if args["title"] and args["title"] != existing_task.title:
                # Query the database to see if a task with the same title exists
                task_with_same_title = Task.query.filter_by(title=args["title"]).first()
                if task_with_same_title:
                    return {
                        "message": f"Task with title '{args['title']}' already exists"
                    }, 400

            # Update the task's fields if provided
            if args["title"]:
                existing_task.title = args["title"]
            if args["description"]:
                existing_task.description = args["description"]
            if args["completed"] is not None:
                existing_task.completed = args["completed"].lower() == "true"

            db.session.commit()

            return {"message": f"Task updated successfully"}, 200

        except Exception as err:
            print(err)
            db.session.rollback()
            abort(500, message="Server Error", statusCode=500, error=str(err))

    def delete(self, task_id):
        try:
            existing_task = db.session.get(Task, task_id)
            if not existing_task:
                return {"message": f"Task not found"}, 404

            db.session.delete(existing_task)
            db.session.commit()

            return {"message": f"Task deleted successfully"}, 200

        except Exception as err:
            print(err)
            db.session.rollback()
            abort(500, message="Server Error", statusCode=500, error=str(err))
