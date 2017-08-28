#-*- coding:utf-8 -*-s = u
from openerp import fields,api,exceptions,models
import func
import datetime
import sys
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_DATETIME_FORMAT

reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(1000000)
class equipment_info(models.Model):
    _name ='assets_management.equipment_info'
    _rec_name = 'sn'    #上标题显示信息

    sn = fields.Char(string=u"序列号", required=True)
    firms = fields.Char(string=u"设备厂商", required=True)
    # device_name = fields.Char(string="设备名称", )
    device_type = fields.Char(string=u"设备类型", required=True)
    # asset_number = fields.Char(string=u"资产编号", )
    unit_type = fields.Char(string=u"设备型号", required=True)
    equipment_source = fields.Char(string=u"设备来源")
    equipment_use = fields.Selection([
        (u'公共备件', u"公共备件"),
        (u'专用备件', u"专用备件"),
        (u'实验室', u"实验室"),
        # (u'故障件', u"故障件"),
        # (u'待报废', u"待报废"),
        # (u'暂存设备', u"暂存设备"),
    ], string=u"设备用途", required=True,default=u'公共备件')
    # dev_state = fields.Char(string='设备状态', default=u'待入库',readonly=True)
    state = fields.Selection(
        [('toSubmit',u'待提交'),('haveSubmit',u'已提交')],
        readonly=True,string=u'提交状态',default='toSubmit'
    )
    dev_state = fields.Selection([
        (u'待入库', u'待入库'),
        (u'库存', u'库存'),
        (u'流程中', u'流程中'),
        (u'领用', u'领用'),
        (u'借用', u'借用'),
        # (u'IT环境', u'IT环境'),
        (u'归还', u'归还'),
    ], string=u'状态', default=u'待入库')
    owner = fields.Many2one('res.users', string=u"归属人", required=True)
    # owner_compute =
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
    get_ids = fields.Many2many('assets_management.equipment_get', "i_get_equipment_ref", )
    lend_ids = fields.Many2many('assets_management.equipment_lend', "i_lend_equipment_ref", )
    back_ids = fields.Many2many('assets_management.back_to_store', "i_back_equipment_ref", )

    user_id = fields.Many2one('res.users', string=u'创建人', default=lambda self: self.env.user)

    # New Add
    store_flag = fields.Char(string=u"是否正在入库标识", readonly=True, default='0')   #是否正在入库标识，默认为0，正在入库标识为入库请求单的请求号，入库完毕更新为0
    bar_code = fields.Char(string=u"条码号")

    got_count = fields.Integer(string=u"领用次数", readonly=True)
    lend_count = fields.Integer(string=u"借用次数", readonly=True)
    devUse_user_id = fields.Many2one('res.users', string=u'设备使用人', default=None)  # 领用、借用
    dev_integrality = fields.Selection(
        [('OK', u'完好'), ('Destroyed', u'损坏')],
        string=u'设备完整性', default="OK"
    )
    #是否借用、领用成功,在借用成功后可以显示归还按钮，在领用成功后显示 再入库 按钮
    use_state =  fields.Selection(
        [('haveLent',u'已借用'),('haveGet',u'已领用'),
         ('Lending', u'借用中'), ('Getting', u'领用中'),
         ('Backing', u'归还中'), ('haveBack', u'已归还'),
         ('none',u'none')],
        readonly=True,string=u'是否借用、领用成功', default="none"
    )

    #控制非编辑人员不可编辑 主要入库用到
    can_edit = fields.Boolean(string=u'button操作：当前操作人员是否是否可以编辑',default=True)

    # 因使用ReadOnly无效，使用如下计算字段控制用户无法编辑请求中申请的设备信息
    sn_compute = fields.Char(string=u"序列号", compute="_dev_compute")
    firms_compute = fields.Char(string=u"设备厂商", compute="_dev_compute")
    device_type_compute = fields.Char(string=u"设备类型", compute="_dev_compute")
    unit_type_compute = fields.Char(string=u"设备型号", compute="_dev_compute")
    equipment_source_compute = fields.Char(string=u"设备来源", compute="_dev_compute")
    equipment_use_compute = fields.Char(string=u"设备用途", compute="_dev_compute")
    company_compute = fields.Boolean(string=u"是否公司资产", compute="_dev_compute")
    note_compute = fields.Char(string=u"备注", compute="_dev_compute")
    area_compute = fields.Char(string=u"存放地址", compute="_dev_compute")
    floor_compute = fields.Char(string=u"库房楼层", compute="_dev_compute")
    cabinet_number_compute = fields.Char(string=u"货架编号", compute="_dev_compute")
    seat_compute = fields.Char(string=u"货架位置", compute="_dev_compute")
    bar_code_compute = fields.Char(string=u"条码号", compute="_dev_compute")
    owner_compute = fields.Many2one('res.users', string=u"归属人", compute="_dev_compute")
    dev_state_compute = fields.Selection([
        (u'待入库', u'待入库'),
        (u'库存', u'库存'),
        (u'流程中', u'流程中'),
        (u'领用', u'领用'),
        (u'借用', u'借用'),
        # (u'IT环境', u'IT环境'),
        (u'归还', u'归还'),
    ], string=u'状态',readonly=True,compute="_dev_compute")
    dev_integrality_compute =  fields.Selection(
        [('OK', u'完好'), ('Destroyed', u'损坏')],
        string=u'设备完整性', default="OK",readonly = True
    )
    note_compute = fields.Char(string=u"备注")

    def _dev_compute(self):
        for dev in self:
            dev.sn_compute = dev.sn
            dev.firms_compute = dev.firms
            dev.device_type_compute = dev.device_type
            dev.unit_type_compute = dev.unit_type
            dev.equipment_source_compute = dev.equipment_source
            dev.equipment_use_compute = dev.equipment_use
            dev.company_compute = dev.company
            dev.note_compute = dev.note
            dev.area_compute = dev.area
            dev.floor_compute = dev.floor
            dev.cabinet_number_compute = dev.cabinet_number
            dev.seat_compute = dev.seat
            dev.bar_code_compute = dev.bar_code
            dev.owner_compute = dev.owner
            dev.dev_state_compute = dev.dev_state
            dev.dev_integrality_compute = dev.dev_integrality
            dev.note_compute = dev.note
        # self.sn_compute = self.sn
        # self.firms_compute = self.firms
        # self.device_type_compute = self.device_type
        # self.unit_type_compute = self.unit_type
        # self.equipment_source_compute = self.equipment_source
        # self.equipment_use_compute = self.equipment_use
        # self.company_compute = self.company
        # self.note_compute = self.note
        # self.area_compute = self.area
        # self.floor_compute = self.floor
        # self.cabinet_number_compute = self.cabinet_number
        # self.seat_compute = self.seat
        # self.bar_code_compute = self.bar_code
        # self.owner_compute = self.owner
        # self.dev_state_compute = self.dev_state
        # self.dev_integrality_compute = self.dev_integrality
        # self.note_compute = self.note
    # @api.constrains('user_editID')
    # def _checkCanEdit(self):
    #     print '-----------------_checkCanEdit - ----------------'
    #     flag = False
    #     ids = str(self.user_editID).split(',')
    #     for id in ids:
    #         if str(self.env.user.id) == id:
    #             flag = True
    #             break
    #     if flag == False:
    #         raise exceptions.ValidationError("Can not Edit !")
    _sql_constraints = [
        ('SN UNIQUE',
         'UNIQUE(sn)',
         u'该序列号已存在'),
    ]

    # 重写父类的create函数
    def create(self, cr, uid, vals, context=None):
        vals['state'] = 'haveSubmit'
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
        return self.env['assets_management.equipment_info'].browse(self._context.get('active_ids'))
        # return self.env['assets_management.equipment_info'].search([('dev_state', '=', u'待入库'),('user_id', '=', self.env.uid)])

    storage_id = fields.Char(string=u"入库单号")
    user_id = fields.Many2one('res.users', string=u"申请人",default=lambda self: self.env.user, required=True)
    approver_id = fields.Many2one('res.users', string=u"审批人",default=lambda self: self.env.user,)
    # SN = fields.Char()
    purpose = fields.Char(string=u"目的",required=True)
    purpose_compute = fields.Char(string=u"目的",compute="_purpose_compute")
    SN = fields.Many2many('assets_management.equipment_info',"i_storge_equipment_ref",string=u"设备SN",required=True,default=_default_SN,)
    # SN = fields.Many2many('assets_management.equipment_info', "storge_equipment_ref", string=u"设备SN", required=True,
    #                       default=_default_SN, )
    opinion = fields.Char(string=u"审批意见")       #每次保存时清空，用于显示
    opinion_bak = fields.Char(string=u"审批意见")   #实际审批意见，用于校验
    approve_flag = fields.Boolean(string=u"同意或者不同意标识",default=True) #False，不同意 True 同意

    state = fields.Selection([
        ('demander', u"提交人"),
        ('ass_admin', u"资产管理员审批"),
        ('owner', u"资产归属人审批"),
        ('ass_admin_manager', u"资产管理领导审批"),
        ('ass_admin_detection', u"资产管理员检测确认"),
        ('done',u'完成'),
        # ('cancel',u'已作废'),
    ],string=u"状态",required=True,default='demander')
    owners = fields.Many2many('res.users', string=u'设备归属人', ondelete='set null')
    store_exam_ids = fields.One2many('assets_management.entry_store_examine', 'store_id', string=u'审批记录')


    curApproveUser = fields.Char(string=u'当前处理人',default=lambda self: self.env.user.name,readonly=True)
    curApproveUserID = fields.Char(string=u'当前处理人ID', default=lambda self: self.env.user.id)
    # user_toApprove = fields.Many2many('res.users',"i_storge_equipment_toApprove_ref")       #当前环节待审批的人员
    # user_haveApprove = fields.Many2many('res.users',"i_storge_equipment_haveApprove_ref")   #所有环节已经审批的人员
    user_toApprove = fields.Many2many('res.users')  # 当前环节待审批的人员    弃用
    user_haveApprove = fields.Many2many('res.users')  # 所有环节已经审批的人员 弃用

    user_toApproveChar = fields.Char(string=u'当前环节审批人员ID')  # 当前环节待审批的人员
    user_haveApproveChar = fields.Char(string=u'所有环节审批人员ID')  # 所有环节已经审批的人员

    if_invisible = fields.Boolean(string=u'当前环节审批人员是否可见')
    curlogUser = fields.Char(string=u'当前登录人员',compute="_curlogUser")

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
            raise exceptions.ValidationError(u"所选取的设备归属人必须唯一!")

    @api.constrains('opinion_bak')
    def _checkDisagree(self):
        print '-----------------_checkDisagree-----------------'

        if self.approve_flag == False:
            # self.opinion_bak = self.opinion
            if self.opinion_bak == '':
                raise exceptions.ValidationError(u"请输入意见!")

    # 重写父类的create函数
    def create(self, cr, uid, vals, context=None):
        # print cr
        # print uid
        # print vals
        # print context

        #获取当前的action ，通过context方式
        # context_1 = dict(context)
        action_id = context.get(u'params').get(u'action')
        action_template_model = self.pool.get('ir.actions.actions')
        print action_template_model
        # action_ids = action_template_model.search(cr, uid, [('id', '=', action_id)], context=None)
        action_stores = action_template_model.browse(cr, uid, action_id, context=None)

        # print action_id
        # print action_stores
        # print action_stores.name

        # 创建 设备信息对象---计算设备信息的SN号
        print '============================创建时的操作==================='
        # print   "-----create----"
        template_model = self.pool.get('assets_management.equipment_info')
        # print  vals['SN']
        # print  vals['SN'][0][2]
        devices = template_model.browse(cr, uid, vals['SN'][0][2], context=None)
        # print len(devices)
        #入库时所选设备状态必须为待入库状态，由于领用有再入库功能，再入库的情况特殊处理
        for device in devices:
            if action_stores.name != u'我领用的设备':
                if device.dev_state != '待入库':
                    raise exceptions.ValidationError("正在入库，所选设备状态必须为【待入库】")
                    break
            device.dev_state = u'流程中'
            device.can_edit = True

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
        #避免入库设备被退回时显示‘待入库’状态而被再次建立入库请求时特殊处理
        for device in devices:
            if device.store_flag <> '0' and device.store_flag <> vals['storage_id']:
                raise exceptions.Warning(u"所选设备正在入库中，无法再次入库")
                break

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

    #0-Plus 申请人关闭
    @api.multi
    def action_appUser_close(self):
        pre_state = self.state
        self.state = 'done'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': 'close', 'store_id': self.id, 'app_state': 'done',
             'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'待入库'
            dev.store_flag = '0'

            # 4.返回到代办tree界面
            # treeviews = self.get_todo_assets_storing()
            # return treeviews

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
            # if sn.dev_state <> '待入库':
            #     raise exceptions.ValidationError("设备状态必须为【待入库】")
            #     break
            self.owners |= sn.owner
            sn.can_edit = False
            if sn.store_flag == '0':
                sn.store_flag = self.storage_id
            sn.dev_state = u'流程中'

        # print self.owners

        #3.设备归属人只有一个的情况，多个归属人暂时没有处理
        int_len = len(self.owners)
        if int_len == 1:
            pre_state = self.state
            self.state = 'ass_admin'

            # 4.创建审批流程日志文档
            print sys.getdefaultencoding()
            self.env['assets_management.entry_store_examine'].create(
                {'approver_id': self.approver_id.id, 'result': 'submit', 'store_id': self.id, 'app_state':pre_state.decode('utf-8'), 'reason':self.opinion_bak})

            # 5.将下一个审批人员加入到相关字段中
            nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')],limit=1).users[0]
            # self.curApproveUser = str(nextAppuser.name)
            # self.curApproveUserID = str(nextAppuser.id)
            # self.user_toApproveChar = nextAppuser.id
            # self.user_haveApproveChar = str(self.env.uid)

            # 6.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
            self.approver_id = nextAppuser
        print '=======申请人【提交】操作 End======'

    # 2-1.资产管理员【同意】操作
    @api.multi
    def action_store_ass_admin_agree(self):
        pre_state = self.state
        self.state = 'owner'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

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

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 2-2.资产管理员【退回】操作
    @api.multi
    def action_store_ass_admin_disagree(self):
        print '===================资产管理员退回========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'待入库'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 3-1.资产归属人【同意】操作
    @api.multi
    def action_store_owners_agree(self):
        pre_state = self.state
        self.state = 'ass_admin_manager'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

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

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 3-2.资产归属人【退回】操作
    @api.multi
    def action_store_owners_disagree(self):
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.dev_state = u'待入库'
            dev.can_edit = True

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 4-1.MA部门主管【同意】操作
    @api.multi
    def action_store_MA_manager_agree(self):
        pre_state = self.state
        self.state = 'ass_admin_detection'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

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

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 4-2.MA部门主管【退回】操作
    @api.multi
    def action_store_MA_manager_disagree(self):
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.dev_state = u'待入库'
            dev.can_edit = True

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 5-1.资产管理员检测【同意】操作
    @api.multi
    def action_store_admin_detec_agree(self):
        pre_state = self.state
        self.state = 'done'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'close', 'store_id': self.id, 'app_state':'done', 'reason':''})

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

            if dev.store_flag <> '0':
                dev.store_flag = '0'

            # 5-Plus.将入库设备可编辑状态更新为 不可编辑
            dev.can_edit = False
            dev.devUse_user_id = None   #入库后，讲设备使用人员字段清空（针对于领用后又入库）

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        #6.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 5-2.资产管理员检测【退回】操作
    @api.multi
    def action_store_admin_detec_disagree(self):
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.entry_store_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'store_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        self.curApproveUser = str(nextAppuser.name)
        self.curApproveUserID = str(nextAppuser.id)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # # 3-Plus.将入库设备可编辑状态更新为 编辑
        devs = self.SN
        for dev in devs:
            dev.dev_state = u'待入库'
            dev.can_edit = True

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews
class entry_store_examine(models.Model):
    _name='assets_management.entry_store_examine'
    # _rec_name = 'exam_num'

    # exam_num = fields.Char(sting='审批id')
    approver_id = fields.Many2one('res.users',required = 'True',string=u'审批人')
    date = fields.Datetime(string=u'审批时间',default=lambda self:fields.Datetime.now())
    result=fields.Selection([
                               (u'agree', u"通过"),
                               (u'disagree', u"拒绝"),
                               (u'submit', u"提交"),
                               (u'callback', u"收回"),
                               (u'close', u"关闭"),
                                ],string=u"操作")
    store_id = fields.Many2one('assets_management.equipment_storage',string=u'入库单')
    # app_state = fields.Char(string=u'申请单审批时状态')
    app_state = fields.Selection([
        ('demander', u"提交人"),
        ('ass_admin', u"资产管理员审批"),
        ('owner', u"资产归属人审批"),
        ('ass_admin_manager', u"资产管理领导审批"),
        ('ass_admin_detection', u"资产管理员检测确认"),
        ('done',u'完成'),
        # ('cancel',u'已作废'),
    ],string=u"申请单审批时状态",readonly="True")

    reason = fields.Char(string=u'审批意见')

