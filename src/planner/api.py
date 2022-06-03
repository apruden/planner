from flask import request, jsonify, abort
from flask_restful import Resource, Api
from .model import db, Worker, Allocation, Shift
import datetime

api = Api()


class WorkersResource(Resource):
    def get(self):
        return jsonify(Worker.query.all())

    def post(self):
        worker = Worker(**request.json)
        db.session.add(worker)
        db.session.commit()
        return jsonify(worker)


class WorkerResource(Resource):
    def get(self, worker_id):
        worker = Worker.query.get(worker_id)
        if not worker:
            raise abort(404)
        return jsonify(worker)

    def put(self, worker_id):
        worker = Worker.query.get(worker_id)
        worker.name = request.json['name']
        db.session.commit()
        return jsonify(worker)

    def delete(self, worker_id):
        worker = Worker.query.get(worker_id)
        db.session.delete(worker)
        db.session.commit()


class WorkerAllocationsResource(Resource):
    def get(self, worker_id):
        worker = Worker.query.get(worker_id)
        return jsonify(worker.allocations)

    def post(self, worker_id):
        worker = Worker.query.get(worker_id)
        date = datetime.date.fromisoformat(request.json['date'])
        shift = Shift[request.json['shift']]

        allocation_on_same_date = list(Allocation.query.filter_by(worker=worker, date=date))

        if allocation_on_same_date:
            abort(400)
            return

        allocation = Allocation(worker=worker, date=date, shift=shift)
        db.session.add(allocation)
        db.session.commit()
        return jsonify(allocation)


class AllocationsResource(Resource):
    def get(self):
        return jsonify(Allocation.query.all())


api.add_resource(WorkersResource, '/workers')
api.add_resource(WorkerResource, '/workers/<worker_id>')
api.add_resource(WorkerAllocationsResource, '/workers/<worker_id>/allocations')
api.add_resource(AllocationsResource, '/allocations')

