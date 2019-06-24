from flask import Blueprint, jsonify, request
from bson import ObjectId
from auth import raise_status, filter
from datetime import datetime
import logging
import traceback
import requests

projects = Blueprint('projects', __name__)


@projects.route('/projects', methods=['POST'])
def project_create():
    from application.project_app import project_app
    from model import PROJECT
    requestObj = request.json
    try:
        requestObj['creator'] = ObjectId(requestObj['creator'])
        requestObj['tag'] = ObjectId(requestObj['tag'])
        try:
            git_list = requestObj['githuburl'].split('/')
            git_account = git_list[3] + '/'
            if '.git' in git_list[4]:
                repoName = git_list[4][: -4]
                repo = git_list[4][: -4] + '/'
            else:
                repoName = git_list[4]
                repo = git_list[4] + '/'
            url = 'https://raw.githubusercontent.com/' + git_account + repo + 'master/index.json'
            r = requests.get(url=url)
            labs = r.json()['labs']
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            return raise_status(400, 'github地址有误')
        query_list = ['creator', 'title', 'description', 'requirement', 'timeConsume',
                      'material', 'reference', 'image', 'base', 'spec', 'tag']
        requestObj = filter(query_list=query_list, updateObj=requestObj)
        if project_app(requestObj={'title': requestObj['title']}).project_check():
            return raise_status(400, 'project标题重复')
        if not requestObj.get('base'):
            requestObj['base'] = None
        else:
            requestObj['base'] = ObjectId(requestObj['base'])
            try:
                PROJECT.objects.get({'_id': requestObj['base'], 'delete': False})
            except PROJECT.DoesNotExist:
                return raise_status(400, '无效的引用信息')
        try:
            requestObj['repoName'] = repoName
            project_model = project_app(requestObj=requestObj).project_create()
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            return raise_status(500, '后台异常')
        lab_list = []
        for lab in labs:
            index = str(labs.index(lab)) if labs.index(lab) >= 10 else '0' + str(labs.index(lab))
            key_list = list(lab.keys())
            value_list = list(lab.values())
            lab_list.append({
                'id': str(project_model._id) + index,
                'filename': key_list[0],
                'name': value_list[0]
            })
        try:
            project_app(requestObj={'_id': project_model._id}, updateObj={'labs': lab_list}).project_update_set()
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            return raise_status(500, '后台异常')
        project_model = PROJECT.objects.get({'_id': project_model._id, 'delete': False})
        data = project_app().unfold_project(model=project_model, embed=request.args.get('embed'))
        # if project_model.base is None:
        #     base = None
        # else:
        #     if request.args.get('embed'):
        #         if project_model.base.base is None:
        #             base_reference = None
        #         else:
        #             base_reference = str(project_model.base.base._id)
        #         base = {
        #             'id': str(project_model.base._id),
        #             'creator': str(project_model.base.creator),
        #             'description': project_model.base.description,
        #             'title': project_model.base.title,
        #             'requirement': project_model.base.requirement,
        #             'material': project_model.base.material,
        #             'timeConsume': project_model.base.timeConsume,
        #             'tag': project_model.base.tag.name,
        #             'reference': project_model.base.reference,
        #             'labs': project_model.base.labs,
        #             'image': project_model.base.image,
        #             'base': base_reference,
        #             'spec': project_model.base.spec,
        #             'createdAt': project_model.base.createdAt,
        #             'updatedAt': project_model.base.updatedAt
        #         }
        #     else:
        #         base = str(project_model.base._id)
        # data = {
        #     'id': str(project_model._id),
        #     'creator': str(project_model.creator),
        #     'title': project_model.title,
        #     'description': project_model.description,
        #     'requirement': project_model.requirement,
        #     'material': project_model.material,
        #     'timeConsume': project_model.timeConsume,
        #     'tag': project_model.tag.name,
        #     'labs': lab_list,
        #     'reference': project_model.reference,
        #     'image': project_model.image,
        #     'base': base,
        #     'spec': project_model.spec,
        #     'createdAt': project_model.createdAt,
        #     'updatedAt': project_model.updatedAt
        # }
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return raise_status(500, '后台异常')
    return jsonify(data)