class equipment_lend(models.Model):
    _name = 'assets_management.equipment_lend'
    _rec_name = 'lend_id'
    _inherit = ['ir.needaction_mixin']

    @api.model
    def _needaction_domain_get(self):
        return [('approver_id.id', '=', self.env.uid)]

    def _default_SN(self):
        return self.env['assets_management.equipment_info'].browse(self._context.get('active_ids'))

    lend_id = fields.Char(string=u"借用单号")
    user_id = fields.Many2one('res.users', string=u"申请人", default=lambda self: self.env.user, required=True)
    # user_id = fields.Many2one('res.users', string=u"申请人",required=True)
    approver_id = fields.Many2one('res.users', default=lambda self: self.env.user, string=u"审批人", )
    SN = fields.Many2many('assets_management.equipment_info', "i_lend_equipment_ref", string=u"设备SN", default=_default_SN,
                          required=True)
    state = fields.Selection([
        ('demander', u"申请人"),
        ('dem_leader', u"上级领导审批"),
        ('owner', u"资产归属人审批"),
        ('ass_admin', u"资产管理员审批"),
        ('ass_admin_manager', u"资产管理领导审批"),
        ('ass_admin_detection', u"资产管理员检测确认"),
        ('done',u'已借用'),
    ], string=u"状态", required=True, default='demander')
    lend_date = fields.Date(string=u"借用日期", required=True)
    promise_date = fields.Date(string=u"归还日期", required=True)
    # actual_date = fields.Date(string=u"实际归还日期")
    lend_purpose = fields.Char(string=u"借用目的", required=True)
    owners = fields.Many2many('res.users', string=u"归属人们")
    lend_exam_ids = fields.One2many('assets_management.lend_examine', 'lend_id', string=u'审批记录')

    #New Add
    opinion = fields.Char(string=u"审批意见")       #每次保存时清空，用于显示
    opinion_bak = fields.Char(string=u"审批意见")   #实际审批意见，用于校验
    approve_flag = fields.Boolean(string=u"同意或者不同意标识",default=True) #False，不同意 True 同意
    lend_purpose_compute = fields.Char(string=u"借用目的", compute="_compute")
    lend_date_compute = fields.Date(string=u"借用日期",compute="_compute")
    promise_date_compute = fields.Date(string=u"归还日期", compute="_compute")
    equipment_use = fields.Char(string=u"设备用途",default='')

    def _compute(self):
        self.lend_purpose_compute = self.lend_purpose
        self.lend_date_compute = self.lend_date
        self.promise_date_compute = self.promise_date

    # 不同意填写意见校验
    @api.constrains('opinion_bak')
    def _checkDisagree(self):
        print '-----------------_checkDisagree-----------------'

        if self.approve_flag == False:
            # self.opinion_bak = self.opinion
            if self.opinion_bak == '':
                raise exceptions.ValidationError(u"请输入意见!")

    # 借出日期不能小于归还日期校验
    @api.one
    @api.constrains('lend_date', 'promise_date')
    def _check_promise_date_more_than_lend_date(self):
        dateNow = fields.Date.today()

        if self.lend_date > self.promise_date:
            raise exceptions.ValidationError(u"归还日期不能小于申请日期！")
        if self.lend_date < dateNow:
            raise exceptions.ValidationError(u"借用日期不能小于当前日期！")
        if self.promise_date < dateNow:
            raise exceptions.ValidationError(u"归还日期不能小于当前日期！")

        promise_date = datetime.datetime.strptime(self.promise_date, DEFAULT_SERVER_DATE_FORMAT)
        lend_date = datetime.datetime.strptime(self.lend_date, DEFAULT_SERVER_DATE_FORMAT)
        timedelta = promise_date - lend_date
        if int(timedelta.days) > 30:
            raise exceptions.ValidationError(u"借用时间不能超过30天！")

    # 所选取的设备归属人必须唯一校验
    @api.constrains('SN')
    def _checkDevOwnersUnique(self):
        print '-----------------_checkDevOwnersUnique-----------------'
        for dev in self.SN:
            self.owners |= dev.owner
        # print '&&&&&&&&&&&&&&&& self.owners&&&&&&&&&&&&'
        # print self.owners
        if len(self.owners) > 1:
            raise exceptions.ValidationError(u"所选取的设备归属人必须唯一!")

    # 设备用途唯一校验（所选设备）
    @api.constrains('equipment_use')
    def _check_Equipment_Use_Unique(self):
        print '-----------------_checkEquipment_useUnique-----------------'
        set_equipment_use = set()
        for dev in self.SN:
            set_equipment_use.add(dev.equipment_use)
        # self.equipment_use = list(set_equipment_use)[0]
        print set_equipment_use
        if set_equipment_use.__len__() > 1:
            raise exceptions.ValidationError(u"所选取的设备用途必须类型统一!")

    def create(self, cr, uid, vals, context=None):
        print '------------lend create begin------------'
        template_model = self.pool.get('assets_management.equipment_info')
        devices = template_model.browse(cr, uid, vals['SN'][0][2], context=None)
        for device in devices:
            if device.dev_state != '库存':
                raise exceptions.ValidationError("正在借用，所选设备状态必须为【库存】")
                break
            device.dev_state = u'借用'
        dates = fields.Date.today().split('-')
        date = ''.join(dates)
        template_model = self.pool.get('assets_management.equipment_lend')
        ids = template_model.search(cr, uid, [('lend_id', 'like', date)], context=None)
        lends = template_model.browse(cr, uid, ids, context=None).sorted(key=lambda r: r.lend_id)
        if len(lends):
            vals['lend_id'] = 'L' + str(int(lends[-1].lend_id[1:]) + 1)
        else:
            vals['lend_id'] = 'L' + date + '001'

        #避免借用设备被退回时显示‘库存’状态而被再次建立领用或者借用请求时特殊处理
        for device in devices:
            if device.store_flag <> '0' and device.store_flag <> vals['lend_id']:
                raise exceptions.Warning(u"所选设备正在借用中，无法再次被借用")
                break
        print '------------lend create end------------'
        return super(equipment_lend, self).create(cr, uid, vals, context=context)
    # 0-Plus 申请人关闭
    @api.multi
    def action_appUser_close(self):
        pre_state = self.state
        self.state = 'done'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': 'close', 'lend_id': self.id, 'app_state': 'close',
             'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'库存'
            dev.use_state = u'none'
            dev.store_flag = '0'

            # 4.返回到代办tree界面
            # treeviews = self.get_todo_assets_storing()
            # return treeviews

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
            self.owners |= sn.owner
            sn.dev_state = u'借用'
            sn.can_edit = False
            if sn.store_flag == '0':
                sn.store_flag = self.lend_id


        #3.设备归属人只有一个的情况，多个归属人暂时没有处理
        int_len = len(self.owners)
        if int_len == 1:
            pre_state = self.state
            self.state = 'dem_leader'

            # 4.创建审批流程日志文档
            self.env['assets_management.lend_examine'].create(
                {'approver_id': self.approver_id.id, 'result': u'submit', 'lend_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

            # 4-Plus.设备用途记录
            set_equipment_use = set()
            for dev in self.SN:
                dev.use_state = u'Lending'
                set_equipment_use.add(dev.equipment_use)
            self.equipment_use = list(set_equipment_use)[0]

            # 5.将下一个审批人员加入到相关字段中(上级领导审批)
            nextAppuser = self.user_id.employee_ids[0].parent_id.user_id
            # res.users()
            # print len(nextAppuser)
            if len(nextAppuser) == 0:
                nextAppuser = self.user_id.employee_ids[0].department_id.manager_id.user_id
            # print self.user_id.employee_ids[0].id
            # nextAppuser = self.env['hr.employee'].sudo().search([('parent_id', '=', self.user_id.employee_ids[0].id)])
            # nextAppuser = nextAppuser.user_id
            # 6.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
            self.approver_id = nextAppuser

    # 2-1.需求团队主管【同意】操作
    @api.multi
    def action_lent_dem_leader_agree(self):
        print '===================需求团队主管【同意】操作========='
        pre_state = self.state
        equipment_use = self.equipment_use
        if equipment_use == u'专用备件':
            self.state = "owner"
            nextleader = self.owners
        else:
            self.state = "ass_admin"
            nextleader = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'lend_id': self.id, 'app_state':pre_state, 'reason': self.opinion_bak})

        #3.将下一个审批人员加入到相关字段中
        nextAppuser = nextleader
        # print len(nextAppuser)
        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将借用设备可编辑状态更新为 不可编辑   此段目前可以不用，因为设备所有字段在对应的XML中都为 readOnly
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews
    # 2-2.需求团队主管【退回】操作
    @api.multi
    def action_lent_dem_leader_disagree(self):
        print '===================需求团队主管【退回】操作========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'lend_id': self.id, 'app_state':pre_state, 'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 3-1.资产归属人【同意】操作
    @api.multi
    def action_lent_owners_agree(self):
        pre_state = self.state
        self.state = 'ass_admin'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'lend_id': self.id, 'app_state':pre_state, 'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        # nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理团队领导')],limit=1).users[0]
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        # 4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 3-2.资产归属人【退回】操作
    @api.multi
    def action_lent_owners_disagree(self):
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'lend_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 4-1.资产管理员【同意】操作
    @api.multi
    def action_lent_ass_admin_agree(self):
        print '===================资产管理员【同意】操作========='
        pre_state = self.state
        self.state = 'ass_admin_manager'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'lend_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理团队领导')], limit=1).users[0]

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 4-2.资产管理员【退回】操作
    @api.multi
    def action_lent_ass_admin_disagree(self):
        print '===================资产管理员【退回】操作========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'lend_id': self.id, 'app_state':pre_state, 'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 5-1.资产管理团队领导【同意】操作
    @api.multi
    def action_lent_ass_admin_manager_agree(self):
        print '===================资产管理团队领导【同意】========='
        pre_state = self.state
        self.state = 'ass_admin_detection'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'lend_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 5-2.资产管理团队领导【退回】操作
    @api.multi
    def action_lent_ass_admin_manager_disagree(self):
        print '===================资产管理团队领导【退回】========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'lend_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 6-1.备件管理员检测确认【同意】操作
    @api.multi
    def action_lent_ass_admin_detection_agree(self):
        print '===================备件管理员检测确认【同意】========='
        pre_state = self.state
        self.state = 'done'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'lend_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'close', 'lend_id': self.id, 'app_state':'done', 'reason':''})
        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.use_state = u'haveLent'
            dev.devUse_user_id = self.user_id       #借用人记录到设备单中，设备单被归还后，清空该字段
            if dev.store_flag <> '0':
                dev.store_flag = '0'

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 6-2.备件管理员检测确认【退回】操作
    @api.multi
    def action_lent_ass_admin_detection_disagree(self):
        print '===================资产管理团队领导【退回】========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.lend_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'lend_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews
