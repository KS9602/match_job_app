var button_01 = document.getElementById('button_01')
var form_requirements_must_have = document.getElementById('form_requirements_must_have')
var i = 2

button_01.addEventListener('click',function(){
    var br = document.createElement('br');
    var inputName = 'requirement_must_have_0' + i;
    var newInput = document.createElement('input');
    form_requirements_must_have.appendChild(br);
    newInput.type = 'text';
    newInput.id = inputName;
    newInput.className = 'requirement_must_have';
    newInput.name = inputName;

    form_requirements_must_have.appendChild(newInput);

    i++
})

var button_02 = document.getElementById('button_02')
var form_requirements_optional = document.getElementById('form_requirements_optional')
var k = 2

button_02.addEventListener('click',function(){
    var br = document.createElement('br');
    var inputName = 'requirement_optional_0' + k;
    var newInput = document.createElement('input');
    form_requirements_optional.appendChild(br)
    newInput.type = 'text';
    newInput.id = inputName;
    newInput.className = 'requirement_optional';
    newInput.name = inputName;

    form_requirements_optional.appendChild(newInput);

    k++
})

var button_03 = document.getElementById('button_03')
var form_features = document.getElementById('form_features')
var j = 2

button_03.addEventListener('click',function(){
    var br = document.createElement('br');
    var inputName = 'feature_0' + j;
    var newInput = document.createElement('input');
    form_features.appendChild(br);
    newInput.type = 'text';
    newInput.id = inputName;
    newInput.className = 'feature';
    newInput.name = inputName;

    form_features.appendChild(newInput);

    j++
})