@projects.route('/projects', methods=['GET'])
def project_list():
    from application.project_app import project_app
    from model import PROJECT, PURCHASE
    try:
        page = int(request.args.get('page', '1'))
        pageSize = int(request.args.get('pageSize', '20'))
        if request.args.get('id'):
            id_list = request.args['id'].replace('[', '').replace(']', '').replace(' ', ''). \
                replace("'", '').replace('"', '').split(',')
            ObjectId_list = []
            for i in id_list:
                ObjectId_list.append(ObjectId(i))
            model_list = list(PROJECT.objects.raw({'_id': {'$in': ObjectId_list}, 'delete': False}))
            project_dict = {}
            for project_model in model_list:
                project_dict[str(project_model._id)] = project_app().unfold_project(model=project_model,
                                                                                    embed=request.args.get('embed'))
                # if project_model.base is None:
                #     base = None
                # else:
                #     base = str(project_model.base._id)
                # project_dict[str(project_model._id)] = {
                #     'id': str(project_model._id),
                #     'creator': str(project_model.creator),
                #     'description': project_model.description,
                #     'title': project_model.title,
                #     'requirement': project_model.requirement,
                #     'labs': project_model.labs,
                #     'tag': project_model.tag.name,
                #     'material': project_model.material,
                #     'reference': project_model.reference,
                #     'timeConsume': project_model.timeConsume,
                #     'image': project_model.image,
                #     'base': base,
                #     'spec': project_model.spec,
                #     'createdAt': project_model.createdAt,
                #     'updatedAt': project_model.updatedAt
                # }
            return jsonify(project_dict)
        query = [ObjectId(x) for x in
                 request.args['tag'].replace('[', '').replace(']', '').replace('"', '').replace("'", '').replace(' ',
                                                                                                                 '').split(
                     ',')] if request.args.get('tag') else None
        creator = request.args.get('creator')
        querySet = {}
        if query:
            querySet['tag'] = {'$in': query}
        if creator:
            querySet['creator'] = ObjectId(creator)
        try:
            if request.args.get('all'):
                page = pageSize = None
            else:
                count = project_app(requestObj=querySet).project_count()
                if count % pageSize == 0:
                    totalPage = count // pageSize if count != 0 else 1
                else:
                    totalPage = (count // pageSize) + 1
                if page > totalPage:
                    return raise_status(400, '页数超出范围')
            projects_list = project_app(requestObj=querySet).project_find_all(page, pageSize)
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            return '后台异常', 500
        project_ln_list = []
        for project_model in projects_list:
            project_ln_list.append(project_app().unfold_project(model=project_model, embed=request.args.get('embed')))
        # TODO 在这里加purchase判断
        if request.args.get('tenant'):
            for project in project_ln_list:
                purchases = list(PURCHASE.objects.raw(
                    {'project': ObjectId(project['id']), 'purchaser': ObjectId(request.args.get('tenant')),
                     'delete': False}))
                if purchases == []:
                    project['purchase'] = False
                for purchase in purchases:
                    if purchase.limit > datetime.now():
                        project['purchase'] = True
                    elif purchase.limit < datetime.now() and not project.get('purchase'):
                        project['purchase'] = False
        if not request.args.get('all'):
            meta = {'page': page, 'pageSize': pageSize, 'total': count, 'totalPage': totalPage}
            returnObj = {'projects': project_ln_list, 'meta': meta}
        else:
            returnObj = {
                'projects': project_ln_list
            }
        return jsonify(returnObj)
    except Exception as e:
        logging.error('error id: %s' % i)
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return raise_status(500, '后台异常')


@projects.route('/projects/<projectId>', methods=['GET'])
def get_project(projectId):
    from application.project_app import project_app
    from model import PROJECT
    from bson import ObjectId
    # fields = request.args.get('field')
    try:
        projectId = ObjectId(projectId)
        project_app().projectId_check(projectId=projectId)
    except PROJECT.DoesNotExist:
        return raise_status(400, '无效的项目')
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return raise_status(400, '错误的ObjectId')
    requestObj = {'_id': projectId}
    project = project_app(requestObj=requestObj).project_find_one()
    data = project_app().unfold_project(model=project, embed=request.args.get('embed'))
    # if project.base == None:
    #     base = None
    # else:
    #     if request.args.get('embed'):
    #         if project.base.base is None:
    #             base_reference = None
    #         else:
    #             base_reference = str(project.base.base._id)
    #         base = {
    #             'id': str(project.base._id),
    #             'creator': str(project.base.creator),
    #             'description': project.base.description,
    #             'requirement': project.base.requirement,
    #             'title': project.base.title,
    #             'tag': project.base.tag.name,
    #             'timeConsume': project.base.timeConsume,
    #             'labs': project.base.labs,
    #             'material': project.base.material,
    #             'reference': project.base.reference,
    #             'image': project.base.image,
    #             'base': base_reference,
    #             'spec': project.base.spec,
    #             'createdAt': project.base.createdAt,
    #             'updatedAt': project.base.updatedAt
    #         }
    #     else:
    #         base = str(project.base._id)
    # data = {
    #     'id': str(project._id),
    #     'creator': str(project.creator),
    #     'description': project.description,
    #     'requirement': project.requirement,
    #     'material': project.material,
    #     'title': project.title,
    #     'tag': project.tag.name,
    #     'labs': project.labs,
    #     'reference': project.reference,
    #     'timeConsume': project.timeConsume,
    #     'image': project.image,
    #     'base': base,
    #     'spec': project.spec,
    #     'createdAt': project.createdAt,
    #     'updatedAt': project.updatedAt
    # }
    return jsonify(data)


@projects.route('/projects/<projectId>', methods=['PUT'])
def project_replace(projectId):
    # from application.project_app import project_app
    # from model import PROJECT
    # from bson import ObjectId

    return '请改用PATCH接口', 400
    # try:
    #     projectId = ObjectId(projectId)
    #     project_app().projectId_check(projectId=projectId)
    # except PROJECT.DoesNotExist:
    #     return raise_status(400, '无效的项目')
    # except Exception as e:
    #     logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
    #     return raise_status(400, '错误的ObjectId')
    # requestObj = {'_id': projectId}
    # updateObj = request.json
    # query_list = ['creator', 'title', 'description', 'requirement', 'timeConsume',
    #               'material', 'reference', 'image', 'base', 'spec', 'tag']
    # updateObj = filter(query_list=query_list, updateObj=updateObj)
    # if updateObj.get('id'):
    #     del updateObj['id']
    # try:
    #     if updateObj.get('base') and updateObj.get('base') is not None:
    #         updateObj['base'] = ObjectId(updateObj['base'])
    #         project_app().project_reference_check(reference=updateObj['base'])
    # except PROJECT.DoesNotExist:
    #     return raise_status(400, '引用错误')
    # try:
    #     project_app(requestObj=requestObj, updateObj=updateObj).project_update_set()
    #     project = project_app(requestObj=requestObj).project_find_one()
    # except Exception as e:
    #     logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
    #     return '后台异常', 500
    # returnObj = project_app().unfold_project(model=project, embed=request.args.get('embed'))
    # # if project._id == project.base:
    # #     baseId = None
    # # else:
    # #     if project.base is None:
    # #         baseId = project.base
    # #     else:
    # #         baseId = str(project.base._id)
    # # returnObj = {
    # #     'id': str(project._id),
    # #     'creator': str(project.creator),
    # #     'title': project.title,
    # #     'description': project.description,
    # #     'requirement': project.requirement,
    # #     'material': project.material,
    # #     'labs': project.labs,
    # #     'tag': project.tag.name,
    # #     'timeConsume': project.timeConsume,
    # #     'reference': project.reference,
    # #     'image': project.image,
    # #     'base': baseId,
    # #     'spec': project.spec,
    # #     'createdAt': project.createdAt,
    # #     'updatedAt': project.updatedAt
    # # }
    # return jsonify(returnObj)


@projects.route('/projects/<projectId>', methods=['PATCH'])
def project_change(projectId):
    from application.project_app import project_app
    from model import PROJECT
    from bson import ObjectId

    # 校验projectid是否有异常
    try:
        projectId = ObjectId(projectId)
        project_app().projectId_check(projectId=projectId)
    except PROJECT.DoesNotExist:
        return '实验已删除', 400
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return '后台异常', 500
    requestObj = {'_id': projectId}
    updateObj = request.json
    logging.info('updateObj: %s' % str(updateObj))
    query_list = ['title', 'description', 'requirement', 'timeConsume',
                  'material', 'reference', 'image', 'base', 'spec', 'tag']
    updateObj = filter(query_list=query_list, updateObj=updateObj, ObjectId_list=['tag', 'image'])
    if updateObj.get('id'):
        del updateObj['id']
    try:
        if updateObj.get('base') and updateObj.get('base') != projectId:
            updateObj['base'] = ObjectId(updateObj['base'])
            project_app().project_reference_check(reference=updateObj['base'])
    except PROJECT.DoesNotExist:
        return '实验已被删除', 400
    try:
        # 更新index.json
        if updateObj.get('spec'):
            git_list = updateObj['spec'].split('/')
            git_account = git_list[3] + '/'
            repoName = git_list[4][:-4]
            repo = git_list[4][: -4] + '/'
            url = 'https://raw.githubusercontent.com/' + git_account + repo + 'master/index.json'
            r = requests.get(url=url)
            if r.status_code == 200:
                labs = r.json()['labs']
                lab_list = []
                for lab in labs:
                    index = str(labs.index(lab)) if labs.index(lab) >= 10 else '0' + str(labs.index(lab))
                    key_list = list(lab.keys())
                    value_list = list(lab.values())
                    lab_list.append({
                        'id': str(projectId) + index,
                        'filename': key_list[0],
                        'name': value_list[0]
                    })
                updateObj['labs'] = lab_list
            else:
                return 'github异常', 400
            updateObj['repoName'] = repoName
        # logging.info('updateObj: %s' % str(updateObj))
        project_app(requestObj=requestObj, updateObj=updateObj).project_update_set()
        project = project_app(requestObj=requestObj).project_find_one()
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return '后台异常', 500
    returnObj = project_app().unfold_project(model=project, embed=request.args.get('embed'))
    # if project._id == project.base:
    #     baseId = None
    # else:
    #     baseId = str(project.base._id)
    # returnObj = {
    #     'id': str(project._id),
    #     'creator': str(project.creator),
    #     'title': project.title,
    #     'description': project.description,
    #     'requirement': project.requirement,
    #     'material': project.material,
    #     'reference': project.reference,
    #     'tag': project.tag.name,
    #     'labs': project.labs,
    #     'timeConsume': project.timeConsume,
    #     'image': project.image,
    #     'base': baseId,
    #     'spec': project.spec,
    #     'createdAt': project.createdAt,
    #     'updatedAt': project.updatedAt
    # }
    return jsonify(returnObj)


@projects.route('/projects/<projectId>', methods=['DELETE'])
def project_delete(projectId):
    from application.project_app import project_app
    from model import PROJECT
    from auth import raise_status
    from bson import ObjectId

    try:
        projectId = ObjectId(projectId)
        project_app().projectId_check(projectId=projectId)
        requestObj = {'_id': projectId}
        project_app(requestObj=requestObj).project_delete()
    except PROJECT.DoesNotExist:
        return raise_status(400, '无效的项目')
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return jsonify({'error': raise_status(400, '错误的ObjectId')})
    return raise_status(200)


# 获取分类列表
@projects.route('/tag', methods=['GET'])
def project_tag():
    from model import CATEGORY, TYPE, PROJECT
    try:
        category_model_list = list(CATEGORY.objects.raw({'delete': False}))
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return raise_status(500, '后台异常')
    tag_list = []
    for model in category_model_list:
        category = {'id': str(model._id), 'category': model.name}
        try:
            type_list = list(TYPE.objects.raw({'category': model._id, 'delete': False}))
        except Exception as e:
            logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
            return raise_status(500, '后台异常')
        tag = []
        for type_model in type_list:
            count = PROJECT.objects.raw({'tag': type_model._id, 'delete': False}).count()
            tag.append({
                'id': str(type_model._id),
                'name': type_model.name,
                'count': count
            })
        category['type'] = tag
        tag_list.append(category)
    return jsonify(tag_list)


@projects.route('/projects/management', methods=['GET'])
def project_management():
    from application.project_app import project_app
    from model import PURCHASE
    sort = request.args.get('sort', [])
    search = request.args.get('search', [])
    filt = request.args.get('filter')
    status = request.args.get('all')
    page = int(request.args.get('page', 1)) if not status else None
    pageSize = int(request.args.get('pageSize', 20)) if not status else None
    tenant = request.args.get('tenant')
    order = ()
    for x in sort:
        order += [x, 1]
    requestObj = {}
    for x in search:
        requestObj = dict(requestObj, **x)
    # 存在过滤数组
    if filt:
        requestObj['_id'] = {'$nin': [ObjectId(x) for x in filt]}
    # 此时总数已经考虑了过滤数组
    try:
        count = project_app(requestObj=requestObj).project_count()
        model_list = project_app(requestObj=requestObj).project_find_many_by_order(page=page, pageSize=pageSize,
                                                                                   order=order)
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return '后台异常', 500
    # 只返回需要数据，_id、title、creator
    returnObj = []
    for model in model_list:
        # TODO 可以改成first方法
        purchases = list(PURCHASE.objects.raw({'purchaser': ObjectId(tenant), 'project': model._id, 'delete': False}))
        deadline = None
        # 只选取最晚的limit
        for purchase in purchases:
            if not deadline or purchase.limit > deadline:
                deadline = purchase.limit
        returnObj.append({
            'id': str(model._id),
            'title': model.title,
            'creator': str(model.creator),
            'limit': deadline
        })
    return jsonify({'count': count, 'returnObj': returnObj})


# 获取镜像列表
@projects.route('/image', methods=['GET'])
def project_image():
    from model import IMAGE
    from application.project_app import project_app
    try:
        model_list = list(IMAGE.objects.raw({'delete': False}))
        return_list = []
        for model in model_list:
            return_list.append(project_app().unfold_image(model=model))
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return '后台异常', 500
    return jsonify(return_list)


# 获取购买列表
@projects.route('/purchase', methods=['GET'])
def purchase_get():
    from model import PURCHASE
    from application.project_app import project_app
    tenant = request.args.get('tenant')
    try:
        purchase_model = list(PURCHASE.objects.raw({'purchaser': ObjectId(tenant), 'delete': False}))
        purchase_list = []
        for purchase in purchase_model:
            purchase_list.append(project_app().unfold_purchase(model=purchase, embed=request.args.get('embed')))
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return '后台异常', 500
    return jsonify(purchase_list)


@projects.route('/purchase', methods=['POST'])
def purchase_post():
    from model import PURCHASE
    from datetime import datetime
    from application.project_app import project_app
    # TODO 还需考虑上传的是个列表
    requestObj = request.json
    query_list = ['purchaser', 'limit', 'project', 'remark']
    requestObj = filter(query_list=query_list, updateObj=requestObj, ObjectId_list=['project', 'purchaser'])
    try:
        model = PURCHASE(
            purchaser=requestObj['purchaser'],
            limit=datetime.strptime(requestObj['limit'].replace('T', ' '), '%Y-%m-%d %H:%M:%S'),
            project=requestObj['project'],
            remark=requestObj.get('remark'),
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
            delete=False
        ).save()
        purchase = project_app().unfold_purchase(model)
    except Exception as e:
        logging.error('Request Error: {}\nStack: {}\n'.format(e, traceback.format_exc()))
        return '后台异常', 500
    return jsonify(purchase)