class lend_examine(models.Model):
    _name = 'assets_management.lend_examine'
    # _rec_name = 'exam_num'
    #
    # exam_num = fields.Char(sting='审批id')
    approver_id = fields.Many2one('res.users', required='True', string=u'审批人')
    date = fields.Datetime(string=u'审批时间', default=lambda self: fields.Datetime.now())
    result = fields.Selection([
            (u'agree', u"通过"),
            (u'disagree', u"拒绝"),
            (u'submit', u"提交"),
            (u'callback', u"收回"),
            (u'close', u"关闭"),
        ], string=u"操作")
    lend_id = fields.Many2one('assets_management.equipment_lend', string=u'借用单')
    # app_state = fields.Char(string='申请单审批时状态')
    app_state = fields.Selection([
        ('demander', u"申请人"),
        ('dem_leader', u"上级领导审批"),
        ('ass_admin', u"资产管理员审批"),
        ('owner', u"资产归属人审批"),
        ('ass_admin_manager', u"资产管理领导审批"),
        ('ass_admin_detection', u"资产管理员检测确认"),
        ('done',u'已借用'),
        ('close', u"关闭"),
    ], string=u"审批状态", readonly="True")
    reason = fields.Char(string=u'审批意见')

class equipment_back_to_store(models.Model):
    _name = 'assets_management.back_to_store'
    _rec_name = 'back_id'
    _inherit = ['ir.needaction_mixin']

    @api.model
    def _needaction_domain_get(self):
        return [('approver_id.id', '=', self.env.uid)]

    def _default_SN(self):
        return self.env['assets_management.equipment_info'].browse(self._context.get('active_ids'))

    back_id = fields.Char(string=u"归还单号")
    user_id = fields.Many2one('res.users', string=u"申请人",default=lambda self: self.env.user, required=True)
    approver_id = fields.Many2one('res.users', string=u"审批人",default=lambda self: self.env.user)

    SN = fields.Many2many('assets_management.equipment_info', "i_back_equipment_ref", string=u"设备SN",default= _default_SN,
                          required=True,)
    state = fields.Selection([
        ('demander', u"申请人"),
        ('ass_admin', u"资产管理员审批"),
        ('done', u'已归还'),
    ], string=u"状态", required=True, default='demander')
    back_date = fields.Date(string=u"归还时间",required=True)
    back_exam_ids = fields.One2many('assets_management.back_examine', 'back_id', string=u'审批记录')
    lend_id = fields.Many2one('assets_management.equipment_lend',string=u'借用单')

    # New Add
    opinion = fields.Char(string=u"审批意见")  # 每次保存时清空，用于显示
    opinion_bak = fields.Char(string=u"审批意见")  # 实际审批意见，用于校验
    approve_flag = fields.Boolean(string=u"同意或者不同意标识", default=True)  # False，不同意 True 同意
    back_date_compute = fields.Date(string=u"归还时间", compute="_compute")
    # 不同意填写意见校验
    @api.constrains('opinion_bak')
    def _checkDisagree(self):
        print '-----------------_checkDisagree-----------------'
        if self.approve_flag == False:
            # self.opinion_bak = self.opinion
            if self.opinion_bak == '':
                raise exceptions.ValidationError(u"请输入意见!")

    #计算字段赋值
    def _compute(self):
        self.back_date_compute = self.back_date

    def create(self, cr, uid, vals, context=None):
        template_model = self.pool.get('assets_management.equipment_info')
        devices = template_model.browse(cr, uid, vals['SN'][0][2], context=None)
        print vals['SN']
        for device in devices:
            if device.dev_state != '借用':
                raise exceptions.ValidationError("正在归还，所选设备状态必须为【借用】")
                break
            print device.devUse_user_id.id
            print uid
            if device.devUse_user_id.id != uid:
                raise exceptions.ValidationError("设备借用人员与归还人员不一致，不允许归还！")
                break
            device.dev_state = u'归还'
        dates = fields.Date.today().split('-')
        date = ''.join(dates)
        template_model = self.pool.get('assets_management.back_to_store')
        ids = template_model.search(cr, uid, [('back_id', 'like', date)], context=None)
        backs = template_model.browse(cr, uid, ids, context=None).sorted(key=lambda r: r.back_id)
        if len(backs):
            vals['back_id'] = 'B' + str(int(backs[-1].back_id[1:]) + 1)
        else:
            vals['back_id'] = 'B' + date + '001'

        #避免归还设备被退回时显示‘借用’状态而被再次建立归还请求时特殊处理
        for device in devices:
            if device.store_flag <> '0' and device.store_flag <> vals['back_id']:
                raise exceptions.Warning(u"所选设备正在归还中，无法再次归还")
                break
        #查看当前人员是否与归还设备的中的所有人
        return super(equipment_back_to_store, self).create(cr, uid, vals, context=context)

    # 0-Plus 申请人关闭
    @api.multi
    def action_appUser_close(self):
        pre_state = self.state
        self.state = 'done'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.back_examine'].create(
            {'approver_id': self.approver_id.id, 'result': 'close', 'store_id': self.id, 'app_state': 'close',
             'reason': self.opinion_bak})
        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将归还设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'借用'
            dev.use_state = u'haveLent'
            dev.store_flag = '0'

            # 4.返回到代办tree界面
            # treeviews = self.get_todo_assets_storing()
            # return treeviews

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
            # self.owners |= sn.owner
            # sn.dev_state = u'归还'  #设备归还完毕后最终状态变为'库存'状态，是一个循环，无需将dev_state赋值
            sn.can_edit = False
            if sn.store_flag == '0':
                sn.store_flag = self.back_id
            sn.use_state = u'Backing'

        #3.设备归属人只有一个的情况，多个归属人暂时没有处理
        # int_len = len(self.owners)
        # if int_len == 1:
        pre_state = self.state
        self.state = 'ass_admin'

        # 4.创建审批流程日志文档
        self.env['assets_management.back_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'submit', 'back_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

        # 5.将下一个审批人员加入到相关字段中(上级领导审批)
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        # 6.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        self.approver_id = nextAppuser

    # 2-1.资产管理员【同意】操作
    @api.multi
    def action_back_ass_admin_agree(self):
        print '===================资产管理员【同意】操作========='
        pre_state = self.state
        self.state = 'done'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.back_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'back_id': self.id, 'app_state': pre_state,
             'reason': self.opinion_bak})
        self.env['assets_management.back_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'close', 'back_id': self.id, 'app_state':'done', 'reason':''})
        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'库存'
            dev.use_state = u'haveBack'
            dev.devUse_user_id = None       #借用人记录到设备单中，设备单被归还后，清空该字段

            if dev.store_flag <> '0':
                dev.store_flag = '0'
        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 2-2.资产管理员【退回】操作
    @api.multi
    def action_back_ass_admin_disagree(self):
        print '===================资产管理员【退回】操作========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.back_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'back_id': self.id, 'app_state': pre_state,
             'reason': self.opinion_bak})
        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将归还设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'借用'
            dev.use_state = u'haveLent'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews
