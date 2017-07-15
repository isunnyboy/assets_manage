/**
 * Created by Administrator on 2017-7-16.
 */
openerp.assets_manage=function(instance){
    var _t=instance.web._t,
        _lt=instance.web._lt,
        QWeb=instance.web.qweb;
    instance.assets_manage={
        enabled:false
    };

    instance.web.FormView.include({
        load_record:function(data){

            if(this.model == "assets_management.equipment_storage"){
                var user_id = data.user_id[0],
                login_user_id = instance.session.uid;
                if(user_id != login_user_id){
                    instance.assets_manage.enabled = true;
                }
            }

            return this._super.apply(this, arguments);
        }
    });

    instance.web.form.Many2ManyList = instance.web.form.Many2ManyList.extend({
        is_readonly:function(){
            if(instance.assets_manage.enabled){
                return true;
            }else{
                return this.view.m2m_field.get('effective_readonly');
            }
        }
    });

    instance.web.form.Many2ManyListView.include({
        init:function(parent, dataset, view_id, options){
            if(instance.assets_manage.enabled){
                options.deletable = false;
            }
            return this._super.apply(this, arguments);
        }
    });
};
