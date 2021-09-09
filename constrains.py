# @api.constrains("buy")
    # def _checkofferstatus_(self):
    #     for rec in self:
    #         for status in rec.buy:
    #             objs = self.env["estate.offers"].search([("status","=","Accepted"),("buy_name","=",status.buy_name)])
    #             if objs:
    #                 # objs.write({
    #                 #     "status":"Refused",
    #                 # })
    #                 raise ValidationError(_("Multiple Offers cannot be accepted."))
    
@api.constrains("status")
    def _checkofferstatus_(self):
        for rec in self:
            objs = self.search([("status",'=',"Accepted")])
            if objs>=2:
                raise ValidationError(_("You cannot accept mutiple offers."))