class back_examine(models.Model):
    _name = 'assets_management.back_examine'
    # _rec_name = 'exam_num'

    approver_id = fields.Many2one('res.users', required='True', string=u'审批人')
    date = fields.Datetime(string=u'审批时间', default=lambda self: fields.Datetime.now())
    result = fields.Selection([
        (u'agree', u"通过"),
        (u'disagree', u"拒绝"),
        (u'submit', u"提交"),
        (u'callback', u"收回"),
        (u'close', u"关闭"),
    ], string=u"操作")
    back_id = fields.Many2one('assets_management.back_to_store', string=u'设备归还单')
    # app_state = fields.Char(string='申请单审批时状态')
    app_state = fields.Selection([
        ('demander', u"申请人"),
        ('ass_admin', u"资产管理员审批"),
        ('done', u'已归还'),
        (u'close', u"关闭"),
    ], string=u"审批状态", readonly="True")
    reason = fields.Char(string=u'审批意见')

class equipment_get(models.Model):
    _name = 'assets_management.equipment_get'
    _rec_name = 'get_id'
    _inherit = ['ir.needaction_mixin']

    @api.model
    def _needaction_domain_get(self):
        return [('approver_id.id', '=', self.env.uid)]

    def _default_SN(self):
        return self.env['assets_management.equipment_info'].browse(self._context.get('active_ids'))
    get_id = fields.Char(string=u"领用单号")
    user_id = fields.Many2one('res.users', string=u"申请人", default=lambda self: self.env.user,required=True)
    approver_id = fields.Many2one('res.users', string=u"审批人",default=lambda self: self.env.user)
    SN = fields.Many2many('assets_management.equipment_info',"i_get_equipment_ref",string=u"设备SN", default=_default_SN,required=True)
    state = fields.Selection([
        ('demander', u"申请人"),
        ('dem_leader', u"上级领导审批"),
        ('owner', u"资产归属人审批"),
        ('ass_admin', u"资产管理员审批"),
        ('ass_admin_manager', u"资产管理领导审批"),
        ('ass_admin_detection', u"资产管理员检测确认"),
        ('done',u'已领用'),
    ], string=u"状态", required=True, default='demander')
    get_date = fields.Date(string=u"领用日期",required=True)
    get_purpose = fields.Char(string=u"领用目的",required=True)
    owners = fields.Many2many('res.users', string=u'设备归属人', ondelete = 'set null')
    get_exam_ids = fields.One2many('assets_management.get_examine','get_id',string=u'审批记录')

    # New Add
    opinion = fields.Char(string=u"审批意见")  # 每次保存时清空，用于显示
    opinion_bak = fields.Char(string=u"审批意见")  # 实际审批意见，用于校验
    approve_flag = fields.Boolean(string=u"同意或者不同意标识", default=True)  # False，不同意 True 同意
    get_purpose_compute = fields.Char(string=u"领用目的", compute="_compute")
    get_date_compute = fields.Date(string=u"领用日期", compute="_compute")
    equipment_use = fields.Char(string=u"设备用途")

    def _compute(self):
        self.get_purpose_compute = self.get_purpose
        self.get_date_compute = self.get_date

    # 不同意填写意见校验
    @api.constrains('opinion_bak')
    def _checkDisagree(self):
        print '-----------------_checkDisagree-----------------'

        if self.approve_flag == False:
            # self.opinion_bak = self.opinion
            if self.opinion_bak == '':
                raise exceptions.ValidationError(u"请输入意见!")

    # 所选取的设备归属人必须唯一校验
    @api.constrains('SN')
    def _checkDevOwnersUnique(self):
        print '-----------------_checkDevOwnersUnique-----------------'
        for dev in self.SN:
            self.owners |= dev.owner
        if len(self.owners) > 1:
            raise exceptions.ValidationError(u"所选取的设备归属人必须唯一!")

    # 设备用途唯一校验（所选设备）
    @api.constrains('equipment_use')
    def _check_Equipment_Use_Unique(self):
        print '-----------------_checkEquipment_useUnique-----------------'
        set_equipment_use = set()
        for dev in self.SN:
            set_equipment_use.add(dev.equipment_use)
        # self.equipment_use = list(set_equipment_use)[0]
        if set_equipment_use.__len__() > 1:
            raise exceptions.ValidationError(u"所选取的设备用途必须类型统一!")
    def create(self, cr, uid, vals, context=None):
        template_model = self.pool.get('assets_management.equipment_info')
        print vals['SN'][0][2]
        devices = template_model.browse(cr, uid, vals['SN'][0][2], context=None)
        for device in devices:
            if device.dev_state != '库存':
                raise exceptions.ValidationError("正在领用，所选设备状态必须为【库存】")
                break
            device.dev_state = u'领用'
        dates = fields.Date.today().split('-')
        date = ''.join(dates)
        template_model = self.pool.get('assets_management.equipment_get')
        ids = template_model.search(cr, uid, [('get_id', 'like', date)], context=None)
        gets = template_model.browse(cr, uid, ids, context=None).sorted(key=lambda r: r.get_id)
        if len(gets):
            vals['get_id'] = 'G' + str(int(gets[-1].get_id[1:]) + 1)
        else:
            vals['get_id'] = 'G' + date + '001'

        #避免领用设备被退回时显示‘库存’状态而被再次建立库存请求时特殊处理
        for device in devices:
            if device.store_flag <> '0' and device.store_flag <> vals['get_id']:
                raise exceptions.Warning(u"所选设备正在领用中，无法再次领用")
                break

        return super(equipment_get, self).create(cr, uid, vals, context=context)

    # 借出日期不能小于当前日期校验
    @api.one
    @api.constrains('get_date')
    def _check_promise_date_more_than_lend_date(self):
        dateNow = fields.Date.today()
        if self.get_date < dateNow:
            raise exceptions.ValidationError(u"领用日期不能小于当前日期！")

    # 0-Plus 申请人关闭
    @api.multi
    def action_appUser_close(self):
        pre_state = self.state
        self.state = 'done'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': 'close', 'get_id': self.id, 'app_state': 'close',
             'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'库存'
            dev.use_state = u'none'
            dev.store_flag = '0'

            # 4.返回到代办tree界面
            # treeviews = self.get_todo_assets_storing()
            # return treeviews

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
            self.owners |= sn.owner
            sn.dev_state = u'领用'
            sn.can_edit = False
            if sn.store_flag == '0':
                sn.store_flag = self.get_id

        #3.设备归属人只有一个的情况，多个归属人暂时没有处理
        int_len = len(self.owners)
        if int_len == 1:
            pre_state = self.state
            self.state = 'dem_leader'

            # 4.创建审批流程日志文档
            self.env['assets_management.get_examine'].create(
                {'approver_id': self.approver_id.id, 'result': u'submit', 'get_id': self.id, 'app_state':pre_state, 'reason':self.opinion_bak})

            # 4-Plus.设备用途记录
            set_equipment_use = set()
            for dev in self.SN:
                dev.use_state = u'Lending'
                set_equipment_use.add(dev.equipment_use)
            self.equipment_use = list(set_equipment_use)[0]

            # 5.将下一个审批人员加入到相关字段中(上级领导审批)

            nextAppuser = self.user_id.employee_ids[0].parent_id.user_id
            if len(nextAppuser) == 0:
                nextAppuser = self.user_id.employee_ids[0].department_id.manager_id.user_id

            # 6.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
            self.approver_id = nextAppuser

    # 2-1.需求团队主管【同意】操作
    @api.multi
    def action_get_dem_leader_agree(self):
        print '===================需求团队主管【同意】操作========='
        pre_state = self.state
        equipment_use = self.equipment_use
        if equipment_use == u'专用备件':
            self.state = "owner"
            nextleader = self.owners
        else:
            self.state = "ass_admin"
            nextleader = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})

        #3.将下一个审批人员加入到相关字段中
        nextAppuser = nextleader

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将借用设备可编辑状态更新为 不可编辑   此段目前可以不用，因为设备所有字段在对应的XML中都为 readOnly
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews
    # 2-2.需求团队主管【退回】操作
    @api.multi
    def action_get_dem_leader_disagree(self):
        print '===================需求团队主管【退回】操作========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 3-1.资产归属人【同意】操作
    @api.multi
    def action_get_owners_agree(self):
        pre_state = self.state
        self.state = 'ass_admin'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        # nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理团队领导')],limit=1).users[0]
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        # 4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 3-2.资产归属人【退回】操作
    @api.multi
    def action_get_owners_disagree(self):
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 4-1.资产管理员【同意】操作
    @api.multi
    def action_get_ass_admin_agree(self):
        print '===================资产管理员【同意】操作========='
        pre_state = self.state
        self.state = 'ass_admin_manager'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})


        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理团队领导')], limit=1).users[0]

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 4-2.资产管理员【退回】操作
    @api.multi
    def action_get_ass_admin_disagree(self):
        print '===================资产管理员【退回】操作========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id
        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 不可编辑  标识设备为【库存】
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews
    # 5-1.资产管理团队领导【同意】操作
    @api.multi
    def action_get_ass_admin_manager_agree(self):
        print '===================资产管理团队领导【同意】========='
        pre_state = self.state
        self.state = 'ass_admin_detection'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})

        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.env['res.groups'].search([('name', '=', u'备件管理员')], limit=1).users[0]

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False

        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 5-2.资产管理团队领导【退回】操作
    @api.multi
    def action_get_ass_admin_manager_disagree(self):
        print '===================资产管理团队领导【退回】========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'库存'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 6-1.备件管理员检测确认【同意】操作
    @api.multi
    def action_get_ass_admin_detection_agree(self):
        print '===================备件管理员检测确认【同意】========='
        pre_state = self.state
        self.state = 'done'

        #1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = True
        self.opinion_bak = self.opinion
        self.opinion = ''

        #2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'agree', 'get_id': self.id, 'app_state': pre_state,              'reason': self.opinion_bak})
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'close', 'get_id': self.id, 'app_state':'done', 'reason':''})
        
        #3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        #4.设备归属人不止一个情况处理，暂时只处理只有一个人情况，并增加了py 的constrains
        lenth = len(nextAppuser)

        #审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 4-Plus.将入库设备可编辑状态更新为 不可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = False
            dev.use_state = u'haveGet'
            dev.devUse_user_id = self.user_id       #领用人记录到设备单中，设备单被归还后，清空该字段
            if dev.store_flag <> '0':
                dev.store_flag = '0'
        #5.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews

    # 6-2.备件管理员检测确认【退回】操作
    @api.multi
    def action_get_ass_admin_detection_disagree(self):
        print '===================资产管理团队领导【退回】========='
        pre_state = self.state
        self.state = 'demander'

        # 1.审批意见 申请人可editable、其他人员readonly 的相关字段赋值
        self.approve_flag = False
        self.opinion_bak = self.opinion
        self.opinion = ''

        # 2.创建审批流程日志文档
        self.env['assets_management.get_examine'].create(
            {'approver_id': self.approver_id.id, 'result': u'disagree', 'get_id': self.id, 'app_state': pre_state,
             'reason': self.opinion_bak})

        # 3.将下一个审批人员加入到相关字段中
        nextAppuser = self.user_id

        # 审批人员字段更新，因为constrains的缘故，必须在所有逻辑完毕后才层新approver_id 字段
        self.approver_id = nextAppuser

        # 3-Plus.将入库设备可编辑状态更新为 可编辑
        devs = self.SN
        for dev in devs:
            dev.can_edit = True
            dev.dev_state = u'领用'
            dev.use_state = u'none'

        #4.返回到代办tree界面
        # treeviews = self.get_todo_assets_storing()
        # return treeviews
class get_examine(models.Model):
    _name = 'assets_management.get_examine'
    # _rec_name = 'exam_num'

    approver_id = fields.Many2one('res.users', required='True', string=u'审批人')
    date = fields.Datetime(string=u'审批时间', default=lambda self: fields.Datetime.now())
    result = fields.Selection([
        (u'agree', u"通过"),
        (u'disagree', u"拒绝"),
        (u'submit', u"提交"),
        (u'callback', u"收回"),
        (u'close', u"关闭"),
    ], string=u"操作")
    get_id = fields.Many2one('assets_management.equipment_get', string=u'设备领用单')
    # app_state = fields.Char(string='申请单审批时状态')
    app_state = fields.Selection([
        ('demander', u"申请人"),
        ('dem_leader', u"上级领导审批"),
        ('ass_admin', u"资产管理员审批"),
        ('owner', u"资产归属人审批"),
        ('ass_admin_manager', u"资产管理领导审批"),
        ('ass_admin_detection', u"资产管理员检测确认"),
        (u'close', u"关闭"),
        ('done',u'已借用'),
    ], string=u"审批状态", readonly="True")
    reason = fields.Char(string=u'审批意见')

