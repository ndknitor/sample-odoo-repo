/** @odoo-module **/
import AbstractField from 'web.AbstractField';
import fieldRegistry from 'web.field_registry';

var QCCheckList = AbstractField.extend({
    template: "qclist",
    start: function () {
        this._super.apply(this, arguments);
        if (this.recordData[this.nodeOptions.currentValue]) {
            this.value = this.recordData[this.nodeOptions.currentValue]
        }
    },
    _render: function () {
        var self = this;
        console.log(self)
        var form_selection = this.record.context.form_selection
        var form_id = this.record.context.form_id
        console.log(form_id)
        var rows = [];
        var gridrows = []
        var gridccolumnstring = [];
        var columntype = [];
        var columnwidth = [];
        var raw_material_col_data = []
        var material_col_data = [];
        var pqc_data = {};
        var inputtype = "";
        var qc_sop_array = [];
        var listgridcolumnstring = [
            {width: 150, id: "qc_sop_type", header: [{text: "QC SOP Type"}]},
            {width: 150, id: "qc_sop", header: [{text: "QC SOP"}]},
            {width: 150, id: "qc_id", header: [{text: "QC ID"}]}
        ]
        var list_row_data = [];
        for (var form in form_selection) {
            var title = Object.keys(form_selection[form])
            var question_type = Object.values(form_selection[form])
            list_row_data.push({
                "qc_sop_type": title[0],
                "qc_sop": question_type[0],
                "qc_id": form_id[form]
            })
            console.log(title)
            console.log(question_type)
            if (title[0] == 'matrix') {
                console.log("matrix")
                console.log(title[0])
                var grid_header_string = ""
                grid_header_string += title[0]
                const matrix_data = this.record.context.data[form]
                console.log(matrix_data)

                for (let i = 0; i < matrix_data.answer_ids.length; i++) {
                    grid_header_string += "," + matrix_data.answer_ids[i]

                }
                for (let i = 0; i < matrix_data.matrix_rows_ids.length; i++) {

                    gridrows.push(matrix_data.matrix_rows_ids[i])
                }
                gridccolumnstring.push(grid_header_string)
            }
            if (title[0] == 'Raw Material') {
                console.log(form)

                const raw_material_data = this.record.context.data[form]
                console.log(raw_material_data)
                const qc_type = raw_material_data['mes_qc_type']
                const qc_item = raw_material_data['mes_qc_item']
                const n_values = raw_material_data['n_values']
                const units = raw_material_data['units']
                var grid_header_string = ""
                grid_header_string += "QC Type, QC Item, N-Values, Unit"
                var columntypestring = "ro,ro,co,ro"
                var columnwidthstring = "*,*,100,*"
                var griddata = [qc_type, qc_item]
                griddata[3] = units
                var data_col_data = []

                console.log(data_col_data)
                var n_values_col = []
                for (var i = 0; i < n_values; i++) {
                    n_values_col.push({
                        type: "input",
                        name: 'input' + i,
                        width: 100
                    })
                }
                raw_material_col_data.push({
                        css: "dhx_layout-cell--bordered",
                        title: "QC Type",
                        cols: [
                            {
                                type: "text",
                                name: 'qc_type',
                                value: qc_type
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Item",
                        cols: [
                            {
                                type: "text",
                                name: 'qc_item',
                                value: qc_item
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "Input",
                        cols: n_values_col
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Item",
                        cols: [
                            {
                                type: "text",
                                name: 'units',
                                value: units
                            },
                        ]
                    },
                )
            }

            if (title[0] == 'Material') {
                const material_data = this.record.context.data[form]
                const qc_type = material_data['mes_qc_type']
                const qc_item = material_data['mes_qc_item']
                const qc_standard = material_data['mes_qc_standard']
                const qc_tool = material_data['mes_qc_tool']
                const qc_frequency = material_data['mes_qc_frequency']
                console.log(qc_type)
                console.log(qc_item)
                console.log(qc_standard)
                console.log(qc_tool)
                console.log(qc_frequency)
                console.log(material_col_data)
                rows.push({
                    type: "container",
                    name: question_type[0],
                    padding: "12px 0px",
                    height: "300"
                })
                material_col_data.push({
                        css: "dhx_layout-cell--bordered",
                        title: "QC Type",
                        cols: [
                            {
                                type: "text",
                                name: 'qc_type',
                                value: qc_type
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Item",
                        cols: [
                            {
                                type: "text",
                                name: 'qc_item',
                                value: qc_item
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Standard",
                        cols: [
                            {
                                type: "text",
                                name: 'qc_standard',
                                value: qc_standard
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Tool",
                        cols: [
                            {
                                type: "text",
                                name: 'qc_tool',
                                value: qc_tool
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Frequency",
                        cols: [
                            {
                                type: "text",
                                name: 'qc_frequency',
                                value: qc_frequency
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "Input",
                        cols: [
                            {
                                type: "select",
                                name: 'input',
                                labelWidth: "70px",
                                labelPosition: "top",
                                options: [
                                    {content: "OK", value: "ok"},
                                    {content: "NG", value: "ng"}
                                ]
                            },
                        ]
                    }
                )
                // var data_col_data = {}
                // data_col_data['rows'] = [{
                //     id: 1,
                //     data: [qc_type, qc_item, qc_standard, qc_tool, qc_frequency]
                // }]
                // console.log(data_col_data)
                // inputtype += "ComboBox"
                // gridccolumnstring.push(grid_header_string)
                // columntype.push(columntypestring)
                // columnwidth.push(columnwidthstring)
                // raw_material_col_data.push(data_col_data)
            }
            if (title[0] == 'After Setting' || title[0] == 'SEMI LOT') {
                const material_data = this.record.context.data[form]
                const qc_type = material_data['mes_qc_type']
                const qc_item = material_data['mes_qc_item']
                const qc_standard = material_data['mes_qc_standard']
                const qc_tool = material_data['mes_qc_tool']
                const qc_frequency = material_data['mes_qc_frequency']
                rows.push({
                    type: "container",
                    name: question_type[0],
                    padding: "12px 0px",
                    height: "300"
                })
                pqc_data.push({
                        css: "dhx_layout-cell--bordered",
                        title: "QC Type",
                        cols: [
                            {
                                type: "text",
                                name: qc_type,
                                value: qc_type
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Item",
                        cols: [
                            {
                                type: "text",
                                name: qc_item,
                                value: qc_item
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Standard",
                        cols: [
                            {
                                type: "text",
                                name: qc_standard,
                                value: qc_standard
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Tool",
                        cols: [
                            {
                                type: "text",
                                name: qc_tool,
                                value: qc_tool
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "QC Frequency",
                        cols: [
                            {
                                type: "text",
                                name: qc_frequency,
                                value: qc_frequency
                            },
                        ]
                    },
                    {
                        css: "dhx_layout-cell--bordered",
                        title: "Input",
                        cols: [
                            {
                                type: "select",
                                name: 'input',
                                options: [
                                    {content: "OK", value: "ok"},
                                    {content: "NG", value: "ng"}
                                ]
                            },
                        ]
                    }
                )
            }
            if (title[0] == 'After QC') {
                const material_data = this.record.context.data[form]
                const qc_type = material_data['mes_qc_type']
                const qc_item = material_data['mes_qc_item']
                const qc_standard = material_data['mes_qc_standard']
                const qc_tool = material_data['mes_qc_tool']
                const qc_frequency = material_data['mes_qc_frequency']
                console.log(qc_type)
                console.log(qc_item)
                console.log(qc_standard)
                console.log(qc_tool)
                console.log(qc_frequency)
                var grid_header_string = ""
                grid_header_string += "QC Type, QC Item, QC Standard, QC Tool, QC Frenquency, Input"
                var columntypestring = "ro,ro,ro,ro,ro,co"
                var columnwidthstring = "*,*,*,*,*,80"
                console.log(material_data)
                var data_col_data = {}
                data_col_data['rows'] = [{
                    id: 1,
                    data: [qc_type, qc_item, qc_standard, qc_tool, qc_frequency]
                }]
                inputtype += "ComboBox"
                gridccolumnstring.push(grid_header_string)
                columntype.push(columntypestring)
                columnwidth.push(columnwidthstring)
                raw_material_col_data.push(data_col_data)
            }
        }
        qc_sop_array['rows'] = list_row_data
        setTimeout(() => {
            const layout = new dhx.Layout("QCListFormLayout1", {
                type: "none",
                rows: [
                    {
                        cols: [{
                            id: "С1",
                            html: "1",
                            width: 300,
                            height: 400
                        },
                            {
                                id: "C2",
                                html: "2",
                                width: 1200,
                                height: 500
                            }]

                    },
                    {
                        id: "R1",
                        html: "3",
                        height: 120,
                        width: 300
                    }],
                height: 500,
                width: 1500
            });
            const grid = new dhx.Grid("С1", {
                columns: listgridcolumnstring,
                data: list_row_data,
                selection: "row"
            })
            grid.hideColumn("qc_id");
            grid.events.on('afterSelect', function (id) {
                console.log(id)
                layout.getCell("C2").detach()
                if (id.qc_sop_type == "Raw Material") {
                    console.log(id.qc_sop_type)
                    const form = new dhx.Form(null, {
                        css: "dhx_widget--bg_white dhx_layout-cell--bordered",
                        padding: 40,
                        rows: [
                            {
                                cols: raw_material_col_data
                            },
                        ]
                    });
                    layout.getCell("C2").attach(form)
                }
                if (id.qc_sop_type == "Material") {
                    console.log(id.qc_sop_type)
                    const form = new dhx.Form(null, {
                        css: "dhx_widget--bg_white dhx_layout-cell--bordered",
                        padding: 40,
                        rows: [
                            {
                                cols: material_col_data
                            },
                        ]
                    });
                    layout.getCell("C2").attach(form)
                }
            })
            layout.getCell("С1").attach(grid)
            const buttonform = new dhx.Form(null, {
                css: "dhx_widget--bg_white dhx_layout-cell--bordered",
                padding: 40,
                rows: [
                    {
                        type: "button",
                        name: "button",
                        text: "Submit",
                        size: "medium",
                        view: "flat",
                        color: "primary"
                    }
                ]
            });
            buttonform.events.on("click", function (name, e) {
                console.log(e)
                console.log(name)
                const widgetform = layout.getCell("C2").getWidget()
                console.log(widgetform)
                var answer_id;
                var answer_data = new Array();
                const selected_form = grid.selection.getCell()
                const selected_qc_id = selected_form.row.qc_id
                const selected_form_type = selected_form.row.qc_sop_type
                console.log(selected_form.row.qc_id)
                console.log(n_values_col.length)
                const widgetname = widgetform.getValue()
                console.log(widgetname)
                var input_values = []
                if (selected_form_type == "Raw Material") {
                    for (var i = 0; i < n_values_col.length; i++) {
                        var input_string = "input" + i
                        console.log(widgetname[input_string])
                        input_values.push({"question_key": input_string, "value": widgetname[input_string]})
                    }
                    console.log(input_values)
                    for (var i = 0; i < input_values.length; i++) {
                        self._rpc({
                            model: 'mes.qc_form_answers_record',
                            method: "create",
                            args: [input_values[i]],

                        }).then(function (result) {
                            console.log('------result-----')
                            answer_id = result
                            console.log(answer_id)
                            answer_data.push(answer_id)

                        });
                    }
                    console.log(answer_data)
                    setTimeout(() => {
                        console.log(answer_data)
                        self._rpc({
                            model: 'mes.qc_answers',
                            method: "create",
                            args: [{'qc_id': selected_qc_id, 'answer_record_ids': answer_data}],

                        }).then(function (result) {
                            console.log(result)
                        });
                    }, 1000)


                }
                if (selected_form_type == "Material") {
                    var input_string = "input"
                    input_values.push({"question_key": input_string, "value": widgetname[input_string]})

                    self._rpc({
                        model: 'mes.qc_form_answers_record',
                        method: "create",
                        args: input_values,

                    }).then(function (result) {
                        console.log('------result-----')
                        answer_id = result
                        console.log(answer_id)
                        answer_data.push(answer_id)
                    });
                    setTimeout(() => {
                        console.log(answer_data)
                        self._rpc({
                            model: 'mes.qc_answers',
                            method: "create",
                            args: [{'qc_id': selected_qc_id, 'answer_record_ids': answer_data}],

                        }).then(function (result) {
                            console.log(result)
                        });
                    }, 1000)


                }
                setTimeout(() => {
                    var action = {
                        type: 'ir.actions.act_window_close'
                    }
                    self.do_action(action)
                }, 1000)

            })
            layout.getCell("R1").attach(buttonform)
            // var listlayout = new dhtmlXLayoutObject({
            //     parent: "QCListFormLayout1",
            //     pattern: "3U",
            //     cells: [{id: "a", header: false, height: 700, width: 100}, {
            //         id: "b",
            //         header: false,
            //         height: 700,
            //         width: 900
            //     }, {id: "c", header: false}]
            // });
            //
            // var mycell = listlayout.cells("a")
            // var qccell = listlayout.cells("b")
            // var buttoncell = listlayout.cells("c")
            // var formData = [
            //     {
            //         padding: 5,
            //         width: 90,
            //         type: "button",
            //         name: "good_button",
            //         value: "Good"
            //     },
            //     {
            //         type: "newcolumn"
            //     },
            //     {
            //         padding: 5,
            //         width: 90,
            //         type: "button",
            //         name: "ng_button",
            //         value: "NG"
            //     }
            // ];
            // // var material_form = mycell.attachForm(material_col_data)
            // var myform = buttoncell.attachForm(formData)
            // var listgrid = mycell.attachGrid()
            // listgrid.setHeader(listgridcolumnstring)
            // listgrid.setColTypes(listgridcolumntype)
            // listgrid.init()
            // listgrid.parse(qc_sop_array, "json")
            // var qcgrid = qccell.attachGrid()
            // listgrid.attachEvent("onRowSelect", function (id, ind) {
            //     qcgrid.clearAll(true);
            //     console.log(columntype)
            //     console.log(raw_material_col_data)
            //     qcgrid.setHeader(gridccolumnstring[id])
            //     var title = Object.keys(form_selection[id])
            //     qcgrid.setColTypes(columntype[id])
            //     qcgrid.setInitWidths(columnwidth[id])
            //     qcgrid.init()
            //     qcgrid.parse(raw_material_col_data[id], "json")
            //
            //     console.log(id)
            //     console.log(ind)
            // })
            // myform.attachEvent("onButtonClick", function (id, ind) {
            //     console.log(id)
            //     console.log(qcgrid);
            //     var serialization = qcgrid.getAllRowIds()
            //     var data = qcgrid.parentFormOnSubmit();
            //     var answer_id;
            //     var answer_data = new Array();
            //     console.log(qcgrid.cell)
            //     console.log(serialization);
            //     var title = Object.keys(form_selection[form])
            //     if (title[0] == 'Material') {
            //         var userdata = qcgrid.cells(1, 5);
            //         var celldata = userdata.getValue();
            //         console.log(celldata)
            //         const answer_input = {"question_key": "input", "value": celldata}
            //         console.log(answer_input)
            //         self._rpc({
            //             model: 'mes.qc_form_answers_record',
            //             method: "create",
            //             args: [answer_input],
            //
            //         }).then(function (result) {
            //             console.log('------result-----')
            //             answer_id = result
            //             console.log(answer_id)
            //             answer_data[0] = answer_id
            //         });
            //         setTimeout(() => {
            //             console.log(answer_data)
            //             self._rpc({
            //                 model: 'mes.qc_answers',
            //                 method: "create",
            //                 args: [{'qc_id': form_id[id], 'answer_record_ids': answer_data}],
            //
            //             }).then(function (result) {
            //                 console.log(result)
            //             });
            //         }, 1000)
            //     }
            //     if (id == "good_button") {
            //         if (qc_id != undefined) {
            //             self._rpc({
            //                 model: 'sh.mrp.quality.check',
            //                 method: "write",
            //                 args: [[form_id[id]], {state: 'pass'}],
            //
            //             }).then(function (result) {
            //                 console.log(result)
            //
            //             });
            //         }
            //         setTimeout(() => {
            //             var action = {
            //                 type: 'ir.actions.act_window_close'
            //             }
            //             self.do_action(action)
            //         }, 1000)
            //     } else {
            //         setTimeout(() => {
            //             var action = {
            //                 type: 'ir.actions.act_window_close'
            //             }
            //             self.do_action(action)
            //         }, 1000)
            //     }
            // })

        }, 400)
    }
})
fieldRegistry.add('qclist', QCCheckList);
