$(document).ready(function () {
  $('#cpf').mask('000.000.000-00', {reverse: true});
  $('#telefone').mask('(00) 0000-0000');
  $('#cep').mask('00000-000');
  $('#valor_unitario').mask('000.000.000.000.000,00', {reverse: true});
})

function validateEmail(email) {
  var re = /\S+@\S+\.\S+/;
  return re.test(email);
}