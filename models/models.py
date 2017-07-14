# -*- coding: utf-8 -*-
from openerp import fields,api,exceptions,models
from myaddons.assets_manage.functions import func

class equipment_info(models.Model):
    _name ='assets_management.equipment_info'
    _rec_name = 'sn'    #上标题显示信息

    sn = fields.Char(string=u"序列号", required=True)
    firms = fields.Char(string=u"设备厂商", required=True)
    # device_name = fields.Char(string="设备名称", )
    device_type = fields.Char(string=u"设备类型", required=True)
    # asset_number = fields.Char(string=u"资产编号", )
    unit_type = fields.Char(string=u"设备型号", required=True)
    equipment_source = fields.Char(string=u"设备来源", required=True)
    # equipment_status = fields.Selection([
    #     (u'完好', u'完好'),
    #     (u'故障', u'故障'),
    #     # (u'库存', u"库存"),
    #     # (u'故障', u"故障"),
    #     # (u'专用', u"专用"),
    #     # (u'待报废', u"待报废"),
    #     # (u'暂存', u"暂存"),
    # ], string=u"设备可用性", required=True)
    equipment_use = fields.Selection([
        (u'公共备件', u"公共备件"),
        (u'专用备件', u"专用备件"),
        (u'故障件', u"故障件"),
        (u'待报废', u"待报废"),
        (u'暂存设备', u"暂存设备"),
    ], string=u"设备用途", required=True,default=u'公共备件')
    # dev_state = fields.Char(string='设备状态', default=u'待入库',readonly=True)
    state = fields.Selection(
        [('toSubmit',u'待提交'),('haveSubmit',u'已提交')],
        readonly=True,string='提交状态',default='toSubmit'
    )
    dev_state = fields.Selection([
        (u'待入库', u'待入库'),
        (u'库存', u'库存'),
        (u'流程中', u'流程中'),
        (u'领用', u'领用'),
        (u'借用', u'借用'),
        # (u'IT环境', u'IT环境'),
        (u'归还', u'归还'),
    ], string='状态', default=u'待入库',readonly=True)
    owner = fields.Many2one('res.users', string=u"归属人", required=True)
    company = fields.Boolean(string=u"是否公司资产")
    note = fields.Char(string=u"备注")
    area = fields.Char(string=u"存放地址")

    floor = fields.Char(string=u"库房楼层")
    cabinet_number = fields.Char(string=u"货架编号")
    seat = fields.Char(string=u"货架位置")
    # machine_room = fields.Char(string=u"存放机房")
    # start_u_post = fields.Char(string=u"起始U位")

    # 增加第二个参数和不增加第二个参数意义是不一样的，必须始终如一使用一种,经过测试和odoo10不一样，必须带第二个参数，否则报错误
    storage_id = fields.Many2many('assets_management.equipment_storage', "i_storge_equipment_ref", )
    # storage_id = fields.Many2many('assets_management.equipment_storage', "storge_equipment_ref", )
    # storage_id = fields.Many2many('assets_management.equipment_storage', )
    # get_ids = fields.Many2many('asset_management.equipment_get', "i_get_equipment_ref", )
    # lend_ids = fields.Many2many('asset_management.equipment_lend', "i_lend_equipment_ref", )
    # apply_ids = fields.Many2many('asset_management.equipment_it_apply', "i_it_equipment_ref", )
    user_id = fields.Many2one('res.users', string='创建人', default=lambda self: self.env.user)

    # New Add
    bar_code = fields.Char(string=u"条码号", required=True)
    got_count = fields.Integer(string=u"领用次数", readonly=True)
    lend_count = fields.Integer(string=u"借用次数", readonly=True)
    devUse_user_id = fields.Many2one('res.users', string='设备使用人', default=None)  # 领用、借用

    _sql_constraints = [
        ('SN UNIQUE',
         'UNIQUE(sn)',
         '该序列号已存在'),
    ]

    # 重写父类的create函数
    def create(self, cr, uid, vals, context=None):
        vals['state'] = 'haveSubmit'
        return super(equipment_info, self).create(cr, uid, vals, context=context)

