
window.onload=function() {


//alerta al eliminar
(function() {
  const btnDelete = document.querySelectorAll('.btn-delete');
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('¿Está seguro que desea eliminar?')) {
        e.preventDefault();
      }
    }); 
  });
}());

// busqueda en tabla
    $(document).ready(function(){
      $("#buscar_tabla").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#tabla_busqueda tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
    });

    function editar_paciente(boton){
      var str = boton.value;
      var res = str.split(",");
      document.getElementById("input_id_paciente_editar").value=res[0];
      document.getElementById("input_nombre_paciente").value=res[1];
      document.getElementById("input_apellido_paciente").value=res[2];
    }
    function mostrarvalor(boton){
      var str = boton.value;
      var res = str.split(",");
      document.getElementById("input_id_paciente_nuevo_turno").value=res[0];
      document.getElementById("nombre_paciente").innerHTML="Nuevo turno Paciente: "+res[1]+" "+res[2];
      
      var id_medico = document.getElementById("tabla_medico");
      document.getElementById("input_id_medico").value=id_medico.value;
    }

    function select_medico(){
      var id_medico = document.getElementById("tabla_medico");
      document.getElementById("input_id_medico").value=id_medico.value;
    }
  }