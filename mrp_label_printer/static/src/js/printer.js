openerp.mrp_label_printer = function(instance, local) {

    local.print = function (parent, action){
        var params = action.params
        var connection = null;
        connection = new instance.web.Session(undefined, params.proxy_url, {use_cors: true});
        connection.rpc('/hw_proxy/serial_write', {'params': JSON.stringify(params)})
            .then(function(result){
                if(result.status == 'error'){
                    throw new Error(result.message);
                }
            },function(){
                throw new Error('Could not connect to proxy');
            });

        parent.do_action({type: 'ir.actions.act_window_close'})
    };
    instance.web.client_actions.add('label_printer', 'instance.mrp_label_printer.print');
}
