$(" .plus-text-input ").click(function() {
    var new_input = document.createElement("span");
    new_input.className = "label label-primary my_tags";
    var input_text = $(this).parent().find(".text-input")[0].value
    $(this).parent().find(".text-input")[0].value = "";
    var test_input = $('<input />', {'type' : 'text' , 'name': 'my_tags', 'value': input_text});
    new_input.append(test_input);
    $(this).parent().append(new_input);

});

$("body").on("click", ".my_tags", function() {
    console.log("ugh");
    $(this).remove();
});