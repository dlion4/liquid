

// document.addEventListener('DOMContentLoaded', (event) => {
//     const investmentRate = parseFloat("0.005")
//     const investmentPriceSlider = document.getElementById("amount-step");
//     const investmentAmount = document.getElementById("custom-amount");
//     const investmentAmountPaymentHiddenInput = document.getElementById("custom-amount-value");

//     const investAmountSum = document.getElementById("invest-cc-amount")
//     const investAmountSummaryDisplay = document.getElementById("select-cc-price-summary")
//     const investmentAmountSummaryCostFee = document.getElementById("select-cc-price-summary-cost-fee")

//     const investmentPaymentChoiceSummary = document.getElementById("selected-cc-payment-option")

//     investmentAmount.value = "0.00"
//     investmentAmountPaymentHiddenInput.value = "0.00"
//     investAmountSum.innerHTML = "0.00"
//     investAmountSummaryDisplay.innerHTML = "0.00"
//     investmentAmountSummaryCostFee.innerHTML = parseInt((investmentRate) * parseFloat(investmentAmount.value))


//     investmentPriceSlider.addEventListener("mouseover", updateSliderValue)
//     investmentPriceSlider.addEventListener("click", updateSliderValue)


//     function updateSliderValue() {
//         const sliderValue = document.querySelector(".noUi-handle-lower")
//         const value = sliderValue.getAttribute("aria-valuenow");
//         const priceValue = parseFloat(Number.parseInt(value) * 100).toFixed(2);
//         investmentAmount.value = priceValue;
//         investmentAmountPaymentHiddenInput.value = priceValue;
//         investAmountSum.innerHTML = priceValue;
//         investAmountSummaryDisplay.innerHTML = priceValue;
//         calculateTheRateInvestment(priceValue);
//         totalInvestment.textContent = priceValue;
//     }

//     function calculateTheRateInvestment(amount) {
//         investmentAmountSummaryCostFee.innerHTML = parseInt(investmentRate * amount)
//     }

//     const paymentSelectionBox = document.getElementById("invest-payment-selection-box")
//     const paymentOptions = document.querySelectorAll("li.invest-cc-item")
//     let selectedPaymentOption = document.getElementById("selected-payment-option")


//     const paymentOptionInput = document.getElementById("invest-choose-wallet")

//     paymentOptions.forEach(option => {
//         option.addEventListener("click", (e) => {
//             const selection = option.innerHTML;
//             selectedPaymentOption.innerHTML = selection
//             // Use querySelector to find the .coin-name span within the clicked option
//             const coinNameSpan = option.querySelector('.coin-name[data-bs-pay-text="coin-pay-select"]');

//             if (coinNameSpan) {
//                 // Perform actions with the coinNameSpan if needed
//                 console.log(coinNameSpan);
//                 // Example action
//                 investmentPaymentChoiceSummary.innerHTML = coinNameSpan.textContent;
//             }

//             // option selected for the input

//             const coinWalletOption = option.querySelector('.invest-cc-opt').getAttribute('data-payment-option')


//             paymentOptionInput.value = coinWalletOption
//         })
//     })


//     const totalInvestment = document.getElementById("total-investment")






//     const amountLabel = document.getElementById('amount-label')
//     const amountSummaryLabel = document.getElementById('amount-summary-label')

//     /// slider summary
//     const formNoteHelpSliderId = document.getElementById("form-note-slider-help-slider");
//     const floatingMaxAmountLabel = document.getElementById("slider-max-money")


//     let investmentPlanOptionBox = document.getElementById("selected-plan-type")
//     const investTypeOptions = document.querySelectorAll(".invest-type-cc-item")
//     const savingsDuration = document.getElementById("savings-duration")

//     const overalInvestType = document.getElementById("overal-invest-type")


//     savingsDuration.style.display = "none"


//     const savingsDurationObject = {
//         "1D": "1-day",
//         "1W": "1-week",
//         "2W": "2-weeks",
//         "1M": "1-month",
//         "3M": "3-months",
//         "C": "custom",
//     }

