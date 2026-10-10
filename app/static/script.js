/**
 * RetailMind: Frontend Interactivity
 * Module: app/static/script.js
 * Handles demand scenario presets, sales forecasts, and RFM customer segmentation API calls.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Forecast form elements
    const forecastForm = document.getElementById('forecastForm');
    const forecastBtn = document.getElementById('forecastBtn');
    const forecastBtnText = forecastBtn.querySelector('.btn-text');
    const forecastSpinner = forecastBtn.querySelector('.loader-spinner');

    const categorySelect = document.getElementById('category');
    const storeIdSelect = document.getElementById('storeId');
    const priceInput = document.getElementById('price');
    const discountSelect = document.getElementById('discount');
    const footfallInput = document.getElementById('footfall');
    const adSpendInput = document.getElementById('adSpend');
    const isHolidayCheck = document.getElementById('isHoliday');
    const isWeekendCheck = document.getElementById('isWeekend');

    // KPI Display Elements
    const demandBadge = document.getElementById('demandBadge');
    const kpiUnits = document.getElementById('kpiUnits');
    const kpiRevenue = document.getElementById('kpiRevenue');
    const kpiEffectivePrice = document.getElementById('kpiEffectivePrice');
    const kpiSafetyStock = document.getElementById('kpiSafetyStock');
    const kpiReorderPoint = document.getElementById('kpiReorderPoint');

    // Scenario preset buttons
    const scenarioButtons = document.querySelectorAll('.scenario-btn');

    // RFM form elements
    const rfmForm = document.getElementById('rfmForm');
    const rfmBtn = document.getElementById('rfmBtn');
    const rfmBtnText = rfmBtn.querySelector('.btn-text');
    const rfmSpinner = rfmBtn.querySelector('.loader-spinner');

    const rfmRecency = document.getElementById('rfmRecency');
    const rfmFrequency = document.getElementById('rfmFrequency');
    const rfmMonetary = document.getElementById('rfmMonetary');

    const segmentBadge = document.getElementById('segmentBadge');
    const strategyText = document.getElementById('strategyText');
    const offerText = document.getElementById('offerText');

    // 1. Scenario Presets Handler
    if (window.RETAIL_SCENARIOS) {
        scenarioButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const scKey = btn.getAttribute('data-scenario');
                const sc = window.RETAIL_SCENARIOS[scKey];
                if (sc) {
                    categorySelect.value = sc.category;
                    priceInput.value = sc.price;
                    discountSelect.value = sc.discount.toFixed(2);
                    footfallInput.value = sc.customer_footfall;
                    adSpendInput.value = sc.advertising_spend;
                    isHolidayCheck.checked = sc.is_holiday === 1;
                    isWeekendCheck.checked = sc.is_weekend === 1;

                    scenarioButtons.forEach(b => b.style.borderColor = '');
                    btn.style.borderColor = '#06b6d4';

                    // Auto run forecast
                    submitForecast();
                }
            });
        });
    }

    // 2. Submit Sales Forecast
    async function submitForecast() {
        forecastBtn.disabled = true;
        forecastBtnText.style.display = 'none';
        forecastSpinner.style.display = 'inline-block';

        const payload = {
            store_id: parseInt(storeIdSelect.value),
            category: categorySelect.value,
            price: parseFloat(priceInput.value),
            discount: parseFloat(discountSelect.value),
            customer_footfall: parseInt(footfallInput.value),
            advertising_spend: parseFloat(adSpendInput.value),
            is_holiday: isHolidayCheck.checked ? 1 : 0,
            is_weekend: isWeekendCheck.checked ? 1 : 0,
            month: 11
        };

        try {
            const res = await fetch('/forecast', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const resData = await res.json();
            if (!res.ok || !resData.success) throw new Error(resData.error || 'Failed to forecast demand');

            const d = resData.data;
            demandBadge.textContent = d.demand_status;
            demandBadge.className = `status-badge ${d.status_color}`;

            kpiUnits.textContent = d.predicted_units.toLocaleString();
            kpiRevenue.textContent = `$${d.projected_revenue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
            kpiEffectivePrice.textContent = `Effective Price: $${d.effective_price.toFixed(2)}/unit`;
            kpiSafetyStock.textContent = `${d.recommended_safety_stock} units`;
            kpiReorderPoint.textContent = `${d.recommended_reorder_point} units`;

        } catch (err) {
            console.error('Forecast error:', err);
            alert(`Error: ${err.message}`);
        } finally {
            forecastBtn.disabled = false;
            forecastBtnText.style.display = 'inline-flex';
            forecastSpinner.style.display = 'none';
        }
    }

    forecastForm.addEventListener('submit', (e) => {
        e.preventDefault();
        submitForecast();
    });

    // 3. Submit Customer RFM Segmentation
    async function submitSegmentation() {
        rfmBtn.disabled = true;
        rfmBtnText.style.display = 'none';
        rfmSpinner.style.display = 'inline-block';

        const payload = {
            recency: parseInt(rfmRecency.value),
            frequency: parseInt(rfmFrequency.value),
            monetary: parseFloat(rfmMonetary.value)
        };

        try {
            const res = await fetch('/segment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const resData = await res.json();
            if (!res.ok || !resData.success) throw new Error(resData.error || 'Failed to segment customer');

            const d = resData.data;
            segmentBadge.textContent = d.segment_name;
            segmentBadge.className = `segment-badge ${d.badge_color}`;

            strategyText.textContent = d.marketing_strategy;
            offerText.textContent = d.recommended_offer;

        } catch (err) {
            console.error('Segmentation error:', err);
            alert(`Error: ${err.message}`);
        } finally {
            rfmBtn.disabled = false;
            rfmBtnText.style.display = 'inline-flex';
            rfmSpinner.style.display = 'none';
        }
    }

    rfmForm.addEventListener('submit', (e) => {
        e.preventDefault();
        submitSegmentation();
    });

    // Run initial demo forecast on page load
    submitForecast();
});
