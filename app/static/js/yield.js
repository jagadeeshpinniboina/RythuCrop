/**
 * RythuCrop - Yield Prediction Module (Frontend Engine)
 * ICAR Agro-Climatic Feasibility Gating, State-Sensitive Dynamic Crop Prioritization,
 * and 100% Reactive Multilingual Localization across all 10 Indic languages.
 */

(function(window, document) {
    'use strict';

    // State to compatible crops matrix for instant synchronous fallback
    const LOCAL_COMPATIBLE_CROPS = {
        "jammu and kashmir": ["Wheat", "Barley", "Maize", "Potato", "Apple"],
        "ladakh": ["Wheat", "Barley", "Potato", "Apple"],
        "himachal pradesh": ["Wheat", "Maize", "Potato", "Apple", "Barley"],
        "uttarakhand": ["Rice", "Wheat", "Maize", "Sugarcane", "Potato", "Soyabean"],
        "punjab": ["Rice", "Wheat", "Cotton(lint)", "Maize", "Sugarcane", "Potato", "Gram"],
        "haryana": ["Rice", "Wheat", "Cotton(lint)", "Bajra", "Sugarcane", "Gram", "Potato"],
        "rajasthan": ["Bajra", "Wheat", "Gram", "Maize", "Groundnut", "Soyabean"],
        "uttar pradesh": ["Rice", "Wheat", "Sugarcane", "Potato", "Maize", "Gram", "Arhar/Tur"],
        "bihar": ["Rice", "Wheat", "Maize", "Potato", "Sugarcane", "Gram", "Arhar/Tur"],
        "west bengal": ["Rice", "Potato", "Jute", "Wheat", "Maize"],
        "assam": ["Rice", "Jute", "Potato", "Wheat", "Maize"],
        "meghalaya": ["Rice", "Maize", "Potato", "Turmeric"],
        "tripura": ["Rice", "Potato", "Jute"],
        "odisha": ["Rice", "Groundnut", "Arhar/Tur", "Sugarcane", "Gram", "Turmeric"],
        "andhra pradesh": ["Rice", "Groundnut", "Cotton(lint)", "Maize", "Sugarcane", "Turmeric", "Dry chillies", "Arhar/Tur"],
        "telangana": ["Cotton(lint)", "Rice", "Maize", "Soyabean", "Arhar/Tur", "Turmeric", "Dry chillies"],
        "tamil nadu": ["Rice", "Sugarcane", "Groundnut", "Cotton(lint)", "Maize", "Coconut", "Turmeric"],
        "karnataka": ["Rice", "Maize", "Cotton(lint)", "Sugarcane", "Groundnut", "Turmeric", "Gram", "Arhar/Tur", "Coconut"],
        "kerala": ["Rice", "Coconut", "Dry chillies", "Turmeric"],
        "maharashtra": ["Cotton(lint)", "Soyabean", "Sugarcane", "Gram", "Arhar/Tur", "Maize", "Onion", "Wheat", "Bajra"],
        "gujarat": ["Cotton(lint)", "Groundnut", "Wheat", "Bajra", "Potato", "Onion", "Gram"],
        "madhya pradesh": ["Soyabean", "Wheat", "Gram", "Maize", "Arhar/Tur", "Cotton(lint)", "Potato"],
        "chhattisgarh": ["Rice", "Maize", "Gram", "Arhar/Tur", "Soyabean"]
    };

    // Seasonal restrictions matrix for known strictly seasonal crops
    const SEASON_RESTRICTIONS = {
        "wheat": ["rabi"],
        "barley": ["rabi"],
        "gram": ["rabi"],
        "apple": ["rabi", "whole year"],
        "cotton": ["kharif", "rabi", "whole year"],
        "cotton(lint)": ["kharif", "rabi", "whole year"],
        "potato": ["rabi", "whole year"],
        "jute": ["kharif", "summer", "whole year"]
    };

    function getActiveLanguage() {
        return (window.AppState && window.AppState.lang) || localStorage.getItem('rythucrop_lang') || 'en';
    }

    function getTranslation(key, lang) {
        lang = lang || getActiveLanguage();
        const dict = (window.TRANSLATIONS && window.TRANSLATIONS[lang]) || {};
        if (dict[key] !== undefined && dict[key] !== "") return dict[key];
        const enDict = (window.TRANSLATIONS && window.TRANSLATIONS['en']) || {};
        if (enDict[key] !== undefined) return enDict[key];
        return key;
    }

    /**
     * Re-renders all Indian State/UT dropdown options in the active language
     * while strictly maintaining standard English canonical values in <option value="...">.
     */
    function updateLocalizedStateSelect(lang) {
        lang = lang || getActiveLanguage();
        const stateSelect = document.getElementById("State");
        if (!stateSelect) return;
        Array.from(stateSelect.options).forEach(opt => {
            const canonical = opt.value;
            if (!canonical) return;
            let localized = null;
            if (typeof window.localizeStateName === 'function') {
                localized = window.localizeStateName(canonical, lang);
            } else if (window.LOCALIZED_STATE_NAMES && window.LOCALIZED_STATE_NAMES[canonical]) {
                localized = window.LOCALIZED_STATE_NAMES[canonical][lang] || window.LOCALIZED_STATE_NAMES[canonical]['en'];
            }
            if (localized) {
                opt.textContent = localized;
            }
        });
    }


    /**
     * Dynamically filter / sort / prioritize compatible crops in #Crop dropdown
     * when State is selected, while strictly preserving user freedom to select
     * unviable crops to inspect climate risk gating.
     */
    async function filterCropsByState(state) {
        const cropSelect = document.getElementById("Crop");
        if (!cropSelect || !state) return;

        const lang = getActiveLanguage();
        const stateKey = state.toLowerCase().trim();
        let compatible = LOCAL_COMPATIBLE_CROPS[stateKey] || [];

        // Attempt async fetch from backend for latest ICAR mapping
        try {
            const resp = await fetch(`/api/state-crops?state=${encodeURIComponent(state)}`);
            if (resp.ok) {
                const json = await resp.json();
                if (json.compatible_crops && json.compatible_crops.length > 0) {
                    compatible = json.compatible_crops;
                }
            }
        } catch (e) {
            // Keep local fallback
        }

        const compSet = new Set(compatible.map(c => c.toLowerCase().trim()));

        // Preserve current selection
        const currentSelected = cropSelect.value;

        // Collect all options from existing optgroups or flat list
        const allOptions = Array.from(cropSelect.querySelectorAll("option")).map(opt => ({
            value: opt.value,
            text: opt.text,
            isCompatible: compSet.has(opt.value.toLowerCase().trim())
        }));

        // Deduplicate options by value
        const uniqueOptions = [];
        const seenValues = new Set();
        allOptions.forEach(opt => {
            if (!seenValues.has(opt.value)) {
                seenValues.add(opt.value);
                uniqueOptions.push(opt);
            }
        });

        // Separate into compatible vs other crops
        const compatibleList = uniqueOptions.filter(o => o.isCompatible);
        const otherList = uniqueOptions.filter(o => !o.isCompatible);

        // Rebuild dropdown with optgroups if compatible crops found
        if (compatibleList.length > 0) {
            cropSelect.innerHTML = "";

            let selectedAssigned = false;
            const optGroupComp = document.createElement("optgroup");
            optGroupComp.dataset.groupType = "optimal";
            optGroupComp.label = getTranslation("optgroup_optimal", "★ Optimal Agro-Climatic Alignment (Recommended for State)");
            compatibleList.forEach(opt => {
                const el = document.createElement("option");
                el.value = opt.value;
                el.text = opt.text;
                if (opt.value === currentSelected) {
                    el.selected = true;
                    selectedAssigned = true;
                }
                optGroupComp.appendChild(el);
            });
            cropSelect.appendChild(optGroupComp);

            if (otherList.length > 0) {
                const optGroupOther = document.createElement("optgroup");
                optGroupOther.dataset.groupType = "incompatible";
                optGroupOther.label = getTranslation("optgroup_incompatible", "⚠ High Risk / Incompatible Crops (Climate Mismatch)");
                otherList.forEach(opt => {
                    const el = document.createElement("option");
                    el.value = opt.value;
                    el.text = opt.text;
                    if (opt.value === currentSelected) {
                        el.selected = true;
                        selectedAssigned = true;
                    }
                    optGroupOther.appendChild(el);
                });
                cropSelect.appendChild(optGroupOther);
            }

            // Pre-select the first crop from the Optimal section by default
            if (!selectedAssigned && compatibleList.length > 0) {
                cropSelect.value = compatibleList[0].value;
            }
        }

        // Trigger crop names localization pass
        if (typeof window.updateLocalizedCropSelects === "function") {
            window.updateLocalizedCropSelects(lang);
        }
        if (typeof updateLocalizedStateSelect === "function") {
            updateLocalizedStateSelect(lang);
        }

        // Trigger inline mismatch notice check
        handleCropChange(cropSelect.value);
    }

    /**
     * Inline notice check when a crop is picked
     */
    function handleCropChange(cropVal) {
        const stateEl = document.getElementById("State");
        const seasonEl = document.getElementById("Season");
        const noticeEl = document.getElementById("cropMismatchNotice");
        const textEl = document.getElementById("cropMismatchNoticeText");
        if (!noticeEl) return;
        const state = stateEl ? (stateEl.value || "").toLowerCase().trim() : "";
        const crop = (cropVal || "").toLowerCase().trim();
        const season = seasonEl ? (seasonEl.value || "").toLowerCase().trim() : "";

        let compatible = LOCAL_COMPATIBLE_CROPS[state] || [];
        const compSet = new Set(compatible.map(c => c.toLowerCase().trim()));
        const isStateIncompatible = compSet.size > 0 && !compSet.has(crop);

        let isSeasonIncompatible = false;
        let seasonCropKey = crop;
        if (seasonCropKey.includes("cotton")) seasonCropKey = "cotton";
        else if (seasonCropKey.includes("gram") || seasonCropKey.includes("chickpea")) seasonCropKey = "gram";
        else if (seasonCropKey.includes("wheat")) seasonCropKey = "wheat";
        else if (seasonCropKey.includes("barley")) seasonCropKey = "barley";
        else if (seasonCropKey.includes("apple")) seasonCropKey = "apple";
        else if (seasonCropKey.includes("potato")) seasonCropKey = "potato";
        else if (seasonCropKey.includes("jute")) seasonCropKey = "jute";

        if (SEASON_RESTRICTIONS[seasonCropKey]) {
            const allowed = SEASON_RESTRICTIONS[seasonCropKey];
            const matchesAllowed = allowed.some(s => season.includes(s));
            if (!matchesAllowed) {
                isSeasonIncompatible = true;
            }
        }

        if (isStateIncompatible) {
            noticeEl.style.display = "block";
            if (textEl) {
                textEl.textContent = getTranslation("crop_mismatch_warning_inline", "⚠️ High Risk Warning: This crop has severe agro-climatic incompatibility with the selected state. Commercial harvest may fail.");
            }
        } else if (isSeasonIncompatible) {
            noticeEl.style.display = "block";
            if (textEl) {
                textEl.textContent = "⚠️ " + getTranslation("warning_seasonal_mismatch", "Seasonal Incompatibility: The selected crop is biologically mismatched with this season's agro-climatic conditions.");
            }
        } else {
            noticeEl.style.display = "none";
        }
    }

    /**
     * Render Yield Prediction Result Card with 100% Reactive Multilingual Localization
     */
    function renderYieldResults(data) {
        if (!data) return;
        const resBox = document.getElementById("yieldResult");
        if (!resBox) return;
        resBox.className = "result-box border-2 border-sky-400 shadow-lg ring-1 ring-sky-200 rounded-2xl bg-white/95";

        // Restore template if container was cleared during refresh/reset
        if (!document.getElementById("yieldHaVal") && window._CONTAINER_TEMPLATES && window._CONTAINER_TEMPLATES.yieldResult) {
            resBox.innerHTML = window._CONTAINER_TEMPLATES.yieldResult;
            if (typeof window.applyTranslations === 'function') {
                try { window.applyTranslations(getActiveLanguage()); } catch (e) {}
            }
        }

        const lang = getActiveLanguage();
        const dict = (window.TRANSLATIONS && window.TRANSLATIONS[lang]) || {};
        const t = (k, fb) => (dict[k] !== undefined && dict[k] !== "") ? dict[k] : (fb !== undefined ? fb : k);

        const isViable = data.is_viable !== false;
        const riskLevel = data.risk_level || (isViable ? "Low Risk / Optimal Climate" : "High Risk / Climate Mismatch");
        const climateSuitability = data.climate_suitability || (isViable ? "Optimal Climate" : "Unviable");

        // 1. Status & Risk Badges
        const seasonBadge = document.getElementById("yieldSeasonBadge");
        if (seasonBadge) {
            seasonBadge.style.display = "inline-block";
            if (data.season_mismatch) {
                seasonBadge.textContent = t("season_badge_mismatch", "Seasonal Incompatibility");
                seasonBadge.style.background = "#fee2e2";
                seasonBadge.style.color = "#991b1b";
                seasonBadge.style.border = "1px solid #f87171";
            } else if (data.season_status === "Sub-Optimal" || (data.season_factor && data.season_factor < 0.75)) {
                seasonBadge.textContent = t("season_badge_stress", "Seasonal Stress");
                seasonBadge.style.background = "#fef3c7";
                seasonBadge.style.color = "#92400e";
                seasonBadge.style.border = "1px solid #fcd34d";
            } else if (data.season_status === "Moderate" || (data.season_factor && data.season_factor < 0.95)) {
                seasonBadge.textContent = t("season_badge_moderate", "Moderate Season");
                seasonBadge.style.background = "#fef9c3";
                seasonBadge.style.color = "#854d0e";
                seasonBadge.style.border = "1px solid #fef08a";
            } else {
                seasonBadge.textContent = t("season_badge_optimal", "Optimal Season");
                seasonBadge.style.background = "#dcfce7";
                seasonBadge.style.color = "#166534";
                seasonBadge.style.border = "1px solid #86efac";
            }
        }

        const suitBadge = document.getElementById("yieldSuitabilityBadge");
        const riskBadge = document.getElementById("yieldRiskBadge");

        if (suitBadge) {
            if (!isViable) {
                suitBadge.textContent = t("yield_suitability_unviable", "Unviable");
                suitBadge.style.background = "#fee2e2";
                suitBadge.style.color = "#991b1b";
                suitBadge.style.border = "1px solid #f87171";
            } else if (climateSuitability.toLowerCase().includes("moderate")) {
                suitBadge.textContent = t("yield_suitability_moderate", "Moderate Feasibility");
                suitBadge.style.background = "#fef3c7";
                suitBadge.style.color = "#92400e";
                suitBadge.style.border = "1px solid #fcd34d";
            } else {
                suitBadge.textContent = t("yield_suitability_optimal", "Optimal Climate");
                suitBadge.style.background = "#dcfce7";
                suitBadge.style.color = "#166534";
                suitBadge.style.border = "1px solid #86efac";
            }
        }

        if (riskBadge) {
            if (!isViable) {
                riskBadge.textContent = t("yield_risk_high", "⚠️ High Risk / Climate Mismatch");
                riskBadge.style.background = "#fef2f2";
                riskBadge.style.color = "#b91c1c";
                riskBadge.style.border = "1px solid #fca5a5";
            } else if (riskLevel.toLowerCase().includes("moderate")) {
                riskBadge.textContent = t("yield_risk_moderate", "⚡ Moderate Risk");
                riskBadge.style.background = "#fffbeb";
                riskBadge.style.color = "#b45309";
                riskBadge.style.border = "1px solid #fde68a";
            } else {
                riskBadge.textContent = t("yield_risk_low", "✓ Low Risk / Optimal Climate");
                riskBadge.style.background = "#f0fdf4";
                riskBadge.style.color = "#15803d";
                riskBadge.style.border = "1px solid #bbf7d0";
            }
        }

        // 2. Warning / Optimal Banners
        const warnBox = document.getElementById("yieldWarningAlert");
        const warnTitle = document.getElementById("yieldWarningTitle");
        const warnText = document.getElementById("yieldWarningText");
        const optBox = document.getElementById("yieldOptimalNotice");
        const optTitle = document.getElementById("yieldOptimalTitle");
        const optText = document.getElementById("yieldOptimalText");

        if (!isViable) {
            if (warnBox) warnBox.style.display = "block";
            if (optBox) optBox.style.display = "none";
            if (warnTitle) {
                if (data.season_mismatch) {
                    warnTitle.textContent = t("yield_season_warning_title", "SEASONAL CLIMATE INCOMPATIBILITY — CULTIVATION UNVIABLE");
                } else {
                    warnTitle.textContent = t("yield_warning_title", "STRICT CLIMATE MISMATCH — CULTIVATION UNVIABLE");
                }
            }
            if (warnText) {
                let resolvedWarning = "";
                const wKey = data.season_warning || data.warning_key;
                if (wKey && dict[wKey]) {
                    resolvedWarning = dict[wKey];
                } else if (data.warning_message) {
                    resolvedWarning = data.warning_message;
                } else {
                    resolvedWarning = t("warning_default_mismatch", "The selected crop is not agro-climatically viable for commercial cultivation in this state's environmental conditions.");
                }
                warnText.textContent = resolvedWarning;
            }
        } else {
            if (warnBox) warnBox.style.display = "none";
            if (optBox) {
                optBox.style.display = "block";
                if (optTitle) optTitle.textContent = t("yield_optimal_title", "Optimal Agro-Climatic Alignment");
                if (optText) {
                    const optTmpl = t("yield_optimal_template", "{crop} is well-suited for cultivation in {state}.");
                    const rawCrop = data.crop || "The selected crop";
                    const cropNames = (window.RYTHUCROP_I18N && window.RYTHUCROP_I18N.crop_names) || (window.LOCALIZED_CROP_NAMES) || {};
                    let cropKey = rawCrop.toLowerCase().replace(/[\(\)\/\s]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
                    if (cropNames[cropKey]) {
                        // Direct match
                    } else if (cropKey.includes("coffee")) {
                        cropKey = "coffee";
                    } else if (cropKey.includes("cotton")) {
                        cropKey = "cotton";
                    } else if (cropKey.includes("turmeric")) {
                        cropKey = "turmeric";
                    } else if (cropKey.includes("tur") || cropKey.includes("arhar") || cropKey.includes("pigeonpea")) {
                        cropKey = cropNames["pigeonpeas"] ? "pigeonpeas" : "arhar_tur";
                    } else if (cropKey.includes("chickpea")) {
                        cropKey = cropNames["chickpea"] ? "chickpea" : "gram";
                    } else if (cropKey.includes("gram")) {
                        cropKey = cropNames["gram"] ? "gram" : "chickpea";
                    } else if (cropKey.includes("chillies")) {
                        cropKey = "dry_chillies";
                    }

                    const localizedCrop = (cropNames[cropKey] && (cropNames[cropKey][lang] || cropNames[cropKey]["en"])) || rawCrop;
                    const locState = (typeof window.localizeStateName === 'function' ? window.localizeStateName(data.state, lang) : null) || data.state || "the selected state";
                    optText.textContent = optTmpl.replace("{crop}", localizedCrop).replace("{state}", locState);
                }
            }
        }

        // 3. Metric Values and Units
        const haValEl = document.getElementById("yieldHaVal");
        const haUnitEl = document.getElementById("yieldHaUnit");
        const haLabelEl = document.getElementById("yieldHaLabel");
        const acreValEl = document.getElementById("yieldAcreVal");
        const acreUnitEl = document.getElementById("yieldAcreUnit");
        const acreLabelEl = document.getElementById("yieldAcreLabel");
        const prodValEl = document.getElementById("yieldProdVal");
        const prodUnitEl = document.getElementById("yieldProdUnit");
        const prodLabelEl = document.getElementById("yieldProdLabel");

        if (haLabelEl) haLabelEl.textContent = t("yield_per_hectare_label", t("yield_ha_label", "Per Hectare Yield"));
        if (acreLabelEl) acreLabelEl.textContent = t("yield_per_acre_label", t("yield_acre_label", "Per Acre Yield"));
        if (prodLabelEl) prodLabelEl.textContent = t("estimated_production_label", "Total Estimated Production");

        if (haValEl) haValEl.textContent = !isViable ? "0.00" : (data.predicted_yield_tonnes_ha !== undefined ? Number(data.predicted_yield_tonnes_ha).toFixed(2) : (Number(data.predicted_yield) || 0).toFixed(2));
        if (haUnitEl) haUnitEl.textContent = t("unit_tonnes_ha", data.yield_unit || "tonnes/ha");
        if (acreValEl) acreValEl.textContent = !isViable ? "0.00" : (data.predicted_yield_per_acre !== undefined ? Number(data.predicted_yield_per_acre).toFixed(2) : "0.00");
        if (acreUnitEl) acreUnitEl.textContent = t("unit_quintals_acre", data.acre_unit || "quintals/acre");
        if (prodValEl) prodValEl.textContent = !isViable ? "0.00" : (data.estimated_production !== undefined ? Number(data.estimated_production).toFixed(2) : "0.00");
        let pUnit = data.production_unit || "tonnes";
        let pUnitKey = (pUnit.toLowerCase().includes("thousand") || pUnit.toLowerCase().includes("nut")) ? "unit_thousand_nuts" : "unit_tonnes";
        if (prodUnitEl) prodUnitEl.textContent = t(pUnitKey, pUnit);

        // 4. Methodology & Limitations
        const methodEl = document.getElementById("yieldMethodology");
        if (methodEl) {
            const locMethodology = t("yield_methodology_desc", "Pre-harvest Random Forest Regression (DES Agricultural Statistics, ICAR Agro-Climatic Gating & Seasonal Affinity Model)");
            const locLimitations = t("yield_limitations_desc", "Estimates assume normal seasonal weather without severe unseasonal floods, extreme hailstorms, or major pest outbreaks.");

            methodEl.innerHTML = `
                <strong>${t("methodology_label", "Methodology:")}</strong> ${locMethodology}<br>
                <strong>${t("assumptions_label", "Assumptions & Limitations:")}</strong> ${locLimitations}
            `;
        }

        // 5. Suggestions Box & List
        const sugBox = document.getElementById("yieldSuggestionsBox");
        const sugTitle = document.getElementById("yieldSuggestionsTitle");
        const sugIcon = document.getElementById("yieldSuggestionsIcon");
        const sugHeaderText = document.getElementById("yieldSuggestionsHeaderText");
        const sugList = document.getElementById("yieldSuggestionsList");

        if (sugBox && sugList) {
            sugList.innerHTML = "";

            if (!isViable) {
                // Failure mitigation styling
                sugBox.style.background = "#fff7ed";
                sugBox.style.border = "1.5px solid #fed7aa";
                if (sugTitle) sugTitle.style.color = "#9a3412";
                if (sugIcon) sugIcon.textContent = "🛡️";
                if (sugHeaderText) sugHeaderText.textContent = t("yield_mitigation_title", "Agronomic Alternatives & Risk Mitigation Guidance");

                const suggestions = data.actionable_suggestions || [
                    `Agro-Climatic Alert: ${data.crop} is biologically incompatible with ${data.state}'s climate zone.`,
                    `Shift to high-performing crops recommended for ${data.state}.`,
                    "Avoid applying expensive synthetic inputs for unviable pairings."
                ];

                suggestions.forEach((step, idx) => {
                    const item = document.createElement("div");
                    item.className = "flex items-start gap-3 p-3 rounded-xl bg-white/90 border border-orange-200/70 shadow-xs mb-2 transition hover:bg-white";
                    item.innerHTML = `<span class="w-6 h-6 rounded-full bg-orange-600 text-white text-xs font-extrabold flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm">${idx + 1}</span> <span class="text-xs text-orange-950 leading-relaxed font-medium">${step}</span>`;
                    sugList.appendChild(item);
                });
            } else {
                // Normal cultivation suggestions
                sugBox.style.background = "#f0fdf4";
                sugBox.style.border = "1px solid #bbf7d0";
                if (sugTitle) sugTitle.style.color = "#166534";
                if (sugIcon) sugIcon.textContent = "💡";
                if (sugHeaderText) sugHeaderText.textContent = t("suggestions_title", t("yield_suggestions_title", "Actionable Suggestions to Optimize Harvest Output"));

                const steps = [
                    {
                        title: t("yield_step_1_title", "Split Nitrogen Application"),
                        text: t("yield_step_1_text", "Apply 50% nitrogen as basal dose, 25% at active tillering, and 25% at panicle initiation/flowering.")
                    },
                    {
                        title: t("yield_step_2_title", "Critical Irrigation Timing"),
                        text: t("yield_step_2_text", "Avoid moisture stress during anthesis and grain/pod-filling; maintain field-capacity moisture for optimal test weight.")
                    },
                    {
                        title: t("yield_step_3_title", "Micronutrient Foliar Spray"),
                        text: t("yield_step_3_text", "Spray 0.5% Zinc Sulphate + 1% Urea at 30 and 45 days after sowing to prevent hidden micronutrient hunger.")
                    },
                    {
                        title: t("yield_step_4_title", "Integrated Pest Scouting"),
                        text: t("yield_step_4_text", "Inspect weekly for early borer/blight symptoms; deploy pheromone traps (5/acre) before applying targeted biocontrol.")
                    },
                    {
                        title: t("yield_step_5_title", "Harvest Index Management"),
                        text: t("yield_step_5_text", "Drain field water 10-12 days before harvest; harvest when 80-85% of ears/pods turn straw golden to minimize grain shattering.")
                    }
                ];

                steps.forEach((step, idx) => {
                    let stepTitle = "";
                    let stepText = "";
                    if (typeof step === "object" && step !== null) {
                        stepTitle = step.title ? `<strong class="text-slate-900 font-bold">${step.title}:</strong> ` : "";
                        stepText = step.text || "";
                        if (step.title && stepText.startsWith(step.title)) {
                            stepText = stepText.substring(step.title.length).replace(/^[:\s\-]+/, "");
                        }
                    } else {
                        stepText = String(step);
                    }

                    const item = document.createElement("div");
                    item.className = "flex items-start gap-3 p-3 rounded-xl bg-white/90 border border-emerald-100/90 shadow-xs mb-2 transition hover:bg-white";
                    item.innerHTML = `<span class="w-6 h-6 rounded-full bg-emerald-600 text-white text-xs font-extrabold flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm">${idx + 1}</span> <span class="text-xs text-slate-700 leading-relaxed">${stepTitle}${stepText}</span>`;
                    sugList.appendChild(item);
                });
            }
        }

        resBox.style.display = "block";
    }

    /**
     * Form Submission Handler
     */
    async function handleYieldPrediction(e) {
        if (e && e.preventDefault) e.preventDefault();

        const cropEl = document.getElementById("Crop");
        const stateEl = document.getElementById("State");
        const seasonEl = document.getElementById("Season");
        const areaEl = document.getElementById("Area");
        const areaUnitEl = document.getElementById("areaUnit");
        const rainfallEl = document.getElementById("Annual_Rainfall");
        const fertEl = document.getElementById("Fertilizer");
        const pestEl = document.getElementById("Pesticide");

        const submitBtn = document.querySelector("#yieldForm button[type='submit']");
        const originalBtnText = submitBtn ? submitBtn.innerHTML : "";

        const payload = {
            Crop: cropEl ? cropEl.value : "Rice",
            State: stateEl ? stateEl.value : "Andhra Pradesh",
            Season: seasonEl ? seasonEl.value : "Kharif",
            Crop_Year: 2020,
            Area: areaEl ? (parseFloat(areaEl.value) || 1.0) : 1.0,
            area_unit: areaUnitEl ? areaUnitEl.value : "acres",
            Annual_Rainfall: rainfallEl ? (parseFloat(rainfallEl.value) || 0) : 0,
            Fertilizer: fertEl ? (parseFloat(fertEl.value) || 0) : 0,
            Pesticide: pestEl ? (parseFloat(pestEl.value) || 0) : 0
        };

        try {
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = "<span>⏳</span> " + getTranslation("yield_btn_loading", "Estimating Pre-Harvest Yield...");
            }

            const res = await fetch("/predict-yield", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                if (res.status === 401) {
                    alert("Yield Prediction error: Authentication required. Please login with your Email.");
                    const resBox = document.getElementById("yieldResult");
                    if (resBox) {
                        resBox.style.display = "none";
                        resBox.innerHTML = "";
                    }
                    return;
                }
                const data = await res.json().catch(() => ({}));
                throw new Error(data.error || data.message || "Yield prediction failed");
            }

            const data = await res.json();

            window.lastYieldData = data;
            renderYieldResults(data);

            const resBox = document.getElementById("yieldResult");
            if (resBox) {
                resBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
        } catch (err) {
            alert("Yield prediction error: " + err.message);
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        }
    }

    // Expose functions to global window namespace
    window.filterCropsByState = filterCropsByState;
    window.handleCropChange = handleCropChange;
    window.renderYieldResults = renderYieldResults;
    window.renderYieldResultsModule = renderYieldResults;
    window.handleYieldPrediction = handleYieldPrediction;
    window.handleYieldPredictionModule = handleYieldPrediction;
    window.updateLocalizedStateSelect = updateLocalizedStateSelect;

    if (typeof document !== 'undefined') {
        const setupYieldListeners = () => {
            const langSelect = document.getElementById('langSelect');
            if (langSelect) {
                langSelect.addEventListener('change', () => {
                    const newLang = langSelect.value || getActiveLanguage();
                    updateLocalizedStateSelect(newLang);
                    if (window.lastYieldData) {
                        renderYieldResults(window.lastYieldData);
                    }
                });
            }
            window.addEventListener('languageChanged', (e) => {
                const newLang = (e && e.detail && e.detail.lang) || getActiveLanguage();
                updateLocalizedStateSelect(newLang);
                if (window.lastYieldData) {
                    renderYieldResults(window.lastYieldData);
                }
            });
            const stateEl = document.getElementById("State");
            if (stateEl) {
                stateEl.addEventListener("change", () => {
                    const resBox = document.getElementById("yieldResult");
                    if (resBox && resBox.style.display !== "none") {
                        handleYieldPrediction();
                    }
                });
            }

            const seasonEl = document.getElementById("Season");
            if (seasonEl) {
                seasonEl.addEventListener("change", () => {
                    handleCropChange(document.getElementById("Crop")?.value);
                    const resBox = document.getElementById("yieldResult");
                    if (resBox && resBox.style.display !== "none") {
                        handleYieldPrediction();
                    }
                });
            }

            const cropEl = document.getElementById("Crop");
            if (cropEl) {
                cropEl.addEventListener("change", (e) => {
                    handleCropChange(e.target.value);
                    const resBox = document.getElementById("yieldResult");
                    if (resBox && resBox.style.display !== "none") {
                        handleYieldPrediction();
                    }
                });
            }

            updateLocalizedStateSelect(getActiveLanguage());
        };
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupYieldListeners);
        } else {
            setupYieldListeners();
        }
    }

})(window, document);
