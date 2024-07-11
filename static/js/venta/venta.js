const url = "/customer";
var tblProducts;
var vents ={
    items : {
        fecha_pedido : '',
        empresa_id : '',
        sucursal_id:'',
        nro_pedido : '',
        tipo_pedido_id: '',
        condicion_venta: '',
        plazo:'',
        cliente_id: '',
        tcli:'',
        tipo_documento:'',
        total_pedido:0.00,
        detvent: []
    },
    calculate_invoice: function(){
        var subtotal = 0.00;
        //var iva = $('input[name="iva"]').val();
        $.each(this.items.detvent, function(pos,dict){
            console.log(pos)
            console.log(dict)
            dict.subtotal = dict.cantidad * parseFloat(dict.punitario);
            subtotal += dict.subtotal;
        });
        this.items.total_pedido = subtotal;
        //this.items.iva = this.items.subtotal * iva;
        //this.items.total = this.items.subtotal - this.items.iva;

        $('input[name="total_pedido"]').val(this.items.total_pedido.toFixed(2));
        //$('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        //$('input[name="total"]').val(this.items.total.toFixed(2));

        console.log(subtotal);
    },
    add: function(item){
        this.items.detvent.push(item);
        this.list();

    },
    list: function(){
        this.calculate_invoice();
        $(function () {
            tblProducts = $('#tblProducts').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                data: vents.items.detvent,
                columns: [
                    {"data": "articulo_id"},
                    {"data": "descripcion"},
                    {"data": "marca_id.marca_nombre"},
                    {"data": "punitario"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [0],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                        }
                    },
                    {
                        targets: [-3],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<input type="text" name="punitario" class="form-control form-contro-sm input-sm" autocomplete="off" value="'+row.punitario+'">';

                            //return 'S/. ' + parseFloat(data).toFixed(2);    
                        }                    
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<input type="text" name="cantidad" class="form-control form-contro-sm input-sm" autocomplete="off" value="'+row.cantidad+'">';
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return 'S/. ' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                rowCallback(row, data, displayNum, displayIndex, dataIndex){
                    $(row).find('input[name="cantidad"]').TouchSpin({
                        min: 1,
                        max: 10000000,
                        step: 1
                    });
                },
                initComplete: function (settings, json) {
        
                }
            });
        });
    }
};
function agregarCliente(id,nombre,tcliente,tdoc) {
	console.log("Nombre:" + nombre);
    console.log("ID:" + id);
    console.log("Tipo de Cliente:" + tcliente);
    console.log("Tipo de Documento:" + tdoc);
	$('#ncliente').val(nombre);
    $('#tcliente').val(tcliente);
    $('#tdocument').val(tdoc);
}
$(function (){
    $('input[name="search"]').autocomplete({
        source: function(request, response){
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function(event,ui){
            event.preventDefault();
            console.clear();
            ui.item.cantidad=1;
            ui.item.subtotal=0.00;
            ui.item.punitario=0.00;
            vents.add(ui.item);
            vents.list();
            console.log(vents.items);
            $(this).val('');
        }

    });
    $('input[name="searchc"]').autocomplete({
        source: function(request, response){
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_cliente',
                    'term': request.term
                },
                success: function(data){
                    response($.map(data, function(item){
                        return {
                            label: item.name,
                            value: item.cliente_id,
                            tcliente: item.canal_cliente_id,
                            tdoc: item.tipo_identificacion_id

                        }
                    }));
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function(event,ui){
            $('#searchc').val(ui.item.label);
            $('#client_id').val(ui.item.value); 
            $('#tcliente').val(ui.item.tcliente);
            $('#tdocument').val(ui.item.tdoc);
            agregarCliente(ui.item.value,ui.item.label,ui.item.tcliente,ui.item.tdoc);
            console.log(ui.item.value);
            console.log(ui.item.label);
            console.log(ui.item.tcliente);
            console.log(ui.item.tdoc);
            $(this).val('');
            return false;    
        }
    });
    $('#searchc').keyup(function (e) {
        if (e.keyCode === 13) {
          agregarCliente();
        }
      });
      
    $('.btnRemoveAll').on('click', function(){
        vents.items.detvent = [];
        vents.list();
    });
    $('#tblProducts tbody')
    .on('click','a[rel="remove"]', function(){
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.detvent.splice(tr.row, 1);
        vents.list();
    })
    .on('change keyup', 'input[name ="cantidad"]', function () {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();


        //var data = tblProducts.row(tr.row).node();
        vents.items.detvent[tr.row].cantidad = cant;
        vents.calculate_invoice();
        $('td:eq(5)', tblProducts.row(tr.row).node()).html('S/. ' + vents.items.detvent[tr.row].subtotal.toFixed(2));
        console.log(cant);
    })

    .on('change keyup', 'input[name ="punitario"]', function () {
        console.clear();
        var puni = parseFloat($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();


        //var data = tblProducts.row(tr.row).node();
        vents.items.detvent[tr.row].punitario = puni;
        vents.calculate_invoice();
        $('td:eq(5)', tblProducts.row(tr.row).node()).html('S/. ' + vents.items.detvent[tr.row].subtotal.toFixed(2));
        console.log(puni);
    });
    //Guarda Datos
    $('form').on('submit', function (e) {
        e.preventDefault();
        vents.items.fecha_pedido = $('input[name="fecha_pedido"]').val();
        vents.items.empresa_id = $('select[name="empresa_id"]').val();
        vents.items.sucursal_id = $('select[name="sucursal_id"]').val();
        vents.items.nro_pedido = $('input[name="nro_pedido"]').val();
        vents.items.tipo_pedido_id = $('select[name="tipo_pedido_id"]').val();
        vents.items.condicion_venta = $('select[name="condicion_venta"]').val();
        vents.items.plazo = $('input[name="plazo"]').val();
        vents.items.cliente_id = $('input[id="client_id"]').val();
        vents.items.tcli = $('input[id="tcliente"]').val();
        vents.items.tipo_documento = $('input[id="tdocument"]').val();

        console.log("Fecha Pedido: "+vents.items.fecha_pedido);
        console.log("Empresa: "+vents.items.empresa_id);
        console.log("Sucursal: "+vents.items.sucursal_id);
        console.log("Nro Pedido: "+vents.items.nro_pedido);
        console.log("Tipo Pedido: "+vents.items.tipo_pedido_id);
        console.log("Condiciones: "+vents.items.condicion_venta);
        console.log("Plazo: "+vents.items.plazo);
        console.log("Cliente ID: "+vents.items.cliente_id);
        console.log("Tipo Cliente: "+vents.items.tcli);
        console.log("Tipo Documento: "+vents.items.tipo_documento);

        var parameters = new FormData();
        parameters.append('action',$('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));


        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (){
                location.href = '../../home';
        });
    });
});