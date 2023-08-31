function addToCart(id,name, price){
    event.preventDefault()
    alert("hello")
    body: JSON.stringify({
            "id": id,
            "price": price
    }),
    headers: {
            "Content-Type": "application/json"
        }
}