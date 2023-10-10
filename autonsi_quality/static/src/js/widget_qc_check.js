/** @odoo-module **/
import AbstractField from 'web.AbstractField';
import fieldRegistry from 'web.field_registry';

function getKeyByValue(object, value) {
    return Object.keys(object).find(key => object[key] === value);
}

var QCCheckForm = AbstractField.extend({
    template: "qccheck",
    start: function () {
        this._super.apply(this, arguments);
        if (this.recordData[this.nodeOptions.currentValue]) {
            this.value = this.recordData[this.nodeOptions.currentValue]
        }
    },
    _render: function () {
        var self = this;
        var question_id = this.record.context.question_id
        var qc_id = this.record.context.quality_check_id
        var view_mode = this.record.context.view_mode
        console.log(this.record.context)
        console.log(question_id)
        var rows = [];
        var gridrows = []
        var gridccolumnstring = "";
        var gridcolumn = []
        var columntype = "";
        var raw_material_col_data = [];
        var widgetlist = new Array();
        var material_col_data = [];
        var inputtype = "";
        console.log(this)
        if (question_id != undefined) {
            for (let i = 0; i < question_id.length; i++) {
                console.log(question_id)
                const title = Object.keys(question_id[i])
                const question_type = Object.values(question_id[i])
                // if (question_type == 'matrix') {
                //     console.log("matrix")
                //     console.log(title[0])
                //     gridccolumnstring += title[0]
                //     const matrix_data = this.record.context.matrix_data
                //     console.log(matrix_data)
                //     for (let i = 0; i < matrix_data.answer_ids.length; i++) {
                //         gridccolumnstring += "," + matrix_data.answer_ids[i]
                //
                //     }
                //     for (let i = 0; i < matrix_data.matrix_rows_ids.length; i++) {
                //
                //         gridrows.push(matrix_data.matrix_rows_ids[i])
                //     }
                //
                // }
                // if (question_type == 'Raw Material') {
                //     const raw_material_data = this.record.context.raw_material
                //     const qc_type = raw_material_data['mes_qc_type']
                //     const qc_item = raw_material_data['mes_qc_item']
                //     const n_values = raw_material_data['n_values']
                //     const units = raw_material_data['units']
                //     gridccolumnstring += "QC Type, QC Item, N-Values, Unit"
                //     columntype += "ro,ro,co,ro"
                //     var griddata = [qc_type,qc_item]
                //     griddata[3] = units
                //     material_col_data['rows'] = [{
                //         id: 1,
                //         data: griddata
                //     }]
                //     var n_values_col = []
                //
                // }
                //
                // if (question_type == 'Material') {
                //     const material_data = this.record.context.material_data
                //     const qc_type = material_data['mes_qc_type']
                //     const qc_item = material_data['mes_qc_item']
                //     const qc_standard = material_data['mes_qc_standard']
                //     const qc_tool = material_data['mes_qc_tool']
                //     const qc_frequency = material_data['mes_qc_frequency']
                //     console.log(qc_type)
                //     console.log(qc_item)
                //     console.log(qc_standard)
                //     console.log(qc_tool)
                //     console.log(qc_frequency)
                //     gridccolumnstring += "QC Type, QC Item, QC Standard, QC Tool, QC Frenquency, Input"
                //     columntype += "ro,ro,ro,ro,ro,co"
                //     console.log(material_data)
                //     material_col_data['rows'] = [{
                //         id: 1,
                //         data: [qc_type, qc_item, qc_standard, qc_tool, qc_frequency]
                //     }]
                if (question_type == 'matrix') {
                    console.log("matrix")
                    console.log(title[0])
                    gridccolumnstring += title[0]
                    const matrix_data = this.record.context.matrix_data
                    console.log(matrix_data)
                    for (let i = 0; i < matrix_data.answer_ids.length; i++) {
                        gridccolumnstring += "," + matrix_data.answer_ids[i]

                    }
                    for (let i = 0; i < matrix_data.matrix_rows_ids.length; i++) {

                        gridrows.push(matrix_data.matrix_rows_ids[i])
                    }


                    inputtype += "ComboBox"
                    for (let i = 0; i < matrix_data.matrix_rows_ids.length; i++) {

                        gridrows.push(matrix_data.matrix_rows_ids[i])
                    }
                }
                if (question_type == 'After Setting' || question_type == 'SEMI LOT') {
                    const material_data = this.record.context.pqc_data
                    widgetlist[widgetlist.length] = title
                    widgetlist[widgetlist.length - 1][1] = question_type
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
                    material_col_data.push({
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
                                    type: "combo",
                                    name: 'Input',
                                    data: [
                                        {value: "OK", id: "id_1"},
                                        {value: "NG", id: "id_2"}
                                    ]
                                },
                            ]
                        }
                    )
                }

                //     if (question_type == 'After Setting' || question_type == 'SEMI LOT') {
                //         const material_data = this.record.context.pqc_data
                //         const qc_type = material_data['mes_qc_type']
                //         const qc_item = material_data['mes_qc_item']
                //         const qc_standard = material_data['mes_qc_standard']
                //         const qc_tool = material_data['mes_qc_tool']
                //         const qc_frequency = material_data['mes_qc_frequency']
                //         console.log(qc_type)
                //         console.log(qc_item)
                //         console.log(qc_standard)
                //         console.log(qc_tool)
                //         console.log(qc_frequency)
                //         gridccolumnstring += "QC Type, QC Item, QC Standard, QC Tool, QC Frenquency, Input"
                //         columntype += "ro,ro,ro,ro,ro,co"
                //         console.log(material_data)
                //         material_col_data['rows'] = [{
                //             id: 1,
                //             data: [qc_type, qc_item, qc_standard, qc_tool, qc_frequency]
                //         }]
                //         inputtype += "ComboBox"
                //     }
                //     if (question_type == 'After QC') {
                //         const material_data = this.record.context.oqc_data
                //         const qc_type = material_data['mes_qc_type']
                //         const qc_item = material_data['mes_qc_item']
                //         const qc_standard = material_data['mes_qc_standard']
                //         const qc_tool = material_data['mes_qc_tool']
                //         const qc_frequency = material_data['mes_qc_frequency']
                //         console.log(qc_type)
                //         console.log(qc_item)
                //         console.log(qc_standard)
                //         console.log(qc_tool)
                //         console.log(qc_frequency)
                //         gridccolumnstring += "QC Type, QC Item, QC Standard, QC Tool, QC Frenquency, Input"
                //         columntype += "ro,ro,ro,ro,ro,co"
                //         console.log(material_data)
                //         material_col_data['rows'] = [{
                //             id: 1,
                //             data: [qc_type, qc_item, qc_standard, qc_tool, qc_frequency]
                //         }]
                //         inputtype += "ComboBox"
                //     }
                // }
            }

            setTimeout(() => {

                rows.push({
                    padding: 5,
                    width: 90,
                    type: "button",
                    name: "button",
                    value: "Submit"

                })
                console.log(rows)
                const layout = new dhx.Layout("QCCheckFormLayout", {
                    type: "none",
                    rows: [
                        {
                            id: "С1",
                            html: "1",
                        },
                    ],
                    height: 500,
                    width: 1200
                });
                console.log(material_col_data)
                console.log(inputtype)
                // var v5layout = new dhtmlXLayoutObject({
                //     parent: "QCCheckFormLayout",
                //     pattern: "2E",
                //     cells: [{id: "a", header: false, height: 700}, {id: "b", header: false}]
                // });
                // var mycell = v5layout.cells("a")
                // var mygrid = mycell.attachGrid()
                // console.log(gridccolumnstring)
                // mygrid.setHeader(gridccolumnstring);
                // mygrid.setColTypes(columntype);
                // mygrid.setInitWidths("*,*,*,*,*,80");
                // if (inputtype == "ComboBox") {
                //     var combobox = mygrid.getCombo(5);
                //     combobox.put("X", "X")
                //     combobox.put("O", "O")
                // }
                // mygrid.init();
                // mygrid.parse(material_col_data, "json")
                //
                // var buttoncell = v5layout.cells("b")
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
                //
                // myform.attachEvent("onButtonClick", function (id) {
                //     console.log(mygrid);
                //     var serialization = mygrid.getAllRowIds()
                //     var data = mygrid.parentFormOnSubmit();
                //     var answer_id;
                //     var answer_data = new Array();
                //     console.log(mygrid.cell)
                //     console.log(serialization);
                //     var userdata = mygrid.cells(1, 5);
                //     var celldata = userdata.getValue();
                //     console.log(celldata)
                //     const answer_input = {"question_key": "input", "value": celldata}
                //     console.log(answer_input)
                //     if (view_mode == "MO Quality Check") {
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
                //                 args: [{'qc_id': qc_id, 'answer_record_ids': answer_data}],
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
                //                 args: [[qc_id], {state: 'pass'}],
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
                //
                //
                // });

                const form = new dhx.Form(null, {
                    css: "dhx_widget--bg_white dhx_layout-cell--bordered",
                    padding: 40,
                    rows: rows
                });

                form.getItem("button").events.on("click", function (events) {
                    const properties = form.getItem("input")
                    var answer_data = new Array();
                    for (let i = 0; i < question_id.length; i++) {
                        const title = Object.keys(question_id[i])
                        const question_type = Object.values(question_id[i])
                        if (question_type != "matrix") {
                            if (form.getItem(title).config.type == "input") {
                                var answer_id;
                                const answer_input = {
                                    "question_key": title[0],
                                    "value": form.getItem(title).config.value
                                }

                                console.log(form.getItem(title).config.value)
                                self._rpc({
                                    model: 'mes.qc_form_answers_record',
                                    method: "create",
                                    args: [answer_input],

                                }).then(function (result) {
                                    console.log('------result-----')

                                    answer_id = result
                                    console.log(answer_id)
                                    answer_data[i] = answer_id
                                });

                            }
                            if (form.getItem(title).config.type == "datepicker") {
                                var answer_id;
                                const answer_input = {
                                    "question_key": title[0],
                                    "value": form.getItem(title).config.value
                                }

                                console.log(form.getItem(title).config.value)
                                self._rpc({
                                    model: 'mes.qc_form_answers_record',
                                    method: "create",
                                    args: [answer_input],

                                }).then(function (result) {
                                    console.log('------result-----')

                                    answer_id = result
                                    console.log(answer_id)
                                    answer_data[i] = answer_id
                                });

                            }
                            if (form.getItem(title).config.type == "checkbox") {
                                var answer_input;
                                if (form.getItem(title).config.checked) {
                                    if (form.getItem(title).config.checked == true)
                                        answer_input = {"question_key": title[0], "value": 'True'}

                                } else {
                                    answer_input = {"question_key": title[0], "value": 'False'}

                                }
                                var answer_id;

                                self._rpc({
                                    model: 'mes.qc_form_answers_record',
                                    method: "create",
                                    args: [answer_input],

                                }).then(function (result) {
                                    console.log('------result-----')

                                    answer_id = result
                                    console.log(answer_id)
                                    answer_data[i] = answer_id
                                });
                            }
                            if (question_type == 'raw_material') {
                                console.log("raw_material")
                                const raw_material = form.getItem(title[0]).container.getWidget()
                                const raw_material_state = raw_material._state
                                const raw_material_data = self.record.context.raw_material
                                const n_values = raw_material_data.n_values
                                var inputdata = ""
                                for (let i = 1; i <= n_values; i++) {
                                    const name = "N" + i
                                    inputdata += name + ": " + raw_material_state[name] + "; "
                                }
                                answer_input = {"question_key": title[0], "value": inputdata}
                                var answer_id;

                                self._rpc({
                                    model: 'mes.qc_form_answers_record',
                                    method: "create",
                                    args: [answer_input],

                                }).then(function (result) {
                                    console.log('------result-----')

                                    answer_id = result
                                    console.log(answer_id)
                                    answer_data[i] = answer_id
                                });

                            }
                            if (question_type == 'material') {
                                console.log("material")
                                const raw_material = form.getItem(title[0]).container.getWidget()
                                console.log(raw_material)
                                answer_input = {"question_key": title[0], "value": inputdata}

                            }
                        }
                        if (question_type == 'matrix') {
                            console.log(">0")
                            for (let j = 0; j < question_id.length - length + 1; j++) {
                                var inputdata = "";
                                if (widgetlist[j][1] == "grid") {
                                    var gridvalue = grid.data
                                    for (let k = 0; k < gridvalue._order.length; k++) {
                                        inputdata += gridvalue._order[k]['Checklist'] + ": " + getKeyByValue(gridvalue._order[k], true) + "; "
                                    }
                                    answer_input = {"question_key": title[0], "value": inputdata}

                                    console.log(inputdata)
                                    console.log(gridvalue)
                                    var answer_id;

                                    self._rpc({
                                        model: 'mes.qc_form_answers_record',
                                        method: "create",
                                        args: [answer_input],

                                    }).then(function (result) {
                                        console.log('------result-----')

                                        answer_id = result
                                        console.log(answer_id)
                                        answer_data[i] = answer_id
                                    });
                                }
                            }
                        }


                    }
                    setTimeout(() => {
                        console.log(answer_data)
                        self._rpc({
                            model: 'mes.qc_answers',
                            method: "create",
                            args: [{'qc_id': qc_id, 'answer_record_ids': answer_data}],

                        }).then(function (result) {
                            console.log(result)
                        });

                    }, 1000)

                    if (properties.config.checked === true) {
                        console.log("true")
                        self._rpc({
                            model: 'sh.mrp.quality.check',
                            method: "write",
                            args: [[qc_id], {state: 'pass'}],

                        }).then(function (result) {
                            console.log(result)

                        });

                        setTimeout(() => {
                            var action = {
                                type: 'ir.actions.client',
                                tag: 'reload',
                            }
                            self.do_action(action)
                        }, 1000)
                    }
                    if (properties.config.checked === false || !("checked" in properties.config)) {
                        console.log("false")
                        self._rpc({
                            model: 'sh.mrp.quality.check',
                            method: "write",
                            args: [[qc_id], {state: 'fail'}],

                        }).then(function (result) {
                            console.log(result)
                        });

                        setTimeout(() => {
                            var action = {
                                type: 'ir.actions.client',
                                tag: 'reload',
                            }
                            self.do_action(action)
                        }, 800)
                    }
                })

                // const grid = new dhx.Grid(null, {
                //     columns: material_col_data,
                //     data: gridrows,
                //     selection: "row",
                //     adjust: true,
                //     editable: true
                // });

                for (let i = 0; i < question_id.length - length; i++) {
                    if (widgetlist[i][1] == "grid") {
                        form.getItem(widgetlist[i][0]).attach(grid)
                    }
                    if (widgetlist[i][1] == "raw_material") {
                        console.log(widgetlist[i][0])
                        const raw_material_form = new dhx.Form(null, {
                            css: "dhx_widget--bg_white dhx_layout-cell--bordered",
                            padding: 40,
                            rows: [
                                {
                                    cols: raw_material_col_data
                                }
                            ]
                        });
                        //raw_material_form.getItem(widgetlist[i][0]).attachHTML(raw_material_html)
                        console.log(raw_material_form)
                        form.getItem(widgetlist[i][0]).attach(raw_material_form)
                    }
                    if (widgetlist[i][1] == "material") {

                        const material_form = new dhx.Form(null, {
                            css: "dhx_widget--bg_white dhx_layout-cell--bordered",
                            padding: 40,
                            rows: [
                                {
                                    cols: material_col_data
                                },
                            ]
                        });
                        form.getItem(widgetlist[i][0]).attach(material_form)
                    }
                    if (widgetlist[i][1] == 'After Setting' || widgetlist[i][1] == 'SEMI LOT') {
                        const material_form = new dhx.Form(null, {
                            css: "dhx_widget--bg_white dhx_layout-cell--bordered",
                            padding: 40,
                            rows: [
                                {
                                    cols: material_col_data
                                },
                            ]
                        });
                        console.log(widgetlist)
                        var list = form.getItem(widgetlist[i][1])
                        console.log(list)
                        form.getItem(widgetlist[i][1]).attach(material_form)
                    }
                }

                layout.getCell("С1").attach(form)
            }, 400)
        }
    }

})
fieldRegistry.add('qccheck', QCCheckForm);

