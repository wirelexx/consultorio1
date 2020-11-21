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