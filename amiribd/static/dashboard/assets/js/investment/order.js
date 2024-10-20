$(document).ready(function () {
    const investmentRate = parseFloat("2.00");
    $("#daily-rate").html(`(${investmentRate}%)`);
    const investmentPriceSlider = $("#amount-step");
    const investmentAmount = $("#custom-amount");
    const investmentAmountPaymentHiddenInput = $("#custom-amount-value");

    const investAmountSum = $("#invest-cc-amount");
    const investAmountSummaryDisplay = $("#select-cc-price-summary");
    const investmentAmountSummaryCostFee = $("#select-cc-price-summary-cost-fee");

    const investmentPaymentChoiceSummary = $("#selected-cc-payment-option");

    investmentAmount.val("0.00");
    investmentAmountPaymentHiddenInput.val("0.00");
    investAmountSum.html("0.00");
    investAmountSummaryDisplay.html("0.00");
    investmentAmountSummaryCostFee.html(parseInt(investmentRate * parseFloat(investmentAmount.val())));

    investmentPriceSlider.on("mouseover click", updateSliderValue);

    function updateSliderValue() {
        const sliderValue = $(".noUi-handle-lower").attr("aria-valuenow");
        const priceValue = parseFloat(parseInt(sliderValue) * 100).toFixed(2);
        investmentAmount.val(priceValue);
        investmentAmountPaymentHiddenInput.val(priceValue);
        investAmountSum.html(priceValue);
        investAmountSummaryDisplay.html(priceValue);
        calculateTheRateInvestment(priceValue);
        const amount = parseFloat(priceValue + parseFloat((investmentRate * priceValue))).toFixed(2)
        $("#total-investment").text(amount);
    }

    function calculateTheRateInvestment(amount) {
        investmentAmountSummaryCostFee.html(parseInt(investmentRate * amount));
    }

    const paymentOptions = $("li.invest-cc-item");
    let selectedPaymentOption = $("#selected-payment-option");

    const paymentOptionInput = $("#invest-choose-wallet");

    paymentOptions.each(function () {
        $(this).on("click", function () {
            const selection = $(this).html();
            selectedPaymentOption.html(selection);
            const coinNameSpan = $(this).find('.coin-name[data-bs-pay-text="coin-pay-select"]');
            if (coinNameSpan.length) {
                console.log(coinNameSpan);
                investmentPaymentChoiceSummary.html(coinNameSpan.text());
            }

            const coinWalletOption = $(this).find('.invest-cc-opt').attr('data-payment-option');
            paymentOptionInput.val(coinWalletOption);
        });
    });

    const amountLabel = $('#amount-label');
    const amountSummaryLabel = $('#amount-summary-label');

    const formNoteHelpSliderId = $("#form-note-slider-help-slider");
    const floatingMaxAmountLabel = $("#slider-max-money");

    let investmentPlanOptionBox = $("#selected-plan-type");
    const investTypeOptions = $(".invest-type-cc-item");
    const savingsDuration = $("#savings-duration");

    const overalInvestType = $("#overal-invest-type");

    savingsDuration.hide();

    const savingsDurationObject = {
        "1D": "1-day",
        "1W": "1-week",
        "2W": "2-weeks",
        "1M": "1-month",
        "3M": "3-months",
        "C": "custom",
    };

    const savingsPricing = {
        "1D": { min: 100, max: 1000 },
        "1W": { min: 500, max: 1500 },
        "2W": { min: 1000, max: 3000 },
        "1M": { min: 2000, max: 6000 },
        "3M": { min: 6000, max: 12000 }
    };

    investTypeOptions.each(function () {
        $(this).on("click", function () {
            investmentPlanOptionBox.html($(this).html());

            const investTypePlan = $(this).find(".invest-type-cc-opt");
            const savingDurationSummary = $("#savings-duration-sumary");
            const savingDurationSummaryValue = $("#selected-cc-saving-duration");

            if (investTypePlan.length) {
                const investTypePlanOption = investTypePlan.attr("data-investment-option");

                if (investTypePlanOption.toLowerCase() === 'savings') {
                    overalInvestType.val("save");

                    const SavingLimitDiv = $("#savings-limit");

                    savingDurationSummary.show();
                    investmentPriceSlider.hide();
                    investmentAmount.removeAttr("disabled").attr("type", "number");
                    savingsDuration.show();
                    amountLabel.html("Principal Savings");
                    amountSummaryLabel.html("to Saving");

                    const saveDurations = $(".invest-amount-control");

                    saveDurations.each(function () {
                        let saveDuration = $(this)
                        $(this).on("click", function () {
                            if ($(this).is(":checked")) {
                                if (Object.values(savingsDurationObject).includes($(this).val())) {
                                    if ($(this).val() === 'custom') {
                                        const summaryForm = $("#custom-save-duration-form");
                                        $(summaryForm).submit(function (event) {
                                            event.preventDefault();
                                            console.log($(this).serialize());

                                            const duration = $(this).find("input[name=duration_in_days]").val();
                                            const amount = $(this).find("input[name=custom_amount_to_save]").val();
                                            const dailyInterest = parseFloat(investmentRate * amount).toFixed(2);

                                            $(savingDurationSummaryValue).text(`${duration} Day${duration >= 2 ? 's' : ''}`);
                                            $("#select-cc-price-summary-cost-fee").text(dailyInterest);

                                            const totalPlusInterest = parseFloat(dailyInterest) + parseFloat(amount);
                                            $("#total-investment").text(totalPlusInterest.toFixed(2));

                                            // Clear all form fields
                                            $(this).find('input[type="text"], input[type="number"], input[type="email"], textarea').val('');
                                            $(this).find('input[type="checkbox"], input[type="radio"]').prop('checked', false);

                                            $("#upload-custom-save-button-close").click();
                                        });

                                        $("input[name=custom_amount_to_save]").on("input", function(event){
                                            const duration = $("input[name=duration_in_days]").val()
                                            const amount = parseFloat(event.target.value)
                                            $(savingDurationSummaryValue).text(`${duration} Day${duration >= 2 ? 's' : ''}`);
                                            const dailyInterest = parseFloat(investmentRate * amount).toFixed(2);
                                            $("#select-cc-price-summary").text(amount)
                                            $("#select-cc-price-summary-cost-fee").text(dailyInterest);
                                            const totalPlusInterest = parseFloat(dailyInterest) + parseFloat(amount);
                                            $("#total-investment").text(parseFloat(totalPlusInterest).toFixed(2));
                                        })
                                    }

                                    function updateMinMaxValue(minValue, maxValue) {
                                        const savingValue = $(".noUi-handle-lower");
                                        savingValue.attr("aria-valuemin", parseFloat(minValue));
                                        savingValue.attr("aria-valuemax", parseFloat(maxValue));
                                    }

                                    function updateTheMinMaxHelpTextValue(minValue, maxValue) {
                                        formNoteHelpSliderId.html(`invest ${parseFloat(minValue).toFixed(2)} ksh and upto ${parseFloat(maxValue).toFixed(2)} ksh`);
                                        floatingMaxAmountLabel.html(`Max Amout ${maxValue.toLocaleString()} KSH`);
                                    }

                                    function updateTheValueAndText(index) {
                                        updateMinMaxValue(savingsPricing[index].min, savingsPricing[index].max);
                                        updateTheMinMaxHelpTextValue(savingsPricing[index].min, savingsPricing[index].max);
                                        investmentAmount.attr("min", savingsPricing[index].min).attr("max", savingsPricing[index].max);
                                        investmentAmount.val(savingsPricing[index].min);
                                        InputSavingListenerFunction(savingsPricing[index].min, savingsPricing[index].max);
                                    }

                                    function InputSavingListenerFunction(min, max) {
                                        investAmountSummaryDisplay.html(min);
                                        investmentAmountPaymentHiddenInput.val(min);
                                        $("#total-investment").text(min);
                                        investmentAmountSummaryCostFee.html(parseInt(investmentRate * min));
                                    }


                                    function InputSavingListenerFunction(min, max) {
                                        $('#select-cc-price-summary').html(min);
                                        $('#custom-amount-value').val(min);
                                        $('#total-investment').text(min);

                                        $('#select-cc-price-summary-cost-fee').html(parseInt(investmentRate * parseFloat($('#custom-amount').val())));

                                        $('#custom-amount').on('keyup', function (e) {
                                            let inputAmount = parseInt($(this).val());

                                            if (inputAmount < min) {
                                                // Reset to min if below minimum
                                                // inputAmount = min;
                                                $('#savings-limit').addClass("text-danger form-note pt-1").html(`Amount can only be between ${min} and ${max} for the ${$(saveDuration).val()} saving duration. Resetting to minimum value.`);
                                            } else if (inputAmount > max) {
                                                // Reset to max if above maximum
                                                inputAmount = max;
                                                $('#savings-limit').addClass("text-danger form-note pt-1").html(`Amount can only be between ${min} and ${max} for the ${$(saveDuration).val()} saving duration. Resetting to maximum value.`);
                                            } else {
                                                $('#savings-limit').removeClass("text-danger").html("");
                                            }

                                            // Set the reset input value
                                            $('#custom-amount').val(inputAmount);

                                            // Calculate and update the displayed values
                                            calculateTheRateInvestment(inputAmount);

                                            $('#select-cc-price-summary').html(inputAmount);
                                            $('#custom-amount-value').val(inputAmount);
                                            const investmentSummary = parseFloat(
                                                parseFloat($('#custom-amount-value').val() * investmentRate) + parseFloat($('#custom-amount-value').val())
                                            ).toFixed(2)

                                            $('#total-investment').text(investmentSummary);

                                            let costFee = parseInt(investmentRate * parseFloat(inputAmount));
                                            $('#select-cc-price-summary-cost-fee').html(costFee);
                                            $('#total-investment').text(costFee);
                                        });


                                    }

                                    function updateSaveDurationValue(value) {
                                        if (value.includes("-")) {
                                            const parts = value.split("-");
                                            const formattedValue = parts[1].charAt(0).toUpperCase() + parts[1].slice(1);
                                            savingDurationSummaryValue.html(parts[0] + " " + formattedValue);
                                        } else {
                                            savingDurationSummaryValue.html(value);
                                        }
                                    }

                                    switch ($(this).val()) {
                                        case "1-day":
                                            updateTheValueAndText('1D');
                                            updateSaveDurationValue($(this).val());
                                            break;
                                        case "1-week":
                                            updateTheValueAndText('1W');
                                            updateSaveDurationValue($(this).val());
                                            break;
                                        case "2-weeks":
                                            updateTheValueAndText('2W');
                                            updateSaveDurationValue($(this).val());
                                            break;
                                        case "1-month":
                                            updateTheValueAndText('1M');
                                            updateSaveDurationValue($(this).val());
                                            break;
                                        case "3-months":
                                            updateTheValueAndText('3M');
                                            updateSaveDurationValue($(this).val());
                                            break;
                                        default:
                                            break;
                                    }
                                }
                            }
                        });
                    });
                } else if (investTypePlanOption.toLowerCase() === 'investment') {
                    savingsDuration.hide();
                    amountLabel.html("Principal Investment");
                    amountSummaryLabel.html("to Investment");

                    formNoteHelpSliderId.html("invest 1000 ksh and upto 10,000 ksh");
                    floatingMaxAmountLabel.html("Max Amout 10,000 KSH");

                    investmentPriceSlider.show();
                    investmentAmount.attr("disabled", "disabled");
                    savingDurationSummary.hide();
                    overalInvestType.val("invest");
                } else {
                    savingsDuration.hide();
                }
            }
        });
    });
});


