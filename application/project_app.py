from model import PROJECT
from flask import render_template
from datetime import datetime
from app import app
from auth import raise_status


class project_app():

    def __init__(self, requestObj=None, updateObj=None):
        self.requestObj = requestObj
        if self.requestObj == None:
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
                reference=self.requestObj['reference'],
                base=self.requestObj['base'],
                spec=self.requestObj['spec'],
                delete=False,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            ).save()
            return project_model
        except Exception as e:
            print('project_create error:', e)
            app.logger.exception(e)
            raise

    def project_find_all(self, page=None, pageSize=None):
        try:
            if page and pageSize:
                project = list(PROJECT.objects.raw(self.requestObj).skip((page - 1) * pageSize).limit(pageSize))
            else:
                project = list(PROJECT.objects.raw(self.requestObj))
        except Exception as e:
            print('project_find_all error:', e)
            app.logger.exception(e)
            info = '后台异常'
            return render_template('index.html', error=info)
        return project

    def project_find_one(self):
        try:
            project = PROJECT.objects.get(self.requestObj)
        except PROJECT.DoesNotExist:
            print("project doesn't exist")
            return None
        except Exception as e:
            print('project_find_one error:', e)
            app.logger.exception(e)
            info = '后台异常'
            return render_template('index.html', error=info)
        return project

    def project_update_set(self):
        try:
            self.updateObj['updatedAt'] = datetime.now()
            PROJECT.objects.raw(self.requestObj).update({'$set': self.updateObj})
        except Exception as e:
            print('project_update_set errpr:', e)
            app.logger.exception(e)
            return render_template('index.html', error=e)

    def project_delete(self):
        try:
            PROJECT.objects.raw(self.requestObj).update({'$set': {'delete': True}})
        except Exception as e:
            print('project_delete error:', e)
            app.logger.exception(e)
            info = '后台异常'
            return render_template('index.html', error=info)

    def project_count(self):
        try:
            count = PROJECT.objects.raw(self.requestObj).count()
            return count
        except Exception as e:
            print('project_count error:', e)
            app.logger.exception(e)
            error = raise_status(500, '后台异常')
            return error

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