class equipment_storage(models.Model):
    _name = 'assets_management.equipment_storage'
    _rec_name = 'storage_id'
    _inherit = ['ir.needaction_mixin']

    @api.model
    def _needaction_domain_get(self):
        return [('approver_id.id', '=', self.env.uid)]

    @api.multi
    def _default_SN(self):
        return self.env['assets_management.equipment_info'].search([('dev_state', '=', u'待入库'),('user_id', '=', self.env.uid)])

    storage_id = fields.Char(string=u"入库单号")
    user_id = fields.Many2one('res.users', string=u"申请人",default=lambda self: self.env.user, required=True)
    approver_id = fields.Many2one('res.users', string=u"审批人",default=lambda self: self.env.user,)
    # SN = fields.Char()
    purpose = fields.Char(string=u"目的")
    purpose_compute = fields.Char(string=u"目的",compute="_purpose_compute")
    SN = fields.Many2many('assets_management.equipment_info',"i_storge_equipment_ref",string=u"设备SN",required=True,default=_default_SN,)
    # SN = fields.Many2many('assets_management.equipment_info', "storge_equipment_ref", string=u"设备SN", required=True,
    #                       default=_default_SN, )
    opinion = fields.Char(string=u"审批意见")       #每次保存时清空，用于显示
    opinion_bak = fields.Char(string=u"审批意见")   #实际审批意见，用于校验
    approve_flag = fields.Boolean(string=u"同意或者不同意标识",default=True) #False，不同意 True 同意

    state = fields.Selection([
        ('demander', u"提交人"),
        ('ass_admin', u"备件管理员审核"),
        ('owner', u"资产归属人审核"),
        ('ass_admin_manager', u"备件管理团队领导审批"),
        ('ass_admin_detection', u"备件管理员检测确认"),
        ('done',u'完成'),
        # ('cancel',u'已作废'),
    ],string=u"状态",required=True,default='demander')
    owners = fields.Many2many('res.users', string=u'设备归属人', ondelete='set null')
    store_exam_ids = fields.One2many('assets_management.entry_store_examine', 'store_id', string='审批记录')


    curApproveUser = fields.Char(string='当前处理人',default=lambda self: self.env.user.name,readonly=True)
    curApproveUserID = fields.Char(string='当前处理人ID', default=lambda self: self.env.user.id)
    # user_toApprove = fields.Many2many('res.users',"i_storge_equipment_toApprove_ref")       #当前环节待审批的人员
    # user_haveApprove = fields.Many2many('res.users',"i_storge_equipment_haveApprove_ref")   #所有环节已经审批的人员
    user_toApprove = fields.Many2many('res.users')  # 当前环节待审批的人员    弃用
    user_haveApprove = fields.Many2many('res.users')  # 所有环节已经审批的人员 弃用

    user_toApproveChar = fields.Char(string='当前环节审批人员ID')  # 当前环节待审批的人员
    user_haveApproveChar = fields.Char(string='所有环节审批人员ID')  # 所有环节已经审批的人员

    if_invisible = fields.Boolean(string='当前环节审批人员是否可见')
    curlogUser = fields.Char(string='当前登录人员',compute="_curlogUser")

    def _curlogUser(self):
        self.curlogUser = self.env.user.id

    def _purpose_compute(self):
        self.purpose_compute = self.purpose

    @api.constrains('SN')
    def _checkDevOwnersUnique(self):
        print '-----------------_checkDevOwnersUnique-----------------'
        for dev in self.SN:
            self.owners |= dev.owner
        # print '&&&&&&&&&&&&&&&& self.owners&&&&&&&&&&&&'
        # print self.owners
        if len(self.owners) > 1:
            raise exceptions.ValidationError("The SN's owner must be only one,please reselect SN!")

    @api.constrains('opinion_bak')
    def _checkDisagree(self):
        print '-----------------_checkDisagree-----------------'

        if self.approve_flag == False:
            # self.opinion_bak = self.opinion
            if self.opinion_bak == '':
                raise exceptions.ValidationError("Please enter the opinion!")

    # 重写父类的create函数
    def create(self, cr, uid, vals, context=None):
        print cr
        print uid
        print vals
        print context
        # 创建 设备信息对象---计算设备信息的SN号
        print '============================创建时的操作==================='
        # print   "-----create----"
        template_model = self.pool.get('assets_management.equipment_info')
        # print  vals['SN']
        # print  vals['SN'][0][2]
        devices = template_model.browse(cr, uid, vals['SN'][0][2], context=None)
        print len(devices)
        for device in devices:
            device.dev_state = u'流程中'
        #     print device.dev_state
        # print  fields.Date.today()
        dates = fields.Date.today().split('-')
        # print dates
        date = ''.join(dates)
        # print date
        # 查找当天提交的设备入库SN号的最大值，同时在最大值基础上+1
        template_model = self.pool.get('assets_management.equipment_storage')
        ids = template_model.search(cr, uid, [('storage_id', 'like', date)], context=None)
        stores = template_model.browse(cr, uid, ids, context=None).sorted(key=lambda r: r.storage_id)
        # print len(stores)
        if len(stores):
            # print 'len >= 1 '
            # print int(stores[-1].storage_id[1:])
            vals['storage_id'] = 'S' + str(int(stores[-1].storage_id[1:]) + 1)
        else:
            # print 'new lenth'
            vals['storage_id'] = 'S' + date + '001'

        return super(equipment_storage, self).create(cr, uid, vals, context=context)

    #0.返回动态action_window，每一个审批操作完成后，重新返回到入库代办界面。后续每一个审批操作都调用此函数
    @api.multi
    def get_todo_assets_storing(self):
        mod_obj = self.pool.get('ir.model.data')
        if mod_obj:
            #必须增加 【assets_manage.】否则在数据库中无法找到 action
            result = mod_obj.xmlid_to_res_id(self.env.cr, self.env.uid, 'assets_manage.toDo_assets_storing_action')
            act_obj = self.pool.get('ir.actions.act_window')
            if result:
                result = act_obj.read(self.env.cr, self.env.uid, [result], context=self._context)[0]
                # result['domain'] = "[('id','in',[" + ','.join(map(str, route_ids)) + "])]"
            else:
                # print 'nothing'
                result = []
        else:
            result = []
        return result

    # 1.申请人【提交】操作
    @api.multi
    def action_appUser_submit(self):
        print '=======申请人【提交】操作======'
        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.计算设备所有人，并进行记录
        for sn in(self.SN):
            # print sn.dev_state
            self.owners |= sn.owner
        # print self.owners

        #3.设备归属人只有一个的情况，多个归属人暂时没有处理
        int_len = len(self.owners)
        if int_len == 1:
            self.state = 'ass_admin'

            # 4.创建审批流程日志文档
            self.env['assets_management.entry_store_examine'].create(
                {'approver_id': self.approver_id.id, 'result': u'submit', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

            # print self.env['res.groups'].search([('name', '=', u'资产管理员')], limit=1)     #返回值：res.groups(46,)
            # print self.env['res.groups'].search([('name', '=', u'资产管理员')],limit=1).users[0] #返回值：res.users(8,)


            # 5.将下一个审批人员加入到相关字段中
            nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')],limit=1).users[0]
            self.curApproveUser = str(nextAppuser.name)
            self.curApproveUserID = str(nextAppuser.id)
            self.user_toApproveChar = nextAppuser.id
            self.user_haveApproveChar = str(self.env.uid)

            # 6.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
            self.approver_id = nextAppuser

    # 2-1.资产管理员【同意】操作
    @api.multi
    def action_store_ass_admin_agree(self):
        self.state = 'owner'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.owners

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)
        if lenth > 1:
            for user in nextAppuser:
                if strUserName == "":
                    strUserName = str(user.name)
                    strUserID = str(user.id)
                else:
                    strUserName = strUserName + ',' + str(user.name)
                    strUserID = strUserID + ',' + str(user.id)

            self.curApproveUser = str(strUserName)
            self.curApproveUserID = str(strUserID)

            self.user_toApproveChar = ''
            self.user_toApproveChar = str(strUserID)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar,str(strUserID))
        elif lenth == 1:
            self.curApproveUser = str(nextAppuser.name)
            self.curApproveUserID = str(nextAppuser.id)
            self.user_toApproveChar = str(nextAppuser.id)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar,str(nextAppuser.id))
        else:
            self.user_toApprove = None
        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #5.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

    # 2-2.资产管理员【退回】操作
    @api.multi
    def action_store_ass_admin_disagree(self):
        print '===================资产管理员退回========='
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #4.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

    # 3-1.资产归属人【同意】操作
    @api.multi
    def action_store_owners_agree(self):
        self.state = 'ass_admin_manager'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'submit', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理团队领导')],limit=1).users[0]

        # 4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)
        if lenth > 1:
            for user in nextAppuser:
                if strUserName == "":
                    strUserName = str(user.name)
                    strUserID = str(user.id)
                else:
                    strUserName = strUserName + ',' + str(user.name)
                    strUserID = strUserID + ',' + str(user.id)

            self.curApproveUser = str(strUserName)
            self.curApproveUserID = str(strUserID)

            self.user_toApproveChar = ''
            self.user_toApproveChar = str(strUserID)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar,str(strUserID))
        elif lenth == 1:
            self.curApproveUser = str(nextAppuser.name)
            self.curApproveUserID = str(nextAppuser.id)
            self.user_toApproveChar = str(nextAppuser.id)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar,str(nextAppuser.id))
        else:
            self.user_toApprove = None

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #5.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

    # 3-2.资产归属人【退回】操作
    @api.multi
    def action_store_owners_disagree(self):
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #4.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

    # 4-1.MA部门主管【同意】操作
    @api.multi
    def action_store_MA_manager_agree(self):
        self.state = 'ass_admin_detection'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        # 4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)
        if lenth > 1:
            for user in nextAppuser:
                if strUserName == "":
                    strUserName = str(user.name)
                    strUserID = str(user.id)
                else:
                    strUserName = strUserName + ',' + str(user.name)
                    strUserID = strUserID + ',' + str(user.id)

            self.curApproveUser = str(strUserName)
            self.curApproveUserID = str(strUserID)

            self.user_toApproveChar = ''
            self.user_toApproveChar = str(strUserID)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar, str(strUserID))
        elif lenth == 1:
            self.curApproveUser = str(nextAppuser.name)
            self.curApproveUserID = str(nextAppuser.id)
            self.user_toApproveChar = str(nextAppuser.id)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar, str(nextAppuser.id))
        else:
            self.user_toApprove = None

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #5.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

    # 4-2.MA部门主管【退回】操作
    @api.multi
    def action_store_MA_manager_disagree(self):
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #4.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

    # 5-1.资产管理员检测【同意】操作
    @api.multi
    def action_store_admin_detec_agree(self):
        self.state = 'done'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        # 4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)
        if lenth > 1:
            for user in nextAppuser:
                if strUserName == "":
                    strUserName = str(user.name)
                    strUserID = str(user.id)
                else:
                    strUserName = strUserName + ',' + str(user.name)
                    strUserID = strUserID + ',' + str(user.id)

            self.curApproveUser = str(strUserName)
            self.curApproveUserID = str(strUserID)

            self.user_toApproveChar = ''
            self.user_toApproveChar = str(strUserID)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar, str(strUserID))
        elif lenth == 1:
            self.curApproveUser = str(nextAppuser.name)
            self.curApproveUserID = str(nextAppuser.id)
            self.user_toApproveChar = str(nextAppuser.id)
            self.user_haveApproveChar = func.strPlus(self.user_haveApproveChar, str(nextAppuser.id))
        else:
            self.user_toApprove = None

        #5.将入库设备状态更新为【库存】
        devs = self.SN
        for dev in devs:
            dev.dev_state = u'库存'

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #6.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

    # 5-2.资产管理员检测【退回】操作
    @api.multi
    def action_store_admin_detec_disagree(self):
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state': lambda self:fields.Datetime.now(),'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #4.返回到代办tree界面
        treeviews = self.get_todo_assets_storing()
        return treeviews

class entry_store_examine(models.Model):
    _name='assets_management.entry_store_examine'
    # _rec_name = 'exam_num'

    # exam_num = fields.Char(sting='审批id')
    approver_id = fields.Many2one('res.users',required = 'True',string='审批人')
    date = fields.Datetime(string='审批时间',default=lambda self:fields.Datetime.now())
    result=fields.Selection([
                               (u'agree', u"通过"),
                               (u'disagree', u"拒绝"),
                               (u'submit', u"提交"),
                               (u'callback', u"收回"),
                                ],string=u"操作")
    store_id = fields.Many2one('assets_management.equipment_storage',string='入库单')
    app_state = fields.Char(string='申请单审批时状态')
    reason = fields.Char(string='审批意见')

