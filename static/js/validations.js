// Función para limpiar el RUT, eliminando cualquier punto y guion
function limpiarRut(rut) {
    let rutLimpio = rut.replace(/[^\dKk-]/g, '').toUpperCase();  // Elimina todo excepto números y el guion
    console.log("RUT limpio: ", rutLimpio);  // Depuración: Ver el RUT después de limpiarlo
    return rutLimpio;
}

// Función para calcular el dígito verificador (DV) del RUT usando el algoritmo módulo 11
// Función para calcular el dígito verificador (DV) del RUT usando el algoritmo módulo 11
function calcularDV(rut) {
    let suma = 0;
    let multiplicador = 2;
    console.log("Calculando DV para el RUT: ", rut);

    for (let i = rut.length - 1; i >= 0; i--) {
        suma += parseInt(rut[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    const resto = suma % 11;
    const dv = 11 - resto;
    console.log("Suma total: ", suma, "Resto: ", resto, "DV calculado: ", dv);

    if (dv === 10) return "K";
    if (dv === 11) return "0";
    return dv.toString();
}

// Función para validar el RUT
function validarRut(rutCompleto) {
    rutCompleto = limpiarRut(rutCompleto);
    console.log("RUT limpio: ", rutCompleto);

    // Verificar si el RUT tiene el formato correcto
    if (rutCompleto.length !== 9 || rutCompleto.indexOf('-') === -1) {
        alert("El RUT debe tener el formato: 12345678-9");
        return false;
    }

    // Extraer el cuerpo (sin el dígito verificador) y el dígito verificador ingresado
    const [cuerpo, dvIngresado] = rutCompleto.split('-');
    console.log(`Cuerpo: ${cuerpo}, DV ingresado: ${dvIngresado}`);

    // Validar que el cuerpo del RUT contenga solo dígitos
    if (!/^\d{8}$/.test(cuerpo)) {
        alert("El cuerpo del RUT debe contener solo 8 dígitos.");
        return false;
    }

    // Calcular el dígito verificador esperado
    const dvCalculado = calcularDV(cuerpo);
    console.log(`DV calculado: ${dvCalculado}`);

    // Comparar el dígito verificador calculado con el ingresado
    if (dvCalculado !== dvIngresado.toUpperCase()) {
        alert(`El dígito verificador es incorrecto. Calculado: ${dvCalculado}, Ingresado: ${dvIngresado}`);
        return false;
    }

    // Si todo es válido, retornar true
    return true;
}