//     const savingsPricing = {
//         "1D": {
//             min: 100,
//             max: 1000
//         },
//         "1W": {
//             min: 500,
//             max: 1500
//         },
//         "2W": {
//             min: 1000,
//             max: 3000
//         },
//         "1M": {
//             min: 2000,
//             max: 6000
//         },
//         "3M": {
//             min: 6000,
//             max: 12000
//         },
//     }


//     investTypeOptions.forEach(investTypeOption => {
//         investTypeOption.addEventListener("click", () => {
//             investmentPlanOptionBox.innerHTML = investTypeOption.innerHTML

//             const investTypePlan = investTypeOption.querySelector(".invest-type-cc-opt")
//             const savingDurationSummary = document.getElementById("savings-duration-sumary")
//             const savingDurationSummaryValue = document.getElementById("selected-cc-saving-duration")

//             if (investTypePlan) {
//                 const investTypePlanOption = investTypePlan.getAttribute("data-investment-option")

//                 if (investTypePlanOption.toLowerCase() === 'savings') {


//                     overalInvestType.value = "save"


//                     const SavingLimitDiv = document.getElementById("savings-limit")

//                     savingDurationSummary.style.display = "block"

//                     // remove the slider btn for the price range
//                     investmentPriceSlider.style.display = "none"
//                     // activate the input field
//                     investmentAmount.removeAttribute("disabled")
//                     investmentAmount.type = "number"

//                     savingsDuration.style.display = "block";
//                     amountLabel.innerHTML = "Principal Savings"
//                     amountSummaryLabel.innerHTML = "to Saving"
//                     // the savings buttons are there
//                     const saveDurations = document.querySelectorAll(".invest-amount-control")

//                     saveDurations.forEach(saveDuration => {
//                         saveDuration.addEventListener("click", () => {
//                             if (saveDuration.checked) {
//                                 if (Object.values(savingsDurationObject).includes(saveDuration.value)) {
//                                     if (saveDuration.value === 'custom') {
//                                         const summaryForm = document.getElementById("custom-save-duration-form")
//                                     }

//                                     function updateMinMaxValue(minValue, maxValue) {
//                                         const savingValue = document.querySelector(".noUi-handle-lower");
//                                         savingValue.setAttribute("aria-valuemin", parseFloat(minValue))
//                                         savingValue.setAttribute("aria-valuemax", parseFloat(maxValue))
//                                     }

//                                     function updateTheMinMaxHelpTextValue(minValue, maxValue) {
//                                         // const formNoteId = document.getElementById("form-note-id");
//                                         // invest 1000 ksh and upto 1000 ksh
//                                         formNoteHelpSliderId.innerHTML = `invest ${parseFloat(minValue).toFixed(2)} ksh and upto ${parseFloat(maxValue).toFixed(2)} ksh`;
//                                         // floating summary
//                                         floatingMaxAmountLabel.innerHTML = `Max Amout ${maxValue.toLocaleString()} KSH`;

//                                     }

//                                     function updateTheValueAndText(index) {
//                                         updateMinMaxValue(savingsPricing[index].min, savingsPricing[index].max)
//                                         updateTheMinMaxHelpTextValue(savingsPricing[index].min, savingsPricing[index].max)
//                                         investmentAmount.setAttribute("min", savingsPricing[index].min)
//                                         investmentAmount.setAttribute("max", savingsPricing[index].max)
//                                         investmentAmount.value = savingsPricing[index].min;
//                                         InputSavingListenerFunction(savingsPricing[index].min, savingsPricing[index].max)
//                                     }

//                                     function InputSavingListenerFunction(min, max) {


//                                         investAmountSummaryDisplay.innerHTML = min
//                                         investmentAmountPaymentHiddenInput.value = min
//                                         totalInvestment.textContent = min

