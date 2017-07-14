# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions

# Internationalization
from odoo import _

from datetime import timedelta  # Calendars View


class openacademy(models.Model):
    _name = 'openacademy.openacademy'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

class course(models.Model):
    _name =  'openacademy.course'

    name = fields.Char(string = 'model-Tilte',required=True,help='name field is not Empy',index=True)
    # name2 = fields.Char(required=True)
    description = fields.Text(string='model-Description')
    state = fields.Text(string='model-State')
    responsible_id = fields.Many2one('res.users',ondelete='set null',string='Responsible',index=True)
    session_id = fields.One2many('openacademy.session','course_id',string='Session')


    # -------Model constrains---SQL Begin-----------  可以查看数据库，约束条件已经添加
    _sql_constraints=[
        (
            "name_description_check",
            "CHECK(name != description) ",
            "The title of the course should not be the description!"
        ),
        (
            "name_Unique",
            "UNIQUE(name)",
            "The course name must be unique"
        )
    ]
    # -------Model constrains---SQL END-----------

    # -------Model constrains---Implement Copy Method to copy record     Begin-----------
    # 重写copy方法，实现复制记录（由于实现了主键（name）相同不允许保存，所以要实现复制功能，必须重新copy 方法）
    @api.multi
    # def copy(self, default=None):
    #     default = dict(default or {})
    #
    #     copied_count = self.search_count(
    #         [('name', '=like', u"Copy of {}%".format(self.name))])
    #     if not copied_count:
    #         new_name = u"Copy of {}".format(self.name)
    #     else:
    #         new_name = u"Copy of {} ({})".format(self.name, copied_count)
    #
    #     default['name'] = new_name
    #     return super(Course, self).copy(default)
    def copy(self,default=None):    #self 为记录本身
        default = dict(default or {})
        copied_count = self.search_count(
            [("name","=like",_(u"copy of {}%").format(self.name))]  #Internationalization
        )

        if not copied_count:
            new_name = _(u"copy of {}%").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)
        default["name"] = new_name
        return super(course,self).copy(default)

    # -------Model constrains---Implement Copy Method to copy record     END-----------
class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    # Default Values
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    # Domain & Models Relation
    instructor_id = fields.Many2one('res.partner',string='Instructor',
                                    domain=['|',('instructor','=',True),
                                            ('category_id.name','ilike','Teacher')])

    # Models Relation
    course_id = fields.Many2one('openacademy.course',ondelete='cascade',string='Course',required=True)
    attendee_ids = fields.Many2many('res.partner',string='Attendees')


    # -------compute field and default values Begin-----------需要在View中定义展示XML
    taken_seats = fields.Float(string="Taken Seats",compute="_taken_seats")

    # -------Default Values Begin----------- 默认值 系统自动去识别，如果为False reocord默认不显示
    active = fields.Boolean(default=True)
    # -------Default Values END-----------

    @api.depends("seats","attendee_ids")
    def _taken_seats(self):
        print 11111
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100*len(r.attendee_ids)/r.seats
    # -------compute field and default values END-------------

    # -------Calendars View Begin-----------
    end_date = fields.Date(string="End Date", store=True, compute="_get_end_date",inverse="_set_end_date")
    @api.depends("start_date","duration")
    def _get_end_date(self):
        print 3333333333
        print("_get_end_date")
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration,seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        print("_set_end_date")
        for r in self:
            if not (r.start_date and r.duration):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1
    # -------Calendars View END-------------

    # -------onchange Begin----------- 不需要 在model中定义字段、也不需要在View中定义展示XML
    @api.onchange("seats","attendee_ids")
    def _verify_valid_seats(self):  #函数名称随便定义
        print 2222222
        # self.seats = 1000
        if self.seats <0 :
            return {                #worning  title  message 字符不能随便更改，否则会报错
                'warning': {
                    'title': _("Incorrect's seats' value"), #Internationalization
                    'message':_("The number of available seat may not be negative"),    #Internationalization
                },
            }

        if self.seats < len(self.attendee_ids) :
            return {
                'warning':{
                    'title':_("Too many attendees"),            #Internationalization
                    'message':_("Increase seats or remove excess attendees"),       #Internationalization
                },
            }
    # -------onchange END-----------

    # -------Model constrains---python Begin-----------
    @api.constrains("instructor_id","attendee_ids")
    def _check_instrutor_not_in_attendees(self):
        for r in self:
            if  r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError(_("A session's instrutor can not be an attendee!"))

    # -------Model constrains---python END-----------

    # -------Advance Views ---Gannt Begin-----------
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24
    # -------Advance Views ---Gannt END-----------

    # -------Advance Views ---Graph Begin-----------
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)
    # -------Advance Views ---Graph END-----------

    # -------Advance Views ---KanBan Begin-----------
    color = fields.Integer()
    # -------Advance Views ---KanBan END-----------

    # -------Workflows-ish Begin-----------   workflow-ish 与 workflow只能二选一
    # state = fields.Selection([
    #     ('draft', "DDraft"),
    #     ('confirmed', "Confirmed"),
    #     ('done', "Done"),
    # ], default='draft')
    #
    # @api.multi
    # def action_draft(self):
    #     self.state = 'draft'
    #
    # @api.multi
    # def action_confirm(self):
    #     self.state = 'confirmed'
    #
    # @api.multi
    # def action_done(self):
    #     self.state = 'done'
    # -------Workflows-ish END-----------

    # -------Workflows Begin----------- workflow-ish 与 workflow只能二选一
    state = fields.Selection([
        ('draft', "DDraft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ])

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'
    # -------Workflows END-----------

    def call(self):
        return self.check("model Session")

    def check(self, s):
        return "This is {} record {}".format(s, self.name)

# Classic Inheritance
class SessionExtension(models.Model):
    _name = 'openacademy.session'
    _inherit = 'openacademy.session'
    notes = fields.Text(defult='notesValue')

#Prototype Inheritance
class SessionCopy(models.Model):
    _name = 'openacademy.session.copy'
    _inherit = 'openacademy.session'

    copy = fields.Text()
    def call(self):
        return self.check('model SessionExctensionCopy')



#Delegation Inheritance
class Child0(models.Model):
    _name = 'delegation.child0'
    field_0 = fields.Integer()

class Child1(models.Model):
    _name = 'delegation.child1'
    field_1 = fields.Integer()

class Delegating(models.Model):
    _name = 'delegation.parent'
    _inherits = {
        'delegation.child0':'child0_id',
        'delegation.child1':'child1_id',
    }

    child0_id = fields.Many2one('delegation.child0',reqired =True,ondelete = 'cascade')
    child1_id = fields.Many2one('delegation.child1',reqired =True,ondelete = 'cascade')
