const url = "/customer";
var tblPromocion;
var vents ={
    items : {
        fecha_inicio:'',
        fecha_fin : '',
        descripcion : '',
        canal_cliente_id : '',
        tipo_promocion_id: '',
        producto_bonificar_id: '',
        monto: 0.00,
        cantidad_bonificar:'',   
        descuento: '',
        detprom: []
    },
    add: function(item){
        this.items.detprom.push(item);
        this.list();
    },
    list: function(){
        $(function () {
            tblPromocion = $('#tblPromocion').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                data: vents.items.detprom,
                columns: [
                    {"data": "id"},
                    {"data": "descripcion"},
                    {"data": "marca_id.marca_nombre"},
                    {"data": "cant"},
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
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<input type="text" name="cant" class="form-control form-contro-sm input-sm" autocomplete="off" value="'+row.cant+'">';
                        }
                    },
                ],
                rowCallback(row, data, displayNum, displayIndex, dataIndex){
                    $(row).find('input[name="cant"]').TouchSpin({
                        min: 1,
                        max: 10000000,
                        step: 1
                    });
                },
                initComplete: function (settings, json) {
        
                },
                paging: true,
                searching: true
            });
        });
    }
};
function agregarCliente(id,nombre,tcliente) {
	console.log("Nombre:" + nombre);
    console.log("ID:" + id);
    console.log("Tipo de Cliente:" + tcliente);
	$('#ncliente').val(nombre);
    $('#tcliente').val(tcliente);
    vents.items.cli = id;
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
            ui.item.cant=1;
            vents.add(ui.item);
            vents.list();
            console.log(vents.items);
            $(this).val('');
        }

    });
    $('.btnRemoveAll').on('click', function(){
        vents.items.detprom = [];
        vents.list();
    });
    
    $('#tblPromocion tbody')
    .on('click','a[rel="remove"]', function(){
        var tr = tblPromocion.cell($(this).closest('td, li')).index();
        vents.items.detprom.splice(tr.row, 1);
        vents.list();
    })
    .on('change keyup', 'input[name ="cant"]', function () {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblPromocion.cell($(this).closest('td, li')).index();


        //var data = tblProducts.row(tr.row).node();
        vents.items.detprom[tr.row].cant = cant;
       
    });
    

    //Guarda Datos
    $('form').on('submit', function (e) {
        e.preventDefault();
        vents.items.fecha_inicio = $('input[name="fecha_inicio"]').val();
        vents.items.fecha_fin = $('input[name="fecha_fin"]').val();
        vents.items.descripcion = $('input[name="descripcion"]').val();
        vents.items.canal_cliente_id = $('select[name="canal_cliente_id"]').val();
        vents.items.tipo_promocion_id = $('select[name="tipo_promocion_id"]').val();
        vents.items.producto_bonificar_id = $('select[name="producto_bonificar_id"]').val();
        vents.items.monto = $('input[name="monto"]').val();
        vents.items.cantidad_bonificar = $('input[name="cantidad_bonificar"]').val();
        vents.items.descuento = $('input[name="descuento"]').val();

        console.log(vents.items.fecha_inicio);
        console.log(vents.items.fecha_fin);
        console.log(vents.items.descripcion);
        console.log("CANAL : "+vents.items.canal_cliente_id);
        console.log(vents.items.tipo_promocion_id);
        console.log("BONI : "+ vents.items.producto_bonificar_id);
        console.log(vents.items.monto);


        var parameters = new FormData();
        parameters.append('action',$('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));


        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (){
                location.href = '../../home';
        });
    });
});