class InvestmentOrder {
    constructor() {
        this.principalElement = $("#select-cc-price-summary");
        this.durationElement = $("#selected-cc-saving-duration");
        this.interestElement = $("#select-cc-price-summary-cost-fee");
        this.submitButton = $("#saving-invesment-submit-form").find("button[id='submit-saving-button']");
        this.price = null;
        this.principal = null;
        this.duration = null;
        this.interest = null;
        this.amount = null;

        this.principal_amount = null;
        this.duration_of_saving_investment = null;
        this.interest_amount = null;
        this.expected_daily_interest_plus_amount = null;
        this.instruction = null;

        // Initialize the MutationObserver
        this.initObserver();
    }

    init =()=> {
        this.checkFields();
        
        $(this.submitButton).click(function (event) {
            event.preventDefault();
            
            // Update the class properties
            this.principal = $("#select-cc-price-summary").text();
            this.duration = $("#selected-cc-saving-duration").text();
            this.interest = $("#select-cc-price-summary-cost-fee").text();
            this.amount = parseFloat(this.principal) + parseFloat(this.interest);
            const data = {
                principal: this.principal,
                duration: this.duration,
                interest: this.interest,
                amount: this.amount
            };
            $("#pay-amount").val(data.principal);
            $("#modalOverlay").fadeIn(300);
            $("#modalZoom").fadeIn(300).addClass("show");
        });

        this.processPayment()
    }

