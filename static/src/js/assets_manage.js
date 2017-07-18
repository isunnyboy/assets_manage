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

    //获取当前视图中申请人的id和登陆人id做对比
    instance.web.FormView.include({
        load_record:function(data){

            if(this.model == "assets_management.equipment_storage"){
                var user_id = data.user_id[0] || data.user_id,
                login_user_id = instance.session.uid;
                console.log(data);
                if(user_id != login_user_id || data.state != "demander"){
                    instance.assets_manage.enabled = true;
                }
            }

            return this._super.apply(this, arguments);
        }
    });

    //用来控制是否放开添加功能
    instance.web.form.Many2ManyList = instance.web.form.Many2ManyList.extend({
        is_readonly:function(){
            if(instance.assets_manage.enabled){
                return true;
            }else{
                return this.view.m2m_field.get('effective_readonly');
            }
        }
    });

    //用来控制是否放开删除功能
    instance.web.form.Many2ManyListView.include({
        init:function(parent, dataset, view_id, options){
            if(instance.assets_manage.enabled){
                options.deletable = false;
            }
            return this._super.apply(this, arguments);
        }
    });

    //当流程状态发生变化时插入自定义代码
    instance.web.form.FieldStatus.include({
        self_status:false,
        set_value:function(v){
            //根据需求删除
            if(this.view.model == "assets_management.equipment_storage"){
                if(!this.self_status){
                    this.self_status = v;
                }else{
                    if(this.self_status != v){
                        $("a.oe_breadcrumb_item").trigger("click")
                    }
                }
            }

            return this._super.apply(this, arguments);
        }
    });


};
