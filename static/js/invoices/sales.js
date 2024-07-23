document.addEventListener('DOMContentLoaded', function () {
  let $customer = document.getElementById("id_customer");
  let $payment_method = document.getElementById("id_payment_method");
  $customer.selectedIndex = 1;
  $payment_method.selectedIndex = 1;
  let $detailBody = document.getElementById('detalle');
  let $product = document.getElementById('product');
  let $btnAdd = document.getElementById("btnAdd");
  let $btnGrabar = document.getElementById("btnGrabar");
  let $form = document.getElementById("frmSale");
  let $paymentInput = document.getElementById('id_payment');
  let $changeInput = document.getElementById('id_change');
  const $totalInput = document.getElementById('id_total');
  let detailSale = [];
  let sub = 0;

  console.log("detalle= ", detail_sales);
  if (detail_sales.length > 0) {
    detailSale = detail_sales.map(item => {
      let { product: id, product__description: description, quantity, price, subtotal: sub, iva } = item;
      price = parseFloat(price);
      quantity = parseFloat(quantity);
      iva = parseFloat(iva);
      sub = parseFloat(sub);
      return { id, description, price, quantity, iva, sub };
    });
    present();
    totals();
  }

  const calculation = (id, description, iva, price, quantity) => {
    const product = detailSale.find(prod => prod.id == id);
    if (product) {
      if (!confirm(`¿Ya existe ingresado ${product.description} =>  Desea actualizarlo?`)) return;
      quantity += product.quantity;
      detailSale = detailSale.filter(prod => prod.id !== id);
    }
    iva = iva > 0 ? ((price * quantity) * (iva / 100)).toFixed(2) : "0";
    iva = parseFloat(iva);
    sub = (price * quantity + iva).toFixed(2);
    sub = parseFloat(sub);
    detailSale.push({ id, description, price, quantity, iva, sub });
    present();
    totals();
  };

  const productChange = (e) => {
    const selectedOption = e.target.selectedOptions[0];
    const price = selectedOption.getAttribute('data-price');
    document.getElementById('price').value = price;
  };
  $product.addEventListener('change', productChange);
  productChange({ target: $product });

  const deleteproduct = (id) => {
    detailSale = detailSale.filter((item) => item.id !== id);
    present();
    totals();
  };

  function present() {
    let detalle = document.getElementById('detalle');
    detalle.innerHTML = "";
    detailSale.forEach((product) => {
      detalle.innerHTML += `<tr class="dark:text-gray-400 bg-white border-b dark:bg-[#0b1121] dark:border-secundario hover:bg-gray-50 dark:hover:bg-[#121c33]">
            <td>${product.id}</td>
            <td>${product.description}</td>
            <td>${product.price}</td>
            <td>${product.quantity}</td>
            <td>${product.iva}</td>
            <td>${product.sub}</td>
            <td class="text-center">
                <button rel="rel-delete" data-id="${product.id}" class="text-red-600 dark:text-red-500"><i class="fa-solid fa-trash"></i></button>
            </td>
          </tr>`;
    });
  }

  function totals() {
    const result = detailSale.reduce((acc, product) => {
      acc.iva += product.iva;
      acc.sub += product.sub;
      return acc;
    }, { iva: 0, sub: 0 });
    document.getElementById('id_subtotal').value = (result.sub - result.iva).toFixed(2);
    document.getElementById('id_iva').value = result.iva.toFixed(2);
    document.getElementById('id_total').value = result.sub.toFixed(2);
  }

  async function saveSale(urlPost, urlSuccess) {
    const formData = new FormData($form);
    formData.append("detail", JSON.stringify(detailSale));

    let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    console.log('FormData antes de enviar:');
    console.log(`csrf=${csrf}`);
    for (let [name, value] of formData.entries()) {
      console.log(`${name}: ${value}`);
    }

    try {
      const res = await fetch(urlPost, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrf,
        },
        body: formData
      });
      console.log(res);
      if (!res.ok) {
        const text = await res.text();
        console.log("error=> " + text);
        throw new Error(`HTTP error! Status: ${res.status}, Response: ${text}`);
      }

      const post = await res.json();
      console.log("Server message:", post.msg);
      alert(post.msg);
      window.location.href = urlSuccess;
    } catch (error) {
      console.error("Fetch error:", error);
      alert("Fetch error: " + error);
    }
  }

  $form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const total = parseFloat($totalInput.value) || 0;
    const payment = parseFloat($paymentInput.value) || 0;
    if (total > 0 && payment >= total) {
      $changeInput.value = (payment - total).toFixed(2);  // Asegura que el cambio esté actualizado
      await saveSale(save_url, '/sales/sales_list/');
    } else {
      alert("!!!Faltan datos de productos para grabar la venta o el pago no es suficiente!!!");
    }
  });

  $btnAdd.addEventListener('click', (e) => {
    let quantity = parseInt(document.getElementById('quantify').value);
    let stock = parseInt($product.options[$product.selectedIndex].dataset.stock);
    if (quantity > 0 && quantity <= stock) {
      let idProd = parseInt($product.value);
      let price = document.getElementById('price').value;
      price = parseFloat(price.replace(',', '.'));
      let iva = $product.options[$product.selectedIndex].dataset.iva;
      iva = parseFloat(iva.replace(',', '.'));
      let description = $product.options[$product.selectedIndex].text;
      calculation(idProd, description, iva, price, quantity);
    } else {
      alert(`cantidad negativa o superior al stock:[${stock}]`);
    }
  });

  $detailBody.addEventListener('click', (e) => {
    const fil = e.target.closest('button[rel=rel-delete]');
    if (fil) deleteproduct(parseInt(fil.getAttribute('data-id')));
  });

  $paymentInput.addEventListener('input', function () {
    const total = parseFloat($totalInput.value) || 0;
    const payment = parseFloat($paymentInput.value) || 0;
    const change = payment - total;
    console.log('Total:', total);
    console.log('Payment:', payment);
    console.log('Change:', change);
    $changeInput.value = change.toFixed(2);
  });
});