     processPayment (){
        let paystackBtn = document.getElementById('paystackbtn');
        const paystackKey = $("input[name=active_paystack_key]").val()
        paystackBtn.addEventListener('click', async function (event) {
            event.preventDefault();
            const payAmount = $("#pay-amount").val();
            const duration = $("#selected-cc-saving-duration").text();
            const interestAmount = $("#select-cc-price-summary-cost-fee").text();
            const expectedDailyInterestPlusAmount = parseFloat(payAmount) + parseFloat(interestAmount);
            const instruction = `
            <h2>Investment Plan: <strong>${duration} Duration</strong></h2> <br />
            <h2>Total Investment: <strong>${payAmount} KES</strong> </h2> <br />
            <h2>Interest: <strong>${interestAmount} KES</strong> </h2> <br />
            <h2>Total Amount: <strong>${expectedDailyInterestPlusAmount} KES</strong> </h2> <br />`;
            const instructionToSubmit = `
            ${instruction}
            <br />
            <br />
            ${$("#id_instruction").val()}
            `
            const dataToSubmit = {
                principal_amount:payAmount,
                duration_of_saving_investment:duration,
                interest_amount: interestAmount,
                expected_daily_interest_plus_amount: expectedDailyInterestPlusAmount,
                instruction: instructionToSubmit,
                reason: "savings_investment"
            }
            const profileUserId = event.target.dataset.bsProfile;
            const emailAddress = event.target.dataset.bsEmail;


            const handleProcessTransactionForSaveInvestPayment = (url, dataToSubmit) => {
                $.ajax({
                    url: url,
                    method: 'POST',
                    data: JSON.stringify(dataToSubmit),
                    success: function (data) {
                        if (data.success) {
                            setTimeout(()=>{
                                window.location.href = data.url
                            }, 1000)
                        }
                    },
                    error: function(xhr, status, error){
                        console.log(xhr)
                        alert(error)
                    }
                })
            }

            let handler = PaystackPop.setup({
                key: paystackKey,
                email: emailAddress,
                amount: parseFloat($("#pay-amount").val()).toFixed(2) * 100,
                currency: "KES", 
                ref: '',
                callback: function (response) {
                    var reference = response.reference;
                    alert('Payment complete! Reference: ' + reference);
                    const url = `/payments/paystack/payment-status/?reference=${reference}`
                    const newUrl = `/payments/paystack/payment-status/?reference=${reference}&principal_amount=${encodeURIComponent(dataToSubmit.principal_amount)}&duration_of_saving_investment=${encodeURIComponent(dataToSubmit.duration_of_saving_investment)}&interest_amount=${encodeURIComponent(dataToSubmit.interest_amount)}&expected_daily_interest_plus_amount=${encodeURIComponent(dataToSubmit.expected_daily_interest_plus_amount)}&instruction=${encodeURIComponent(dataToSubmit.instruction)}&reason=${encodeURIComponent(dataToSubmit.reason)}`;
                    $.ajax({
                        url: newUrl,
                        method: 'GET',
                        success: function (data) {
                            alert('Payment successful! Your transaction has been processed.');
                            if (data.success && data.reason=="save_invest") {
                                const url = data.update_transaction_url
                                $("a#closeAddPlanPopupForm-subscribe").click();
                                handleProcessTransactionForSaveInvestPayment(url, {
                                    amount: parseFloat($("#pay-amount").val()).toFixed(2),
                                    reference: reference,
                                });
                            }
                        },
                        error: function(xhr, status, error){
                            console.log(xhr)
                            alert(error)
                        }
                    })
                },
                onClose: function (error) {
                    alert('Transaction was not completed, window closed.');
                    console.log(error);
                }
            });
            handler.openIframe();

        })
    }

    checkFields() {
        const principal = $.trim(this.principalElement.text());
        const duration = $.trim(this.durationElement.text());
        const interest = $.trim(this.interestElement.text());
        const amount = parseFloat(principal) + parseFloat(interest);

        if (principal === '' || duration === 'Nill' || interest === '' || isNaN(amount) || amount === 0) {
            $(this.submitButton).prop("disabled", true);
        } else {
            $(this.submitButton).prop("disabled", false);
        }
    }

    initObserver() {
        const config = { childList: true, subtree: true };

        const observer = new MutationObserver(() => {
            this.checkFields();
        });

        // Start observing the target nodes for changes
        observer.observe(this.principalElement[0], config);
        observer.observe(this.durationElement[0], config);
        observer.observe(this.interestElement[0], config);
    }
}



// Handle modal close
$("a#closeAddPlanPopupForm-subscribe").click(function () {
    $("#modalZoom").fadeOut(300).removeClass("show");
    $("#modalOverlay").fadeOut(300);  // Hide background overlay
});