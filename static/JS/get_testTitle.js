function select_change(){
            var options = $("#select option:selected");
            $("#id_pid").children().filter("option").remove();
            $.ajax({
                url: "/makepaper/",
                type: 'post',
                dataType: 'json',
                data: {'options': options.text()},
                headers: {'X-CSRFToken': '{{ csrf_token }}'},
                success: function (data) {
                    // var ret = eval("("+data.responseText+")");
                    // console.log(data)
                    str = ''
                    var select = document.getElementById("id_pid")
                    for (var i = 0; i < data.length; i++) {
                        var option = document.createElement("option")
                        option.innerText = data[i].title
                        option.value = data[i].id
                        select.appendChild(option)
                    }
                    }
                })
        }