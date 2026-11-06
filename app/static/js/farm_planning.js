/**
 * RythuCrop - Farm Planning Engine
 * Strict Email Auth Gated & Multilingual Dynamic Farm Planning
 * Modern Tailwind CSS Card Presentation
 */

(function(window, document) {
    'use strict';

    function renderFarmPlanResults(data) {
        const resBox = document.getElementById("farmPlanResult") || document.getElementById("planningResult");
        if (!resBox || !data) return;

        if (!document.getElementById("planningCropCards") && window._CONTAINER_TEMPLATES && window._CONTAINER_TEMPLATES.farmPlanResult) {
            resBox.innerHTML = window._CONTAINER_TEMPLATES.farmPlanResult;
            if (typeof window.applyTranslations === 'function') {
                try { window.applyTranslations(window.AppState?.lang || 'en'); } catch (e) {}
            }
        }

        const cardsBox = document.getElementById("planningCropCards");
        const disc = document.getElementById("planDisclaimer");
        if (!cardsBox) return;

        cardsBox.innerHTML = "";
        const lang = (window.AppState && window.AppState.lang) || localStorage.getItem('rythucrop_lang') || 'en';
        const dict = (window.TRANSLATIONS && window.TRANSLATIONS[lang]) || {};
        const t = (k, fb) => (dict[k] !== undefined && dict[k] !== "") ? dict[k] : (fb !== undefined ? fb : k);
        const cropNames = (window.RYTHUCROP_I18N && window.RYTHUCROP_I18N.crop_names) || (window.LOCALIZED_CROP_NAMES) || {};
        const advisoryMap = window.CROP_PLAN_ADVISORY || (window.RYTHUCROP_I18N && window.RYTHUCROP_I18N.farm_planning) || {};
        const localizeText = (txt, l) => (typeof window.localizeFarmPlanText === 'function') ? window.localizeFarmPlanText(txt, l) : txt;

        (data.plan_details || []).forEach(item => {
            const card = document.createElement("div");
            card.className = "border-2 border-emerald-400/90 shadow-md rounded-2xl bg-white hover:border-emerald-500 transition-colors p-6 mb-6";

            let rawCrop = item.crop || item.crop_name || "";
            let cropKey = rawCrop.toLowerCase().replace(/[\(\)\/\s]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
            if (cropKey.includes("cotton")) cropKey = "cotton";
            else if (cropKey.includes("turmeric")) cropKey = "turmeric";
            else if (cropKey.includes("tur") || cropKey.includes("arhar") || cropKey.includes("pigeonpea")) cropKey = "arhar_tur";
            else if (cropKey.includes("gram")) cropKey = "gram";
            else if (cropKey.includes("chillies")) cropKey = "dry_chillies";
            else if (cropKey.includes("pepper")) cropKey = "black_pepper";
            else if (cropKey.includes("castor")) cropKey = "castor_seed";

            const cropAdv = advisoryMap[cropKey] || advisoryMap[rawCrop] || {};
            const locCrop = (cropNames[cropKey] && (cropNames[cropKey][lang] || cropNames[cropKey]["en"])) || rawCrop.replace(/\s*\([^)]*\)/g, '');

            const baseReasons = item.reasons_en || item.reasons || item.key_reasons || [];
            const locReasonsList = baseReasons.map(r => localizeText(r, lang));

            const locSoil = (cropAdv.soil_guidance && cropAdv.soil_guidance[lang]) || localizeText(item.soil_consideration_en || item.soil_guidance || item.soil_consideration, lang);
            const locWater = (cropAdv.water_scheduling && cropAdv.water_scheduling[lang]) || localizeText(item.water_consideration_en || item.water_scheduling || item.water_consideration, lang);
            const locRisks = (cropAdv.risks && cropAdv.risks[lang]) || localizeText(item.risks_en || item.risks, lang);
            const locNextSteps = (cropAdv.next_steps && cropAdv.next_steps[lang]) || localizeText(item.next_steps_en || item.next_steps, lang);

            // Cultivation Economics (Per Acre)
            const econ = item.economics || {};
            const locMarketDemand = (cropAdv.market_demand && cropAdv.market_demand[lang]) || econ.market_demand || "";
            const perAcreSuffix = t("per_acre_suffix", " / acre");

            let cleanCost = econ.estimated_cost_per_acre ? (econ.estimated_cost_per_acre.includes('₹') ? econ.estimated_cost_per_acre : '₹' + econ.estimated_cost_per_acre) : '';
            if (cleanCost) cleanCost = cleanCost.replace(/\s*\/\s*(?:acre|ఎకరాకి|एकड़|ஏக்கர்|ಎಕರೆಗೆ|ഏക്കറിന്|एकर|একর|એકર|ଏକର)?$/i, '') + perAcreSuffix;

            let cleanGross = econ.estimated_gross_return ? (econ.estimated_gross_return.includes('₹') ? econ.estimated_gross_return : '₹' + econ.estimated_gross_return) : '';
            if (cleanGross) cleanGross = cleanGross.replace(/\s*\/\s*(?:acre|ఎకరాకి|एकड़|ஏக்கர்|ಎಕರೆಗೆ|ഏക്കറിന്|एकर|একর|એકર|ଏକର)?$/i, '') + perAcreSuffix;

            let cleanProfit = econ.estimated_profit_per_acre ? (econ.estimated_profit_per_acre.includes('₹') ? econ.estimated_profit_per_acre : '₹' + econ.estimated_profit_per_acre) : '';
            if (cleanProfit) cleanProfit = cleanProfit.replace(/\s*\/\s*(?:acre|ఎకరాకి|एकड़|ஏக்கர்|ಎಕರೆಗೆ|ഏക്കറിന്|एकर|একর|એકર|ଏକର)?$/i, '') + perAcreSuffix;

            const economicsHtml = (cleanCost || cleanProfit) ? `
                <div class="mt-4 pt-4 border-t border-slate-100">
                    <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                        <span>💰</span>
                        <span>${t("economics_title", "Cultivation Economics (Per Acre)")}</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="bg-rose-50/70 border border-rose-200/60 rounded-xl p-3 text-rose-900">
                            <div class="text-xs text-rose-600/80 font-medium mb-1">${t("cost_label", "Estimated Cost:")}</div>
                            <div class="text-base font-bold">${cleanCost || 'N/A'}</div>
                        </div>
                        <div class="bg-sky-50/70 border border-sky-200/60 rounded-xl p-3 text-sky-900">
                            <div class="text-xs text-sky-600/80 font-medium mb-1">${t("gross_label", "Estimated Gross Return:")}</div>
                            <div class="text-base font-bold">${cleanGross || 'N/A'}</div>
                        </div>
                        <div class="bg-emerald-50/70 border border-emerald-200/60 rounded-xl p-3 text-emerald-900 font-bold">
                            <div class="text-xs text-emerald-600/80 font-medium mb-1">${t("profit_label", "Estimated Net Profit:")}</div>
                            <div class="text-base font-extrabold text-emerald-700">${cleanProfit || 'N/A'}</div>
                        </div>
                    </div>
                    ${locMarketDemand ? `
                        <div class="bg-amber-50 text-amber-900 rounded-lg p-2.5 text-xs mt-3 border border-amber-200/60 flex items-center gap-2">
                            <span class="font-semibold">${t("demand_label", "Market Demand:")}</span>
                            <span>${locMarketDemand}</span>
                        </div>
                    ` : ''}
                </div>
            ` : '';

            card.innerHTML = `
                <div class="flex justify-between items-center mb-4 flex-wrap gap-2">
                    <h4 class="text-xl font-extrabold text-slate-800 m-0 tracking-tight">${locCrop}</h4>
                    <span class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200 flex items-center gap-1.5 shadow-sm">
                        <span>★</span>
                        <span>${t("suitability_score", "Suitability Score")}: ${item.score || item.suitability_score}</span>
                    </span>
                </div>

                <div class="mb-3">
                    <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">${t("reasons_label", "Reasons:")}</div>
                    <div class="space-y-1">
                        ${locReasonsList.map(r => `
                            <div class="flex items-start gap-2 text-sm text-slate-700">
                                <span class="text-emerald-500 font-bold flex-shrink-0 mt-0.5">✓</span>
                                <span>${r}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-600 mb-2 bg-slate-50/80 rounded-xl p-3 border border-slate-100">
                    <div><strong class="text-slate-700 font-semibold">${t("soil_label", "Soil:")}</strong> ${locSoil}</div>
                    <div><strong class="text-slate-700 font-semibold">${t("water_label", "Water:")}</strong> ${locWater}</div>
                    <div class="text-amber-700"><strong class="font-semibold">${t("risks_label", "Risks:")}</strong> ${locRisks}</div>
                    <div class="text-sky-700"><strong class="font-semibold">${t("next_steps_label", "Next Steps:")}</strong> ${locNextSteps}</div>
                </div>

                ${economicsHtml}
            `;

            cardsBox.appendChild(card);
        });

        if (disc) disc.textContent = localizeText(data.disclaimer, lang);
        if (resBox) resBox.style.display = "block";
    }

    async function handleFarmPlanning(e) {
        if (e && e.preventDefault) e.preventDefault();

        const landEl = document.getElementById("land");
        const seasonEl = document.getElementById("season");
        const soilEl = document.getElementById("soil");
        const irrEl = document.getElementById("irrigation");
        const goalEl = document.getElementById("goal");
        const expEl = document.getElementById("experience");

        const payload = {
            land: parseFloat(landEl ? landEl.value : 1) || 1,
            season: seasonEl ? seasonEl.value : "Kharif",
            soil: soilEl ? soilEl.value : "Loamy Soil",
            irrigation: irrEl ? irrEl.value : "Good water availability",
            goal: goalEl ? goalEl.value : "Higher yield",
            experience: expEl ? expEl.value : "Beginner",
            lang: (window.AppState && window.AppState.lang) || localStorage.getItem('rythucrop_lang') || 'en'
        };

        try {
            const res = await fetch("/farm-plan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                if (res.status === 401) {
                    alert("Farm Planning error: Authentication required. Please login with your Email.");
                    const resBox = document.getElementById("farmPlanResult") || document.getElementById("planningResult");
                    if (resBox) {
                        resBox.style.display = "none";
                        resBox.innerHTML = "";
                    }
                    return;
                }
                const data = await res.json().catch(() => ({}));
                throw new Error(data.error || data.message || "Failed to generate plan");
            }

            const data = await res.json();
            window.lastFarmPlanData = data;
            window.lastFarmPlanningResponse = data;

            try {
                sessionStorage.setItem('lastFarmPlanningResponse', JSON.stringify(data));
            } catch (err) {}

            renderFarmPlanResults(data);

            const resBox = document.getElementById("farmPlanResult") || document.getElementById("planningResult");
            if (resBox) {
                resBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
        } catch (err) {
            alert("Error: " + err.message);
        }
    }

    // Expose globally
    window.renderFarmPlanResults = renderFarmPlanResults;
    window.renderFarmPlanResultsModule = renderFarmPlanResults;
    window.handleFarmPlanning = handleFarmPlanning;
    window.handleFarmPlanningModule = handleFarmPlanning;

    // Attach listeners
    function setupFarmPlanListeners() {
        const form = document.getElementById("farmPlanForm") || document.getElementById("planningForm");
        if (form) {
            form.addEventListener("submit", handleFarmPlanning);
        }
    }

    if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupFarmPlanListeners);
        } else {
            setupFarmPlanListeners();
        }
    }
})(window, document);