//                                         investmentAmountSummaryCostFee.innerHTML = parseInt((investmentRate) * parseFloat(investmentAmount.value))



                                        // investmentAmount.addEventListener("keyup", function (e) {

                                        //     investmentAmount.value = e.target.value;
                                        //     calculateTheRateInvestment(investmentAmount.value);

                                        //     investAmountSummaryDisplay.innerHTML = investmentAmount.value
                                        //     investmentAmountPaymentHiddenInput.value = investmentAmount.value
                                        //     totalInvestment.textContent = investmentAmountPaymentHiddenInput.value

                                        //     investmentAmountSummaryCostFee.innerHTML = parseInt((investmentRate) * parseFloat(investmentAmount.value))

                                        //     totalInvestment.textContent = parseInt((investmentRate) * parseFloat(investmentAmount.value))

                                        //     if (
                                        //         parseInt(investmentAmount.value) < min ||
                                        //         parseInt(investmentAmount.value) > max ||
                                        //         investmentAmount.value == '' ||
                                        //         investmentAmount.value == undefined ||
                                        //         investmentAmount.value == null
                                        //     ) {
                                        //         SavingLimitDiv.classList.add("text-danger", "form-note", "pt-1")
                                        //         SavingLimitDiv.innerHTML = `Amount can only be between ${min} and ${max} for the ${saveDuration.value} saving duration`
                                        //         // investmentAmount.value = min;
                                        //         return false;
                                        //     } else {
                                        //         SavingLimitDiv.classList.remove("text-danger")
                                        //         SavingLimitDiv.innerHTML = ""
                                        //     }
                                        // })
//                                     }

//                                     function updateSaveDurationValue(value) {

//                                         if (value.includes("-")) {
//                                             const parts = value.split("-");
//                                             const part1 = parts[0]
//                                             const formattedValue = parts[1].charAt(0).toUpperCase() + parts[1].slice(1);
//                                             savingDurationSummaryValue.innerHTML = part1 + " " + formattedValue;
//                                         } else {
//                                             savingDurationSummaryValue.innerHTML = value;
//                                         }
//                                     }

//                                     switch (saveDuration.value) {
//                                         case "1-day":
//                                             updateTheValueAndText('1D')
//                                             updateSaveDurationValue(saveDuration.value)
//                                             break;
//                                         case "1-week":
//                                             updateTheValueAndText('1W')
//                                             updateSaveDurationValue(saveDuration.value)
//                                             break;
//                                         case "2-weeks":
//                                             updateTheValueAndText('2W')
//                                             updateSaveDurationValue(saveDuration.value)
//                                             break;
//                                         case "1-month":
//                                             updateTheValueAndText('1M')
//                                             updateSaveDurationValue(saveDuration.value)
//                                             break;
//                                         case "3-months":
//                                             updateTheValueAndText('3M')
//                                             updateSaveDurationValue(saveDuration.value)
//                                             break;

//                                         default:
//                                             break;
//                                     }
//                                 }
//                                 else {
//                                     console.log(Object.values(savingsDurationObject))
//                                 }
//                             }

//                         })


//                     })

//                     console.log(savingsDurationObject)
//                 }
//                 else if (investTypePlanOption.toLowerCase() === 'investment') {
//                     savingsDuration.style.display = "none"
//                     amountLabel.innerHTML = "Principal Investment"
//                     amountSummaryLabel.innerHTML = "to Investment"

//                     formNoteHelpSliderId.innerHTML = `invest 1000 ksh and upto 10,000 ksh`;
//                     // floating summary
//                     floatingMaxAmountLabel.innerHTML = `Max Amout 10,000 KSH`;

//                     // remove the slider btn for the price range
//                     investmentPriceSlider.style.display = "block"
//                     // activate the input field
//                     investmentAmount.setAttribute("disabled", "disabled");
//                     investmentAmount.type = "number"
//                     // remove the summary section on the summary form

//                     savingDurationSummary.style.display = "none";

//                     overalInvestType.value = "invest"

//                 }

//                 else {
//                     savingsDuration.style.display = "none"
//                 }
//             }
//         })
//     })




// });

