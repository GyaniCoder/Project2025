function updateProduct(id) {
  const name = document.getElementById(`name-${id}`).value;
  const price = document.getElementById(`price-${id}`).value;
  const qty = document.getElementById(`qty-${id}`).value;

  fetch(`/api/edit_product/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name, price: price, quantity: qty })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      document.querySelector(`#product-${id} .product-name`).value = data.product.name;
      document.querySelector(`#product-${id} .product-price`).value = data.product.price;
      document.querySelector(`#product-${id} .product-quantity`).textContent = data.product.quantity;
      alert("Product updated!");
    } else {
      alert("Update failed: " + data.message);
    }
  });
}


function deleteProduct(id) {
  if (!confirm("Delete this product?")) return;

  fetch(`/api/delete_product/${id}`, {
    method: "POST"
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      document.getElementById(`product-${id}`).remove();
    } else {
      alert("Delete failed: " + data.message);
    }
  });
}
