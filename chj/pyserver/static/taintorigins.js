//Taint Origins

import { Util } from './util.js';

var TaintOrigins = {
    addtaintorigins : function(response) {
        var prdata = document.getElementById('prdata');
        var datatable = document.getElementById('datatable');

        prdata.replaceChild(this.get_taintorigins_data(response), datatable);
    },

    get_taintorigins_data : function(response) {
        var taints = response;

        var new_taint_data = document.createElement('div');
        new_taint_data.setAttribute('id', 'prdata');

        var table = document.createElement('table');
        table.setAttribute('id', 'datatable');
        table.classList.add('balanced');

        var header_row = document.createElement('tr');
        Util.add_table_header('Taint Origin', header_row);
        Util.add_table_header('Taint', header_row);
        table.appendChild(header_row);

        for (var taintorigin in taints) {
            var drow = document.createElement('tr');
        
            var dtaintorigin = document.createElement('td');
            var dtaint = document.createElement('td');

            dtaintorigin.textContent = taintorigin;

            drow.appendChild(dtaintorigin);
            var taintlink = Util.get_taint_link(taintorigin);
            Util.add_table_data_with_link(taints[taintorigin], drow, taintlink)

            table.appendChild(drow);

            new_taint_data.appendChild(table);
        }

        return table;
    }
}

export { TaintOrigins };
