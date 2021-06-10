var types = ["ANGER", "ANTICIPATION", "DISGUST", "FEAR", "JOY", "SADNESS", "SURPRISE", "TRUST"]
var colors = [[183, 0, 32], [244, 85, 1], [60, 0, 60], [80, 150, 0], [231, 211, 0], [0, 124, 216], [3, 128, 37], [155, 183, 0]]
var data = [];
function getAddr(endpoint) {
    IP = "127.0.0.1"
    PORT = "5000"
    ADDR = "http://" + IP + ":" + PORT + endpoint
    return ADDR
}

//Functions to mix colors
function colorChannelMixer(colorChannelA, colorChannelB, amountToMix) {
    var channelA = colorChannelA * amountToMix;
    var channelB = colorChannelB * (1 - amountToMix);
    return parseInt(channelA + channelB);
}

function colorMixer(rgbA, rgbB, amountToMix) {
    var r = colorChannelMixer(rgbA[0], rgbB[0], amountToMix);
    var g = colorChannelMixer(rgbA[1], rgbB[1], amountToMix);
    var b = colorChannelMixer(rgbA[2], rgbB[2], amountToMix);
    return [r, g, b];
}

function colorCode(a) {
    return "rgb(" +a[0] + "," + a[1] + "," + a[2] + ")";
}

function fillTarget(target, template, elem) {
    var template_html = $(template).html()
    var content = Mustache.to_html(template_html, elem)
    $(target).html(content);
}

function reformat(elem) {
    var currentColor = [255, 255, 255];
    if (elem.POSITIVE === true)
        elem.TYPE = "Positive"
    else if (elem.NEGATIVE == true)
        elem.TYPE = "Negative"
    types.forEach((emotion, index) => {
        if (elem[emotion] === true) {
            elem[emotion] = "✔️";
            currentColor = colorMixer(colors[index], currentColor, 0.5);
        }
        else {
            elem[emotion] = "❌";
        }
    });
    elem.color = colorCode(currentColor);
}

function updateScreen(item) {
    var newColor = data.results[item.id].color;
    var isPositive = data.results[item.id].POSITIVE;
    fillTarget("#_top", "#header_template", data.results[item.id]); //Change the data at top
    item.style.background = newColor; // Change the color of the dot
    $("#message").css("color",newColor); // Change color of header text
    if (isPositive)
        $("#type").css("color","green"); // Change color of "Type of emotion"
    else 
        $("#type").css("color","red"); // Change color of "Type of emotion"
}
var URL = getAddr("/sentences/200")
$.get(URL, (d => {
    // console.log(d);
    data = d;
    data.results.forEach(reformat);
}));
