// ================================ FUNCIÓN DE ALERTA PERSONALIZADA ================================
function mostrarAlerta() {
    alert("¡Acción realizada con éxito!");
}

// ================================ VALIDACIÓN DEL FORMULARIO ================================
document.getElementById("formulario").addEventListener("submit", function (e) {
    e.preventDefault(); // Evita el envío automático

    let esValido = true;

    // Campos del formulario
    const nombre = document.getElementById("nombre");
    const correo = document.getElementById("correo");
    const mensaje = document.getElementById("mensaje");

    // Limpiar mensajes de error
    document.getElementById("errorNombre").textContent = "";
    document.getElementById("errorCorreo").textContent = "";
    document.getElementById("errorMensaje").textContent = "";

    // Validación del nombre
    if (nombre.value.trim() === "") {
        document.getElementById("errorNombre").textContent = "Por favor, ingresa tu nombre.";
        esValido = false;
    }

    // Validación del correo
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexEmail.test(correo.value.trim())) {
        document.getElementById("errorCorreo").textContent = "Ingresa un correo válido.";
        esValido = false;
    }

    // Validación del mensaje
    if (mensaje.value.trim().length < 5) {
        document.getElementById("errorMensaje").textContent = "El mensaje debe tener al menos 5 caracteres.";
        esValido = false;
    }

    // Si todo es correcto
    if (esValido) {
        alert("¡Gracias, " + nombre.value + "! Tu mensaje ha sido enviado.");
        this.reset();
    }
});
