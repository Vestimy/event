        function choice_category(){
            var tmp_id = parseInt ($("#city_id").val());
            if(tmp_id == 0)
            {
                $("#arena_id").attr('disabled', 'disabled');
            }
            else
            {
                $("#arena_id").removeAttr('disabled');
                load_subcategory();
            }
        }

        function load_subcategory(){
            $.ajax({
                type: "POST",
                url: "/events/get_city_all",
                data: $('form').serialize(),
                success: function(response) {
                    var json = jQuery.parseJSON(response)
                    obj = Object.keys(json)

                    $("#arena_id")
                        .find('option')
                        .remove()
                        .end()
                        .append('<option value="0">Не выбрано</option>')
                        .val('0');

                    var value, key;
                    for(item in obj){
                        value = json[obj[item]];
                        key = obj[item];
                    $("#arena_id").append($("<option></option>")
                            .attr("value",key)
                            .text(value));
                    }

                },
            error: function(error) {
                console.log(error);
            }
        });
        }

        $(document).ready(function() {
            choice_category();
            $("#city_id").change(function() {
                choice_category();
            });

            $("#arena_id").change(function() {
            });
        });
