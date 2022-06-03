from flask import request, jsonify, abort
from flask_restful import Resource, Api
from .model import db, Worker, Allocation, Shift
import datetime
from functools import wraps

api = Api()


def json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return jsonify(f(*args,**kwargs))

    return wrapper


def check_worker_exists(worker_id):
    worker = Worker.query.get(worker_id)
    if not worker:
        abort(404, message=f'worker {worker_id} not found')

    return worker


class WorkersResource(Resource):
    @json_response
    def get(self):
        '''
        Get all workers
        ---
        responses:
          200:
            description: get all workers
            schema:
                type: array
                items:
                  $ref: '#/definitions/Worker'
        '''
        return Worker.query.all()

    @json_response
    def post(self):
        '''
        Create a worker
        ---
        parameters:
          - in: body
            description: worker data
            schema:
              $ref: '#/definitions/Worker'
            required: true
        responses:
          200:
            description: created worker
            schema:
              $ref: '#/definitions/Worker'
        '''

        worker = Worker(**request.json)
        db.session.add(worker)
        db.session.commit()
        return worker


class WorkerResource(Resource):
    @json_response
    def get(self, worker_id):
        '''
        Get a worker by id
        ---
        parameters:
          - in: path
            name: worker_id
            type: integer
            required: true
        responses:
          200:
            description: a worker
            schema:
              id: Worker
              properties:
                id:
                  description: auto-generated id
                  type: integer
                name:
                  descrition: full name
                  type: string
        '''

        worker = check_worker_exists(worker_id)
        if not worker:
            raise abort(404)
        return worker

    @json_response
    def put(self, worker_id):
        '''
        Update a worker by id
        ---
        parameters:
          - in: path
            name: worker_id
            type: integer
            required: true
        responses:
          200:
            description: updated worker
            schema:
              $ref: '#/definitions/Worker'
        '''

        worker = check_worker_exists(worker_id)
        worker.name = request.json['name']
        db.session.commit()
        return worker

    @json_response
    def delete(self, worker_id):
        '''
        Delete a worker by id
        ---
        parameters:
          - in: path
            name: worker_id
            type: integer
            required: true
        responses:
          200:
            description: worker deleted successfully
        '''

        worker = check_worker_exists(worker_id)
        db.session.delete(worker)
        db.session.commit()


class WorkerAllocationsResource(Resource):
    @json_response
    def get(self, worker_id):
        '''
        Get all allocations for a worker
        ---
        responses:
          200:
            description: allocations list
            schema:
                type: array
                items:
                  $ref: '#/definitions/Allocation'
        '''
        worker = check_worker_exists(worker_id)
        return sorted(worker.allocations, key=lambda a: a.date)

    @json_response
    def post(self, worker_id):
        '''
        Create an allocation
        ---
        parameters:
          - in: body
            description: allocation data
            schema:
              $ref: '#/definitions/Allocation'
            required: true
        responses:
          200:
            description: created allocation
            schema:
              id: Allocation
              properties:
                id:
                  description: auto-generated id
                  type: integer
                date:
                  description: iso date
                  type: string
                shift:
                  description: shift enum
                  type: string
                  enum:
                    - DAY
                    - LATE
                    - NIGHT
                worker:
                  description: worker this allocation is assigned to
                  $ref: '#/definitions/Worker'
        '''

        worker = check_worker_exists(worker_id)
        date = datetime.date.fromisoformat(request.json['date'])
        shift = Shift[request.json['shift']]

        allocation_on_same_date = list(Allocation.query.filter_by(worker=worker, date=date))

        if allocation_on_same_date:
            abort(400)
            return

        allocation = Allocation(worker=worker, date=date, shift=shift)
        db.session.add(allocation)
        db.session.commit()
        return allocation


class AllocationsResource(Resource):
    @json_response
    def get(self):
        '''
        Get all allocations
        ---
        responses:
          200:
            description: allocations list
            schema:
                type: array
                items:
                  $ref: '#/definitions/Allocation'
        '''
        return Allocation.query.all().order_by(Allocation.date.asc())


api.add_resource(WorkersResource, '/workers')
api.add_resource(WorkerResource, '/workers/<worker_id>')
api.add_resource(WorkerAllocationsResource, '/workers/<worker_id>/allocations')
api.add_resource(AllocationsResource, '/allocations')

