if (data.success) {
    // window.location.href = data.url;

    if (data.response.invoice.state == "PENDING") {

      paymentBtnFormSpinner.style.display = "block";
      paymentBtnFormText.textContent = "Payment in progress...";
      paymentBtnForm.setAttribute("disabled", "disabled");

      let invoice_id = data.response.invoice.invoice_id;

      console.log(invoice_id)

      let intervalId = setInterval(async () => {
        const res = await checkPaymentStatus(invoice_id);

        if (res.response.invoice.state === "PROCESSING") {
          paymentBtnFormText.textContent = "Received. Validating payment ..."

        } else if (res.response.invoice.state === "COMPLETE") {
          clearInterval(intervalId);
          paymentBtnFormSpinner.style.display = "none";
          paymentBtnFormText.textContent = "Payment Completed successfully.";
          paymentBtnForm.removeAttribute("disabled");
          document
            .getElementById("payment-btn-help-text")
            .innerHTML = "Payment was successful"

          setTimeout(() => {
            handleCreateTransaction(poolId, accountId, planId)
          }, 4000)

          //}, 30000);  Stop checking after 40 seconds
        } else if (res.response.invoice.state === "FAILED") {
          clearInterval(intervalId);
          paymentBtnFormSpinner.style.display = "none";
          paymentBtnFormText.textContent = "Payment Failed. Retry?";
          paymentBtnForm.removeAttribute("disabled");
          document
            .getElementById("payment-btn-help-text")
            .innerHTML = "You cancelled the payment. Would you like to retry?"
        } else if (res.response.invoice.state === "RETRY") {
          clearInterval(intervalId);
          paymentBtnFormSpinner.style.display = "none";
          paymentBtnFormText.textContent = "Payment Failed";
          paymentBtnForm.removeAttribute("disabled");
          document
            .getElementById("payment-btn-help-text")
            .innerHTML = "Failed to initiate transaction. Retry";
        }
      }, 15000); // Check every 10 seconds
      // Set a timeout to clear the interval after 40 seconds
    }

    async function checkPaymentStatus(id) {
      // Implement the logic to check the payment status
      // You might need to make another API call here to check the status
      const response = await fetch(`{% url 'dashboard:invest:check-payment-status' %}?invoice_id=${id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      const data = await response.json();
      return data;

    }

    async function handleCreateTransaction(pool_id, account_id, plan_id) {
      const response = await fetch(`/dashboard/invest/handle-payment-create-transaction/${pool_id}/${account_id}/${plan_id}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({phone_number: phoneNo.value})
      });

      console.log(phoneNo.value)

      const data = await response.json()

      console.log(data)

      window.location.href = data.url

    }

  }