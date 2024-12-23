function get_user_data() {
    fetch("http://localhost:2500/get_user_profile", {method: "GET", credentials: 'include'})
    .then(response => response.json()) 
    .then(data => {
        if (data.status == 'not_logged_in') {
            return;
        }
        document.getElementById("city").value = data.city
        document.getElementById("street").value = data.street
        document.getElementById("apartment_num").value = data.apartment_num
        document.getElementById("phone").value = data.phone
    });
}

function make_order() {
    const city = document.getElementById("city").value
    const street = document.getElementById("street").value
    const apartment_num = document.getElementById("apartment_num").value
    const phone = document.getElementById("phone").value

    let cart = JSON.parse(localStorage.getItem("cart"))

    const orderData = {
        'items' : cart,
        'city' : city,
        'street' : street,
        'apartment_num' : apartment_num,
        'phone' : phone
        }

    fetch("http://localhost:2500/make_order", {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
    })
    .then(response => response.json()) // Dekodowanie JSON z odpowiedzi
    .then(result => { 
        // localStorage.clear();
    });

    
}