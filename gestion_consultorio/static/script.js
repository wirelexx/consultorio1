function editar_paciente(boton){
  var str = boton.value;
  alert(str);
  var res = str.split(",");
  document.getElementById("input_id_paciente").value=res[0];
  document.getElementById("input_nombre_paciente").value=res[1];
  document.getElementById("input_apellido_paciente").value=res[2];
}