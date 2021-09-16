from odoo import api, fields, models, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class SchoolStudentModel(models.Model):
    _name = "school.student"
    # _description = "School students data"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(compute = "AgeCalculator",string = "Age")
    gender = fields.Selection([("m","Male"),("f","Female")], string="Gender")
    image = fields.Binary(string="Image")
    email = fields.Char(string="E-mail")
    phone = fields.Char(string="Phone", size=10)
    registration_number = fields.Char(string="Registration Number")
    date_registration = fields.Date(string = "Date of Registration")
    street = fields.Text(string="Street")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state",string="State ID")
    country_id = fields.Many2one("res.country",string = "Country ID")
    zip = fields.Char(string="Zip", size=6)
    state = fields.Selection([("new","New"),("current","Current"),("passout","Pass Out")], string="State",default="new")
    course_id = fields.Many2one(comodel_name="school.course",relation="student_course_relation",column1="studentid",column2="courseid", string = "Course ID")
    subject_ids = fields.Many2many(comodel_name="school.subject",relation="student_subject_relation",column1="studentid",column2="subjectid", string = "Subject IDs")

    def action_new(self):
        self.state = "new"

    def action_passout(self):
        self.state = "passout"

    def action_current(self):
        self.state = "current"

    @api.depends("date_of_birth")
    def AgeCalculator(self):
        for rec in self:
            rec.age = 0
            # _logger.info("===========Search-----%r-------",rec.date_of_birth)
            # today = datetime.date.today()
            # dob = rec.date_of_birth
            if rec.date_of_birth:
                # _logger.info("===========Search-----%r---%r----",date.today().year -  rec.date_of_birth.year.year, rec.date_of_birth)
                rec.write({
                    "age": date.today().year -  rec.date_of_birth.year,
                })

    # @api.constrains("course_id")
    # def studentcourseids(self):
    #     for rec in self:
    #         for course in rec.course_id:
    #             _logger.info("===========Search-----%r---%r-",rec.course_id.id,course.id)
    #             obj = self.env["school.course"].search([('id','=',rec.course_id.id)])
    #             if obj:
    #                 obj.write({
    #                     "student_ids": self.name,
    #                 })

class SchoolTeacherModel(models.Model):
    _name = "school.teacher"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(compute = "AgeCalculator",string = "Age")
    gender = fields.Selection([("m","Male"),("f","Female")], string="Gender")
    image = fields.Binary(string="Image")
    email = fields.Char(string="E-mail")
    phone = fields.Char(string="Phone", size=10)
    registration_number = fields.Char(string="Registration Number")
    date_registration = fields.Date(string = "Date of Registration")
    street = fields.Text(string="Street")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state",string="State ID")
    country_id = fields.Many2one("res.country",string = "Country ID")
    zip = fields.Char(string="Zip", size=6)
    state = fields.Selection([("active","Active"),("inactive","Inactive")], string="State")
    course_ids = fields.Many2many(comodel_name="school.course",relation="teacher_course_relation",column1="teacherid",column2="courseid", string = "Course IDs")
    subject_ids = fields.Many2many(comodel_name="school.subject",relation="teacher_subject_relation",column1="teacherid",column2="subjectid", string = "Subject IDs")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")

    def action_active(self):
        self.state = "active"

    def action_inactive(self):
        self.state = "inactive"

    @api.depends("date_of_birth")
    def AgeCalculator(self):
        for rec in self:
            rec.age = 0
            if rec.date_of_birth:
                rec.write({
                    "age": date.today().year -  rec.date_of_birth.year,
                })

    # @api.constrains("course_ids")
    # def studentcourseids(self):
    #     for rec in self:
    #         for course in rec.course_ids:
    #             _logger.info("===========Search-----%r---%r-",rec.course_ids.id,course.id)
    #             obj = self.env["school.course"].search([('id','=',rec.course_id.id)])
    #             if obj:
    #                 obj.write({
    #                     "teacher_ids": self.name,
    #                 })

class SchoolCourseModel(models.Model):
    _name = "school.course"
    _rec_name = "name"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    duration = fields.Integer(string="Duration")
    fee = fields.Integer(string="Fee")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")
    position = fields.Char(string="Position/Designation")
    teacher_ids = fields.One2many("school.teacher",inverse_name="course_ids",string="Teacher's Name")
    student_ids = fields.One2many("school.student",inverse_name="course_id",string="Student's Name")


class SchoolSubjectModel(models.Model):
    _name = "school.subject"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    description = fields.Text(string="Description")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")

class SchoolFeesModel(models.Model):
    _name = "school.fee"
    _rec_name = "student_id"

    student_id = fields.Many2one("school.student",string="Student ID")
    total_fee = fields.Float(compute="TotalFee",string="Total Fees")
    due_fee = fields.Float(compute = "DuesCalculator", string="Due Fees")
    amount_paid = fields.Float(string="Amount Paid")
    course_id = fields.Many2one("school.course",string="Course ID")

    # @api.depends(course_id)
    # def TotalFee(self):
    #     for rec in self:
    #         rec.total_fee = 0
    #         if 
    @api.depends("course_id")
    def TotalFee(self):
        # self.ensure_one()
        for rec in self:
            rec.total_fee = 0
            if rec:
                rec.write({
                    "total_fee": rec.student_id.course_id.fee,
                })

    @api.depends("total_fee","amount_paid")
    def DuesCalculator(self):
        for rec in self:
            rec.due_fee = 0
            if rec.total_fee and rec.amount_paid:
                rec.write({
                    "due_fee" : rec.total_fee - rec.amount_paid,
                })

    def action_register_payment(self):
        return{
            "name":("Register Payment"),
            "view_mode":"form",
            "res_model":"school.fee.wizard",
            "type":"ir.actions.act_window",
            "target":"new",
        }

class SchoolFeeLineModel(models.Model):
    _name="school.fee.line"
    _rec_name = "student_id"

    student_id = fields.Many2one("school.student",string="Student ID",required=True)
    due_fee = fields.Float(string="Due Fees")
    amount_paid = fields.Float(string="Amount Paid")

    @api.onchange("student_id")
    def dues(self):
        for rec in self:
            rec.due_fee = 0
            if rec.student_id:
                obj = self.env["school.fee"].search([("student_id.id","=",rec.student_id.id)])
                _logger.info("===========Search-----%r---%r-",obj.due_fee,rec.student_id.id)
                if obj:
                    rec.due_fee = obj.due_fee
