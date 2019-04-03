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
                requirement=self.requestObj['requirement'],
                material=self.requestObj['material'],
                timeConsume=self.requestObj['timeConsume'],
                reference=self.requestObj['reference'],
                image=self.requestObj['image'],
                base=self.requestObj['base'],
                spec=self.requestObj['spec'],
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
            info = '后台异常'
            return raise_status(500, info)
        return project

    def project_find_one(self):
        try:
            project = PROJECT.objects.get(self.requestObj)
        except PROJECT.DoesNotExist:
            print("project doesn't exist")
            return None
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            info = '后台异常'
            return raise_status(500, info)
        return project

    def project_update_set(self):
        try:
            self.updateObj['updatedAt'] = datetime.now()
            PROJECT.objects.raw(self.requestObj).update({'$set': self.updateObj})
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            return raise_status(500, '后台异常')

    def project_delete(self):
        try:
            PROJECT.objects.raw(self.requestObj).update({'$set': {'delete': True}})
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            info = '后台异常'
            return raise_status(500, info)

    def project_count(self):
        try:
            count = PROJECT.objects.raw(self.requestObj).count()
            return count
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            return raise_status(500, '后台异常')

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
            PROJECT.objects.get({'_id': projectId, 'delete': False})
        except PROJECT.DoesNotExist:
            raise
