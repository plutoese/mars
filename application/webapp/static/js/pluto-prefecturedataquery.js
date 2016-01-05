
/**
 * @author plutoese <glen.zhang7@gmail.com>
 * @version 1.0
 * @function form process
 * @dependency
 * @plugin：
 * @时期多选框：http://wenzhixin.net.cn/p/multiple-select/docs
 * @区域树形多选框：http://jonmiles.github.io/bootstrap-treeview/
 * @区域树形多选框：https://github.com/jonmiles/bootstrap-treeview
 * @变量多选框：http://pbauerochse.github.io/searchable-option-list/examples.html
 */

$(document).ready(function(){
	// 初始设置
	// 设置网站根目录


	// 设置区域表单的初始数据
    var region_defaultData = [
		{
			text: '中国',
			tags:['100000'],
			selectable: false
		}
    ];
    // 获取变量表单的html，存入变量$variable_form_html
    var $variable_form_html = $("#variable_form").html();

    // 初始化时期多选框
    $("select#period").multipleSelect({
        placeholder: "年份",
        width: 180,
        // 事件：关闭选择框
        onClose: function() {
        	// 获得选择的时期
            var period_choosen = $("select#period").multipleSelect('getSelects');

            // 如果选择了时期
            if (period_choosen.length > 0) {
	            // 通过ajax获得数据
	            $.post($SCRIPT_ROOT + '/_prefeture_from_year_get_regions', {
	                period_done: period_choosen
	                }, function(data) {
	                	// 设置区域表单
	                	$('#region').treeview({
	                		// 设置区域数据
	                    	data: data.regions,
	                    	multiSelect: true,
	                    	// 定义区域表单中的节点选择，如何选择某个节点，则全选下属一级节点
	                    	onNodeSelected: function(event,node){
	                        	var $myselected = $(this);
                                if (node.state['expanded']) {
                                    if (node['nodes']) {
                                        // 选好选择所有的子节点
                                        $.each(node['nodes'], function (index, value) {
                                            $myselected.treeview('selectNode', [value['nodeId'], {silent: true}]);
                                        });
                                    }
                                }
	                    	},
	                    	// 定义区域表单中的节点选择，如何反选某个节点，则反选所有下属一级节点
		                    onNodeUnselected: function(event,node){
		                        var $myunselected = $(this);
                                if (!node.state['expanded']) {
                                    if (node['nodes']) {
                                        $.each(node['nodes'], function (index, value) {
                                            $myunselected.treeview('unselectNode', [value['nodeId'], {silent: true}]);
                                        });
                                    }
                                }
		                    }
	                });
	                $('#region').treeview('uncheckAll', { silent: true });
	                $('#region').treeview('collapseAll', { silent: true });
	                $('#region_done').removeAttr('disabled');
	         	});
			}else{
				$('#region').treeview({
                    data: region_defaultData,
                });
                $('#region_done').attr('disabled','disabled');
			}
        },
    });

	// 设置初始的区域表单
	$('#region').treeview({
        data: region_defaultData,
    });

    // 设置初始的变量表单
    $("select#variable").searchableOptionList({
        showSelectAll: true,
        maxHeight: '250px'
    });

    // 点击选择区域完成按钮
    $('#region_done').click(function(){
    	 // 获取时期和区域选择变量period_choosen和region_choosen
        var region_nodes = $('#region').treeview('getSelected');

        // 如果选择了区域
        if (region_nodes.length > 0) {
            var period_choosen = $("select#period").multipleSelect('getSelects');
            var region_choosen = [];
            var i = 0;
            $.each(region_nodes, function (index, value) {
                //region_choosen[i] = value['text'];
                region_choosen[i] = value['tags'][0];
                i += 1;
            });

            // 重新设置变量表单，并复制
            $("#variable_area").remove();
            $("#variable_form").prepend($variable_form_html);
            $("#hregion").attr('value', region_choosen);

            // 通过ajax获得变量数据
            $.post($SCRIPT_ROOT + '/_prefeture_from_region_get_variables', {
                region_selected: region_choosen,
                period_selected: period_choosen
            }, function (data) {
                $("select#variable").searchableOptionList({
                    data: data.variables,
                    showSelectionBelowList: true,
                    showSelectAll: true,
                    maxHeight: '250px'
                });
            });
            $('#to_be_submit').removeAttr('disabled');
        }else{
            $("#variable_area").remove();
            $("#variable_form").prepend($variable_form_html);
            // 设置初始的变量表单
            $("select#variable").searchableOptionList({
                showSelectAll: true,
                maxHeight: '250px'
            });
            $('#to_be_submit').attr('disabled','disabled');
        }
    });

});
