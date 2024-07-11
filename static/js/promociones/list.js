$(function () {

        tblSale = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'searchdata'
                },
                dataSrc: ""
            },
            columns: [
                {"data": "descripcion"},
                {"data": "fecha_inicio"},
                {"data": "fecha_fin"},
                {"data": "canal_cliente_id.canal_cliente_descripcion"},
                {"data": "tipo_promocion_id.descripcion"},
                //{"data": "producto_bonificar_id"},
                {"data": "monto"},
                {"data": "cantidad_bonificar"},
                {"data": "descuento"},
    
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // var buttons = '<a href="#' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        // buttons += '<a href="#' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return data;
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            },
            paging: true,
            searching: true
        });

        $('#data tbody')
         .on('click', 'a[rel="details"]', function () {
             var tr = tblSale.cell($(this).closest('td, li')).index();
             var data = tblSale.row(tr.row).data();
             console.log(data);

             $('#tblDet').DataTable({
                 responsive: true,
                 autoWidth: false,
                 destroy: true,
                 deferRender: true,
                 //data: data.det,
                 ajax: {
                     url: window.location.pathname,
                     type: 'POST',
                     data: {
                         'action': 'search_details_prod',
                         'id': data.id
                     },
                     dataSrc: ""
                 },
                 columns: [
                     {"data": "articulo_id.descripcion"},
                     {"data": "precio_unitario"},
                     {"data": "cantidad"},
                     {"data": "total_item_bruto"},

                 ],
                 columnDefs: [
                     {
                         targets: [-1, -3],
                         class: 'text-center',
                         render: function (data, type, row) {
                             return '$' + parseFloat(data).toFixed(2);
                         }
                     },
                     {
                         targets: [-2],
                         class: 'text-center',
                         render: function (data, type, row) {
                             return data;
                         }
                     },
                 ],
                 initComplete: function (settings, json) {

                 }
             });

             $('#myModelDet').modal('show');
         });
});


