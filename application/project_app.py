from model import PROJECT
from datetime import datetime
from auth import raise_status
import logging
import traceback


class project_app():

    def __init__(self, requestObj=None, updateObj=None):
        self.requestObj = requestObj
        if self.requestObj is None:
            self.requestObj = {'delete': False}
        else:
            self.requestObj['delete'] = False
        self.updateObj = updateObj

    def project_create(self):
        from datetime import datetime
        try:
            project_model = PROJECT(
                creator=self.requestObj['creator'],
                title=self.requestObj['title'],
                description=self.requestObj['description'],
                requirement=self.requestObj.get('requirement'),
                material=self.requestObj.get('material'),
                tag=self.requestObj['tag'],
                timeConsume=self.requestObj.get('timeConsume'),
                reference=self.requestObj.get('reference'),
                image=self.requestObj.get('image'),
                repoName=self.requestObj.get('repoName'),
                base=self.requestObj.get('base'),
                spec=self.requestObj.get('spec'),
                delete=False,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            ).save()
            return project_model
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            raise

    def project_find_all(self, page=None, pageSize=None):
        try:
            if page and pageSize:
                project = list(PROJECT.objects.raw(self.requestObj).skip((page - 1) * pageSize).limit(pageSize))
            else:
                project = list(PROJECT.objects.raw(self.requestObj))
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            raise
        return project

    def project_find_one(self):
        try:
            project = PROJECT.objects.get(self.requestObj)
        except PROJECT.DoesNotExist:
            print("project doesn't exist")
            return None
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            raise
        return project

    def project_update_set(self):
        try:
            self.updateObj['updatedAt'] = datetime.now()
            PROJECT.objects.raw(self.requestObj).update({'$set': self.updateObj})
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            raise

    def project_delete(self):
        try:
            PROJECT.objects.raw(self.requestObj).update({'$set': {'delete': True}})
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            raise

    def project_count(self):
        try:
            count = PROJECT.objects.raw(self.requestObj).count()
            return count
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            raise

    def project_check(self):
        try:
            PROJECT.objects.get(self.requestObj)
            return True
        except PROJECT.DoesNotExist:
            return False

    def project_reference_check(self, reference):
        try:
            PROJECT.objects.get({'_id': reference, 'delete': False})
        except PROJECT.DoesNotExist:
            raise

    def projectId_check(self, projectId):
        try:
            model = PROJECT.objects.get({'_id': projectId, 'delete': False})
            return model
        except PROJECT.DoesNotExist:
            raise

    def project_find_many_by_order(self, page=None, pageSize=None, order=None):
        try:
            if page and pageSize:
                model_list = list(
                    PROJECT.objects.raw(self.requestObj).order_by(order).skip((page - 1) * pageSize).limit(pageSize))
            else:
                model_list = list(PROJECT.objects.raw(self.requestObj).order_by(order))
            return model_list
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            raise

    def unfold_image(self, model):
        return {
            'id': str(model._id),
            'url': model.url,
            'desc': model.desc,
            'package': model.package
        }

    def unfold_project(self, model, embed=None):
        return {
            'id': str(model._id),
            'creator': str(model.creator),
            'title': model.title,
            'description': model.description,
            'requirement': model.requirement,
            'material': model.material,
            'reference': model.reference,
            'tag': str(model.tag._id) if not embed else {
                'id': str(model.tag._id),
                'category': model.tag.category.name,
                'name': model.tag.name
            },
            'image': model.image.url,
            'repoName': model.repoName,
            'timeConsume': model.timeConsume,
            'base': (str(model.base._id) if not embed else project_app().unfold_project(
                model=model.base)) if model.base else None,
            'spec': model.spec,
            'createdAt': model.createdAt,
            'updatedAt': model.updatedAt,
            'labs': model.labs
        }

    def unfold_purchase(self, model, embed=None):
        return {
            'id': str(model._id),
            'purchaser': str(model.purchaser),
            'limit': model.limit,
            'project': str(model.project._id) if not embed else project_app().unfold_project(model=model.project),
            'remark': model.remark,
            'createdAt': model.createdAt,
            'updatedAt': model.updatedAt
        }
