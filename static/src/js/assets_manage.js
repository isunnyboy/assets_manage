/**
 * Created by Administrator on 2017-7-16.
 */
openerp.assets_manage=function(instance){
    var _t=instance.web._t,
        _lt=instance.web._lt,
        QWeb=instance.web.qweb;
    instance.assets_manage={
        enabled:false,
        //SN_list:null
    };

    instance.web.FormView.include({
        //获取当前视图中申请人的id和登陆人id做对比
        load_record:function(data){

            if(this.model == "assets_management.equipment_storage"){
                instance.assets_manage.enabled = false;
                var user_id = data.user_id[0] || data.user_id,
                login_user_id = instance.session.uid;
                if(user_id != login_user_id || data.state != "demander"){
                    instance.assets_manage.enabled = true;
                }
                //instance.assets_manage.SN_list = data.SN;
            }

            return this._super.apply(this, arguments);
        },

        //当删除关联关系并保存时改变设备的状态(暂时不需要)
        /*on_button_save:function(e){

            if(this.model == "assets_management.equipment_storage"){
                var self = this;
                $(e.target).attr("disabled", true);
                return this.save().done(function(result) {
                    self.trigger("save", result);
                    self.reload().then(function() {
                        self.to_view_mode();
                        var menu = instance.webclient.menu;
                        if (menu) {
                            menu.do_reload_needaction();
                        }
                    });

                    //找出保存前后的差异
                    var ids = [];
                    console.log(self);
                    debugger;
                    $.each(instance.assets_manage['SN_list'],function(i,v){
                        if(self.datarecord["SN"].indexOf(v) < 0){
                            ids.push(v);
                        }
                    });
                    self.rpc("/web/test",{
                        "ids":ids
                    });

                }).always(function(){
                    $(e.target).attr("disabled", false);
                });
            }else{
                this._super.apply(this, arguments);
            }
        }*/
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
                        this.self_status = false;
                        setTimeout(function(){
                            $("a.oe_vm_switch_list").trigger("click");
                        },200);
                    }
                }
            }

            return this._super.apply(this, arguments);
        }
    });


};
